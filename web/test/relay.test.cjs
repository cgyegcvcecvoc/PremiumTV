'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');

// The module reads `location` at call time, so give it a browser-shaped global
// before requiring it.
global.location = { protocol: 'https:' };
global.document = { baseURI: 'https://player.test/web/' };

const Relay = require(path.join(__dirname, '..', 'src', 'relay-client.js'));

const ON = { enabled: true, base: 'https://relay.example' };

test('a disabled or malformed relay document never enables the relay', () => {
  assert.equal(Relay.validate({ enabled: false, base: 'https://r.example' }), null);
  assert.equal(Relay.validate({ enabled: true, base: '' }), null);
  assert.equal(Relay.validate({ enabled: true, base: 'javascript:alert(1)' }), null);
  assert.equal(Relay.validate(null), null);
  assert.equal(Relay.validate({ enabled: 'true', base: 'https://r.example' }), null);

  const ok = Relay.validate({ enabled: true, base: 'https://relay.example/', provider: 'Mine' });
  assert.equal(ok.base, 'https://relay.example', 'a trailing slash is normalised off');
  assert.equal(ok.provider, 'Mine');
});

test('a plain https feed is not sent through the relay', () => {
  const plan = Relay.plan({ url: 'https://cdn.example/live.m3u8' }, ON);
  assert.equal(plan.needsRelay, false);
  assert.equal(plan.available, true);
});

test('plain http on a secure page is flagged as relay-only', () => {
  const plan = Relay.plan({ url: 'http://cdn.example/live.m3u8' }, ON);
  assert.equal(plan.needsRelay, true);
  assert.match(plan.reason, /plain HTTP/);
});

test('a feed with published headers is flagged as relay-only', () => {
  for (const headers of [{ referrer: 'https://r.example/' }, { ua: 'Agent/1' }, { origin: 'https://o.example' }]) {
    const plan = Relay.plan({ url: 'https://cdn.example/live.m3u8', ...headers }, ON);
    assert.equal(plan.needsRelay, true, JSON.stringify(headers));
    assert.match(plan.reason, /Referer, Origin or User-Agent/);
  }
});

test('without a relay the plan is honest and never points at one', () => {
  const plan = Relay.plan({ url: 'http://cdn.example/live.m3u8' }, false);
  assert.equal(plan.needsRelay, false);
  assert.equal(plan.available, false);
  assert.match(plan.reason, /plain HTTP/);
});

test('opening a session posts the feed to the relay and returns its path', async (t) => {
  const calls = [];
  const realFetch = global.fetch;
  global.fetch = async (url, init) => {
    calls.push({ url: String(url), init });
    return {
      ok: true,
      status: 200,
      json: async () => ({ ok: true, sessionId: 'abc123', path: '/s/abc123' }),
    };
  };
  t.after(() => {
    global.fetch = realFetch;
  });

  const opened = await Relay.open({ url: 'http://cdn.example/live.m3u8?a=1' }, ON);
  assert.equal(opened.url, 'https://relay.example/s/abc123');
  assert.equal(opened.sessionId, 'abc123');
  assert.equal(
    calls[0].url,
    'https://relay.example/open?u=http%3A%2F%2Fcdn.example%2Flive.m3u8%3Fa%3D1',
  );
  assert.equal(calls[0].init.credentials, 'omit', 'the relay never receives credentials');
});

test('a relay refusal or a hostile path is treated as no relay at all', async (t) => {
  const realFetch = global.fetch;
  t.after(() => {
    global.fetch = realFetch;
  });

  global.fetch = async () => ({ ok: false, status: 403, json: async () => ({ ok: false }) });
  assert.equal(await Relay.open({ url: 'http://cdn.example/x.m3u8' }, ON), null);

  // A relay must not be able to steer the player at an arbitrary absolute URL.
  global.fetch = async () => ({
    ok: true,
    status: 200,
    json: async () => ({ ok: true, path: 'https://evil.example/steal' }),
  });
  assert.equal(await Relay.open({ url: 'http://cdn.example/x.m3u8' }, ON), null);

  global.fetch = async () => {
    throw new Error('offline');
  };
  assert.equal(await Relay.open({ url: 'http://cdn.example/x.m3u8' }, ON), null);

  assert.equal(await Relay.open({ url: 'file:///etc/passwd' }, ON), null);
  assert.equal(await Relay.open({ url: 'http://cdn.example/x.m3u8' }, false), null);
});
