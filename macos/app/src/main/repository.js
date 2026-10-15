'use strict';

/**
 * Owns the channel list and the guide.
 *
 * Two sources, one shape:
 *  - the bundle shipped inside the .app (Contents/Resources/bundle), produced
 *    by android/tools/build_bundle.py from this repository;
 *  - a cache in ~/Library/Application Support/PremiumTV, written by refresh().
 *
 * The cache wins when it exists, so automatic and manual refreshes survive a
 * restart - but only while it was written by this same build: a copy left by
 * another version or library scope (a 1.0.x USA cache after installing the
 * global preview, say) is discarded on load, because it would otherwise hide
 * everything the new build ships. Resetting in Settings deletes it and falls
 * back to what the .app shipped with. Every load and write shares one serialized queue, so the
 * background scheduler can never replace files while the window is reading
 * them. A refresh is staged in a sibling directory and swapped in with a
 * rename: an interrupted or bad download leaves the previous usable copy
 * untouched.
 */

const fs = require('node:fs');
const fsp = require('node:fs/promises');
const path = require('node:path');
const readline = require('node:readline');
const { EventEmitter } = require('node:events');

const { parseM3u, parseXmltv, orderGroups } = require('./parsers');

const USER_AGENT =
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) PremiumTV/1.0 Safari/537.36';

class TvRepository extends EventEmitter {
  /**
   * @param {object} options
   * @param {string} options.bundleDir  read-only bundle inside the app
   * @param {string} options.cacheDir   writable downloaded copy
   * @param {string} options.stateFile  refresh state + HTTP validators
   * @param {Function} [options.fetchImpl] injectable for tests
   */
  constructor(options) {
    super();
    this.bundleDir = options.bundleDir;
    this.cacheDir = options.cacheDir;
    this.stateFile = options.stateFile;
    this.fetchImpl = options.fetchImpl || ((url, init) => fetch(url, init));

    this.stagingDir = `${this.cacheDir}-staging`;
    this.backupDir = `${this.cacheDir}-backup`;

    this.state = { phase: 'loading', source: null, meta: null, guideError: null, message: 'Loading channels…' };
    this.library = { meta: null, groups: [], channels: [], programmes: [] };
    this.info = this.readState().info || {};
    this.queue = Promise.resolve();
  }

  get stagingCacheDir() {
    return this.stagingDir;
  }

  get backupCacheDir() {
    return this.backupDir;
  }

  // ------------------------------------------------------------- public API

  /** Serializes an operation behind everything already queued. */
  serialize(operation) {
    const run = this.queue.then(operation, operation);
    this.queue = run.then(
      () => undefined,
      () => undefined,
    );
    return run;
  }

  load() {
    return this.serialize(() => this.loadLocked());
  }

  /**
   * Refreshes both data sources.
   *
   * A manual refresh deliberately downloads both files even when their HTTP
   * validators are unchanged - that is the Settings screen's "force" action.
   * Automatic checks send ETag/Last-Modified validators, so matching the
   * repository's frequent publishing windows normally costs two tiny HTTP 304
   * responses instead of a full guide download.
   */
  refresh(trigger, meta = {}) {
    return this.serialize(() => this.refreshLocked(trigger, meta));
  }

  /** Drops the downloaded copy and goes back to what the .app shipped with. */
  resetToBundled() {
    return this.serialize(async () => {
      await fsp.rm(this.cacheDir, { recursive: true, force: true });
      await fsp.rm(this.stagingDir, { recursive: true, force: true });
      await fsp.rm(this.backupDir, { recursive: true, force: true });
      this.clearValidators();
      await this.loadLocked();
      this.setStatus('Using the channel list and guide bundled in this app.');
    });
  }

  /** Called by the scheduler so Settings can show the next check. */
  noteNextAutomaticRefresh(epochMillis) {
    this.info = { ...this.info, nextAutomaticAt: epochMillis };
    this.writeState();
    this.emit('info', this.info);
  }

  snapshot() {
    return {
      state: this.state,
      info: this.info,
      library: this.library,
    };
  }

  /**
   * Channel ids are EPG ids, not unique stream ids: backups intentionally share
   * them. Resolve an exact id+URL pair first so choosing a backup actually plays
   * that backup rather than silently opening the primary feed.
   */
  findChannel(channelId, streamUrl = '') {
    const channels = this.library.channels || [];
    if (streamUrl) {
      const exact = channels.find((channel) => channel.id === channelId && channel.url === streamUrl);
      if (exact) return exact;
    }
    return channels.find((channel) => channel.id === channelId) || null;
  }

  // ------------------------------------------------------------- operations

  async loadLocked() {
    await this.recoverInterruptedCacheWrite();
    await this.discardCacheFromAnotherBuild();
    this.setState({ phase: 'loading', message: 'Loading channels…' });

    const cached = await this.readCache();
    if (cached) {
      this.library = cached.library;
      this.setState({
        phase: 'ready',
        source: 'cache',
        meta: cached.library.meta,
        guideError: cached.library.guideError || null,
        message: cached.library.guideError
          ? 'Channels loaded; the programme guide is unavailable.'
          : 'Showing the latest copy downloaded in the app.',
      });
      return;
    }

    this.setState({ phase: 'loading', source: null, message: 'Loading bundled channels…' });
    const bundled = await this.readBundle();
    if (!bundled) {
      this.setState({
        phase: 'error',
        source: null,
        message:
          'The bundled channel list could not be read. Reinstall PremiumTV, or use Settings → Force refresh all now.',
      });
      return;
    }
    this.library = bundled.library;
    this.setState({
      phase: 'ready',
      source: 'bundled',
      meta: bundled.library.meta,
      guideError: bundled.library.guideError || null,
      message: bundled.library.guideError
        ? 'Channels loaded; the programme guide is unavailable.'
        : 'Showing the channel list and guide bundled in this app.',
    });
  }

  async refreshLocked(trigger) {
    const isManual = trigger === 'manual';
    const startedAt = Date.now();
    this.info = { ...this.info, lastAttemptAt: startedAt, lastTrigger: trigger };
    this.writeState();
    this.emit('info', this.info);

    const stored = this.readState();
    const validators = (stored.info && stored.info.validators) || stored.validators || {};
    const conditional = !isManual && this.state.source === 'cache' && Boolean(stored.info && stored.info.lastSuccessAt);

    const meta = this.currentMeta();
    const playlistUrl = meta && meta.playlist_url;
    const guideUrl = meta && meta.guide_url;
    if (!playlistUrl || !guideUrl) {
      return this.finishRefresh(trigger, {
        ok: false,
        retryable: true,
        message: 'No refresh URL is known yet; the bundled metadata is missing.',
      });
    }

    let playlistResponse;
    let guideResponse;
    try {
      playlistResponse = await this.download(playlistUrl, conditional ? validators.playlist : null);
      guideResponse = await this.download(guideUrl, conditional ? validators.guide : null);
    } catch (error) {
      return this.finishRefresh(trigger, {
        ok: false,
        retryable: true,
        message: this.describeNetworkFailure(error),
      });
    }

    if (playlistResponse.status === 304 && guideResponse.status === 304) {
      return this.finishRefresh(trigger, {
        ok: true,
        updated: false,
        message: 'Already current: neither the playlist nor the guide changed.',
      });
    }
    if (playlistResponse.status === 304 || guideResponse.status === 304) {
      // One file changed and the other did not. The bundle is written as a
      // pair, so re-download the unchanged one rather than mixing generations.
      const which = playlistResponse.status === 304 ? 'playlist' : 'guide';
      const url = playlistResponse.status === 304 ? playlistUrl : guideUrl;
      try {
        const fresh = await this.download(url, null);
        if (playlistResponse.status === 304) playlistResponse = fresh;
        else guideResponse = fresh;
      } catch (error) {
        return this.finishRefresh(trigger, {
          ok: false,
          retryable: true,
          message: `The ${which} changed but its full copy could not be downloaded (${error.message}).`,
        });
      }
      if (playlistResponse.status === 304 || guideResponse.status === 304) {
        return this.finishRefresh(trigger, {
          ok: false,
          retryable: true,
          message: 'The server still reports an unchanged file; nothing was replaced.',
        });
      }
    }

    if (!playlistResponse.ok || !guideResponse.ok) {
      const failed = !playlistResponse.ok ? playlistUrl : guideUrl;
      return this.finishRefresh(trigger, {
        ok: false,
        retryable: playlistResponse.status >= 500 || guideResponse.status >= 500,
        message: `The server answered ${playlistResponse.ok ? guideResponse.status : playlistResponse.status} for ${failed}; the copy already on this Mac is still in use.`,
      });
    }

    let parsed;
    try {
      parsed = this.parseDownloaded(playlistResponse.body, guideResponse.body);
    } catch (error) {
      return this.finishRefresh(trigger, {
        ok: false,
        retryable: false,
        message: `The downloaded data could not be parsed: ${error.message}`,
      });
    }

    try {
      await this.publishStaged(parsed);
    } catch (error) {
      return this.finishRefresh(trigger, {
        ok: false,
        retryable: true,
        message: `The new copy could not be installed: ${error.message}`,
      });
    }

    this.info = {
      ...this.info,
      validators: {
        playlist: validatorsOf(playlistResponse),
        guide: validatorsOf(guideResponse),
      },
    };

    await this.loadLocked();
    return this.finishRefresh(trigger, {
      ok: true,
      updated: true,
      message: `Updated: ${this.library.channels.length} channels, ${this.library.programmes.length} guide listings.`,
    });
  }

  parseDownloaded(playlistText, guideText) {
    const { channels, guideUrl } = parseM3u(playlistText);
    if (channels.length === 0) throw new Error('the playlist contains no channels');
    const known = new Set(channels.map((c) => c.id).filter(Boolean));

    let programmes = [];
    let guideError = null;
    try {
      programmes = parseXmltv(guideText, { knownIds: known });
    } catch (error) {
      // A damaged guide must not block the channel browser.
      guideError = error.message;
    }

    const baseMeta = this.currentMeta() || {};
    const starts = programmes.map((p) => p.s);
    const stops = programmes.map((p) => p.e);
    const now = Math.floor(Date.now() / 1000);
    const meta = {
      ...baseMeta,
      generated_utc: new Date().toISOString().replace('T', ' ').slice(0, 16) + ' UTC',
      channel_count: channels.length,
      group_count: 0,
      programme_count: programmes.length,
      guide_channels: new Set(programmes.map((p) => p.c)).size,
      window_start: starts.length ? Math.min(...starts) : now,
      window_end: stops.length ? Math.max(...stops) : now,
      playlist_url: baseMeta.playlist_url,
      guide_url: guideUrl || baseMeta.guide_url,
      refreshed_from_network: true,
    };
    const groups = orderGroups(channels, (baseMeta.published_order || []).concat());
    meta.group_count = groups.length;
    meta.published_order = baseMeta.published_order || [];
    return { meta, groups, channels, programmes, guideError };
  }

  /** Writes a parsed library to the staging directory, then swaps it in. */
  async publishStaged(parsed) {
    await fsp.rm(this.stagingDir, { recursive: true, force: true });
    await fsp.mkdir(this.stagingDir, { recursive: true });

    await writeJsonl(path.join(this.stagingDir, 'channels.jsonl'), parsed.channels);
    await writeJsonl(path.join(this.stagingDir, 'groups.jsonl'), parsed.groups);
    await writeJsonl(path.join(this.stagingDir, 'epg.jsonl'), parsed.programmes);
    await fsp.writeFile(
      path.join(this.stagingDir, 'meta.json'),
      `${JSON.stringify(parsed.meta, null, 2)}\n`,
      'utf8',
    );
    if (parsed.guideError) {
      await fsp.writeFile(path.join(this.stagingDir, 'guide-error.txt'), parsed.guideError, 'utf8');
    }

    // Swap: current cache becomes the backup, staging becomes the cache. If
    // anything fails, the backup is renamed back.
    const hadCache = await isDirectory(this.cacheDir);
    if (hadCache) {
      await fsp.rm(this.backupDir, { recursive: true, force: true });
      await fsp.rename(this.cacheDir, this.backupDir);
    }
    try {
      await fsp.mkdir(path.dirname(this.cacheDir), { recursive: true });
      await fsp.rename(this.stagingDir, this.cacheDir);
    } catch (error) {
      if (hadCache) await fsp.rename(this.backupDir, this.cacheDir);
      throw error;
    }
    await fsp.rm(this.backupDir, { recursive: true, force: true });
  }

  /** The metadata of the bundle baked into this .app (version, scope, features). */
  async bundledMeta() {
    if (this.bundledMetaCache === undefined) {
      this.bundledMetaCache = await readJson(path.join(this.bundleDir, 'meta.json'));
    }
    return this.bundledMetaCache;
  }

  /**
   * Drops a downloaded copy that another build wrote.
   *
   * The cache always records the version and library scope of the bundle it
   * replaced. When those differ from this .app's bundle, the copy belongs to
   * an earlier install - for example a 1.0.x USA refresh still sitting in
   * Application Support after the global preview is installed - and loading it
   * would show the old lineup and keep the new Guide hidden. The validators go
   * with it, so the next refresh downloads the new build's playlist in full.
   */
  async discardCacheFromAnotherBuild() {
    if (!(await isDirectory(this.cacheDir))) return false;
    const bundled = await this.bundledMeta();
    if (!bundled) return false;
    const cached = await readJson(path.join(this.cacheDir, 'meta.json'));
    const sameBuild = Boolean(cached) &&
      String(cached.version || '') === String(bundled.version || '') &&
      String(cached.library_scope || 'usa') === String(bundled.library_scope || 'usa');
    if (sameBuild) return false;
    await fsp.rm(this.cacheDir, { recursive: true, force: true });
    this.clearValidators();
    return true;
  }

  /** Removes a half-written cache left behind by a crash or a forced quit. */
  async recoverInterruptedCacheWrite() {
    const stagingExists = await isDirectory(this.stagingDir);
    const cacheExists = await isDirectory(this.cacheDir);
    const backupExists = await isDirectory(this.backupDir);

    if (stagingExists) await fsp.rm(this.stagingDir, { recursive: true, force: true });
    if (!cacheExists && backupExists) {
      await fsp.rename(this.backupDir, this.cacheDir);
      return;
    }
    if (backupExists) await fsp.rm(this.backupDir, { recursive: true, force: true });
  }

  // ---------------------------------------------------------------- reading

  async readCache() {
    if (!(await isDirectory(this.cacheDir))) return null;
    try {
      return await this.readLibraryFrom(this.cacheDir);
    } catch (error) {
      // A cache we cannot read is treated as no cache: fall back to the bundle
      // rather than showing an empty app.
      await fsp.rm(this.cacheDir, { recursive: true, force: true });
      this.clearValidators();
      return null;
    }
  }

  async readBundle() {
    if (!(await isDirectory(this.bundleDir))) return null;
    try {
      return await this.readLibraryFrom(this.bundleDir);
    } catch (error) {
      return null;
    }
  }

  /**
   * Reads one library directory. Channels and groups are published as soon as
   * their small files are parsed; the larger guide is parsed afterwards so a
   * slow or damaged guide never holds the channel browser back.
   */
  async readLibraryFrom(dir) {
    const meta = await readJson(path.join(dir, 'meta.json'));
    if (!meta) throw new Error(`${dir}/meta.json is missing`);
    if (meta.published_order === undefined) {
      const published = await readJson(path.join(dir, 'published-order.json'));
      meta.published_order = published || [];
    }

    const channels = await readJsonl(path.join(dir, 'channels.jsonl'));
    if (!channels.length) throw new Error(`${dir}/channels.jsonl is empty`);
    let groups = await readJsonl(path.join(dir, 'groups.jsonl'));
    if (!groups.length) groups = orderGroups(channels, meta.published_order || []);

    // Publish the rows first: the renderer can paint categories immediately.
    this.library = { meta, groups, channels, programmes: [] };
    this.emit('progress', { phase: 'channels', count: channels.length });

    let programmes = [];
    let guideError = null;
    try {
      const guidePath = path.join(dir, 'epg.jsonl');
      if (await isFile(guidePath)) programmes = await readJsonl(guidePath);
    } catch (error) {
      guideError = error.message;
    }
    if (!guideError) {
      const marker = path.join(dir, 'guide-error.txt');
      if (await isFile(marker)) guideError = (await fsp.readFile(marker, 'utf8')).trim();
    }

    return { library: { meta, groups, channels, programmes, guideError } };
  }

  // ------------------------------------------------------------------ state

  readState() {
    try {
      return JSON.parse(fs.readFileSync(this.stateFile, 'utf8'));
    } catch (error) {
      return {};
    }
  }

  writeState() {
    try {
      fs.mkdirSync(path.dirname(this.stateFile), { recursive: true });
      const existing = this.readState();
      const next = { ...existing, info: this.info };
      fs.writeFileSync(this.stateFile, `${JSON.stringify(next, null, 2)}\n`, 'utf8');
    } catch (error) {
      // State is a convenience; losing it must not break playback.
    }
  }

  clearValidators() {
    const stored = this.readState();
    delete stored.validators;
    delete this.info.validators;
    this.info = { ...this.info, lastSuccessAt: null };
    try {
      fs.mkdirSync(path.dirname(this.stateFile), { recursive: true });
      fs.writeFileSync(this.stateFile, `${JSON.stringify({ ...stored, info: this.info }, null, 2)}\n`, 'utf8');
    } catch (error) {
      /* ignored */
    }
  }

  currentMeta() {
    return (this.library && this.library.meta) || null;
  }

  // ------------------------------------------------------------------ fetch

  async download(url, validator) {
    const headers = { 'User-Agent': USER_AGENT, Accept: '*/*' };
    if (validator) {
      if (validator.etag) headers['If-None-Match'] = validator.etag;
      if (validator.lastModified) headers['If-Modified-Since'] = validator.lastModified;
    }

    let response;
    try {
      response = await this.fetchImpl(url, { headers, redirect: 'follow' });
    } catch (error) {
      throw new Error(`network error (${error.message})`);
    }

    if (response.status === 304) return { status: 304, ok: true, headers: response.headers };

    const length = Number(response.headers.get('content-length') || 0);
    if (length > 96 * 1024 * 1024) throw new Error('the server sent more than the 96 MB the app accepts');
    const body = await response.text();
    return { status: response.status, ok: response.ok, body, headers: response.headers };
  }

  describeNetworkFailure(error) {
    const detail = error.message || String(error);
    return `The repository could not be reached: ${detail}. The copy already on this Mac is still in use.`;
  }

  finishRefresh(trigger, outcome) {
    const finishedAt = Date.now();
    if (outcome.ok) {
      this.info = {
        ...this.info,
        lastSuccessAt: finishedAt,
        lastMessage: outcome.message,
        lastTrigger: trigger,
      };
    } else {
      this.info = { ...this.info, lastMessage: outcome.message, lastTrigger: trigger };
    }
    this.writeState();
    this.emit('info', this.info);
    this.setStatus(outcome.message);
    return { ...outcome, trigger, finishedAt };
  }

  setState(patch) {
    this.state = { ...this.state, ...patch };
    this.emit('state', this.state);
  }

  setStatus(message) {
    this.setState({ message });
  }
}

function validatorsOf(response) {
  return {
    etag: response.headers.get('etag') || '',
    lastModified: response.headers.get('last-modified') || '',
  };
}

async function isDirectory(target) {
  try {
    return (await fsp.stat(target)).isDirectory();
  } catch (error) {
    return false;
  }
}

async function isFile(target) {
  try {
    return (await fsp.stat(target)).isFile();
  } catch (error) {
    return false;
  }
}

async function readJson(file) {
  try {
    return JSON.parse(await fsp.readFile(file, 'utf8'));
  } catch (error) {
    return null;
  }
}

/** Streams JSON Lines so a 10 MB guide is never held as one giant string. */
function readJsonl(file) {
  return new Promise((resolve, reject) => {
    const rows = [];
    const stream = fs.createReadStream(file, { encoding: 'utf8' });
    const reader = readline.createInterface({ input: stream, crlfDelay: Infinity });
    reader.on('line', (line) => {
      const trimmed = line.trim();
      if (!trimmed) return;
      try {
        rows.push(JSON.parse(trimmed));
      } catch (error) {
        // A single bad line is skipped, not fatal.
      }
    });
    reader.on('close', () => resolve(rows));
    stream.on('error', reject);
  });
}

async function writeJsonl(file, rows) {
  const handle = await fsp.open(file, 'w');
  try {
    for (const row of rows) await handle.write(`${JSON.stringify(row)}\n`);
  } finally {
    await handle.close();
  }
}

module.exports = { TvRepository, readJsonl, writeJsonl, USER_AGENT };
