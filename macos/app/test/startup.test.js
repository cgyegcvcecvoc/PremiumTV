'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { JSDOM } = require('jsdom');
const renderer = path.join(__dirname, '..', 'src', 'renderer');
const tick = () => new Promise((resolve) => setImmediate(resolve));

function library(name = 'Sports One') {
  return {
    channels: [{ id: 'one', name, group: 'Sports', country: 'US', url: 'https://example.org/live.m3u8' }],
    groups: [{ name: 'Sports', count: 1 }],
    programmes: [{ c: 'one', s: Date.now() / 1000 - 60, e: Date.now() / 1000 + 3600, t: 'Live match' }],
  };
}
function setup(t, initial, appInfo = { version: '1.0.2' }) {
  const dom = new JSDOM(fs.readFileSync(path.join(renderer, 'index.html'), 'utf8'), {
    runScripts: 'outside-only', url: 'http://127.0.0.1:1234',
  });
  t.after(() => dom.window.close());
  let current = initial;
  const events = {};
  dom.window.premiumtv = {
    getAppInfo: async () => structuredClone(appInfo),
    getSnapshot: async () => structuredClone(current),
    onState: (fn) => { events.state = fn; },
    onProgress: (fn) => { events.progress = fn; },
    onInfo: (fn) => { events.info = fn; },
    onSelectTab() {},
  };
  dom.window.PremiumPlayer = { stop() {} };
  dom.window.eval(fs.readFileSync(path.join(renderer, 'app.js'), 'utf8'));
  return { window: dom.window, events, set: (value) => { current = value; } };
}
const empty = () => ({ state: { phase: 'loading' }, info: {}, library: { channels: [], groups: [], programmes: [] } });
const ready = (name) => ({ state: { phase: 'ready', message: 'Loaded' }, info: {}, library: library(name) });

test('cold launch fetches channels and guide when ready arrives after the initial empty snapshot', async (t) => {
  const app = setup(t, empty());
  await tick();
  assert.equal(app.window.document.querySelectorAll('.card').length, 0);
  app.set(ready());
  app.events.state({ phase: 'ready', message: 'Loaded' });
  await tick();
  assert.equal(app.window.document.querySelector('.card-name')?.textContent, 'Sports One');
  assert.equal(app.window.document.querySelector('.card-now')?.textContent, 'Live match');
  assert.match(app.window.document.getElementById('foot-count').textContent, /1 channels/);
});

test('channels are visible during guide loading and a refresh replaces displayed rows', async (t) => {
  const app = setup(t, empty());
  await tick();
  const partial = ready();
  partial.state.phase = 'loading';
  partial.library.programmes = [];
  app.set(partial);
  app.events.progress({ phase: 'channels', count: 1 });
  await tick();
  assert.equal(app.window.document.querySelector('.card-name')?.textContent, 'Sports One');
  app.set(ready('Updated Sports'));
  app.events.state({ phase: 'ready' });
  await tick();
  assert.equal(app.window.document.querySelector('.card-name')?.textContent, 'Updated Sports');
  assert.equal(app.window.document.querySelector('.card-now')?.textContent, 'Live match');
});

test('a late initial snapshot cannot overwrite a newer ready snapshot', async (t) => {
  const app = setup(t, empty());
  let resolveOld;
  let first = true;
  app.window.premiumtv.getSnapshot = () => {
    if (first) {
      first = false;
      return new Promise((resolve) => { resolveOld = resolve; });
    }
    return Promise.resolve(ready());
  };
  await tick();
  app.events.state({ phase: 'ready' });
  await tick();
  resolveOld(empty());
  await tick();
  assert.equal(app.window.document.querySelector('.card-name')?.textContent, 'Sports One');
});

test('loading failure is visible rather than silently showing an empty grid', async (t) => {
  const app = setup(t, empty());
  await tick();
  const failure = empty();
  failure.state = { phase: 'error', message: 'Bundle missing <retry>' };
  app.set(failure);
  app.events.state(failure.state);
  await tick();
  assert.equal(app.window.document.querySelector('.empty-state')?.textContent, failure.state.message);
  assert.equal(app.window.document.querySelector('retry'), null);
});

function previewLibrary() {
  const preview = ready('Public One');
  const now = Math.floor(Date.now() / 1000);
  preview.library.meta = { version: '1.1.1', library_scope: 'all', preview_features: ['cable-guide'] };
  preview.library.channels = [
    { id: 'one', name: 'Public One', group: 'Sports', country: 'US', chno: '12', url: 'https://example.org/one.m3u8' },
    // A backup feed shares the EPG id of its channel: the grid shows one row.
    { id: 'one', name: 'Public One (Backup 1)', group: 'Sports Backups', country: 'US', url: 'https://example.org/one-b.m3u8' },
    { id: 'news', name: 'Newsroom', group: 'News', country: 'US', url: 'https://example.org/news.m3u8' },
    { id: 'quiet', name: 'No Listings TV', group: 'News', country: 'US', url: 'https://example.org/quiet.m3u8' },
  ];
  preview.library.groups = [
    { name: 'Sports', count: 1 }, { name: 'News', count: 2 }, { name: 'Sports Backups', count: 1 },
  ];
  preview.library.programmes = [
    { c: 'one', s: now - 900, e: now + 1800, t: 'Live match', g: 'Sports', d: 'The big game.' },
    { c: 'one', s: now + 1800, e: now + 5400, t: 'Post-game', g: 'Sports' },
    { c: 'news', s: now - 1200, e: now + 2400, t: 'Evening News' },
  ];
  return preview;
}

test('the preview Guide tab is the cable-style grid: channels left, shows right, times on top', async (t) => {
  const app = setup(t, previewLibrary());
  await tick();
  const doc = app.window.document;
  assert.equal(doc.getElementById('cable-tab'), null, 'the separate 1.1.0 Cable tab is gone');
  doc.querySelector('[data-tab="guide"]').click();

  assert.equal(doc.getElementById('view-guide').hidden, false);
  assert.equal(doc.getElementById('guide-grid').hidden, false);
  assert.equal(doc.getElementById('guide-list').hidden, true);
  // Times across the top: sixteen half-hour slots from the current half hour.
  const ticks = [...doc.querySelectorAll('.cable-header-row .cable-time-tick')];
  assert.equal(ticks.length, 16);
  assert.match(ticks[0].textContent, /\d{1,2}:\d{2}/);
  assert.ok(doc.querySelector('.guide-now-marker'));
  // Channels down the left, one row each, in the published category order.
  const rows = [...doc.querySelectorAll('.cable-row:not(.cable-header-row)')];
  assert.deepEqual(rows.map((row) => row.querySelector('.cable-channel-name').textContent), ['Public One', 'Newsroom']);
  assert.deepEqual([...doc.querySelectorAll('.cable-section-name')].map((n) => n.textContent), ['Sports', 'News']);
  assert.equal(rows[0].querySelector('.cable-number').textContent, '12');
  // What is playing, to the right, sized by time, with the live show marked.
  const cells = [...rows[0].querySelectorAll('.cable-programme')];
  assert.deepEqual(cells.map((cell) => cell.querySelector('.cable-programme-title').textContent), ['Live match', 'Post-game']);
  assert.ok(cells[0].classList.contains('current'));
  assert.ok(parseFloat(cells[1].style.left) > parseFloat(cells[0].style.left));
  assert.ok(rows[0].querySelector('.cable-now-line'));

  // The detail strip follows the pointer and the keyboard.
  cells[0].dispatchEvent(new app.window.MouseEvent('mouseover', { bubbles: true }));
  assert.equal(doc.querySelector('#guide-info .guide-info-title').textContent, 'Live match');
  assert.equal(doc.querySelector('#guide-info .guide-info-desc').textContent, 'The big game.');
  cells[0].focus();
  cells[0].dispatchEvent(new app.window.KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true }));
  assert.equal(doc.activeElement, cells[1]);
  assert.equal(doc.querySelector('#guide-info .guide-info-title').textContent, 'Post-game');
  cells[1].dispatchEvent(new app.window.KeyboardEvent('keydown', { key: 'ArrowDown', bubbles: true }));
  assert.equal(doc.activeElement.querySelector('.cable-programme-title').textContent, 'Evening News');
});

test('the category list filters the grid', async (t) => {
  const app = setup(t, previewLibrary());
  await tick();
  const doc = app.window.document;
  doc.querySelector('[data-tab="guide"]').click();
  assert.notEqual(doc.getElementById('categories').style.display, 'none');
  const news = [...doc.querySelectorAll('.cat')].find((button) => button.textContent.startsWith('News'));
  news.click();
  const names = [...doc.querySelectorAll('.cable-row:not(.cable-header-row) .cable-channel-name')].map((n) => n.textContent);
  assert.deepEqual(names, ['Newsroom']);
});

test('a preview build shows the grid even when the loaded copy came from an older stable download', async (t) => {
  // A 1.0.x refresh cached USA data with no preview features. The build's own
  // bundle, reported by the main process, decides that the Guide is the grid.
  const stale = previewLibrary();
  stale.library.meta = { version: '1.0.2', library_scope: 'usa', preview_features: [] };
  const app = setup(t, stale, { version: '1.1.1', previewFeatures: ['cable-guide'] });
  await tick();
  app.window.document.querySelector('[data-tab="guide"]').click();
  assert.equal(app.window.document.getElementById('guide-grid').hidden, false);
  assert.ok(app.window.document.querySelectorAll('.cable-programme').length >= 3);
});

test('stable builds keep the list-style Guide', async (t) => {
  const app = setup(t, ready());
  await tick();
  const doc = app.window.document;
  doc.querySelector('[data-tab="guide"]').click();
  assert.equal(doc.getElementById('guide-grid').hidden, true);
  assert.equal(doc.getElementById('guide-list').hidden, false);
  assert.equal(doc.querySelectorAll('#guide-list .guide-row').length, 1);
  assert.equal(doc.getElementById('categories').style.display, 'none');
});
