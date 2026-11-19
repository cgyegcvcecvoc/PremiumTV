# PremiumTV Relay

A small, self-hostable service that makes the repository's browser-hostile
streams playable in a browser — without turning into an open proxy.

- **Status:** opt-in. The shipped `relay/relay.json` is `enabled: false`, so
  GitHub Pages and the default web build behave exactly as before.
- **Code:** `relay/relay.js` (~600 lines, Node 20+, no dependencies).
- **Tests:** `node --test relay/test/relay.test.js` (16 tests, including an
  end-to-end run against a real HTTP server).

## Why it exists

Measured on `playlists/live/USA.m3u` (2,978 published feeds):

| Browser blocker | Feeds | Why the browser cannot fix it |
|---|---|---|
| Plain `http://` | 771 (25%) | An HTTPS page cannot load insecure media; it is blocked as mixed content. |
| Publishes a Referer / UA / Origin | 135 | `Referer`, `User-Agent` and `Origin` are forbidden request headers in `fetch` and cannot be set from a `<video>` element. |
| No CORS header on the media host | varies | Even when the bytes arrive, the player may not be allowed to read them. |

`http-origin` reaches the native apps through the bundle builder and the
Android parser, so Android could always play those feeds. The browser had no
equivalent path at all: this closes that gap.

## What it refuses to do

An open proxy is how a small project gets its host suspended, so the relay is
deliberately narrow:

1. **Published-playlist allowlist.** `--playlist` is read once at startup. A
   stream URL that is not literally in that M3U is rejected — `openSession()`
   returns `null` and the HTTP surface answers `403`.
2. **Per-session child allowlist.** Variant playlists, segments, `#EXT-X-KEY`
   keys and `#EXT-X-MAP` init sections are added only when they appear inside a
   playlist the relay has already served for that session.
3. **Literal address restrictions, not complete SSRF protection.** Private and
   loopback IPv4 literals, localhost and raw IPv6 literals are rejected for
   both parent and child URLs; redirects are not followed. DNS names can still
   resolve or rebind to private addresses. **Do not expose this relay without an
   outbound firewall blocking private, loopback, link-local, and metadata
   networks** (including IPv6). Redirect-dependent feeds will not work.
4. **No credentials.** No cookies, no auth headers, no client IP forwarding.
5. **Bounded.** 4 MB playlist cap, 12 s playlist deadline and 20 s connection
   deadline for media, 6 parallel requests per session, 512 sessions, 12 h TTL.
6. **No logging of what you watch.** The relay keeps no access log of playback.

## Run it

```bash
# Local, against the checked-in playlist
node relay/relay.js --playlist playlists/live/USA.m3u --port 8099

# Behind a domain (so rewritten playlists use absolute URLs)
PUBLIC_ORIGIN=https://relay.example.com node relay/relay.js \
  --playlist playlists/live/USA.m3u

# Regenerate the discovery document the web player reads
node relay/relay.js --playlist playlists/live/USA.m3u --descriptor relay/relay.json
```

Or with Docker:

```bash
docker build -f relay/Dockerfile -t premiumtv-relay .
docker run -p 8099:8099 -e PUBLIC_ORIGIN=https://relay.example.com premiumtv-relay
```

`GET /healthz` returns `{"ok":true,"channels":2978,"sessions":0}`.

## Turn it on in the web player

1. Deploy the relay somewhere with a public HTTPS URL.
2. Edit `relay/relay.json`:

   ```json
   {
     "enabled": true,
     "provider": "My relay",
     "base": "https://relay.example.com",
     "scope": "published-playlist-only"
   }
   ```

3. Rebuild the web client (`cd web && npm run build`). `relay.json` is copied
   into the artifact, and `relay-client.js` picks it up on load.

The player then uses the relay in exactly two situations, and says so on screen
when it does:

- a feed is plain `http://` on an HTTPS page, or
- a feed publishes a Referer / Origin / User-Agent the browser cannot send.

A feed that plays directly is **never** routed through the relay, so the common
case costs the operator nothing. If a direct attempt fails on a feed the browser
*could* have played, the relay is tried once before the channel is written off.

Anything else — a missing relay, a blocked `relay.json`, a relay that is down —
falls back to the previous behaviour: the player reports the restriction
honestly and moves to the native app as the recommendation.

## API

| Route | Purpose |
|---|---|
| `GET /open?u=<encoded stream URL>` | Opens a playback session and answers `{ sessionId, path, absolute }`. Used by the player. A published stream URL is required. |
| `GET /s/<sessionId>` | The session's playlist (rewritten) or a single segment/key. `?u=` selects a child URI already allowlisted for this session. |
| `GET /s/<sessionId>?u=<child>` | One rewritten child URI from that session. `403` when it was never part of the stream. |
| `GET /healthz` | Liveness, allowlist size, session count. |
| `GET /relay.json` | The discovery document this build ships. |

Responses carry `access-control-allow-origin: *` so the player can read them.
Playlists and segments are `cache-control: no-store`: nothing about a live feed
is cached on the relay.

## Operational notes

- **Bandwidth is the cost.** A relayed 1080p feed is roughly 3–6 Mbps per
  viewer. The relay never transcodes or re-muxes; it only forwards bytes, so
  the CPU cost is small and the egress cost is not.
- **Range requests are forwarded**, so seeking inside an HLS rendition and
  direct MP4 playback both work.
- **Timeouts are short on purpose.** A browser already retries; a stuck relay
  socket is worse than an honest failure.
- **Keep the playlist current.** Re-run the relay (or restart the container)
  after a scrape so the allowlist matches what is actually published. A newly
  promoted feed is unreachable through a stale relay by design.

## What it does not fix

- **Codecs.** AC-3 / E-AC-3 / DTS audio and some HEVC profiles are a browser
  decoder question. The relay cannot make a browser decode what it has no
  decoder for; the native apps' FFmpeg path still covers those.
- **Geo-blocking.** If a provider refuses the relay's egress region, the feed
  stays refused. The relay does not pretend otherwise.
- **DRM.** Not supported anywhere in PremiumTV, and not added here.
