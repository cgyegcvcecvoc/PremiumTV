# Movies & Shows — HTML embeds

> **Live since 2026-11-13.** The shelf is published again: 21 titles (13 films,
> 7 classic TV episodes and the repository's own test card), each with an HTML
> embed as its first server and a direct MP4 as its fallback.

## How a title plays now

Every catalogue entry in `playlists/vod/vod-catalog.json` carries two ways to
play it:

| Field | What it is | Who opens it |
|---|---|---|
| `embed` | `https://archive.org/embed/<identifier>` — an iframe player | web, macOS |
| `embed_kind` | `iframe` (an iframe src) or `html` (a pasted snippet) | all |
| `provider` | the label shown in the player, e.g. `Internet Archive` | all |
| `embeds[]` | every embed for the title, Archive first | web, macOS |
| `stream` / `streams[]` | direct MP4 URLs | Android, and as the fallback server everywhere |

The web and macOS players try the embeds first and drop back to the direct MP4
if the provider will not load. Android's ExoPlayer cannot render an iframe, so
it keeps using `stream` exactly as before — which is why every entry still has
one.

## Why embeds first

A direct MP4 has to survive three things a browser can fail at: a
cross-origin fetch, a codec the browser lacks, and a range request the host
will not answer. An iframe hands all three to the provider's own player, so a
title that will not stream in a `<video>` tag still plays.

## Why the Internet Archive

- **Legal and free.** Every title is public domain or published under a licence
  that permits reuse; the licence URL from each item's own metadata is kept in
  `vod-catalog.json`.
- **Stable.** Each item has a permanent identifier, a poster and a documented
  embed endpoint, so a link does not rot the way a scraped stream does.
- **Traceable.** `playlists/vod/FEASIBILITY.md` is regenerated on every build
  and lists each title, its derivative and its probe result.

This repository does **not** ship embeds from commercial streaming sites.
`lookmovie2.to` and similar mirrors host copyrighted films without licences,
their embed URLs are unstable by design (they rotate per host and per
session), and they routinely serve pop-under and redirect scripts inside the
iframe. Wiring one into the published catalogue would put that directly in
front of every viewer, on every platform, with no way to know when it
switched. The hook below exists so a provider can be added deliberately, per
title, by someone who has checked it.

## Adding another free source

Edit `playlists/vod/embed-sources.json` — one object per extra embed:

```json
{
  "extra": [
    {
      "slug": "night-of-the-living-dead",
      "provider": "Internet Archive (alternate)",
      "kind": "iframe",
      "url": "https://archive.org/embed/night-of-the-living-dead_1968"
    },
    {
      "slug": "nosferatu",
      "provider": "My source",
      "kind": "html",
      "html": "<iframe src=\"https://example.com/embed/nosferatu\" allowfullscreen></iframe>",
      "primary": true
    }
  ]
}
```

- `kind: "iframe"` needs `url`; `kind: "html"` needs `html` (a verbatim
  snippet pasted from the provider, exactly as providers publish them).
- `primary: true` puts the embed first, ahead of the Internet Archive player.
  Leave it off to append the embed as an extra server.
- The slug must match `items[].slug` in the catalogue. Unknown slugs, non-http
  URLs and bad kinds are skipped with a warning on the build log; the rest of
  the catalogue is unaffected.

Then rebuild:

```sh
python3 scripts/vod_catalog.py --offline     # re-resolve from the cache, write
python3 scripts/vod_catalog.py --check       # validate the committed document
```

The `--offline` rebuild resolves every title from `RESOLVED` in
`scripts/vod_catalog.py` (the last networked run's answer) and writes the
catalogue, the health file and this report without touching the network at
all, so adding a provider never needs an Archive round-trip. A normal
networked run — including the scheduled one — re-resolves from the Archive's
metadata and refreshes those numbers.

## Content-Security-Policy

An embed is only as reachable as the page's CSP allows. The web
(`web/src/index.html`) and macOS (`macos/app/src/renderer/index.html`)
pages now permit HTTPS iframes:

```
frame-src 'self' https:
```

`https:` is deliberately broad: the point of the shelf is that you can point
a title at any embed provider you trust, and a fixed allow-list would mean a
code change for every new source. It still blocks `javascript:`, `data:` and
plain-HTTP frames, and `object-src 'none'`, `base-uri 'none'` and
`form-action 'none'` are unchanged. Narrow it to the hosts you actually use
if you would rather keep the list explicit.

## What the players do with an embed

- The iframe replaces the `<video>` element inside the same player stage, so
  the docked/expanded/full-screen layouts are unchanged.
- The seek bar, back/forward, audio-track, PiP and AirPlay controls are
  hidden: they drive a `<video>` element that is not in use.
- Resume is not recorded for an embed — the page cannot read the playback
  position out of a cross-origin iframe, and inventing one would leave a
  wrong "Resume at 42:10" badge on the card. Embed playback therefore never
  writes a position; direct-stream playback still does.
- "Open original ↗" points at the embed URL, so the provider's own page is
  one click away when an iframe refuses to load.
