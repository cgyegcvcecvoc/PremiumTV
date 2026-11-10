'use strict';

/**
 * The Movies & Shows shelf's two states.
 *
 * The committed catalogue is paused, so the tracked tab must show its
 * coming-soon page and no poster grid. The second half of this file hands the
 * renderer a small in-memory catalogue with `status: "available"` and proves
 * the shelf, filters, search, multi-source fallback and side player still work
 * the moment the catalogue is restored.
 */

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { JSDOM } = require('jsdom');

const renderer = path.join(__dirname, '..', 'src', 'renderer');
const catalogPath = path.join(__dirname, '..', '..', '..', 'playlists', 'vod', 'vod-catalog.json');
const tick = () => new Promise((resolve) => setImmediate(resolve));

function film(id, title, extra = {}) {
  return {
    id,
    title,
    kind: 'movie',
    show: '',
    season: 0,
    episode: 0,
    year: 1968,
    genre: 'Horror',
    runtime_seconds: 5796,
    summary: 'A test film.',
    stream: `https://archive.org/download/${id}/${id}.mp4`,
    poster: `https://archive.org/services/img/${id}`,
    license: 'https://creativecommons.org/publicdomain/mark/1.0/',
    ...extra,
  };
}

function setup(t, catalogOverride = null) {
  const catalog = catalogOverride || JSON.parse(fs.readFileSync(catalogPath, 'utf8'));
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
    getAppInfo: async () => ({ version: '1.1.5' }),
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

test('the committed catalogue is paused, so the tab shows coming soon', async (t) => {
  const app = setup(t);
  await tick();
  const doc = app.window.document;
  doc.querySelector('[data-tab="movies"]').click();

  assert.equal(app.catalog.status, 'coming_soon');
  assert.equal(doc.querySelectorAll('#movies-grid .vod-card').length, 0, 'no shelf is advertised');
  assert.equal(doc.getElementById('movies-toolbar').hidden, true, 'search and filters are hidden');
  const empty = doc.getElementById('movies-empty');
  assert.equal(empty.hidden, false);
  assert.match(empty.textContent, /COMING SOON/);
  assert.match(empty.textContent, /Films and classic TV, on their way/);
  assert.match(doc.getElementById('movies-subtitle').textContent, /rebuilt/);
});

test('a restored catalogue renders the shelf and plays in the side player', async (t) => {
  const items = [
    film('vod-a', 'A Film'),
    film('vod-b', 'An Episode', { kind: 'episode', show: 'A Show', season: 1, episode: 2 }),
  ];
  const app = setup(t, { schema: 1, status: 'available', items });
  await tick();
  const doc = app.window.document;
  doc.querySelector('[data-tab="movies"]').click();

  assert.equal(doc.getElementById('movies-toolbar').hidden, false);
  assert.equal(doc.getElementById('movies-empty').hidden, true);
  const cards = [...doc.querySelectorAll('#movies-grid .vod-card')];
  assert.equal(cards.length, 2, 'every catalogue entry gets a card');
  assert.match(cards[0].textContent, /A Film/);
  assert.match(cards[0].textContent, /FILM/);

  doc.querySelector('[data-vod-filter="episode"]').click();
  const episodes = [...doc.querySelectorAll('#movies-grid .vod-card')];
  assert.equal(episodes.length, 1, 'the kind filter classifies the episode');
  assert.match(episodes[0].textContent, /S1 E2/);

  episodes[0].click();
  await tick();
  const resolved = app.calls.resolved.find((call) => call.channelId === 'vod-b');
  assert.ok(resolved, 'the card asks the main process for a playback session');
  assert.equal(app.calls.played.length, 1, 'the side player is started once');
  assert.equal(app.calls.played[0][0], 'http://127.0.0.1:1234/p/session-1');
  assert.equal(doc.getElementById('player').hidden, false);
  assert.ok(doc.getElementById('player').classList.contains('mini'), 'it opens docked, not full screen');
});

test('a restored catalogue keeps search, genre chips and multi-source transport', async (t) => {
  const items = [
    film('vod-suddenly', 'Suddenly', {
      year: 1954,
      genre: 'Thriller',
      runtime_seconds: 4500,
      stream: 'https://archive.org/download/suddenly/suddenly_512kb.mp4',
      streams: [
        'https://archive.org/download/suddenly/suddenly_512kb.mp4',
        'https://archive.org/download/suddenly/suddenly.mp4',
      ],
    }),
    film('vod-mclintock', 'McLintock!', { year: 1963, genre: 'Comedy', runtime_seconds: 7620 }),
    film('vod-nosferatu', 'Nosferatu', { year: 1922, genre: 'Horror' }),
  ];
  const app = setup(t, { schema: 1, status: 'available', items });
  await tick();
  const doc = app.window.document;
  doc.querySelector('[data-tab="movies"]').click();

  const genreChips = [...doc.querySelectorAll('#movies-genres [data-vod-genre]')];
  assert.ok(genreChips.length >= 4, 'genre filter chips are rendered');

  const thrillerChip = doc.querySelector('[data-vod-genre="Thriller"]');
  assert.ok(thrillerChip, 'Thriller genre chip is present');
  thrillerChip.click();
  assert.ok(doc.querySelector('[data-vod-id="vod-suddenly"]'), 'Suddenly appears under Thriller');
  assert.equal(doc.querySelectorAll('#movies-grid .vod-card').length, 1);

  doc.querySelector('[data-vod-genre="all"]').click();
  const search = doc.getElementById('movies-search');
  search.value = 'McLintock';
  search.dispatchEvent(new app.window.Event('input'));
  const filteredCards = [...doc.querySelectorAll('#movies-grid .vod-card')];
  assert.equal(filteredCards.length, 1);
  assert.equal(filteredCards[0].dataset.vodId, 'vod-mclintock');

  doc.querySelector('[data-vod-genre="all"]').click();
  search.value = '';
  search.dispatchEvent(new app.window.Event('input'));
  const suddenly = doc.querySelector('[data-vod-id="vod-suddenly"]');
  suddenly.click();
  await tick();
  assert.equal(doc.getElementById('player-server').hidden, false, 'multi-source VOD exposes backup source badge');
  assert.equal(doc.getElementById('player-seek').hidden, false, 'VOD reveals timeline scrubber');
  assert.equal(doc.getElementById('player-live-pill').hidden, true, 'VOD hides live pill');
});

test('the packaged renderer may show archive and CDN artwork', () => {
  const html = fs.readFileSync(path.join(renderer, 'index.html'), 'utf8');
  assert.match(html, /img-src[^;]*https:\/\/cdn\.jsdelivr\.net/);
  assert.match(html, /img-src[^;]*https:\/\/archive\.org/);
});
