'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');

function worker() {
  const handlers = {};
  const stored = new Map();
  const cache = {
    match: async (request) => stored.get(typeof request === 'string' ? request : request.url),
    put: async (request, response) => stored.set(typeof request === 'string' ? request : request.url, response),
  };
  let calls = 0;
  const context = {
    URL, Response,
    self: { location: new URL('https://example.test/web/sw.js'), addEventListener: (name, fn) => { handlers[name] = fn; } },
    caches: { open: async () => cache },
    fetch: async () => ({ ok: true, type: 'basic', value: ++calls, clone() { return { ...this }; } }),
  };
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../src/sw.js'), 'utf8').replace('BUILD_ID_PLACEHOLDER', 'old'), context);
  async function request(url, mode = 'default') {
    let promise;
    handlers.fetch({ request: { url, method: 'GET', cache: mode, headers: { has: () => false } }, respondWith: (p) => { promise = p; } });
    return promise;
  }
  return { request, stored, calls: () => calls };
}

test('a new version never falls back to the old precached data', async () => {
  const sw = worker();
  const base = 'https://example.test/web/data/channels.json';
  sw.stored.set(base, { value: 'old' });
  assert.equal((await sw.request(base + '?v=old')).value, 'old');
  assert.equal((await sw.request(base + '?v=new')).value, 1);
  assert.equal(sw.calls(), 1);
});

test('a forced data refresh updates the cache for later offline use', async () => {
  const sw = worker();
  const url = 'https://example.test/web/data/meta.json';
  sw.stored.set(url, { value: 'old' });
  assert.equal((await sw.request(url, 'no-store')).value, 1);
  assert.equal((await sw.request(url)).value, 1);
  assert.equal(sw.calls(), 1);
});
