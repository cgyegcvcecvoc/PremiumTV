'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync } = require('node:child_process');

const { parseM3u, parseXmltv, orderGroups } = require('../src/main/parsers');

const ROOT = path.join(__dirname, '..', '..', '..');
const PLAYLIST = path.join(ROOT, 'playlists', 'countries', 'USA.m3u');
const GUIDE = path.join(ROOT, 'EPG', 'USA.xml');
const BUILD_BUNDLE = path.join(ROOT, 'android', 'tools', 'build_bundle.py');

/** Run the repository's own bundle builder and return its meta.json. */
function referenceMeta() {
  const out = fs.mkdtempSync(path.join(os.tmpdir(), 'ptv-bundle-'));
  execFileSync('python3', [BUILD_BUNDLE, '--out', out, '--version', 'test'], { stdio: 'pipe' });
  return JSON.parse(fs.readFileSync(path.join(out, 'meta.json'), 'utf8'));
}

test('parseM3u reproduces the channel and group counts the reference builder publishes', { timeout: 120000 }, () => {
  const meta = referenceMeta();
  const text = fs.readFileSync(PLAYLIST, 'utf8');
  const publishedOrder = JSON.parse(
    fs.readFileSync(path.join(ROOT, 'categories', 'index.json'), 'utf8'),
  ).order;

  const { channels, guideUrl } = parseM3u(text);
  assert.equal(channels.length, meta.channel_count, 'channel count must match the reference bundle builder');

  const groups = orderGroups(channels, publishedOrder);
  assert.equal(groups.length, meta.group_count, 'group count must match the reference bundle builder');

  // The first published category is Sports, per the repository taxonomy.
  assert.equal(groups[0].name, 'Sports');

  assert.match(guideUrl, /USA\.xml$/, 'the playlist should advertise the USA guide');

  for (const channel of channels.slice(0, 400)) {
    assert.ok(channel.url, 'every parsed channel must carry a stream URL');
    assert.ok(channel.id, 'every parsed channel must carry an id');
    assert.ok(channel.name.length > 0);
  }
});

test('parseM3u reads stream headers from #EXTVLCOPT / #KODIPROP', () => {
  const sample = [
    '#EXTM3U x-tvg-url="https://example.com/guide.xml"',
    '#EXTINF:-1 tvg-id="demo.us" tvg-logo="https://x/y.png" group-title="Sports",Demo HD',
    '#EXTVLCOPT:http-referrer=https://referrer.example/',
    '#KODIPROP:http-user-agent=DemoAgent/1.0',
    'http://stream.example/demo.m3u8',
  ].join('\n');

  const { channels, guideUrl } = parseM3u(sample);
  assert.equal(guideUrl, 'https://example.com/guide.xml');
  assert.equal(channels.length, 1);
  assert.equal(channels[0].referrer, 'https://referrer.example/');
  assert.equal(channels[0].ua, 'DemoAgent/1.0');
  assert.equal(channels[0].url, 'http://stream.example/demo.m3u8');
  assert.equal(channels[0].group, 'Sports');
});

test('parseM3u drops the sanctioned update notice and keeps lookalikes', () => {
  // scripts/legacy_sunset.py publishes one entry marked tvg-notice="app-update"
  // into the legacy USA feed so an installed build with no updater can be told
  // about a newer release. It is a message, never a channel.
  const sample = [
    '#EXTM3U x-tvg-url="https://example.org/guide.xml"',
    '#EXTINF:-1 tvg-id="premiumtv.notice.update" tvg-notice="app-update" ' +
      'group-title="PremiumTV Notice",⚠ UPDATE PremiumTV — support for 1.0.4 and older ends Nov 16, 2026',
    'https://github.com/cgyegcvcecvoc/PremiumTV1/releases/latest',
    '#EXTINF:-1 tvg-id="notice.tv" tvg-notice="schedule" group-title="News",Notice TV',
    'https://example.org/notice.m3u8',
  ].join('\n');

  const { channels, guideUrl } = parseM3u(sample);
  assert.equal(guideUrl, 'https://example.org/guide.xml');
  assert.equal(channels.length, 1);
  assert.equal(channels[0].name, 'Notice TV');
});

test('parseXmltv parses programmes into the bundle shape and drops stale listings', { timeout: 120000 }, () => {
  const meta = referenceMeta();
  const { channels } = parseM3u(fs.readFileSync(PLAYLIST, 'utf8'));
  const known = new Set(channels.map((c) => c.id).filter(Boolean));

  const programmes = parseXmltv(fs.readFileSync(GUIDE, 'utf8'), { knownIds: known });
  assert.ok(programmes.length > 5000, `expected thousands of listings, got ${programmes.length}`);
  assert.ok(
    Math.abs(programmes.length - meta.programme_count) <= 5,
    `JS guide parse (${programmes.length}) should match the reference builder (${meta.programme_count})`,
  );

  const first = programmes[0];
  for (const key of ['c', 's', 'e', 't', 'd', 'g', 'i', 'ep']) assert.ok(key in first, `programme needs ${key}`);
  assert.ok(known.has(first.c), 'programmes must be limited to published channels');
});

test('xmltvTime handles offsets both ways', () => {
  const { xmltvTime } = require('../src/main/parsers');
  const utc = xmltvTime('20261011043000 +0000');
  const eastern = xmltvTime('20261011003000 -0400');
  assert.equal(utc, eastern);
  assert.equal(utc, Date.UTC(2026, 9, 11, 4, 30, 0) / 1000);
});


test('parseM3u preserves commas in quoted metadata and channel display names', () => {
  const { channels } = parseM3u([
    '#EXTM3U',
    '#EXTINF:-1 tvg-id="news.local" group-title="News, Local",News, Local',
    'https://example.org/news.m3u8',
  ].join('\n'));
  assert.equal(channels[0].group, 'News, Local');
  assert.equal(channels[0].name, 'News, Local');
});

test('xmltvTime rejects impossible values and malformed suffixes', () => {
  const { xmltvTime } = require('../src/main/parsers');
  assert.equal(xmltvTime('20261131010000 +0000'), 0);
  assert.equal(xmltvTime('00000101000000 +0000'), 0);
  assert.equal(xmltvTime('20261101010000 +2460'), 0);
  assert.equal(xmltvTime('20261101010000 +0000 trailing'), 0);
});

test('parseXmltv repairs a non-positive duration and drops an invalid date', () => {
  const xml = `<tv>
    <programme channel="demo" start="20261101010000 +0000" stop="20261101000000 +0000">
      <title>Valid start</title>
    </programme>
    <programme channel="demo" start="20261131010000 +0000" stop="20261131020000 +0000">
      <title>Invalid calendar date</title>
    </programme>
  </tv>`;
  const programmes = parseXmltv(xml, { knownIds: new Set(['demo']), nowSeconds: 0 });
  assert.equal(programmes.length, 1);
  assert.equal(programmes[0].t, 'Valid start');
  assert.equal(programmes[0].e - programmes[0].s, 1800);
});
