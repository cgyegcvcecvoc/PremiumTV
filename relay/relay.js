'use strict';

/**
 * PremiumTV Relay — the browser's playback rescue path.
 *
 * ## The problem this solves
 *
 * The published library is browser-hostile in three measurable ways (counted on
 * `playlists/live/USA.m3u` at the time this was written):
 *
 *   25% of feeds are plain `http://`   -> blocked as mixed content on an HTTPS site
 *   ~9% publish a required Referer/UA -> browsers cannot set those headers
 *   many hosts send no CORS header     -> the player may not read the bytes at all
 *
 * The native apps do not care about any of the three, which is exactly why a
 * stream "works on Android and not on the web". A browser cannot fix those
 * itself. A server can: it fetches the feed with the headers the playlist
 * publishes and hands the bytes back same-origin.
 *
 * ## What it is careful about
 *
 * This is deliberately NOT an open proxy, because an open proxy is how a small
 * project gets itself abused and blocked:
 *
 *   1. Allowlist. Only a URL that appears in the repository's own published
 *      playlist may be relayed. `loadAllowlist()` reads the M3U and nothing
 *      else is accepted.
 *   2. Per-session child allowlist. Variant playlists, segments and keys are
 *      added only when they appear inside a playlist the relay already served
 *      for that session — the same rule the macOS `streamProxy` uses.
 *   3. Size, time and rate limits. Every request is bounded, and a single
 *      client cannot use the relay as a bandwidth hose.
 *   4. Honest headers. `Referer`/`Origin` are sent only when the playlist
 *      publishes them, and `Origin` is normalised to the scheme+host+port tuple
 *      a CDN expects.
 *   5. No credentials, no cookies, and redirects are not followed. Every DNS
 *      answer is checked and pinned to the socket; an outbound firewall is still
 *      recommended as defense in depth.
 *
 * ## Self-hosting
 *
 * The shipped clients probe `relay/relay.json` next to the player. When that
 * file is absent or says `enabled: false` the relay entry never appears and the
 * player behaves exactly as it did before. Run your own:
 *
 *   node relay/relay.js --playlist playlists/live/USA.m3u --port 8099
 *
 * or deploy the container in `relay/Dockerfile`.
 */

const crypto = require('node:crypto');
const dns = require('node:dns');
const http = require('node:http');
const https = require('node:https');
const net = require('node:net');
const zlib = require('node:zlib');
const fs = require('node:fs');
const path = require('node:path');
const { Readable } = require('node:stream');
const { pipeline } = require('node:stream/promises');

const MAX_PLAYLIST_BYTES = 4 * 1024 * 1024;
const MAX_SESSIONS = 512;
const SESSION_TTL_MS = 12 * 60 * 60 * 1000;
const SEGMENT_TIMEOUT_MS = 20000;
const PLAYLIST_TIMEOUT_MS = 12000;
const MAX_CONCURRENT_PER_SESSION = 6;
const DEFAULT_USER_AGENT =
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ' +
  '(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36';

// --------------------------------------------------------------------- parsing

/**
 * Reads an M3U and returns, per stream URL, the headers the entry publishes.
 *
 * Only the tags this repository actually writes are read: `#EXTINF` attributes
 * (`http-referrer`, `http-user-agent`, `http-origin`) and the
 * `#EXTVLCOPT` / `#KODIPROP` stream options. Anything else is ignored, so a
 * malicious playlist cannot smuggle a header onto a feed.
 */
function parsePlaylistHeaders(text) {
  const entries = new Map();
  let pending = null;

  for (const rawLine of String(text || '').split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line) continue;

    if (line.startsWith('#EXTINF')) {
      const attrs = parseAttrs(line);
      pending = {
        referrer: (attrs['http-referrer'] || '').trim(),
        ua: (attrs['http-user-agent'] || '').trim(),
        origin: (attrs['http-origin'] || '').trim(),
      };
      continue;
    }

    if (line.startsWith('#EXTVLCOPT:') || line.startsWith('#KODIPROP:')) {
      if (!pending) continue;
      const option = line.slice(line.indexOf(':') + 1);
      const eq = option.indexOf('=');
      const key = (eq === -1 ? option : option.slice(0, eq)).trim().toLowerCase();
      const value = (eq === -1 ? '' : option.slice(eq + 1)).trim();
      if (key === 'http-referrer' || key === 'referer') pending.referrer = value;
      else if (key === 'http-user-agent' || key === 'user-agent') pending.ua = value;
      else if (key === 'http-origin' || key === 'origin') pending.origin = value;
      continue;
    }

    if (line.startsWith('#')) continue;
    if (!pending) continue;
    entries.set(line, pending);
    pending = null;
  }

  return entries;
}

function parseAttrs(line) {
  const attrs = {};
  const re = /([A-Za-z0-9_-]+)\s*=\s*"([^"]*)"/g;
  let match;
  while ((match = re.exec(line)) !== null) attrs[match[1].toLowerCase()] = match[2];
  return attrs;
}

// --------------------------------------------------------------------- helpers

/**
 * The Origin header is a scheme+host+port tuple. Playlists routinely publish
 * the embed page instead, and an HTTP client that forwards the page URL is
 * rejected by the CDN. Shared behaviour with the macOS `streamProxy`.
 */
function originHeader(raw) {
  const value = String(raw || '').trim();
  if (!value) return '';
  try {
    const parsed = new URL(value);
    if (!parsed.protocol.startsWith('http')) return '';
    return parsed.origin;
  } catch (error) {
    return '';
  }
}

function headersFor(entry) {
  const headers = {
    'User-Agent': (entry && entry.ua) || DEFAULT_USER_AGENT,
    Accept: '*/*',
  };
  if (entry && entry.referrer) headers.Referer = entry.referrer;
  const origin = originHeader(entry && entry.origin);
  if (origin) headers.Origin = origin;
  return headers;
}

// Block special-use ranges rather than trying to maintain a short list of
// familiar private networks. In particular, shared, documentation, benchmark,
// multicast and reserved IPv4 space is not a valid relay destination either.
const NON_PUBLIC_IPV4 = new net.BlockList();
for (const [address, prefix] of [
  ['0.0.0.0', 8],
  ['10.0.0.0', 8],
  ['100.64.0.0', 10],
  ['127.0.0.0', 8],
  ['169.254.0.0', 16],
  ['172.16.0.0', 12],
  ['192.0.0.0', 24],
  ['192.0.2.0', 24],
  ['192.88.99.0', 24],
  ['192.168.0.0', 16],
  ['198.18.0.0', 15],
  ['198.51.100.0', 24],
  ['203.0.113.0', 24],
  ['224.0.0.0', 4],
  ['240.0.0.0', 4],
]) NON_PUBLIC_IPV4.addSubnet(address, prefix, 'ipv4');

// IPv6 is public only in 2000::/3. Remove protocol-assignment, transition,
// documentation and newer documentation ranges from that global-unicast block.
const GLOBAL_IPV6 = new net.BlockList();
GLOBAL_IPV6.addSubnet('2000::', 3, 'ipv6');
const NON_PUBLIC_IPV6 = new net.BlockList();
for (const [address, prefix] of [
  ['2001::', 23],
  ['2001:db8::', 32],
  ['2002::', 16],
  ['3fff::', 20],
]) NON_PUBLIC_IPV6.addSubnet(address, prefix, 'ipv6');

/** True only for globally routable IPv4 or IPv6 unicast addresses. */
function isPublicAddress(address) {
  const family = net.isIP(String(address || ''));
  if (family === 4) return !NON_PUBLIC_IPV4.check(address, 'ipv4');
  if (family === 6) {
    return GLOBAL_IPV6.check(address, 'ipv6') && !NON_PUBLIC_IPV6.check(address, 'ipv6');
  }
  return false;
}

/**
 * Resolve a hostname once, reject the whole answer set if any address is
 * non-public, then make Node's socket use only those vetted addresses. Pinning
 * the lookup result prevents a DNS change between validation and connect.
 */
function resolvePublicAddresses(hostname, signal) {
  return new Promise((resolve, reject) => {
    if (signal && signal.aborted) {
      reject(signal.reason || new Error('request aborted'));
      return;
    }

    let settled = false;
    const finish = (error, addresses) => {
      if (settled) return;
      settled = true;
      if (signal) signal.removeEventListener('abort', onAbort);
      if (error) {
        reject(error);
        return;
      }
      if (!Array.isArray(addresses) || addresses.length === 0) {
        reject(new Error('upstream hostname returned no addresses'));
        return;
      }
      const records = addresses.map(({ address, family }) => ({ address, family }));
      if (records.some(({ address, family }) => net.isIP(address) !== family || !isPublicAddress(address))) {
        reject(new Error('upstream hostname resolved to a non-public address'));
        return;
      }
      resolve(records);
    };
    const onAbort = () => finish(signal.reason || new Error('request aborted'));
    if (signal) signal.addEventListener('abort', onAbort, { once: true });
    try {
      dns.lookup(hostname, { all: true, verbatim: true }, finish);
    } catch (error) {
      finish(error);
    }
  });
}

/**
 * Return the lookup callback that pins a socket to validated DNS answers.
 * Node may request one family or all families; every returned address has
 * already passed the public-address check.
 */
function pinnedLookup(addresses, expectedHostname = '') {
  return (hostname, options, callback) => {
    if (typeof options === 'function') {
      callback = options;
      options = {};
    }
    if (expectedHostname && hostname.toLowerCase() !== expectedHostname.toLowerCase()) {
      callback(new Error('socket requested an unvalidated hostname'));
      return;
    }
    const family = options && options.family;
    const candidates = addresses.filter((record) => !family || record.family === family);
    if (candidates.length === 0) {
      callback(new Error('no vetted address for the requested family'));
      return;
    }
    if (options && options.all) {
      callback(null, candidates.map(({ address, family: recordFamily }) => ({
        address,
        family: recordFamily,
      })));
      return;
    }
    callback(null, candidates[0].address, candidates[0].family);
  };
}

/**
 * A fetch-compatible HTTP client for relay upstreams. Unlike global fetch, this
 * resolves and pins DNS before connecting; it deliberately never follows
 * redirects. The relay uses Node 20+, whose built-in Response and Web Streams
 * let the rest of the streaming path remain unchanged.
 */
async function fetchPinned(url, init = {}) {
  if (!isRelayable(url)) throw new Error('upstream URL is not relayable');
  const parsed = new URL(url);
  const addresses = await resolvePublicAddresses(parsed.hostname, init.signal);
  if (init.signal && init.signal.aborted) {
    throw init.signal.reason || new Error('request aborted');
  }

  const transport = parsed.protocol === 'https:' ? https : http;
  const headers = init.headers instanceof Headers
    ? Object.fromEntries(init.headers.entries())
    : { ...(init.headers || {}) };
  // Match fetch's common compression negotiation; responses are decoded below
  // so media bytes and playlists retain the old fetch-compatible behavior.
  headers['Accept-Encoding'] = 'gzip, deflate, br';
  const lookup = pinnedLookup(addresses, parsed.hostname);

  return new Promise((resolve, reject) => {
    let request;
    try {
      request = transport.request(parsed, {
        method: init.method || 'GET',
        headers,
        signal: init.signal,
        lookup,
      });
    } catch (error) {
      reject(error);
      return;
    }
    request.once('error', reject);
    request.once('response', (incoming) => {
      try {
        const status = incoming.statusCode || 502;
        const responseHeaders = { ...incoming.headers };
        const encoding = String(responseHeaders['content-encoding'] || '').toLowerCase().trim();
        let stream = incoming;
        if (encoding === 'gzip') stream = incoming.pipe(zlib.createGunzip());
        else if (encoding === 'deflate') stream = incoming.pipe(zlib.createInflate());
        else if (encoding === 'br') stream = incoming.pipe(zlib.createBrotliDecompress());
        if (stream !== incoming) {
          delete responseHeaders['content-encoding'];
          delete responseHeaders['content-length'];
        }
        const body = [204, 205, 304].includes(status) ? null : Readable.toWeb(stream);
        resolve(new Response(body, {
          status,
          statusText: incoming.statusMessage,
          headers: responseHeaders,
        }));
      } catch (error) {
        incoming.destroy(error);
        reject(error);
      }
    });
    request.end();
  });
}

/** Reject non-http(s), credentialed and obvious private-literal URLs up front. */
function isRelayable(url) {
  try {
    const parsed = new URL(url);
    if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') return false;
    const host = parsed.hostname.toLowerCase();
    if (host === 'localhost' || host === '::1' || host.endsWith('.localhost')) return false;
    if (parsed.username || parsed.password) return false;
    if (net.isIP(host) === 4 && !isPublicAddress(host)) return false;
    if (host.startsWith('[') || host.includes(':')) return false; // no raw IPv6 literal
    return true;
  } catch (error) {
    return false;
  }
}

function looksLikePlaylist(url) {
  try {
    const pathname = new URL(url).pathname.toLowerCase();
    return pathname.endsWith('.m3u8') || pathname.endsWith('.m3u');
  } catch (error) {
    return false;
  }
}

function looksLikeExtM3uHead(chunk) {
  if (!chunk || chunk.length < 7) return false;
  const head = chunk.subarray(0, 64).toString('utf8').replace(/^\uFEFF/, '').trimStart();
  return head.startsWith('#EXTM3U');
}

function absoluteUrl(uri, baseUrl) {
  try {
    return new URL(uri, baseUrl).toString();
  } catch (error) {
    return uri;
  }
}

function inferContentType(url) {
  let pathname = '';
  try {
    pathname = new URL(url).pathname.toLowerCase();
  } catch (error) {
    return 'video/mp2t';
  }
  if (pathname.endsWith('.aac') || pathname.endsWith('.adts')) return 'audio/aac';
  if (pathname.endsWith('.mp3')) return 'audio/mpeg';
  if (pathname.endsWith('.ac3')) return 'audio/ac3';
  if (pathname.endsWith('.ec3') || pathname.endsWith('.eac3')) return 'audio/eac3';
  if (pathname.endsWith('.m4a')) return 'audio/mp4';
  if (pathname.endsWith('.mp4') || pathname.endsWith('.m4v')) return 'video/mp4';
  if (pathname.endsWith('.m4s') || pathname.endsWith('.cmfa') || pathname.endsWith('.cmfv')) {
    return 'video/iso.segment';
  }
  if (pathname.endsWith('.webm')) return 'video/webm';
  if (pathname.endsWith('.vtt')) return 'text/vtt';
  if (pathname.endsWith('.key')) return 'application/octet-stream';
  return 'video/mp2t';
}

/**
 * Rewrites an HLS playlist so every URI comes back through the relay, and
 * records each one on the session's child allowlist.
 *
 * `URI="..."` attributes are rewritten too, so `#EXT-X-KEY` keys and
 * `#EXT-X-MAP` init sections arrive with the same published headers.
 */
function rewritePlaylist(text, baseUrl, session, proxyBase) {
  const out = [];
  for (const line of text.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed) {
      out.push(line);
      continue;
    }
    if (trimmed.startsWith('#')) {
      if (/URI="/i.test(trimmed)) {
        out.push(
          trimmed.replace(/URI="([^"]+)"/gi, (_match, uri) => {
            const absolute = absoluteUrl(uri, baseUrl);
            if (session && isRelayable(absolute)) session.allowed.add(absolute);
            return `URI="${proxyBase}?u=${encodeURIComponent(absolute)}"`;
          }),
        );
      } else {
        out.push(line);
      }
      continue;
    }
    const absolute = absoluteUrl(trimmed, baseUrl);
    if (session && isRelayable(absolute)) session.allowed.add(absolute);
    out.push(`${proxyBase}?u=${encodeURIComponent(absolute)}`);
  }
  return out.join('\n');
}

async function readLimited(response, maxBytes) {
  const chunks = [];
  let total = 0;
  for await (const chunk of Readable.fromWeb(response.body)) {
    total += chunk.length;
    if (total > maxBytes) throw new Error('response is larger than the relay accepts');
    chunks.push(chunk);
  }
  return Buffer.concat(chunks);
}

// ----------------------------------------------------------------------- relay

class Relay {
  /**
   * @param {object} options
   * @param {Map<string, object>} options.allowlist stream URL -> published headers
   * @param {Function} [options.fetchImpl] injectable for tests
   * @param {Function} [options.now] clock injectable for tests
   * @param {number} [options.maxSessions]
   * @param {number} [options.sessionTtlMs]
   * @param {string} [options.publicOrigin] absolute base for rewritten URIs
   */
  constructor(options) {
    this.allowlist = options.allowlist || new Map();
    this.fetchImpl = options.fetchImpl || fetchPinned;
    this.now = options.now || (() => Date.now());
    this.maxSessions = options.maxSessions || MAX_SESSIONS;
    this.sessionTtlMs = options.sessionTtlMs || SESSION_TTL_MS;
    this.publicOrigin = options.publicOrigin || '';
    this.sessions = new Map();
    this.server = null;
    this.port = 0;
  }

  get origin() {
    return this.publicOrigin || `http://127.0.0.1:${this.port}`;
  }

  sessionCount() {
    return this.sessions.size;
  }

  pruneSessions(now = this.now(), reserve = 0) {
    for (const [id, session] of this.sessions) {
      if (now - session.lastAccessAt >= this.sessionTtlMs) this.sessions.delete(id);
    }
    const keep = Math.max(0, this.maxSessions - reserve);
    if (this.sessions.size <= keep) return;
    const oldest = [...this.sessions.values()]
      .sort((a, b) => a.lastAccessAt - b.lastAccessAt)
      .slice(0, this.sessions.size - keep);
    for (const session of oldest) this.sessions.delete(session.id);
  }

  /**
   * Opens a playback session for a published stream URL and returns the
   * loopback/relay path a `<video>` element or hls.js can load.
   *
   * Refuses an unpublished URL outright: the allowlist is the whole point.
   */
  openSession(streamUrl) {
    if (!isRelayable(streamUrl)) return null;
    const entry = this.allowlist.get(streamUrl);
    if (!entry) return null;
    const now = this.now();
    this.pruneSessions(now, 1);
    const id = crypto.randomBytes(12).toString('hex');
    this.sessions.set(id, {
      id,
      baseUrl: streamUrl,
      headers: headersFor(entry),
      allowed: new Set([streamUrl]),
      active: 0,
      lastAccessAt: now,
    });
    return { sessionId: id, path: `/s/${id}`, absolute: `${this.origin}/s/${id}` };
  }

  closeSession(sessionId) {
    return this.sessions.delete(String(sessionId || ''));
  }

  async handle(request, response) {
    let url;
    try {
      url = new URL(request.url, 'http://relay.local');
    } catch (error) {
      return sendText(response, 400, 'bad request');
    }

    if (url.pathname === '/healthz') {
      return sendJson(response, 200, {
        ok: true,
        channels: this.allowlist.size,
        sessions: this.sessions.size,
      });
    }
    if (url.pathname === '/relay.json') {
      return sendJson(response, 200, relayDescriptor({}, this.allowlist.size));
    }
    if (url.pathname === '/open') return this.handleOpen(request, response, url);
    if (url.pathname.startsWith('/s/')) return this.handleStream(request, response, url);
    return sendText(response, 404, 'not found');
  }

  /**
   * Opens a session over HTTP so the browser player can ask for one by URL.
   *
   * Only a URL that is literally in the published playlist is accepted, and the
   * answer says plainly whether the relay took it.
   */
  async handleOpen(request, response, url) {
    const target = url.searchParams.get('u') || '';
    if (!target) return sendText(response, 400, 'a stream URL is required');
    const session = this.openSession(target);
    if (!session) {
      return sendJson(response, 403, {
        ok: false,
        message: 'That URL is not in this relay\'s published playlist.',
      });
    }
    return sendJson(response, 200, {
      ok: true,
      sessionId: session.sessionId,
      path: session.path,
      absolute: session.absolute,
    });
  }

  async handleStream(request, response, url) {
    const sessionId = url.pathname.split('/')[2] || '';
    const now = this.now();
    this.pruneSessions(now);
    const session = this.sessions.get(sessionId);
    if (!session) {
      return sendText(response, 410, 'this playback session has ended');
    }
    session.lastAccessAt = now;

    const requested = url.searchParams.get('u');
    const target = requested || session.baseUrl;
    if (!isRelayable(target) || !session.allowed.has(target)) {
      return sendText(response, 403, 'that URL was not part of this stream');
    }
    if (session.active >= MAX_CONCURRENT_PER_SESSION) {
      return sendText(response, 429, 'too many parallel requests; retry shortly');
    }

    const headers = { ...session.headers };
    const range = request.headers.range;
    if (range) headers.Range = range;

    const isPlaylist = looksLikePlaylist(target);
    session.active += 1;
    let upstream;
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), isPlaylist ? PLAYLIST_TIMEOUT_MS : SEGMENT_TIMEOUT_MS);
    try {
      upstream = await this.fetchImpl(target, {
        headers,
        // The production fetcher pins a vetted public DNS answer and never
        // follows redirects. Injected test fetchers must preserve that contract.
        redirect: 'manual',
        signal: controller.signal,
      });
    } catch (error) {
      clearTimeout(timer);
      session.active -= 1;
      return sendText(response, 502, `upstream unreachable: ${describe(error)}`);
    }

    try {
      if (!upstream.ok) {
        return sendText(response, upstream.status === 404 ? 404 : 502,
          `upstream answered ${upstream.status}`);
      }
      const contentType = (upstream.headers.get('content-type') || '').toLowerCase();
      const finalUrl = upstream.url || target;
      const playlistish = isPlaylist || looksLikePlaylist(finalUrl) || /mpegurl|m3u/i.test(contentType);

      // A CDN often serves an HLS master, an audio rendition or a variant from
      // an extensionless URL as application/octet-stream. Streaming it raw
      // leaves the child URLs pointing at a host the browser cannot read, so
      // sniff the first chunk for #EXTM3U before deciding it is media. Never
      // sniff a HEAD, a range request (VOD seeking) or a declared media type.
      const canSniff = request.method !== 'HEAD' && Boolean(upstream.body)
        && !range && !/^(video|audio|image|font)\//i.test(contentType);

      if (!playlistish) clearTimeout(timer); // connect deadline, not a live-stream lifetime
      if (playlistish) {
        const body = await readLimited(upstream, MAX_PLAYLIST_BYTES);
        const text = body.toString('utf8');
        if (!looksLikeExtM3uHead(body)) {
          return sendText(response, 502, 'upstream did not return a playlist');
        }
        const rewritten = rewritePlaylist(
          text,
          finalUrl,
          session,
          `${this.origin}/s/${sessionId}`,
        );
        response.writeHead(200, {
          'content-type': 'application/vnd.apple.mpegurl',
          'cache-control': 'no-store',
          'access-control-allow-origin': '*',
          'content-length': Buffer.byteLength(rewritten),
        });
        return response.end(rewritten);
      }

      const outHeaders = {
        'cache-control': 'no-store',
        'access-control-allow-origin': '*',
      };
      for (const name of ['content-type', 'content-length', 'content-range',
        'accept-ranges', 'last-modified', 'etag']) {
        const value = upstream.headers.get(name);
        if (value) outHeaders[name] = value;
      }
      if (!outHeaders['content-type']) outHeaders['content-type'] = inferContentType(finalUrl);
      if (!canSniff) {
        response.writeHead(upstream.status, outHeaders);
        if (request.method === 'HEAD') return response.end();
        await pipeline(Readable.fromWeb(upstream.body), response);
        return undefined;
      }

      const reader = upstream.body.getReader();
      let firstChunk = null;
      try {
        const first = await reader.read();
        if (!first.done) firstChunk = Buffer.from(first.value);
      } catch (error) {
        await reader.cancel().catch(() => {});
        if (!response.headersSent) return sendText(response, 502, describe(error));
        response.destroy();
        return undefined;
      }

      if (firstChunk && firstChunk.length > MAX_PLAYLIST_BYTES) {
        await reader.cancel().catch(() => {});
        return sendText(response, 502, 'playlist too large');
      }
      if (firstChunk && looksLikeExtM3uHead(firstChunk)) {
        const chunks = [firstChunk];
        let total = firstChunk.length;
        try {
          for (;;) {
            const { done, value } = await reader.read();
            if (done) break;
            const buf = Buffer.from(value);
            total += buf.length;
            if (total > MAX_PLAYLIST_BYTES) {
              await reader.cancel().catch(() => {});
              return sendText(response, 502, 'playlist too large');
            }
            chunks.push(buf);
          }
        } catch (error) {
          response.destroy();
          return undefined;
        }
        const rewritten = rewritePlaylist(
          Buffer.concat(chunks).toString('utf8'),
          finalUrl,
          session,
          `${this.origin}/s/${sessionId}`,
        );
        response.writeHead(200, {
          'content-type': 'application/vnd.apple.mpegurl',
          'cache-control': 'no-store',
          'access-control-allow-origin': '*',
          'content-length': Buffer.byteLength(rewritten),
        });
        return response.end(rewritten);
      }

      // Real media: the first chunk belongs to the client, not to a parser.
      response.writeHead(upstream.status, outHeaders);
      response.on('close', () => { reader.cancel().catch(() => {}); });
      if (firstChunk && !response.destroyed) response.write(firstChunk);
      try {
        for (;;) {
          if (response.destroyed) break;
          const { done, value } = await reader.read();
          if (done || response.destroyed) break;
          if (!response.write(Buffer.from(value))) {
            // A disconnected client fires 'close', not 'drain'; waiting only
            // for 'drain' would keep the session slot occupied forever.
            await new Promise((resolve) => {
              if (response.destroyed) return resolve();
              const done = () => {
                response.off('drain', done);
                response.off('close', done);
                resolve();
              };
              response.once('drain', done);
              response.once('close', done);
            });
          }
        }
        if (!response.destroyed) response.end();
      } catch (error) {
        await reader.cancel().catch(() => {});
        if (!response.headersSent) return sendText(response, 502, describe(error));
        response.destroy();
      }
      return undefined;
    } catch (error) {
      if (!response.headersSent) return sendText(response, 502, describe(error));
      response.destroy();
      return undefined;
    } finally {
      clearTimeout(timer);
      session.active = Math.max(0, session.active - 1);
    }
  }

  async start(port = 0, host = '0.0.0.0') {
    this.server = http.createServer((request, response) => {
      this.handle(request, response).catch((error) => {
        if (!response.headersSent) sendText(response, 500, describe(error));
        else response.destroy();
      });
    });
    await new Promise((resolve, reject) => {
      this.server.once('error', reject);
      this.server.listen(port, host, () => {
        this.server.removeListener('error', reject);
        resolve();
      });
    });
    this.port = this.server.address().port;
    return this.origin;
  }

  async stop() {
    this.sessions.clear();
    if (this.server) await new Promise((resolve) => this.server.close(resolve));
    this.server = null;
  }
}

// ------------------------------------------------------------------- responses

function describe(error) {
  return (error && (error.message || String(error))) || 'unknown error';
}

function sendText(response, status, message) {
  if (response.headersSent) return undefined;
  response.writeHead(status, {
    'content-type': 'text/plain; charset=utf-8',
    'cache-control': 'no-store',
  });
  return response.end(message);
}

function sendJson(response, status, value) {
  if (response.headersSent) return undefined;
  const body = JSON.stringify(value);
  response.writeHead(status, {
    'content-type': 'application/json; charset=utf-8',
    'cache-control': 'no-store',
    'access-control-allow-origin': '*',
    'content-length': Buffer.byteLength(body),
  });
  return response.end(body);
}

// -------------------------------------------------------------------- discovery

/**
 * The document the web player probes to find a relay.
 *
 * `enabled: false` is the default everywhere, including GitHub Pages, because
 * turning the relay on is an explicit deployment decision: it costs bandwidth
 * and it accepts traffic on the operator's behalf.
 */
function relayDescriptor(overrides = {}, channelCount = 0) {
  return {
    enabled: false,
    provider: 'PremiumTV Relay',
    note:
      'Set enabled to true and base to the URL of a running relay (see relay/README.md). ' +
      'The relay only forwards streams listed in this repository.',
    base: '',
    scope: 'published-playlist-only',
    channels: channelCount,
    headers: 'published-referrer-origin-user-agent',
    ...overrides,
  };
}

function loadAllowlist(playlistPath) {
  const text = fs.readFileSync(playlistPath, 'utf8');
  return parsePlaylistHeaders(text);
}

function writeDescriptor(playlistPath, outPath) {
  const allowlist = loadAllowlist(playlistPath);
  const doc = relayDescriptor({}, allowlist.size);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, `${JSON.stringify(doc, null, 2)}\n`, 'utf8');
  return doc;
}

// ------------------------------------------------------------------------- cli

function main(argv) {
  const args = {
    playlist: 'playlists/live/USA.m3u',
    port: process.env.PORT || '8099',
    // A container deployment is reachable at a public URL; without it the
    // rewritten playlists would point at 127.0.0.1 and fail in a browser.
    publicOrigin: process.env.PUBLIC_ORIGIN || '',
  };
  for (let i = 0; i < argv.length; i += 1) {
    const flag = argv[i];
    const value = argv[i + 1];
    if (flag === '--playlist') {
      args.playlist = value;
      i += 1;
    } else if (flag === '--port') {
      args.port = value;
      i += 1;
    } else if (flag === '--public-origin') {
      args.publicOrigin = value;
      i += 1;
    } else if (flag === '--descriptor') {
      const doc = writeDescriptor(args.playlist, value);
      process.stdout.write(`wrote ${value} (${doc.channels} channels, disabled by default)\n`);
      return 0;
    } else if (flag === '--help' || flag === '-h') {
      process.stdout.write(
        'usage: node relay/relay.js [--playlist FILE] [--port N] [--public-origin URL]\n' +
          '       node relay/relay.js --playlist FILE --descriptor relay/relay.json\n',
      );
      return 0;
    }
  }

  const allowlist = loadAllowlist(args.playlist);
  if (allowlist.size === 0) {
    process.stderr.write(`no stream URLs found in ${args.playlist}\n`);
    return 1;
  }
  const relay = new Relay({ allowlist, publicOrigin: args.publicOrigin });
  relay
    .start(Number(args.port))
    .then((origin) => {
      process.stdout.write(
        `PremiumTV Relay on ${origin} — ${allowlist.size} published streams, ` +
          'published-playlist allowlist only\n',
      );
    })
    .catch((error) => {
      process.stderr.write(`relay failed to start: ${describe(error)}\n`);
      process.exitCode = 1;
    });
  return 0;
}

module.exports = {
  Relay,
  parsePlaylistHeaders,
  parseAttrs,
  originHeader,
  headersFor,
  isRelayable,
  isPublicAddress,
  resolvePublicAddresses,
  pinnedLookup,
  fetchPinned,
  looksLikePlaylist,
  looksLikeExtM3uHead,
  absoluteUrl,
  inferContentType,
  rewritePlaylist,
  relayDescriptor,
  loadAllowlist,
  writeDescriptor,
  DEFAULT_USER_AGENT,
  MAX_SESSIONS,
  SESSION_TTL_MS,
  MAX_CONCURRENT_PER_SESSION,
};

if (require.main === module) process.exitCode = main(process.argv.slice(2));
