'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');

const { rewritePlaylist, headersFor, absoluteUrl, LISTEN_HOST } = require('../src/main/stream-proxy');

test('the proxy binds to loopback only', () => {
  assert.equal(LISTEN_HOST, '127.0.0.1');
});

test('headersFor carries the published referrer, origin and user-agent', () => {
  const headers = headersFor({
    ua: 'MyAgent/2',
    referrer: 'https://ref.example/',
    origin: 'https://origin.example',
  });
  assert.equal(headers['User-Agent'], 'MyAgent/2');
  assert.equal(headers.Referer, 'https://ref.example/');
  assert.equal(headers.Origin, 'https://origin.example');

  const bare = headersFor({});
  assert.ok(bare['User-Agent'], 'a default UA is always sent');
  assert.equal(bare.Referer, undefined);
});

test('rewritePlaylist routes every URI back through the proxy and whitelists it', () => {
  const session = { allowed: new Set(['https://host/master.m3u8']) };
  const playlist = [
    '#EXTM3U',
    '#EXT-X-KEY:METHOD=AES-128,URI="key.bin",IV=0x00',
    '#EXTINF:6,',
    'seg0.ts',
    'https://cdn.other/seg1.ts',
  ].join('\n');

  const out = rewritePlaylist(playlist, 'https://host/master.m3u8', session, 'http://127.0.0.1:9/p/abc');

  // Relative and absolute media URIs now point at the proxy.
  assert.match(out, /http:\/\/127\.0\.0\.1:9\/p\/abc\?u=/);
  assert.ok(!/^\s*seg0\.ts$/m.test(out), 'the bare relative segment must be rewritten');

  // The key URI attribute is rewritten too.
  assert.match(out, /URI="http:\/\/127\.0\.0\.1:9\/p\/abc\?u=/);

  // Everything named became allowed for the session.
  assert.ok(session.allowed.has(absoluteUrl('seg0.ts', 'https://host/master.m3u8')));
  assert.ok(session.allowed.has('https://cdn.other/seg1.ts'));
  assert.ok(session.allowed.has(absoluteUrl('key.bin', 'https://host/master.m3u8')));

  // Comment lines are preserved untouched.
  assert.match(out, /#EXTM3U/);
});

test('absoluteUrl resolves relative and absolute URIs', () => {
  assert.equal(absoluteUrl('a/b.ts', 'https://h/x/master.m3u8'), 'https://h/x/a/b.ts');
  assert.equal(absoluteUrl('https://o/z.ts', 'https://h/x/master.m3u8'), 'https://o/z.ts');
});

test('HTTP proxy resolves HLS segments and keys against the final redirected URL', async (t) => {
  const { StreamProxy } = require('../src/main/stream-proxy');
  const path = require('node:path');
  const requests = [];
  const proxy = new StreamProxy({
    rendererDir: path.join(__dirname, '..', 'src', 'renderer'),
    logoCacheDir: '/unused',
    fetchImpl: async (url, init) => {
      requests.push({ url, headers: init.headers });
      const response = new Response('#EXTM3U\n#EXT-X-KEY:METHOD=AES-128,URI="key.bin"\n#EXTINF:6,\nseg.ts\n', {
        headers: { 'content-type': 'application/vnd.apple.mpegurl' },
      });
      Object.defineProperty(response, 'url', { value: 'https://cdn.example/new/live.m3u8' });
      return response;
    },
  });
  await proxy.start();
  t.after(() => proxy.stop());
  const url = proxy.registerChannel({ url: 'https://origin.example/live.m3u8', ua: 'TestUA', referrer: 'https://ref.example' });
  const result = await fetch(url);
  assert.equal(result.status, 200);
  const playlist = await result.text();
  assert.ok(playlist.includes(encodeURIComponent('https://cdn.example/new/seg.ts')));
  assert.ok(playlist.includes(encodeURIComponent('https://cdn.example/new/key.bin')));
  assert.equal(requests[0].headers.Referer, 'https://ref.example');
  assert.equal(requests[0].headers['User-Agent'], 'TestUA');
  assert.equal((await fetch(`${url}?u=${encodeURIComponent('https://not-allowed.example/seg.ts')}`)).status, 403);
  assert.equal((await fetch(`${proxy.origin}/app.js`)).status, 200);

  const sessionId = new URL(url).pathname.split('/').filter(Boolean).at(-1);
  assert.equal(proxy.sessions.size, 1);
  assert.equal(proxy.releaseSession(sessionId), true);
  assert.equal(proxy.sessions.size, 0, 'closing playback releases its whitelist and session');
  assert.equal((await fetch(url)).status, 410);

  const legacyUrl = proxy.registerChannel({ url: 'https://origin.example/legacy.m3u8' });
  assert.equal(proxy.releaseSession(legacyUrl), true, 'older renderers may pass the full URL');
  assert.equal(proxy.sessions.size, 0);
});

test('1.1.3: extensionless audio renditions and AAC segments are rewritten and typed', async (t) => {
  const { StreamProxy, inferMediaContentType } = require('../src/main/stream-proxy');
  const path = require('node:path');

  assert.equal(inferMediaContentType('https://cdn.example/audio/chunk0.aac?token=1'), 'audio/aac');
  assert.equal(inferMediaContentType('https://cdn.example/audio/init.m4a'), 'audio/mp4');
  assert.equal(inferMediaContentType('https://cdn.example/audio/seg1.m4s'), 'video/iso.segment');
  assert.equal(inferMediaContentType('https://cdn.example/vod/film.mp4'), 'video/mp4');
  assert.equal(inferMediaContentType('https://cdn.example/live/seg0.ts'), 'video/mp2t');

  const proxy = new StreamProxy({
    rendererDir: path.join(__dirname, '..', 'src', 'renderer'),
    logoCacheDir: '/unused',
    fetchImpl: async (url) => {
      if (url === 'https://jmp2.example/plu-channel') {
        const master = [
          '#EXTM3U',
          '#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="aud",NAME="English",DEFAULT=YES,URI="audio/eng/rendition"',
          '#EXT-X-STREAM-INF:BANDWIDTH=2000000,AUDIO="aud"',
          'video/main.m3u8',
        ].join('\n');
        const response = new Response(master, { headers: { 'content-type': 'text/plain' } });
        Object.defineProperty(response, 'url', { value: 'https://cdn.example/live/master' });
        return response;
      }
      if (url === 'https://cdn.example/live/audio/eng/rendition') {
        const audioPlaylist = '#EXTM3U\n#EXTINF:4,\nseg0.aac\n';
        return new Response(audioPlaylist, { headers: { 'content-type': 'application/octet-stream' } });
      }
      if (url === 'https://cdn.example/live/audio/eng/seg0.aac') {
        return new Response(Uint8Array.from([0xff, 0xf1, 0x50, 0x80]), { headers: {} });
      }
      return new Response('not found', { status: 404 });
    },
  });
  await proxy.start();
  t.after(() => proxy.stop());

  const sessionUrl = proxy.registerChannel({ url: 'https://jmp2.example/plu-channel' });
  const masterRes = await fetch(sessionUrl);
  assert.equal(masterRes.status, 200);
  assert.match(masterRes.headers.get('content-type'), /mpegurl/);
  const masterBody = await masterRes.text();
  const audioUriMatch = masterBody.match(/URI="([^"]+)"/);
  assert.ok(audioUriMatch, 'the #EXT-X-MEDIA audio URI is rewritten through the proxy');

  const audioRes = await fetch(audioUriMatch[1]);
  assert.equal(audioRes.status, 200);
  assert.match(audioRes.headers.get('content-type'), /mpegurl/);
  const audioBody = await audioRes.text();
  const segLine = audioBody.split('\n').find((line) => line.startsWith('http://127.0.0.1'));
  assert.ok(segLine, 'the AAC audio segment is whitelisted and rewritten through the proxy');

  const segRes = await fetch(segLine);
  assert.equal(segRes.status, 200);
  assert.equal(segRes.headers.get('content-type'), 'audio/aac');
});
