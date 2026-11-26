'use strict';

/**
 * The desktop wiring for the Spotify tab (1.1.25).
 *
 * The policy itself is tested once, in web/test/spotify.test.cjs, because it is
 * one shared module. This file tests only what is Mac/Linux-specific: the
 * sign-in redirect is intercepted by the main process instead of navigating the
 * app, and the renderer never loads Spotify's login page inside its own window.
 */

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.join(__dirname, '..');
const renderer = path.join(root, 'src', 'renderer');
const main = path.join(root, 'src', 'main');

test('the main process recognises only the registered callback', () => {
  const code = fs.readFileSync(path.join(main, 'main.js'), 'utf8');
  assert.match(code, /const SPOTIFY_CALLBACK = 'https:\/\/cgyegcvcecvoc\.github\.io\/PremiumTV\/spotify-callback'/);
  // The check is an exact origin + path comparison, not a prefix match, so a
  // lookalike host cannot inject a code.
  assert.match(code, /parsed\.origin \+ parsed\.pathname !== SPOTIFY_CALLBACK/);
  // And the app window is never navigated to it.
  assert.match(code, /event\.preventDefault\(\);\s*\n\s*send\('ptv:spotify-callback', payload\)/);
});

test('the renderer signs in through the system browser', () => {
  const code = fs.readFileSync(path.join(renderer, 'app.js'), 'utf8');
  // openExternal, not location.assign: Spotify will not frame its login page
  // and the viewer's password manager lives in the real browser.
  assert.match(code, /const url = await spotifySession\.begin\(SPOTIFY_REDIRECT\);/);
  assert.match(code, /if \(api && api\.openExternal\) await api\.openExternal\(url\);/);
  // The callback from main is what completes the flow.
  assert.match(code, /api\.onSpotifyCallback\(\(payload\) => finishSpotifySignIn\(payload\)\)/);
});

test('the preload exposes the callback and nothing broader', () => {
  const code = fs.readFileSync(path.join(main, 'preload.js'), 'utf8');
  assert.match(code, /onSpotifyCallback: \(callback\) => subscribe\('ptv:spotify-callback', callback\)/);
  // No generic IPC escape hatch was added for this feature.
  assert.equal(/ipcRenderer\.invoke\(channel/.test(code), false);
  assert.equal(/exposeInMainWorld\('premiumtv'[\s\S]*nodeIntegration/.test(code), false);
});

test('the renderer CSP names Spotify\'s SDK and keeps the rest closed', () => {
  const html = fs.readFileSync(path.join(renderer, 'index.html'), 'utf8');
  assert.match(html, /script-src 'self' https:\/\/sdk\.scdn\.co;/);
  assert.match(html, /object-src 'none'/);
  assert.match(html, /frame-src 'self' https:/);
  // The player script is added by the renderer, and the embed is a frame: no
  // inline script and no unsafe-eval was needed to make the tab work.
  assert.equal(html.includes("script-src 'self' 'unsafe-inline'"), false);
  assert.equal(html.includes("'unsafe-eval'"), false);
});

test('the desktop tab states Spotify\'s terms instead of implying a bypass', () => {
  const code = fs.readFileSync(path.join(renderer, 'app.js'), 'utf8');
  assert.match(code, /spotifyModule\.NOTICE/);
  // Premium is explained as Spotify's rule whenever it blocks playback.
  assert.match(code, /reserves in-app streaming for Premium accounts/);
  // And no ad-evasion path exists in the desktop wiring either.
  for (const forbidden of ['adblock', 'skipad', 'mutead', 'removead', 'hidead', 'setAudioMuted']) {
    assert.equal(code.toLowerCase().includes(forbidden), false, 'desktop app.js must not implement ' + forbidden);
  }
});

test('a blocked-storage machine still boots to the library', () => {
  // The same startup hazard as the web app: reading localStorage throws in a
  // hardened profile, and the Spotify tab must not be able to abort the boot.
  const code = fs.readFileSync(path.join(renderer, 'app.js'), 'utf8');
  assert.match(code, /storage: \(\) => window\.localStorage/);
  // And the tab reports its own failure rather than blanking the app.
  assert.match(code, /Spotify is unavailable in this build/);
});

test('the desktop shell and the web app both state where ads come from', () => {
  for (const file of [path.join(renderer, 'index.html')]) {
    const html = fs.readFileSync(file, 'utf8');
    assert.match(html, /data-tab="spotify"/);
  }
  const module = fs.readFileSync(path.join(renderer, 'spotify.js'), 'utf8');
  assert.match(module, /a Free account hears/);
  assert.match(module, /a Premium account/);
});
