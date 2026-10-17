'use strict';

/**
 * PremiumTV's in-app updater for macOS.
 *
 * It deliberately does not use Electron's autoUpdater/Squirrel: this app is
 * ad-hoc signed, so macOS would refuse a silent in-place replacement. Instead
 * the updater does the part that can be trusted and verified:
 *
 *   - checks GitHub's public release list at most once a day (ETag, so an
 *     unchanged list is a single 304 response);
 *   - offers only a published stable release numerically above this app;
 *   - downloads the DMG for this Mac only when the user asks for it, checks it
 *     against the release's SHA-256 file, and keeps it until installed;
 *   - opens the verified DMG so the user can drag PremiumTV into Applications.
 *
 * Re-checking after a release is already downloaded never downloads it again.
 */

const { EventEmitter } = require('node:events');
const fs = require('node:fs');
const fsp = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const {
  normalizeVersion,
  isNewer,
  selectStableUpdate,
  describeState,
  macAssetName,
} = require('./update-policy');

const RELEASES_API =
  'https://api.github.com/repos/cgyegcvcecvoc/PremiumTV1/releases?per_page=30';
const CHECK_INTERVAL_MS = 24 * 60 * 60 * 1000;
const RETRY_INTERVAL_MS = 60 * 60 * 1000;
const MAX_RELEASE_BYTES = 2 * 1024 * 1024;
const MAX_CHECKSUM_BYTES = 256 * 1024;

function defaultState(currentVersion) {
  return {
    currentVersion,
    latestStableVersion: null,
    availableVersion: null,
    releaseUrl: null,
    installerUrl: null,
    checksumUrl: null,
    installerSize: 0,
    lastCheckedAtMillis: 0,
    nextCheckAtMillis: 0,
    checking: false,
    downloading: false,
    progressPercent: -1,
    downloadedVersion: null,
    installerPath: null,
    message: 'No update check yet.',
    error: null,
    etag: null,
  };
}

class AppUpdater extends EventEmitter {
  constructor(options = {}) {
    super();
    const version = normalizeVersion(options.currentVersion) || String(options.currentVersion || '');
    this.currentVersion = version;
    this.stateFile = options.stateFile ||
      path.join(options.userData || process.cwd(), 'update-state.json');
    this.downloadDir = options.downloadDir ||
      path.join(path.dirname(this.stateFile), 'updates');
    this.arch = options.arch || process.arch;
    this.fetchImpl = options.fetchImpl || globalThis.fetch;
    this.shell = options.shell || null;
    this.now = options.now || (() => Date.now());
    this.state = this.readState();
    this.checkPromise = null;
    this.downloadPromise = null;
    this.timer = null;
    this.pruneInstallers();
  }

  status() {
    return { ...this.state };
  }

  /** Kick off the daily check and keep a cheap hourly retry while running. */
  start() {
    this.check().catch(() => {});
    this.timer = setInterval(() => this.check().catch(() => {}), 60 * 60 * 1000);
    if (this.timer.unref) this.timer.unref();
    return this;
  }

  stop() {
    if (this.timer) clearInterval(this.timer);
    this.timer = null;
  }

  // --------------------------------------------------------------- checking

  check(force = false) {
    if (this.checkPromise) return this.checkPromise;
    if (this.state.downloading) return Promise.resolve(this.status());
    const now = this.now();
    if (!force && now < this.state.nextCheckAtMillis) {
      return Promise.resolve(this.status());
    }
    this.checkPromise = this.runCheck(force).finally(() => {
      this.checkPromise = null;
    });
    return this.checkPromise;
  }

  async runCheck(force) {
    this.patch({
      checking: true,
      error: null,
      message: 'Checking GitHub for a new stable release…',
    });
    const startedAt = this.now();
    try {
      const headers = {
        'User-Agent': `PremiumTV/${this.currentVersion} (macOS)`,
        Accept: 'application/vnd.github+json',
      };
      if (!force && this.state.etag) headers['If-None-Match'] = this.state.etag;

      const response = await this.fetchImpl(RELEASES_API, { headers, redirect: 'follow' });
      if (response.status === 304) {
        this.patch({
          checking: false,
          lastCheckedAtMillis: startedAt,
          nextCheckAtMillis: startedAt + CHECK_INTERVAL_MS,
          message: this.state.availableVersion
            ? `PremiumTV ${this.state.availableVersion} is still the newest stable release.`
            : 'PremiumTV is up to date.',
          error: null,
        });
        return this.status();
      }
      if (!response.ok) throw new Error(`GitHub returned HTTP ${response.status}`);
      const body = await response.text();
      if (body.length > MAX_RELEASE_BYTES) {
        throw new Error('GitHub returned an unexpectedly large release list');
      }
      const releases = JSON.parse(body);
      const { update, newestStable } = selectStableUpdate(releases, this.currentVersion, this.arch);

      // An installer already downloaded for this exact version stays valid;
      // re-checking must not make the user download it again.
      const keepReady = Boolean(update) && this.state.downloadedVersion === update.version &&
        Boolean(this.state.installerPath) && fs.existsSync(this.state.installerPath);

      this.patch({
        checking: false,
        etag: response.headers.get('etag') || this.state.etag,
        lastCheckedAtMillis: startedAt,
        nextCheckAtMillis: startedAt + CHECK_INTERVAL_MS,
        latestStableVersion: newestStable,
        availableVersion: update ? update.version : null,
        releaseUrl: update ? update.releaseUrl : null,
        installerUrl: update ? update.installerUrl : null,
        checksumUrl: update ? update.checksumUrl : null,
        installerSize: update ? update.installerSize : 0,
        downloadedVersion: keepReady ? this.state.downloadedVersion : null,
        installerPath: keepReady ? this.state.installerPath : null,
        progressPercent: keepReady ? 100 : -1,
        message: describeState(this.currentVersion, newestStable, update),
        error: null,
      });
      return this.status();
    } catch (error) {
      const detail = error && error.message ? error.message : String(error);
      const message = `Could not check for updates: ${detail}. ` +
        'PremiumTV keeps working from the installed version.';
      this.patch({
        checking: false,
        lastCheckedAtMillis: startedAt,
        nextCheckAtMillis: startedAt + RETRY_INTERVAL_MS,
        message,
        error: message,
      });
      return this.status();
    }
  }

  // ------------------------------------------------------------- downloading

  download() {
    if (this.downloadPromise) return this.downloadPromise;
    if (this.state.checking) return Promise.resolve(this.status());
    this.downloadPromise = this.runDownload().finally(() => {
      this.downloadPromise = null;
    });
    return this.downloadPromise;
  }

  async runDownload() {
    const state = this.state;
    const version = state.availableVersion;
    if (!version) {
      const message = 'No newer stable release is available to download.';
      this.patch({ message, error: message });
      return this.status();
    }

    const target = this.installerPathFor(version);
    if (state.downloadedVersion === version && fs.existsSync(target)) {
      this.patch({
        downloading: false,
        progressPercent: 100,
        message: `PremiumTV ${version} is already downloaded and verified. ` +
          'Press Open installer; it will not be downloaded again.',
        error: null,
      });
      return this.status();
    }
    if (!state.installerUrl) {
      const message = 'The release has no Mac installer to download.';
      this.patch({ message, error: message });
      return this.status();
    }

    const part = `${target}.part`;
    await fsp.mkdir(this.downloadDir, { recursive: true });
    await fsp.rm(part, { force: true }).catch(() => {});
    this.patch({
      downloading: true,
      progressPercent: 0,
      error: null,
      message: `Downloading PremiumTV ${version}…`,
    });

    try {
      const response = await this.fetchImpl(state.installerUrl, {
        headers: {
          'User-Agent': `PremiumTV/${this.currentVersion} (macOS)`,
          Accept: 'application/octet-stream',
        },
        redirect: 'follow',
      });
      if (!response.ok) throw new Error(`GitHub returned HTTP ${response.status}`);
      if (!response.body || typeof response.body.getReader !== 'function') {
        throw new Error('the download stream was unavailable');
      }
      const total = Number(response.headers.get('content-length')) ||
        Number(state.installerSize) || 0;
      const reader = response.body.getReader();
      const handle = await fsp.open(part, 'w');
      let copied = 0;
      let reported = 0;
      try {
        for (;;) {
          const { done, value } = await reader.read();
          if (done) break;
          await handle.write(value);
          copied += value.length;
          if (total > 0) {
            const percent = Math.min(99, Math.floor((copied * 100) / total));
            // Two-percent steps keep the Settings panel from re-rendering on
            // every 64 KB chunk while still showing honest progress.
            if (percent >= reported + 2 || (percent === 99 && reported < 99)) {
              reported = percent;
              this.patch({
                progressPercent: percent,
                message: `Downloading PremiumTV ${version}… ${percent}%`,
              }, { persist: false });
            }
          }
        }
      } finally {
        await handle.close();
      }
      if (copied <= 0) throw new Error('the downloaded installer was empty');
      await this.verifyChecksum(part, path.basename(target));
      await fsp.rename(part, target);
      await this.pruneInstallers(target);

      this.patch({
        downloading: false,
        progressPercent: 100,
        downloadedVersion: version,
        installerPath: target,
        message: `PremiumTV ${version} downloaded and verified. ` +
          'Press Open installer to finish.',
        error: null,
      });
      return this.status();
    } catch (error) {
      await fsp.rm(part, { force: true }).catch(() => {});
      const detail = error && error.message ? error.message : String(error);
      const message = `Update download failed: ${detail}`;
      this.patch({ downloading: false, progressPercent: -1, message, error: message });
      return this.status();
    }
  }

  async verifyChecksum(file, assetName) {
    const url = this.state.checksumUrl;
    if (!url) throw new Error('the release has no SHA-256 checksum file');
    const response = await this.fetchImpl(url, {
      headers: {
        'User-Agent': `PremiumTV/${this.currentVersion} (macOS)`,
        Accept: 'text/plain',
      },
      redirect: 'follow',
    });
    if (!response.ok) throw new Error(`the checksum request returned HTTP ${response.status}`);
    const text = await response.text();
    if (text.length > MAX_CHECKSUM_BYTES) throw new Error('the checksum file was larger than expected');
    const expected = text.split(/\r?\n/)
      .map((line) => line.trim())
      .filter(Boolean)
      .map((line) => {
        const match = /^([0-9a-fA-F]{64})\s+\*?(.+)$/.exec(line);
        return match ? { hash: match[1].toLowerCase(), name: match[2].trim() } : null;
      })
      .filter(Boolean)
      .find((entry) => entry.name === assetName);
    if (!expected) throw new Error(`the checksum file has no entry for ${assetName}`);
    const actual = await sha256File(file);
    if (actual !== expected.hash) {
      throw new Error('the downloaded installer failed its SHA-256 check');
    }
  }

  // ------------------------------------------------------------- installing

  async openInstaller() {
    const state = this.state;
    if (!state.installerPath || !fs.existsSync(state.installerPath)) {
      const message = 'The downloaded installer is missing. Check for updates again.';
      this.patch({ downloadedVersion: null, installerPath: null, message, error: message });
      return { ok: false, message, state: this.status() };
    }
    if (!this.shell || typeof this.shell.openPath !== 'function') {
      return { ok: false, message: 'Opening the installer is unavailable.', state: this.status() };
    }
    const error = await this.shell.openPath(state.installerPath);
    if (error) {
      const message = `The installer could not be opened: ${error}`;
      this.patch({ message, error: message });
      return { ok: false, message, state: this.status() };
    }
    const message = 'The PremiumTV installer is open. Drag PremiumTV to Applications to finish.';
    this.patch({ message, error: null });
    return { ok: true, message, state: this.status() };
  }

  async openReleasePage() {
    if (!this.state.releaseUrl || !this.shell ||
        typeof this.shell.openExternal !== 'function') {
      return { ok: false };
    }
    await this.shell.openExternal(this.state.releaseUrl);
    return { ok: true };
  }

  // ----------------------------------------------------------------- state

  installerPathFor(version) {
    return path.join(this.downloadDir, macAssetName(version, this.arch));
  }

  patch(patch, options = {}) {
    this.state = { ...this.state, ...patch };
    if (options.persist !== false) this.writeState();
    if (options.emit !== false) this.emit('state', this.status());
  }

  readState() {
    const base = defaultState(this.currentVersion);
    let stored = null;
    try {
      stored = JSON.parse(fs.readFileSync(this.stateFile, 'utf8'));
    } catch (error) {
      return base;
    }
    if (!stored || normalizeVersion(stored.currentVersion) !== this.currentVersion) {
      // This is a new app version: availability and installers recorded for
      // the old version are obsolete.
      return base;
    }
    const state = { ...base, ...stored, currentVersion: this.currentVersion };
    state.checking = false;
    state.downloading = false;
    if (state.availableVersion && !isNewer(state.availableVersion, this.currentVersion)) {
      state.availableVersion = null;
    }
    if (state.downloadedVersion !== state.availableVersion) {
      state.downloadedVersion = null;
      state.installerPath = null;
      state.progressPercent = -1;
    }
    return state;
  }

  writeState() {
    try {
      fs.mkdirSync(path.dirname(this.stateFile), { recursive: true });
      const temp = `${this.stateFile}.tmp`;
      fs.writeFileSync(temp, `${JSON.stringify(this.state, null, 2)}\n`, 'utf8');
      fs.renameSync(temp, this.stateFile);
    } catch (error) {
      // Update state is a convenience; the next check recreates it.
    }
  }

  pruneInstallers(keepPath) {
    try {
      if (!fs.existsSync(this.downloadDir)) return;
      const keep = keepPath ||
        (this.state.installerPath && fs.existsSync(this.state.installerPath)
          ? this.state.installerPath
          : null);
      for (const name of fs.readdirSync(this.downloadDir)) {
        const full = path.join(this.downloadDir, name);
        if (!keep || path.resolve(full) !== path.resolve(keep)) {
          fs.rmSync(full, { recursive: true, force: true });
        }
      }
    } catch (error) {
      // A locked or already-removed file is harmless.
    }
  }
}

function sha256File(file) {
  return new Promise((resolve, reject) => {
    const hash = crypto.createHash('sha256');
    const stream = fs.createReadStream(file);
    stream.on('error', reject);
    stream.on('data', (chunk) => hash.update(chunk));
    stream.on('end', () => resolve(hash.digest('hex')));
  });
}

module.exports = { AppUpdater, RELEASES_API, CHECK_INTERVAL_MS };
