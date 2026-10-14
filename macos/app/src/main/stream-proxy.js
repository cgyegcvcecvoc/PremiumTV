'use strict';

/**
 * The loopback server the app is served from, and the stream proxy behind it.
 *
 * Two jobs:
 *
 * 1. Serve the renderer. Loading the window from http://127.0.0.1 keeps the UI
 *    and the video element on one origin, so no request is mixed content and no
 *    request needs CORS.
 *
 * 2. Proxy playback. Public IPTV feeds routinely refuse a connection that is
 *    missing the referrer, origin or user-agent their playlist publishes, and
 *    a browser cannot set those headers from a <video> element. The main
 *    process fetches the stream with them instead - the same thing the Android
 *    app's ExoPlayer data source does - and HLS playlists are rewritten so
 *    every segment and key comes back through here with the same headers.
 *
 * It binds to 127.0.0.1 only, and it will only fetch a URL that is either the
 * channel's own stream URL or one that appeared inside a playlist it was
 * already serving. The renderer cannot use it as a general-purpose proxy.
 */

const crypto = require('node:crypto');
const http = require('node:http');
const fs = require('node:fs');
const fsp = require('node:fs/promises');
const path = require('node:path');
const { Readable } = require('node:stream');

const { USER_AGENT } = require('./repository');

const LISTEN_HOST = '127.0.0.1';
const MAX_PLAYLIST_BYTES = 4 * 1024 * 1024;
const MAX_LOGO_BYTES = 2 * 1024 * 1024;
const PLAYLIST_TIMEOUT_MS = 20000;
const CONNECT_TIMEOUT_MS = 15000;

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.map': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
};

class StreamProxy {
  /**
   * @param {object} options
   * @param {string} options.rendererDir directory holding index.html and friends
   * @param {string} options.logoCacheDir writable logo cache
   * @param {Function} [options.fetchImpl] injectable for tests
   */
  constructor(options) {
    this.rendererDir = options.rendererDir;
    this.logoCacheDir = options.logoCacheDir;
    this.fetchImpl = options.fetchImpl || ((url, init) => fetch(url, init));
    this.sessions = new Map();
    this.server = null;
    this.port = 0;
  }

  async start() {
    this.server = http.createServer((request, response) => {
      this.handle(request, response).catch((error) => {
        if (!response.headersSent) response.writeHead(502, { 'content-type': 'text/plain' });
        try {
          response.end(`PremiumTV proxy error: ${error.message}`);
        } catch (error2) {
          /* the socket is gone */
        }
      });
    });
    this.server.on('error', () => {});

    await new Promise((resolve, reject) => {
      this.server.once('error', reject);
      this.server.listen(0, LISTEN_HOST, () => {
        this.server.removeListener('error', reject);
        resolve();
      });
    });
    this.port = this.server.address().port;
    return this.origin;
  }

  get origin() {
    return `http://${LISTEN_HOST}:${this.port}`;
  }

  async stop() {
    this.sessions.clear();
    if (this.server) await new Promise((resolve) => this.server.close(resolve));
    this.server = null;
  }

  // -------------------------------------------------------------- sessions

  /**
   * Registers a channel for playback and returns the loopback URL to give a
   * <video> element. Every fetch for that session carries the channel's
   * published referrer / origin / user-agent.
   */
  registerChannel(channel) {
    const id = crypto.randomBytes(12).toString('hex');
    this.sessions.set(id, {
      id,
      channelId: channel.id,
      baseUrl: channel.url,
      headers: headersFor(channel),
      allowed: new Set([channel.url]),
    });
    return `${this.origin}/p/${id}`;
  }

  releaseSession(sessionId) {
    // Accept either the opaque id or the loopback URL returned by older builds.
    // The Mac renderer used to pass the full URL as the id, leaking one session
    // (and its whitelist) on every playback.
    let key = String(sessionId || '');
    if (key.includes('/p/')) {
      try {
        key = new URL(key).pathname.split('/').filter(Boolean).at(-1) || '';
      } catch (error) {
        return false;
      }
    }
    return this.sessions.delete(key);
  }

  // -------------------------------------------------------------- handling

  async handle(request, response) {
    const url = new URL(request.url, this.origin);
    const pathname = decodeURIComponent(url.pathname);

    if (pathname.startsWith('/p/')) return this.handleProxy(request, response, url);
    if (pathname.startsWith('/logo/')) return this.handleLogo(request, response, url);
    if (pathname === '/healthz') {
      response.writeHead(200, { 'content-type': 'application/json' });
      return response.end(JSON.stringify({ ok: true, sessions: this.sessions.size }));
    }
    return this.handleStatic(request, response, pathname);
  }

  async handleStatic(request, response, pathname) {
    const relative = pathname === '/' ? 'index.html' : pathname.replace(/^\/+/, '');
    const target = path.resolve(this.rendererDir, relative);
    // Never serve anything outside the renderer directory.
    if (target !== this.rendererDir && !target.startsWith(this.rendererDir + path.sep)) {
      response.writeHead(403, { 'content-type': 'text/plain' });
      return response.end('forbidden');
    }
    let body;
    try {
      body = await fsp.readFile(target);
    } catch (error) {
      response.writeHead(404, { 'content-type': 'text/plain' });
      return response.end('not found');
    }
    response.writeHead(200, {
      'content-type': MIME_TYPES[path.extname(target)] || 'application/octet-stream',
      'cache-control': 'no-cache',
    });
    return response.end(body);
  }

  async handleProxy(request, response, url) {
    const sessionId = url.pathname.split('/')[2];
    const session = this.sessions.get(sessionId);
    if (!session) {
      response.writeHead(410, { 'content-type': 'text/plain' });
      return response.end('this playback session has ended');
    }

    const requested = url.searchParams.get('u');
    let target = session.baseUrl;
    if (requested) {
      if (!session.allowed.has(requested)) {
        response.writeHead(403, { 'content-type': 'text/plain' });
        return response.end('that URL was not part of this stream');
      }
      target = requested;
    }

    const headers = { ...session.headers };
    if (request.headers.range) headers.Range = request.headers.range;

    const isPlaylistRequest = looksLikePlaylist(target);
    let upstream;
    try {
      upstream = await this.fetchImpl(target, {
        headers,
        redirect: 'follow',
        signal: AbortSignal.timeout(isPlaylistRequest ? PLAYLIST_TIMEOUT_MS : CONNECT_TIMEOUT_MS),
      });
    } catch (error) {
      response.writeHead(502, { 'content-type': 'text/plain' });
      return response.end(`upstream unreachable: ${error.message}`);
    }

    if (!upstream.ok) {
      response.writeHead(upstream.status, { 'content-type': 'text/plain' });
      return response.end(`upstream answered ${upstream.status}`);
    }

    const contentType = upstream.headers.get('content-type') || '';
    const isPlaylist = isPlaylistRequest || /mpegurl|m3u/i.test(contentType);

    if (isPlaylist) {
      const text = await readLimited(upstream, MAX_PLAYLIST_BYTES);
      const rewritten = rewritePlaylist(text, upstream.url || target, session, `${this.origin}/p/${sessionId}`);
      response.writeHead(200, {
        'content-type': 'application/vnd.apple.mpegurl',
        'cache-control': 'no-cache',
        'content-length': Buffer.byteLength(rewritten),
      });
      return response.end(rewritten);
    }

    const responseHeaders = {};
    const passthrough = ['content-type', 'content-length', 'content-range', 'accept-ranges', 'last-modified', 'etag'];
    for (const name of passthrough) {
      const value = upstream.headers.get(name);
      if (value) responseHeaders[name] = value;
    }
    if (!responseHeaders['content-type']) responseHeaders['content-type'] = 'video/mp2t';
    responseHeaders['cache-control'] = 'no-cache';
    response.writeHead(upstream.status, responseHeaders);

    if (request.method === 'HEAD') return response.end();
    Readable.fromWeb(upstream.body).pipe(response);
    response.on('close', () => {
      if (upstream.body && typeof upstream.body.cancel === 'function') upstream.body.cancel().catch(() => {});
    });
    return undefined;
  }

  /** Channel logos, proxied and cached on disk (they are http:// and hotlink-shy). */
  async handleLogo(request, response, url) {
    const target = url.searchParams.get('u');
    if (!target || !/^https?:\/\//i.test(target)) {
      response.writeHead(400, { 'content-type': 'text/plain' });
      return response.end('bad logo url');
    }
    const key = crypto.createHash('sha1').update(target).digest('hex');
    const cached = path.join(this.logoCacheDir, key);

    try {
      const body = await fsp.readFile(cached);
      response.writeHead(200, {
        'content-type': MIME_TYPES[path.extname(cached)] || 'image/png',
        'cache-control': 'public, max-age=86400',
      });
      return response.end(body);
    } catch (error) {
      /* not cached yet */
    }

    let upstream;
    try {
      upstream = await this.fetchImpl(target, {
        headers: { 'User-Agent': USER_AGENT, Accept: 'image/*,*/*' },
        redirect: 'follow',
        signal: AbortSignal.timeout(PLAYLIST_TIMEOUT_MS),
      });
    } catch (error) {
      response.writeHead(502, { 'content-type': 'text/plain' });
      return response.end('logo unreachable');
    }
    if (!upstream.ok) {
      response.writeHead(upstream.status, { 'content-type': 'text/plain' });
      return response.end('logo unavailable');
    }

    const body = Buffer.from(await readLimited(upstream, MAX_LOGO_BYTES));
    const contentType = upstream.headers.get('content-type') || 'image/png';
    try {
      await fsp.mkdir(this.logoCacheDir, { recursive: true });
      await fsp.writeFile(cached, body);
    } catch (error) {
      /* caching is best-effort */
    }
    response.writeHead(200, { 'content-type': contentType, 'cache-control': 'public, max-age=86400' });
    return response.end(body);
  }
}

function headersFor(channel) {
  const headers = {
    'User-Agent': channel.ua || USER_AGENT,
    Accept: '*/*',
    Connection: 'keep-alive',
  };
  if (channel.referrer) headers.Referer = channel.referrer;
  if (channel.origin) headers.Origin = channel.origin;
  return headers;
}

function looksLikePlaylist(url) {
  const pathname = new URL(url).pathname.toLowerCase();
  return pathname.endsWith('.m3u8') || pathname.endsWith('.m3u');
}

/**
 * Rewrites every URI in an HLS playlist to route back through the proxy.
 *
 * Anything the playlist names becomes an allowed URL for the session, so
 * segments, variant playlists and encryption keys all arrive with the
 * channel's own headers.
 */
function rewritePlaylist(text, baseUrl, session, proxyBase) {
  const lines = text.split(/\r?\n/);
  const out = [];

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) {
      // URI= attributes on #EXT-X-KEY and #EXT-X-MAP tags need rewriting too.
      if (trimmed.startsWith('#') && /URI="/i.test(trimmed)) {
        out.push(
          trimmed.replace(/URI="([^"]+)"/gi, (_match, uri) => {
            const absolute = absoluteUrl(uri, baseUrl);
            session.allowed.add(absolute);
            return `URI="${proxyBase}?u=${encodeURIComponent(absolute)}"`;
          }),
        );
        continue;
      }
      out.push(line);
      continue;
    }

    const absolute = absoluteUrl(trimmed, baseUrl);
    session.allowed.add(absolute);
    out.push(`${proxyBase}?u=${encodeURIComponent(absolute)}`);
  }

  return out.join('\n');
}

function absoluteUrl(uri, baseUrl) {
  try {
    return new URL(uri, baseUrl).toString();
  } catch (error) {
    return uri;
  }
}

async function readLimited(response, maxBytes) {
  const chunks = [];
  let total = 0;
  for await (const chunk of Readable.fromWeb(response.body)) {
    total += chunk.length;
    if (total > maxBytes) throw new Error('response is larger than the app accepts');
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString('utf8');
}

module.exports = { StreamProxy, rewritePlaylist, headersFor, absoluteUrl, LISTEN_HOST };
