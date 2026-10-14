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
function setup(t, initial) {
  const dom = new JSDOM(fs.readFileSync(path.join(renderer, 'index.html'), 'utf8'), {
    runScripts: 'outside-only', url: 'http://127.0.0.1:1234',
  });
  t.after(() => dom.window.close());
  let current = initial;
  const events = {};
  dom.window.premiumtv = {
    getAppInfo: async () => ({ version: '1.0.2' }),
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

test('the cable guide is opt-in bundle preview UI with a real, selectable EPG grid', async (t) => {
  const preview = ready('Public One');
  const now = Math.floor(Date.now() / 1000);
  preview.library.meta = {
    version: '1.1.0',
    library_scope: 'all',
    preview_features: ['cable-guide'],
  };
  preview.library.channels[0].chno = '12';
  preview.library.programmes = [
    { c: 'one', s: now - 900, e: now + 1800, t: 'Live match', g: 'Sports' },
    { c: 'one', s: now + 1800, e: now + 5400, t: 'Post-game', g: 'Sports' },
  ];
  const app = setup(t, preview);
  await tick();

  const cableTab = app.window.document.getElementById('cable-tab');
  assert.equal(cableTab.hidden, false);
  cableTab.click();
  assert.equal(app.window.document.getElementById('view-cable').hidden, false);
  assert.equal(app.window.document.querySelectorAll('.cable-row').length, 2);
  assert.equal(app.window.document.querySelector('.cable-programme-title')?.textContent, 'Live match');
  assert.equal(app.window.document.querySelector('.cable-now-line') !== null, true);
  assert.match(app.window.document.getElementById('cable-subtitle').textContent, /8-hour window/);
});

test('stable bundles keep the preview-only cable tab hidden', async (t) => {
  const app = setup(t, ready());
  await tick();
  assert.equal(app.window.document.getElementById('cable-tab').hidden, true);
});
