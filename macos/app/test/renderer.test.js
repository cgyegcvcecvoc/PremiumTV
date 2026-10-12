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
