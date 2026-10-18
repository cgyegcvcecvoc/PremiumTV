'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const renderer = path.join(__dirname, '..', 'src', 'renderer');

function loadPersonal() {
  const window = {};
  vm.runInNewContext(fs.readFileSync(path.join(renderer, 'personal.js'), 'utf8'), { window });
  return window.PremiumPersonal;
}

const channel = (url) => ({ id: url, name: url, url, group: 'News' });

test('opening a channel files it under Recently watched, newest first, capped', () => {
  const personal = loadPersonal();
  let keys = [];
  keys = personal.recordRecent(keys, 'a');
  keys = personal.recordRecent(keys, 'b');
  keys = personal.recordRecent(keys, 'a');
  assert.deepEqual([...keys], ['a', 'b']);
  for (let i = 0; i < 40; i += 1) keys = personal.recordRecent(keys, `c${i}`);
  assert.equal(keys.length, personal.MAX_RECENTS);
  assert.equal(personal.resolve(keys, [channel('a'), channel('c39')])[0].url, 'c39');
});

test('favorites toggle on and off and resolve in shelf order', () => {
  const personal = loadPersonal();
  let keys = personal.toggleFavorite([], 'a');
  keys = personal.toggleFavorite(keys, 'b');
  assert.deepEqual([...keys], ['b', 'a']);
  assert.equal(personal.isFavorite(keys, 'a'), true);
  keys = personal.toggleFavorite(keys, 'a');
  assert.deepEqual([...keys], ['b']);
  assert.deepEqual([...personal.resolve(keys, [channel('b'), channel('gone')]).map((c) => c.url)], ['b']);
});

test('manual server switching wraps in both directions', () => {
  const personal = loadPersonal();
  assert.equal(personal.nextServerIndex(0, 3, 1), 1);
  assert.equal(personal.nextServerIndex(2, 3, 1), 0);
  assert.equal(personal.nextServerIndex(0, 3, -1), 2);
  assert.equal(personal.nextServerIndex(0, 1, 1), 0);
  assert.equal(personal.nextServerIndex(0, 0, 1), 0);
});

test('corrupt stored shelves load as empty instead of breaking startup', () => {
  const personal = loadPersonal();
  const storage = { getItem: () => '{nope', setItem: () => {} };
  assert.deepEqual([...personal.load(storage, personal.RECENTS_KEY)], []);
});

test('search is click-to-activate: readonly until clicked, never on hover', () => {
  const html = fs.readFileSync(path.join(renderer, 'index.html'), 'utf8');
  const js = fs.readFileSync(path.join(renderer, 'app.js'), 'utf8');
  assert.match(html, /<input id="search"[^>]*readonly/);
  assert.match(html, /<script src="personal\.js"><\/script>/);
  assert.match(js, /els\.search\.addEventListener\('click', activateSearch\)/);
  assert.match(js, /if \(!ui\.searchActive\) return; \/\/ never search without an explicit click/);
  assert.doesNotMatch(js, /search\.addEventListener\('(?:mouseover|mouseenter|pointerenter|hover)'/);
  assert.doesNotMatch(js, /search\.addEventListener\('focus',/);
});

test('player offers manual server switching and a favorite toggle', () => {
  const html = fs.readFileSync(path.join(renderer, 'index.html'), 'utf8');
  const js = fs.readFileSync(path.join(renderer, 'app.js'), 'utf8');
  assert.match(html, /id="player-prev-server"/);
  assert.match(html, /id="player-next-server"/);
  assert.match(html, /id="player-favorite"/);
  assert.match(js, /async function switchServer\(delta\)/);
  assert.match(js, /personal\.nextServerIndex\(playQueueIndex, playQueue\.length, delta\)/);
  assert.match(js, /noteWatched\(channel\)/);
  assert.match(js, /RECENT_CATEGORY = '__recent__'/);
  assert.match(js, /FAVORITE_CATEGORY = '__favorites__'/);
});
