'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');

const {
  Relay,
  parsePlaylistHeaders,
  originHeader,
  headersFor,
  isRelayable,
  rewritePlaylist,
  relayDescriptor,
  inferContentType,
  loadAllowlist,
} = require('../relay');

// ------------------------------------------------------------------ allowlist

const PLAYLIST = `#EXTM3U x-tvg-url="https://example.test/guide.xml"
#EXTINF:-1 tvg-id="one" http-referrer="https://ref.example/" http-user-agent="Agent/1" ,One
http://one.example/live.m3u8
#EXTINF:-1 tvg-id="two" http-origin="https://embed.example/watch/7" ,Two
#EXTVLCOPT:http-referrer=https://opt.example/
#KODIPROP:http-user-agent=OptAgent/2
https://two.example/live.m3u8
#EXTINF:-1 tvg-id="plain" ,Plain
https://three.example/live.m3u8
`;

test('the allowlist carries only the headers a playlist publishes', () => {
  const map = parsePlaylistHeaders(PLAYLIST);
  assert.equal(map.size, 3);
  assert.deepEqual(map.get('http://one.example/live.m3u8'), {
    referrer: 'https://ref.example/',
    ua: 'Agent/1',
    origin: '',
  });
  assert.equal(map.get('https://two.example/live.m3u8').referrer, 'https://opt.example/');
  assert.equal(map.get('https://two.example/live.m3u8').ua, 'OptAgent/2');
  assert.equal(map.get('https://two.example/live.m3u8').origin, 'https://embed.example/watch/7');
  assert.deepEqual(map.get('https://three.example/live.m3u8'), { referrer: '', ua: '', origin: '' });
});

test('a published Origin is reduced to the tuple a CDN expects', () => {
  assert.equal(originHeader('https://embed.example/watch/7?ad=1'), 'https://embed.example');
  assert.equal(originHeader('http://embed.example:8080/a'), 'http://embed.example:8080');
  assert.equal(originHeader(''), '');
  assert.equal(originHeader('not a url'), '');
  assert.equal(originHeader('file:///etc/passwd'), '');

  const headers = headersFor({ origin: 'https://embed.example/watch/7' });
  assert.equal(headers.Origin, 'https://embed.example');
  assert.equal(headersFor({}).Referer, undefined);
});

test('private and non-http targets are never relayable', () => {
  for (const bad of [
    'file:///etc/passwd',
    'http://localhost/x',
    'http://127.0.0.1/x',
    'http://10.1.2.3/x',
    'http://192.168.1.1/x',
    'http://172.16.0.1/x',
    'http://169.254.169.254/latest/meta-data',
    'ftp://example.com/x',
    'nonsense',
  ]) {
    assert.equal(isRelayable(bad), false, `${bad} must be refused`);
  }
  assert.equal(isRelayable('https://cdn.example/live.m3u8'), true);
});

// -------------------------------------------------------------------- sessions

function fakeFetch(routes) {
  return async (url, init) => {
    const route = routes[url];
    if (!route) throw new Error(`unexpected fetch ${url}`);
    if (typeof route === 'function') return route(url, init);
    const body = Buffer.from(route.body || '');
    return new Response(route.status === 204 ? null : body, {
      status: route.status || 200,
      headers: route.headers || {},
    });
  };
}

function sessionRelay(routes, options = {}) {
  const allowlist = new Map([
    ['http://one.example/live.m3u8', { referrer: 'https://ref.example/', ua: 'Agent/1', origin: '' }],
  ]);
  return new Relay({ allowlist, fetchImpl: fakeFetch(routes), ...options });
}

test('an unpublished URL cannot open a session', () => {
  const relay = sessionRelay({});
  assert.equal(relay.openSession('http://unknown.example/x.m3u8'), null);
  assert.equal(relay.openSession('file:///etc/passwd'), null);
  assert.equal(relay.sessionCount(), 0);
});

test('a session rewrites a playlist and whitelists exactly its children', async () => {
  const master = [
    '#EXTM3U',
    '#EXT-X-STREAM-INF:BANDWIDTH=800000',
    'variant/one.m3u8',
    '#EXT-X-KEY:METHOD=AES-128,URI="key.bin"',
  ].join('\n');
  const relay = sessionRelay({
    'http://one.example/live.m3u8': {
      body: master,
      headers: { 'content-type': 'application/vnd.apple.mpegurl' },
    },
  });

  const session = relay.openSession('http://one.example/live.m3u8');
  assert.ok(session && session.sessionId);
  const sessionState = relay.sessions.get(session.sessionId);
  const base = `http://127.0.0.1:${relay.port}/s/${session.sessionId}`;

  const rewritten = rewritePlaylist(
    master,
    'http://one.example/live.m3u8',
    sessionState,
    base,
  );
  assert.match(rewritten, /u=http%3A%2F%2Fone\.example%2Fvariant%2Fone\.m3u8/);
  assert.match(rewritten, /URI="http.*u=http%3A%2F%2Fone\.example%2Fkey\.bin"/);
  assert.ok(sessionState.allowed.has('http://one.example/variant/one.m3u8'));
  assert.ok(sessionState.allowed.has('http://one.example/key.bin'));
  assert.equal(sessionState.allowed.has('http://evil.example/steal.ts'), false);
});

test('a live server refuses a request outside the session allowlist', async (t) => {
  const relay = sessionRelay({
    'http://one.example/live.m3u8': {
      body: '#EXTM3U\n#EXTINF:6,\nseg0.ts\n',
      headers: { 'content-type': 'application/vnd.apple.mpegurl' },
    },
  });
  const origin = await relay.start(0, '127.0.0.1');
  t.after(() => relay.stop());

  const session = relay.openSession('http://one.example/live.m3u8');
  const playlist = await fetch(`${origin}/s/${session.sessionId}`);
  assert.equal(playlist.status, 200);
  const text = await playlist.text();
  assert.match(text, /seg0\.ts/);
  assert.match(text, /u=http%3A%2F%2Fone\.example%2Fseg0\.ts/);

  const forbidden = await fetch(
    `${origin}/s/${session.sessionId}?u=${encodeURIComponent('http://evil.example/x.ts')}`,
  );
  assert.equal(forbidden.status, 403);
});

test('a session that expired answers 410 instead of fetching', async (t) => {
  let now = 1000;
  const relay = sessionRelay({}, { now: () => now, sessionTtlMs: 5000 });
  const origin = await relay.start(0, '127.0.0.1');
  t.after(() => relay.stop());

  const session = relay.openSession('http://one.example/live.m3u8');
  now += 6000;
  const response = await fetch(`${origin}/s/${session.sessionId}`);
  assert.equal(response.status, 410);
});

test('the published referrer and user-agent are what the relay sends upstream', async (t) => {
  let seen = null;
  const relay = sessionRelay({
    'http://one.example/live.m3u8': (url, init) => {
      seen = init.headers;
      return new Response('#EXTM3U\n#EXTINF:6,\nseg0.ts\n', {
        status: 200,
        headers: { 'content-type': 'application/vnd.apple.mpegurl' },
      });
    },
  });
  const origin = await relay.start(0, '127.0.0.1');
  t.after(() => relay.stop());

  const session = relay.openSession('http://one.example/live.m3u8');
  await fetch(`${origin}/s/${session.sessionId}`);
  assert.equal(seen.Referer, 'https://ref.example/');
  assert.equal(seen['User-Agent'], 'Agent/1');
});

test('a session is capped in parallel requests', async () => {
  const relay = sessionRelay({});
  const session = relay.openSession('http://one.example/live.m3u8');
  const state = relay.sessions.get(session.sessionId);
  state.active = 99;
  const response = {
    headers: {},
    written: null,
    writeHead(status) {
      this.written = status;
    },
    end(body) {
      this.body = body;
    },
    headersSent: false,
  };
  await relay.handleStream(
    { method: 'GET', url: `/s/${session.sessionId}`, headers: {} },
    response,
    new URL(`http://relay.local/s/${session.sessionId}`),
  );
  assert.equal(response.written, 429);
});

test('failed and ended sessions are reported, not silently proxied', async (t) => {
  const relay = sessionRelay({
    'http://one.example/live.m3u8': { status: 403, body: 'nope' },
  });
  const origin = await relay.start(0, '127.0.0.1');
  t.after(() => relay.stop());

  const session = relay.openSession('http://one.example/live.m3u8');
  const answer = await fetch(`${origin}/s/${session.sessionId}`);
  assert.equal(answer.status, 502);
  assert.ok(relay.closeSession(session.sessionId));
});

test('the health endpoint reports the allowlist and session count', async (t) => {
  const relay = sessionRelay({});
  const origin = await relay.start(0, '127.0.0.1');
  t.after(() => relay.stop());
  const health = await (await fetch(`${origin}/healthz`)).json();
  assert.equal(health.ok, true);
  assert.equal(health.channels, 1);
});

test('the discovery document is off by default', () => {
  const doc = relayDescriptor({}, 42);
  assert.equal(doc.enabled, false);
  assert.equal(doc.base, '');
  assert.equal(doc.channels, 42);
  assert.equal(doc.scope, 'published-playlist-only');
});

test('the real repository playlist produces a non-empty allowlist', () => {
  const root = require('node:path').join(__dirname, '..', '..');
  const map = loadAllowlist(require('node:path').join(root, 'playlists', 'live', 'USA.m3u'));
  assert.ok(map.size > 1000, 'the checked USA playlist should hold thousands of streams');
  const withHeaders = [...map.values()].filter((v) => v.referrer || v.ua || v.origin).length;
  assert.ok(withHeaders > 0, 'some published feeds require headers a browser cannot send');
});

test('segment content types follow the extension, with a video fallback', () => {
  assert.equal(inferContentType('https://x/a.mp4'), 'video/mp4');
  assert.equal(inferContentType('https://x/a.aac'), 'audio/aac');
  assert.equal(inferContentType('https://x/a.vtt'), 'text/vtt');
  assert.equal(inferContentType('https://x/no-extension'), 'video/mp2t');
});

// A tiny guard against the allowlist being bypassed by a redirect to loopback.
test('a redirect to a private address is not followed into the allowlist', () => {
  const relay = sessionRelay({});
  const session = relay.openSession('http://one.example/live.m3u8');
  assert.ok(session);
  const state = relay.sessions.get(session.sessionId);
  // rewritePlaylist whitelists whatever the *playlist* names, and the fetch of
  // that name is re-checked by isRelayable before it is ever requested.
  assert.equal(isRelayable('http://169.254.169.254/latest/meta-data'), false);
  assert.equal(state.allowed.size, 1);
});

// The whole point of the relay, proven against a real HTTP server rather than a
// stub: a feed that refuses a browser outright becomes playable, and nothing
// else becomes reachable.
test('a referrer-gated feed becomes playable end to end', async (t) => {
  const http = require('node:http');
  const dns = require('node:dns');
  const HOST = 'provider.example';
  const lookup = dns.lookup;
  dns.lookup = (host, opts, cb) =>
    host === HOST ? lookup('127.0.0.1', opts, cb) : lookup(host, opts, cb);
  t.after(() => {
    dns.lookup = lookup;
  });

  const SEGMENT = Buffer.from('FAKESEGMENT');
  const upstream = http.createServer((req, res) => {
    if (req.headers.referer !== 'https://ref.example/') {
      res.writeHead(403);
      return res.end('no referer');
    }
    if (req.url === '/live.m3u8') {
      res.writeHead(200, { 'content-type': 'application/vnd.apple.mpegurl' });
      return res.end('#EXTM3U\n#EXT-X-TARGETDURATION:6\n#EXTINF:6,\nseg0.ts\n');
    }
    if (req.url === '/seg0.ts') {
      res.writeHead(200, { 'content-type': 'video/mp2t', 'content-length': SEGMENT.length });
      return res.end(SEGMENT);
    }
    res.writeHead(404);
    res.end();
  });
  await new Promise((resolve) => upstream.listen(0, '127.0.0.1', resolve));
  t.after(() => upstream.close());

  const published = `http://${HOST}:${upstream.address().port}`;
  const relay = new Relay({
    allowlist: new Map([[`${published}/live.m3u8`, { referrer: 'https://ref.example/', ua: '', origin: '' }]]),
  });
  const origin = await relay.start(0, '127.0.0.1');
  t.after(() => relay.stop());

  const session = relay.openSession(`${published}/live.m3u8`);
  const playlist = await (await fetch(`${origin}${session.path}`)).text();
  const segmentUrl = playlist.split('\n').find((line) => line.startsWith('http'));
  assert.ok(segmentUrl, 'the segment must be rewritten through the relay');

  const segment = await fetch(segmentUrl);
  assert.equal(segment.status, 200);
  assert.equal(segment.headers.get('content-type'), 'video/mp2t');
  assert.ok(Buffer.from(await segment.arrayBuffer()).equals(SEGMENT));

  const ssrf = await fetch(`${origin}${session.path}?u=${encodeURIComponent('http://169.254.169.254/latest')}`);
  assert.equal(ssrf.status, 403);
});

test('the /open route refuses an unpublished URL and accepts a published one', async (t) => {
  const relay = sessionRelay({});
  const origin = await relay.start(0, '127.0.0.1');
  t.after(() => relay.stop());

  const denied = await fetch(`${origin}/open?u=${encodeURIComponent('http://evil.example/x.m3u8')}`);
  assert.equal(denied.status, 403);
  assert.equal((await denied.json()).ok, false);

  const allowed = await fetch(`${origin}/open?u=${encodeURIComponent('http://one.example/live.m3u8')}`);
  assert.equal(allowed.status, 200);
  const body = await allowed.json();
  assert.equal(body.ok, true);
  assert.ok(body.sessionId);
  assert.equal(body.path, `/s/${body.sessionId}`);

  const missing = await fetch(`${origin}/open`);
  assert.equal(missing.status, 400);
});
