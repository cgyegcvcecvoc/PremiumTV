'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const fsp = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');

const { TvRepository } = require('../src/main/repository');

const PLAYLIST_TEXT = [
  '#EXTM3U x-tvg-url="https://example.com/EPG/USA.xml"',
  '#EXTINF:-1 tvg-id="sports.one" group-title="Sports",Sports One',
  'http://stream.example/sports-one.m3u8',
  '#EXTINF:-1 tvg-id="cartoons.two" group-title="Cartoons",Cartoons Two',
  'http://stream.example/cartoons-two.m3u8',
].join('\n');

const GUIDE_TEXT = `<?xml version="1.0" encoding="UTF-8"?>
<tv>
  <programme start="${stamp(+0)}" stop="${stamp(+1)}" channel="sports.one">
    <title>Match of the Day</title><desc>Football.</desc>
  </programme>
</tv>`;

function stamp(offsetHours) {
  const base = Math.floor(Date.now() / 3600000) * 3600; // hour boundary
  const date = new Date((base + offsetHours * 3600) * 1000);
  const p = (n) => String(n).padStart(2, '0');
  return (
    `${date.getUTCFullYear()}${p(date.getUTCMonth() + 1)}${p(date.getUTCDate())}` +
    `${p(date.getUTCHours())}${p(date.getUTCMinutes())}00 +0000`
  );
}

function makeBundleDir(root) {
  const bundle = path.join(root, 'bundle');
  fs.mkdirSync(bundle, { recursive: true });
  fs.writeFileSync(path.join(bundle, 'meta.json'), JSON.stringify({
    version: 'test',
    playlist_url: 'https://raw.example/USA.m3u',
    guide_url: 'https://raw.example/USA.xml',
    channel_count: 2,
    group_count: 2,
    programme_count: 1,
    published_order: ['Sports'],
  }, null, 2));
  fs.writeFileSync(path.join(bundle, 'channels.jsonl'),
    JSON.stringify({ id: 'sports.one', name: 'Sports One', logo: '', group: 'Sports', country: 'US', chno: '', ua: '', referrer: '', url: 'http://stream.example/sports-one.m3u8' }) + '\n' +
    JSON.stringify({ id: 'cartoons.two', name: 'Cartoons Two', logo: '', group: 'Cartoons', country: 'US', chno: '', ua: '', referrer: '', url: 'http://stream.example/cartoons-two.m3u8' }) + '\n');
  fs.writeFileSync(path.join(bundle, 'groups.jsonl'),
    JSON.stringify({ name: 'Sports', count: 1 }) + '\n' + JSON.stringify({ name: 'Cartoons', count: 1 }) + '\n');
  fs.writeFileSync(path.join(bundle, 'epg.jsonl'),
    JSON.stringify({ c: 'sports.one', s: 1, e: 2, t: 'Old', d: '', g: '', i: '', ep: '' }) + '\n');
  return bundle;
}

function makeResponse({ status = 200, body = '', headers = {} } = {}) {
  return {
    status,
    ok: status >= 200 && status < 300,
    headers: new Map(Object.entries(headers)),
    text: async () => body,
  };
}

function makeRepository(root, fetchImpl) {
  return new TvRepository({
    bundleDir: makeBundleDir(root),
    cacheDir: path.join(root, 'cache'),
    stateFile: path.join(root, 'state.json'),
    fetchImpl,
  });
}

test('load falls back to the bundled copy when there is no cache', async () => {
  const root = await fsp.mkdtemp(path.join(os.tmpdir(), 'ptv-'));
  const repository = makeRepository(root, async () => makeResponse());
  await repository.load();
  assert.equal(repository.state.phase, 'ready');
  assert.equal(repository.state.source, 'bundled');
  assert.equal(repository.library.channels.length, 2);
});

test('a manual refresh downloads, parses and swaps the cache atomically', async () => {
  const root = await fsp.mkdtemp(path.join(os.tmpdir(), 'ptv-'));
  const seen = [];
  const repository = makeRepository(root, async (url, init) => {
    seen.push(url);
    return url.endsWith('.xml') || url.includes('guide')
      ? makeResponse({ body: GUIDE_TEXT, headers: { etag: '"g1"', 'last-modified': 'Mon, 05 Oct 2026 00:00:00 GMT' } })
      : makeResponse({ body: PLAYLIST_TEXT, headers: { etag: '"p1"', 'last-modified': 'Mon, 05 Oct 2026 00:00:00 GMT' } });
  });
  await repository.load();

  const outcome = await repository.refresh('manual');
  assert.equal(outcome.ok, true, outcome.message);
  assert.equal(outcome.updated, true);
  assert.equal(seen.length, 2, 'both files download on a manual refresh');

  assert.equal(repository.state.source, 'cache');
  assert.ok(fs.existsSync(path.join(root, 'cache', 'meta.json')));
  assert.ok(!fs.existsSync(path.join(root, 'cache-staging')), 'staging is removed after swap');
  assert.ok(!fs.existsSync(path.join(root, 'cache-backup')), 'backup is removed after swap');

  // The parsed guide from the download replaced the bundled one.
  const names = repository.library.programmes.map((p) => p.t);
  assert.ok(names.includes('Match of the Day'), `guide parsed, got ${names}`);
});

test('an automatic refresh sends validators and honours 304', async () => {
  const root = await fsp.mkdtemp(path.join(os.tmpdir(), 'ptv-'));
  let calls = 0;
  const fetchImpl = async (url, init) => {
    calls += 1;
    if (calls <= 2) {
      // First automatic refresh: full download with validators stored.
      return url.includes('guide') || url.endsWith('.xml')
        ? makeResponse({ body: GUIDE_TEXT, headers: { etag: '"g1"' } })
        : makeResponse({ body: PLAYLIST_TEXT, headers: { etag: '"p1"' } });
    }
    // Subsequent: both 304.
    return makeResponse({ status: 304 });
  };
  const repository = makeRepository(root, fetchImpl);
  await repository.load();

  const first = await repository.refresh('automatic');
  assert.equal(first.updated, true);

  const second = await repository.refresh('automatic');
  assert.equal(second.ok, true);
  assert.equal(second.updated, false, 'two 304s mean no update');
});

test('a failed refresh keeps the previous cache and reports retryable', async () => {
  const root = await fsp.mkdtemp(path.join(os.tmpdir(), 'ptv-'));
  let fail = false;
  const fetchImpl = async (url) => {
    if (fail) throw new Error('ENOTFOUND');
    return url.includes('guide') || url.endsWith('.xml')
      ? makeResponse({ body: GUIDE_TEXT, headers: { etag: '"g1"' } })
      : makeResponse({ body: PLAYLIST_TEXT, headers: { etag: '"p1"' } });
  };
  const repository = makeRepository(root, fetchImpl);
  await repository.load();
  const good = await repository.refresh('manual');
  assert.equal(good.ok, true);

  fail = true;
  const bad = await repository.refresh('automatic');
  assert.equal(bad.ok, false);
  assert.equal(bad.retryable, true);

  // Cache still present and usable.
  assert.ok(fs.existsSync(path.join(root, 'cache', 'meta.json')));
  await repository.load();
  assert.equal(repository.state.phase, 'ready');
});

test('resetToBundled drops the cache and falls back to the bundle', async () => {
  const root = await fsp.mkdtemp(path.join(os.tmpdir(), 'ptv-'));
  const fetchImpl = async (url) =>
    url.includes('guide') || url.endsWith('.xml')
      ? makeResponse({ body: GUIDE_TEXT, headers: { etag: '"g1"' } })
      : makeResponse({ body: PLAYLIST_TEXT, headers: { etag: '"p1"' } });
  const repository = makeRepository(root, fetchImpl);
  await repository.load();
  await repository.refresh('manual');
  assert.equal(repository.state.source, 'cache');

  await repository.resetToBundled();
  assert.equal(repository.state.source, 'bundled');
  assert.ok(!fs.existsSync(path.join(root, 'cache')));
});
