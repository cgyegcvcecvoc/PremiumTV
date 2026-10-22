'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const renderer = path.join(__dirname, '..', 'src', 'renderer');

function loadHealth() {
  const window = {};
  vm.runInNewContext(fs.readFileSync(path.join(renderer, 'health.js'), 'utf8'), { window });
  return window.PremiumHealth;
}

function memoryStorage() {
  const store = new Map();
  return {
    getItem: (key) => (store.has(key) ? store.get(key) : null),
    setItem: (key, value) => store.set(key, String(value)),
    removeItem: (key) => store.delete(key),
  };
}

const channel = (url) => ({ id: url, name: url, url, group: 'News' });

test('a failed feed is remembered and filtered out of the browser', () => {
  const health = loadHealth();
  const storage = memoryStorage();

  assert.equal(health.filterChannels([channel('a'), channel('b')], health.load(storage)).length, 2);
  const dead = health.record(storage, 'a', 1_000);
  assert.deepEqual([...dead], ['a']);
  assert.deepEqual(
    health.filterChannels([channel('a'), channel('b')], dead).map((c) => c.url),
    ['b'],
  );
});

test('a repeated failure refreshes its timestamp and does not duplicate', () => {
  const health = loadHealth();
  const storage = memoryStorage();
  health.record(storage, 'a', 1_000);
  const dead = health.record(storage, 'a', 2_000);
  assert.equal(dead.size, 1);
  const stored = JSON.parse(storage.getItem(health.KEY));
  assert.equal(stored.length, 1);
  assert.equal(stored[0].at, 2_000);
});

test('recordings expire after seven days so a returning feed gets a chance', () => {
  const health = loadHealth();
  const storage = memoryStorage();
  health.record(storage, 'a', 1_000);
  const later = 1_000 + health.TTL_MS + 1;
  assert.equal(health.load(storage, later).size, 0);
});

test('corrupt storage loads empty instead of breaking the browser', () => {
  const health = loadHealth();
  const storage = {
    getItem: () => '{not json',
    setItem: () => {},
    removeItem: () => {},
  };
  assert.equal(health.load(storage).size, 0);
  assert.deepEqual(health.clear(storage).size, 0);
});
