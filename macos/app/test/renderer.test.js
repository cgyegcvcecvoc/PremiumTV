'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const renderer = path.join(__dirname, '..', 'src', 'renderer');

test('the channel browser is not obscured by the player or its error panel on first launch', () => {
  const html = fs.readFileSync(path.join(renderer, 'index.html'), 'utf8');
  const css = fs.readFileSync(path.join(renderer, 'app.css'), 'utf8');
  const js = fs.readFileSync(path.join(renderer, 'app.js'), 'utf8');

  assert.match(html, /<div id="player" hidden>/);
  assert.match(html, /<div id="player-error" hidden>/);
  // #player { display: flex } and #player-error { display: grid } would
  // otherwise override the browser's user-agent [hidden] { display: none }.
  assert.match(css, /\[hidden\]\s*\{\s*display:\s*none\s*!important\s*;/);
  assert.match(js, /els\.player\.hidden = false/);
  assert.match(js, /els\.player\.hidden = true/);
});

test('playback chooses HLS using the original feed, not the extensionless proxy URL', () => {
  const code = fs.readFileSync(path.join(renderer, 'player.js'), 'utf8');
  const called = [];
  const video = {
    pause() {}, removeAttribute() {}, load() {}, addEventListener() {},
    play() { called.push('native'); return Promise.resolve(); },
  };
  const elements = {
    video,
    'player-spinner': { hidden: true },
    'player-error': { hidden: true },
    'player-error-text': { textContent: '' },
  };
  class Hls {
    static isSupported() { return true; }
    static Events = { ERROR: 'error', MANIFEST_PARSED: 'manifest' };
    on() {}
    loadSource(url) { called.push(['hls', url]); }
    attachMedia() {}
    destroy() {}
  }
  const window = { Hls, mpegts: { isSupported: () => false } };
  vm.runInNewContext(code, { window, document: { getElementById: (id) => elements[id] } });
  const proxy = 'http://127.0.0.1:1234/p/session';
  window.PremiumPlayer.play(proxy, 'https://example.org/live.m3u8?token=abc');
  assert.deepEqual(called, [['hls', proxy]]);
  window.PremiumPlayer.retry();
  assert.deepEqual(called, [['hls', proxy], ['hls', proxy]]);
});

test('the launch splash is still: mark, loading line bar and version at the bottom', () => {
  const html = fs.readFileSync(path.join(renderer, 'index.html'), 'utf8');
  const css = fs.readFileSync(path.join(renderer, 'app.css'), 'utf8');
  const js = fs.readFileSync(path.join(renderer, 'app.js'), 'utf8');

  assert.match(html, /<div id="splash" role="status"/);
  assert.match(html, /class="splash-logo"/);
  // 1.1.0 retired the animated splash: no spinner, shimmer or dots on screen.
  assert.doesNotMatch(html, /class="splash-spinner"/);
  assert.doesNotMatch(html, /class="splash-dots"/);
  // The loading line bar the viewer asked to keep is still there.
  assert.match(html, /class="splash-bar"/);
  assert.match(html, /class="splash-bar-fill"/);
  assert.doesNotMatch(css, /@keyframes splash-/);
  assert.match(html, /id="splash-version"/);
  assert.match(html, /class="splash-foot"/);
  assert.match(css, /\.splash-foot \{[^}]*bottom:/);
  assert.match(css, /#splash\.done \{ opacity: 0; visibility: hidden;/);
  // The splash fades out once the first library snapshot is painted, and a
  // failed startup must not leave it in front of the error.
  assert.match(js, /await syncSnapshot\(\);\s*hideSplash\(\);/);
  assert.match(js, /boot\(\)\.catch\(\(error\) => \{\s*hideSplash\(\);/);
  // 1.0.8 V1: the splash derives a V display name from the packaged version
  // (a four-part 1.0.8.1 reads "1.0.8 V1 Patch"; the Mac's three-part alias
  // 1.0.9 reads as itself) and prints it in the foot as the build on show.
  assert.match(js, /const p = String\(appInfo\.version\)\.split\('\.'\);/);
  assert.match(js, /els\.splashVersion\.textContent = `Version \$\{display\}`;/);
});

test('logo-less channels fall back to their category placeholder, not bare text', () => {
  const html = fs.readFileSync(path.join(renderer, 'index.html'), 'utf8');
  const js = fs.readFileSync(path.join(renderer, 'app.js'), 'utf8');

  assert.match(html, /<script src="category-icons.js"><\/script>/);
  assert.match(html, /<script src="live-events.js"><\/script>/);
  assert.match(js, /window\.PremiumIcons\.svgForGroup\(channel\.group, 'card-logo placeholder'\)/);
  assert.match(js, /logo\.innerHTML = window\.PremiumIcons\.svgForGroup\(channel\.group\)/);
});

test('the Live Events tab lists games by sport and opens them with every server', () => {
  const html = fs.readFileSync(path.join(renderer, 'index.html'), 'utf8');
  const js = fs.readFileSync(path.join(renderer, 'app.js'), 'utf8');

  assert.match(html, /data-tab="live"[^>]*>Live Events</);
  assert.match(html, /<div id="live-list"><\/div>/);
  assert.match(js, /live: document\.getElementById\('view-live'\)/);
  assert.match(js, /else if \(ui\.tab === 'live'\) renderLive\(\);/);
  assert.match(js, /openPlayer\(event\.servers\[0\], event\.servers\)/);
});

test('a dead feed hands over to the next server before the error card appears', () => {
  const js = fs.readFileSync(path.join(renderer, 'app.js'), 'utf8');
  const player = fs.readFileSync(path.join(renderer, 'player.js'), 'utf8');

  assert.match(js, /window\.PremiumLive\.serversFor\(channel, snapshot\.library\.channels \|\| \[\]\)/);
  assert.match(js, /window\.PremiumPlayer\.play\(resolved\.url, channel\.url, \{ onFatal: \(\) => advanceServer\(\) \}\)/);
  assert.match(js, /switching to server \$\{playQueueIndex \+ 1\} of \$\{playQueue\.length\}/);
  assert.match(js, /window\.PremiumPlayer\.fail\(/);
  assert.match(player, /onFatal = typeof handlers\.onFatal === 'function' \? handlers\.onFatal : null;/);
  assert.match(player, /fail\(message\) \{/);
});

test('1.0.8: the sidebar sorts categories and a category page sorts its channels', () => {
  const html = fs.readFileSync(path.join(renderer, 'index.html'), 'utf8');
  const js = fs.readFileSync(path.join(renderer, 'app.js'), 'utf8');

  assert.match(html, /id="cat-sort"[^]*/);
  assert.match(html, /data-sort="az"/);
  assert.match(html, /id="cat-back"/);
  assert.match(html, /id="channel-sort"/);
  assert.match(html, /data-chsort="number"/);
  assert.match(js, /function sortedGroups\(\)/);
  assert.match(js, /function sortedChannels\(channels\)/);
  assert.match(js, /return sortedChannels\(filtered\);/);
  assert.match(js, /ui\.categorySort = button\.dataset\.sort;/);
  assert.match(js, /ui\.channelSort = button\.dataset\.chsort;/);
  assert.match(js, /els\.catBack\.addEventListener\('click', \(\) => selectCategory\(null\)\);/);
  assert.match(css(), /#cat-sort \{/);
});

test('1.0.8: the side player tucks into the corner and grows back', () => {
  const html = fs.readFileSync(path.join(renderer, 'index.html'), 'utf8');
  const js = fs.readFileSync(path.join(renderer, 'app.js'), 'utf8');
  const css = fs.readFileSync(path.join(renderer, 'app.css'), 'utf8');

  assert.match(html, /id="player-minimize"/);
  assert.match(js, /let playerMini = false;/);
  assert.match(js, /function minimizePlayer\(\)/);
  assert.match(js, /function expandPlayer\(\)/);
  assert.match(js, /els\.player\.classList\.toggle\('mini', playerMini\)/);
  assert.match(js, /playerMini \? '⤢ Big screen' : '⧉ Side player'/);
  assert.match(js, /if \(playerMini\) closePlayer\(\);\s*else minimizePlayer\(\);/);
  assert.match(css, /#player\.mini \{/);
});

test('1.0.8: the Live Events tab has its own refresh and a live check per game', () => {
  const html = fs.readFileSync(path.join(renderer, 'index.html'), 'utf8');
  const js = fs.readFileSync(path.join(renderer, 'app.js'), 'utf8');
  const live = fs.readFileSync(path.join(renderer, 'live-events.js'), 'utf8');
  const preload = fs.readFileSync(path.join(__dirname, '..', 'src', 'main', 'preload.js'), 'utf8');
  const main = fs.readFileSync(path.join(__dirname, '..', 'src', 'main', 'main.js'), 'utf8');

  assert.match(html, /id="live-refresh"/);
  assert.match(html, />⟳ Refresh live games</);
  assert.match(js, /els\.liveRefresh\.addEventListener\('click'/);
  assert.match(js, /async function probeLiveGames\(force = false\)/);
  assert.match(js, /await api\.probeStream\(server\.url\)/);
  assert.match(js, /NO SIGNAL/);
  assert.match(live, /function teamsOf\(title\)/);
  assert.match(live, /function crestColorsFor\(name\)/);
  assert.match(preload, /probeStream: \(streamUrl\) => ipcRenderer\.invoke\('ptv:probe-stream', streamUrl\)/);
  assert.match(main, /ipcMain\.handle\('ptv:probe-stream'/);
});

test('1.1.2: Movies & Shows renders the on-demand catalogue in the side player', () => {
  const html = fs.readFileSync(path.join(renderer, 'index.html'), 'utf8');
  const js = fs.readFileSync(path.join(renderer, 'app.js'), 'utf8');

  assert.match(html, /data-tab="movies"[^>]*>Movies &amp; Shows</);
  assert.match(html, /id="view-movies"/);
  assert.match(html, /id="movies-grid"/);
  assert.match(html, /data-vod-filter="movie"/);
  assert.match(html, /data-vod-filter="episode"/);
  assert.doesNotMatch(html, /movies-browse/);
  assert.match(js, /movies: document\.getElementById\('view-movies'\)/);
  assert.match(js, /else if \(ui\.tab === 'movies'\) renderMovies\(\)/);
  assert.match(js, /function renderMovies\(\)/);
  assert.match(js, /function watchVod\(item\)/);
  assert.match(js, /meta\.vod_catalog/);
  assert.match(js, /data-vod-id/);
  // The image host must be reachable from the packaged renderer's CSP.
  assert.match(html, /img-src 'self' data: blob: https:\/\/archive\.org/);
  assert.match(css(), /\.vod-grid \{/);
  assert.match(css(), /\.vod-card \{/);
});

test('1.1.2: opening a channel starts in the side player, a click grows it', () => {
  const js = fs.readFileSync(path.join(renderer, 'app.js'), 'utf8');
  const openPlayer = js.slice(js.indexOf('async function openPlayer'), js.indexOf('function minimizePlayer'));
  assert.match(openPlayer, /playerMini = true;/);
  assert.match(js, /if \(playerMini && !els\.player\.hidden\) expandPlayer\(\)/);
  assert.match(js, /function expandPlayer\(\)/);
});

function css() {
  return fs.readFileSync(path.join(renderer, 'app.css'), 'utf8');
}

test('every els.<name> the renderer uses is collected in the els map and exists in the page', () => {
  const html = fs.readFileSync(path.join(renderer, 'index.html'), 'utf8');
  const js = fs.readFileSync(path.join(renderer, 'app.js'), 'utf8');
  const mapBlock = js.match(/const els = \{([\s\S]*?)\n  \};/);
  assert.ok(mapBlock, 'the els map exists');
  const defined = new Set([...mapBlock[1].matchAll(/^\s{4}(\w+):/gm)].map((m) => m[1]));
  const used = new Set([...js.matchAll(/\bels\.(\w+)/g)].map((m) => m[1]));
  // 1.0.8 shipped six dead controls exactly this way: the HTML and the
  // `if (els.X)`-guarded handlers existed, but the els entries did not, so
  // every guard was permanently false - the side-player button, both sort
  // toolbars, the category back button and the live refresh button did
  // nothing when clicked. Only keyboard paths still worked.
  for (const name of used) {
    assert.ok(defined.has(name), `els.${name} is used but never collected in the els map`);
  }
  for (const [, name, id] of mapBlock[1].matchAll(/^\s{4}(\w+): document\.getElementById\('([^']+)'\)/gm)) {
    assert.ok(html.includes(`id="${id}"`), `els.${name} looks up #${id}, which index.html does not contain`);
  }
});

test('1.1.3: HLS playback prefers supported AAC over undecodable AC-3 and recovers from silent SAP tracks', () => {
  const code = fs.readFileSync(path.join(renderer, 'player.js'), 'utf8');
  const videoListeners = {};
  let watchdogCallback = null;
  const video = {
    paused: false,
    ended: false,
    muted: false,
    volume: 1,
    currentTime: 0,
    webkitVideoDecodedByteCount: 0,
    webkitAudioDecodedByteCount: 0,
    pause() {},
    removeAttribute() {},
    load() {},
    addEventListener(name, fn) { videoListeners[name] = fn; },
    play() { return Promise.resolve(); },
  };
  const elements = {
    video,
    'player-spinner': { hidden: true },
    'player-error': { hidden: true },
    'player-error-text': { textContent: '' },
  };
  let activeHls = null;
  class Hls {
    static isSupported() { return true; }
    static Events = {
      ERROR: 'error',
      MANIFEST_PARSED: 'manifest',
      AUDIO_TRACKS_UPDATED: 'audio_tracks',
      AUDIO_TRACK_SWITCHED: 'audio_switched',
    };
    constructor() {
      this.handlers = {};
      this.levels = [
        { bitrate: 4000000, audioCodec: 'ac-3' },
        { bitrate: 2500000, audioCodec: 'mp4a.40.2' },
      ];
      this.currentLevel = 0;
      this.audioTracks = [
        { name: 'SAP Secondary', lang: 'es', audioCodec: 'mp4a.40.2' },
        { name: 'Main English', lang: 'en', audioCodec: 'mp4a.40.2' },
        { name: 'Backup English', lang: 'en', audioCodec: 'mp4a.40.2' },
      ];
      this.audioTrack = 0;
      activeHls = this;
    }
    on(evt, fn) { this.handlers[evt] = fn; }
    loadSource() {}
    attachMedia() {}
    destroy() {}
  }
  const MediaSource = {
    isTypeSupported: (mime) => mime.includes('mp4a.40.2'),
  };
  const sandbox = {
    window: { Hls, MediaSource, mpegts: { isSupported: () => false } },
    document: { getElementById: (id) => elements[id] },
    setTimeout: (fn) => { watchdogCallback = fn; return 1; },
    clearTimeout: () => { watchdogCallback = null; },
  };
  vm.runInNewContext(code, sandbox);

  const states = [];
  sandbox.window.PremiumPlayer.onAudioState((s) => states.push(s));
  sandbox.window.PremiumPlayer.play('http://127.0.0.1:1234/p/s1', 'https://example.org/master.m3u8');

  // Manifest parsed: level 0 (ac-3) is rejected by MSE, so level 1 (mp4a.40.2)
  // is chosen, and SAP track 0 is skipped in favour of Main English (track 1).
  activeHls.handlers.manifest();
  assert.equal(activeHls.currentLevel, 1, 'switches away from undecodable AC-3 variant');
  assert.equal(activeHls.audioTrack, 1, 'prefers primary audio track over SAP');

  // Simulate playing where video advances 4s but track 1 decodes 0 audio bytes:
  // the silent-audio watchdog automatically hops to track 2 (Backup English).
  videoListeners.playing();
  video.currentTime = 4.2;
  video.webkitVideoDecodedByteCount = 65536;
  video.webkitAudioDecodedByteCount = 0;
  assert.ok(watchdogCallback, 'the silent-audio watchdog is armed on playing');
  watchdogCallback();
  assert.equal(activeHls.audioTrack, 2, 'watchdog cycles away from a silent audio track');
  assert.ok(states.some((s) => s.switchedTrack && /Backup English/.test(s.switchedTrack)));

  // Manual track cycling and mute toggle work too.
  const cycled = sandbox.window.PremiumPlayer.cycleAudioTrack();
  assert.match(cycled, /SAP Secondary/);
  assert.equal(sandbox.window.PremiumPlayer.toggleMute(), true);
  assert.equal(sandbox.window.PremiumPlayer.toggleMute(), false);
});
