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

test('the launch splash shows the mark, a spinner and the version at the bottom', () => {
  const html = fs.readFileSync(path.join(renderer, 'index.html'), 'utf8');
  const css = fs.readFileSync(path.join(renderer, 'app.css'), 'utf8');
  const js = fs.readFileSync(path.join(renderer, 'app.js'), 'utf8');

  assert.match(html, /<div id="splash" role="status"/);
  assert.match(html, /class="splash-logo"/);
  assert.match(html, /class="splash-spinner"/);
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

function css() {
  return fs.readFileSync(path.join(renderer, 'app.css'), 'utf8');
}
