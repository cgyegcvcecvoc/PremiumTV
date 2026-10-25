'use strict';

/**
 * The Movies & Shows shelf, exercised against the real committed catalogue.
 *
 * The renderer tests elsewhere prove the tab and the renderer code exist; this
 * one loads playlists/vod/vod-catalog.json the way the bundle hands it over, so
 * the test card added for end-to-end playback checks that it renders, that the
 * filters treat it as a film, and that choosing it resolves the exact stream
 * URL and hands it to the same player a channel uses.
 */

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { JSDOM } = require('jsdom');

const renderer = path.join(__dirname, '..', 'src', 'renderer');
const catalogPath = path.join(__dirname, '..', '..', '..', 'playlists', 'vod', 'vod-catalog.json');
const TEST_CARD_ID = 'vod-premiumtv-test-card';
const tick = () => new Promise((resolve) => setImmediate(resolve));

function setup(t) {
  const catalog = JSON.parse(fs.readFileSync(catalogPath, 'utf8'));
  const dom = new JSDOM(fs.readFileSync(path.join(renderer, 'index.html'), 'utf8'), {
    runScripts: 'outside-only',
    url: 'http://127.0.0.1:1234',
  });
  t.after(() => dom.window.close());

  const calls = { resolved: [], played: [] };
  const snapshot = {
    state: { phase: 'ready', message: 'Loaded' },
    info: {},
    library: {
      channels: [],
      groups: [],
      programmes: [],
      meta: { vod_catalog: catalog },
    },
  };
  dom.window.premiumtv = {
    getAppInfo: async () => ({ version: '1.1.2' }),
    getSnapshot: async () => structuredClone(snapshot),
    updateStatus: async () => null,
    checkForUpdate: async () => null,
    downloadUpdate: async () => null,
    installUpdate: async () => ({ ok: true }),
    openReleasePage: async () => ({ ok: true }),
    dismissUpdateNotice: async () => ({ ok: true }),
    diagnostics: async () => ({}),
    resolveStream: async (channelId, streamUrl) => {
      calls.resolved.push({ channelId, streamUrl });
      return { ok: true, sessionId: 'session-1', url: 'http://127.0.0.1:1234/p/session-1' };
    },
    releaseStream: async () => {},
    probeStream: async () => ({ ok: true }),
    onState: () => {},
    onInfo: () => {},
    onProgress: () => {},
    onUpdate: () => {},
    onSelectTab: () => {},
  };
  dom.window.PremiumPlayer = {
    play: (...args) => calls.played.push(args),
    stop() {},
    retry() {},
    fail() {},
  };
  for (const module of ['category-icons.js', 'live-events.js', 'personal.js', 'app.js']) {
    dom.window.eval(fs.readFileSync(path.join(renderer, module), 'utf8'));
  }
  return { window: dom.window, calls, catalog };
}

test('1.1.2: the test card renders on Movies & Shows and plays in the side player', async (t) => {
  const app = setup(t);
  await tick();
  const doc = app.window.document;
  doc.querySelector('[data-tab="movies"]').click();

  const cards = [...doc.querySelectorAll('#movies-grid .vod-card')];
  assert.equal(cards.length, app.catalog.items.length, 'every catalogue entry gets a card');

  const card = doc.querySelector(`[data-vod-id="${TEST_CARD_ID}"]`);
  assert.ok(card, 'the committed test card is on the shelf');
  assert.match(card.textContent, /PremiumTV Test Card/);
  assert.match(card.textContent, /FILM/, 'the test card is a film, not an episode');
  assert.match(card.textContent, /2026 · Test/);
  assert.equal(card.dataset.vodKind, 'movie');

  const item = app.catalog.items.find((entry) => entry.id === TEST_CARD_ID);
  assert.ok(item.stream.startsWith('https://'), 'the bundled stream is a direct URL');
  assert.ok(item.poster.startsWith('https://'), 'the bundled poster is a direct URL');

  // The filters classify it by kind instead of hard-coding the Archive titles.
  doc.querySelector('[data-vod-filter="episode"]').click();
  assert.equal(doc.querySelector(`[data-vod-id="${TEST_CARD_ID}"]`), null);
  doc.querySelector('[data-vod-filter="movie"]').click();
  assert.ok(doc.querySelector(`[data-vod-id="${TEST_CARD_ID}"]`));

  // Choosing it resolves the stream through the main process and hands the
  // original URL to the player as the format hint, exactly like a channel.
  doc.querySelector(`[data-vod-id="${TEST_CARD_ID}"]`).click();
  await tick();
  const resolved = app.calls.resolved.find((call) => call.channelId === TEST_CARD_ID);
  assert.ok(resolved, 'the card asks the main process for a playback session');
  assert.equal(resolved.streamUrl, item.stream);
  assert.equal(app.calls.played.length, 1, 'the side player is started once');
  assert.equal(app.calls.played[0][0], 'http://127.0.0.1:1234/p/session-1');
  assert.equal(app.calls.played[0][1], item.stream, 'the player receives the test-card stream');
  assert.equal(doc.getElementById('player').hidden, false);
  assert.ok(doc.getElementById('player').classList.contains('mini'), 'it opens docked, not full screen');
});

test('1.1.2: the packaged renderer may show the test card poster', () => {
  const html = fs.readFileSync(path.join(renderer, 'index.html'), 'utf8');
  // Same-origin data URIs are already allowed; the test card's poster is served
  // beside the film from the repository's CDN, which the CSP has to name.
  assert.match(html, /img-src[^;]*https:\/\/cdn\.jsdelivr\.net/);
  assert.match(html, /img-src[^;]*https:\/\/archive\.org/);
});
