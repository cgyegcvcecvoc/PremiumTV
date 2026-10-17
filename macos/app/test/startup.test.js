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
function setup(t, initial, appInfo = { version: '1.0.2' }, updates = null) {
  const dom = new JSDOM(fs.readFileSync(path.join(renderer, 'index.html'), 'utf8'), {
    runScripts: 'outside-only', url: 'http://127.0.0.1:1234',
  });
  t.after(() => dom.window.close());
  let current = initial;
  let updateState = updates;
  const events = {};
  const calls = { check: 0, download: 0, install: 0, release: 0 };
  dom.window.premiumtv = {
    getAppInfo: async () => structuredClone({ ...appInfo, updates: updateState }),
    getSnapshot: async () => structuredClone(current),
    updateStatus: async () => structuredClone(updateState),
    checkForUpdate: async (force) => {
      calls.check += 1;
      calls.checkForced = Boolean(force);
      return structuredClone(updateState);
    },
    downloadUpdate: async () => {
      calls.download += 1;
      if (updateState && updateState.availableVersion) {
        updateState = {
          ...updateState,
          downloadedVersion: updateState.availableVersion,
          progressPercent: 100,
          message: `PremiumTV ${updateState.availableVersion} downloaded and verified. ` +
            'Press Open installer to finish.',
        };
      }
      return structuredClone(updateState);
    },
    installUpdate: async () => { calls.install += 1; return { ok: true }; },
    openReleasePage: async () => { calls.release += 1; return { ok: true }; },
    onState: (fn) => { events.state = fn; },
    onProgress: (fn) => { events.progress = fn; },
    onInfo: (fn) => { events.info = fn; },
    onUpdate: (fn) => { events.update = fn; },
    onSelectTab() {},
  };
  dom.window.PremiumPlayer = { stop() {} };
  dom.window.eval(fs.readFileSync(path.join(renderer, 'app.js'), 'utf8'));
  return {
    window: dom.window,
    events,
    calls,
    set: (value) => { current = value; },
    setUpdate: (value) => { updateState = value; },
  };
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

test('library activity stays non-modal and distinguishes progress from failure', async (t) => {
  const app = setup(t, empty());
  await tick();
  const doc = app.window.document;
  assert.equal(doc.getElementById('library-activity').hidden, false);
  assert.equal(doc.getElementById('activity-spinner').hidden, false);
  assert.match(doc.getElementById('activity-tip').textContent, /TIP/);
  const loading = ready();
  loading.info = { inProgress: true, lastAttemptAt: Date.now() };
  loading.state.message = 'Downloading the complete programme guide…';
  app.set(loading);
  app.events.state(loading.state);
  await tick();
  assert.equal(doc.querySelector('.card-name').textContent, 'Sports One');
  assert.match(doc.getElementById('activity-message').textContent, /programme guide/);
  doc.querySelector('[data-tab="settings"]').click();
  assert.equal(doc.getElementById('force-refresh').disabled, true);
  assert.equal(doc.getElementById('reset-bundled').disabled, true);
  app.events.info({ inProgress: false, lastOutcomeOk: false, lastMessage: 'Offline; your library was kept.' });
  assert.equal(doc.getElementById('activity-spinner').hidden, true);
  assert.match(doc.getElementById('activity-message').textContent, /library was kept/);
  assert.equal(doc.getElementById('library-activity').dataset.outcome, 'error');
  assert.equal(doc.getElementById('force-refresh').disabled, false);
});

test('Settings offers a verified app update and installs it from the same panel', async (t) => {
  const update = {
    currentVersion: '1.0.4',
    latestStableVersion: '1.0.5',
    availableVersion: '1.0.5',
    installerSize: 5 * 1024 * 1024,
    lastCheckedAtMillis: Date.now(),
    checking: false,
    downloading: false,
    progressPercent: -1,
    downloadedVersion: null,
    message: 'PremiumTV 1.0.5 is available (installed: 1.0.4).',
    error: null,
  };
  const app = setup(t, ready(), { version: '1.0.4' }, update);
  await tick();
  const doc = app.window.document;
  doc.querySelector('[data-tab="settings"]').click();

  assert.match(doc.getElementById('view-settings').textContent, /App updates/);
  assert.match(doc.getElementById('view-settings').textContent, /PremiumTV 1\.0\.5 is available/);
  assert.ok(doc.getElementById('download-update'));

  doc.getElementById('download-update').click();
  await tick();
  await tick();
  assert.equal(app.calls.download, 1);
  // The same panel now offers the already-verified installer instead of a
  // second download.
  assert.equal(doc.getElementById('download-update').textContent, 'Open installer');
  assert.match(doc.getElementById('view-settings').textContent, /downloaded and verified/);

  doc.getElementById('download-update').click();
  await tick();
  await tick();
  assert.equal(app.calls.download, 1, 'Open installer must not start another download');
  assert.equal(app.calls.install, 1);
});

test('Settings can ask GitHub for an app update immediately', async (t) => {
  const app = setup(t, ready(), { version: '1.0.4' }, {
    currentVersion: '1.0.4',
    latestStableVersion: '1.0.5',
    availableVersion: '1.0.5',
    checking: false,
    downloading: false,
    message: 'PremiumTV 1.0.5 is available (installed: 1.0.4).',
  });
  await tick();
  const doc = app.window.document;
  doc.querySelector('[data-tab="settings"]').click();
  doc.getElementById('check-update').click();
  await tick();
  await tick();
  assert.equal(app.calls.check, 1);
  assert.equal(app.calls.checkForced, true);
});
