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

test('the committed catalogue publishes a shelf, not a coming-soon page', async (t) => {
  const app = setup(t);
  await tick();
  const doc = app.window.document;
  doc.querySelector('[data-tab="movies"]').click();

  assert.notEqual(app.catalog.status, 'coming_soon', 'the shelf is live again');
  assert.ok(app.catalog.items.length > 0, 'the catalogue publishes titles');
  assert.equal(doc.getElementById('movies-toolbar').hidden, false);
  const cards = [...doc.querySelectorAll('#movies-grid .vod-card')];
  assert.equal(cards.length, app.catalog.items.length, 'every entry gets a card');
  assert.equal(doc.getElementById('movies-empty').hidden, true);
  assert.match(doc.getElementById('movies-subtitle').textContent, /on demand/);
});

test('every published entry carries an embed or a direct stream', () => {
  const catalog = JSON.parse(fs.readFileSync(catalogPath, 'utf8'));
  assert.ok(catalog.items.length > 0);
  for (const item of catalog.items) {
    const playable = Boolean(item.stream || item.embed || item.embed_html);
    assert.ok(playable, `${item.title} has no stream and no embed`);
    if (item.embed) assert.match(item.embed, /^https:\/\//, `${item.title} embed is not https`);
  }
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

test('an embed mounts an iframe player, and the direct stream is the fallback server', async (t) => {
  const items = [
    film('vod-embedded', 'An Embedded Film', {
      embed: 'https://archive.org/embed/vod-embedded',
      embed_kind: 'iframe',
      provider: 'Internet Archive',
      embeds: [{ provider: 'Internet Archive', kind: 'iframe', url: 'https://archive.org/embed/vod-embedded' }],
      streams: ['https://archive.org/download/vod-embedded/vod-embedded.mp4'],
    }),
  ];
  const app = setup(t, { schema: 1, status: 'available', items });
  await tick();
  const doc = app.window.document;
  doc.querySelector('[data-tab="movies"]').click();
  doc.querySelector('[data-vod-id="vod-embedded"]').click();
  await tick();

  const host = doc.getElementById('player-embed');
  assert.equal(host.hidden, false, 'the embed host takes over the stage');
  const frame = host.querySelector('iframe');
  assert.ok(frame, 'an iframe player is mounted');
  assert.equal(frame.getAttribute('src'), 'https://archive.org/embed/vod-embedded');
  assert.equal(frame.getAttribute('allowfullscreen'), '');
  assert.equal(doc.getElementById('video').hidden, true, 'the video element steps aside');
  assert.equal(
    app.calls.resolved.length,
    0,
    'an embed is played by the provider, not by a proxy session',
  );
  // The transport drives a <video> element that is not in use.
  assert.equal(doc.getElementById('player-seek').hidden, true);
  assert.equal(doc.getElementById('player-toggle').hidden, true);
  assert.equal(doc.getElementById('player-mute').hidden, true);
  assert.match(doc.getElementById('player-now').textContent, /Internet Archive player/);

  // Server 2 is the direct MP4: switching to it hands the stage back.
  doc.getElementById('player-next-server').click();
  await tick();
  assert.equal(host.hidden, true, 'the embed is torn down');
  assert.equal(host.querySelector('iframe'), null, 'and its frame is dropped, not left playing');
  assert.equal(doc.getElementById('video').hidden, false);
  assert.equal(app.calls.resolved.length, 1);
  assert.equal(
    app.calls.resolved[0].streamUrl,
    'https://archive.org/download/vod-embedded/vod-embedded.mp4',
  );
});

test('a pasted embed snippet is mounted without running its scripts', async (t) => {
  const items = [
    film('vod-snippet', 'A Snippet Film', {
      embed: '',
      embed_kind: 'html',
      embed_html: '<iframe src="https://example.com/embed/abc" allowfullscreen></iframe><script>window.__pwned = 1;</script>',
      embeds: [],
      streams: ['https://archive.org/download/vod-snippet/vod-snippet.mp4'],
    }),
  ];
  const app = setup(t, { schema: 1, status: 'available', items });
  await tick();
  const doc = app.window.document;
  doc.querySelector('[data-tab="movies"]').click();
  doc.querySelector('[data-vod-id="vod-snippet"]').click();
  await tick();

  const host = doc.getElementById('player-embed');
  assert.equal(host.hidden, false);
  assert.equal(host.querySelector('iframe').getAttribute('src'), 'https://example.com/embed/abc');
  assert.equal(host.querySelector('script'), null, 'scripts never survive the mount');
  assert.equal(app.window.__pwned, undefined);
});

test('the packaged renderer may show archive and CDN artwork', () => {
  const html = fs.readFileSync(path.join(renderer, 'index.html'), 'utf8');
  assert.match(html, /img-src[^;]*https:\/\/cdn\.jsdelivr\.net/);
  assert.match(html, /img-src[^;]*https:\/\/archive\.org/);
});
