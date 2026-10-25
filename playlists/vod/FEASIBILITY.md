# On-demand feasibility test — Movies & Shows

Generated 2026-10-24T17:05:44Z by `scripts/vod_catalog.py`.

This is the evidence behind the Movies & Shows tab: a finite film and
episode library is feasible with the same player, the same side panel and
the same data bundle the live channels already use. It is deliberately
separate from the playlist and guide pipeline.

## Result

| Measure | Value |
|---|---:|
| Catalogue entries | 11 |
| Films | 5 |
| TV episodes | 5 |
| Test card (authored here) | 1 |
| Probe: working | 10 |
| Probe: other | 1 |

The probe opens each stream the way the apps do — a bounded range request
with `Accept: video/mp4` — and requires an MP4 `ftyp` box or a video
content type. A range request that answers `206` also proves the stream is
seekable, which is what lets the side player scrub and resume.

## Entries

| Title | Kind | Year | Runtime | Size | Direct stream | Probe |
|---|---|---:|---:|---:|---|---|
| PremiumTV Test Card | Film | 2026 | 1 min | 1 MB | `premiumtv-test-card.mp4` | unpublished |
| Carnival of Souls ( iPod Video Version ) | Film | — | 83 min | 361 MB | `carnival_of_souls_512kb.mp4` | working |
| His Girl Friday | Film | 1940 | 92 min | 401 MB | `his_girl_friday_512kb.mp4` | working |
| Night of the Living Dead | Film | 1968 | 97 min | 559 MB | `Night of the Living Dead - (1968).mp4` | working |
| Nosferatu (1922) | Film | 1922 | 87 min | 457 MB | `Nosferatu.1922.ia.mp4` | working |
| Plan 9 From Outer Space Full Movie | Film | 1959 | 79 min | 773 MB | `Plan 9 from Outer Space.mp4` | working |
| Dragnet- The Big Ham (1954) | TV episode | 1954 | 26 min | 162 MB | `Dragnet_Big Ham.mp4` | working |
| Sherlock Holmes - The Case of the Pennsylvania Gun | TV episode | 1954 | 27 min | 116 MB | `TheCaseofthePennsylvaniaGun_512kb.mp4` | working |
| The Beverly Hillbillies - Granny's Spring Tonic - Ep 1x27 | TV episode | — | 25 min | 110 MB | `TheBeverlyHillbillies127-GrannysSpringTonic_512kb.mp4` | working |
| The Beverly Hillbillies - Jed Buys Stock - Ep. 1x05 | TV episode | — | 25 min | 109 MB | `TheBeverlyHillbillies105-JedBuysStock_512kb.mp4` | working |
| The Lone Ranger 1949 (S01E06) War Horse | TV episode | 1949 | 22 min | 111 MB | `The Lone Ranger 1949 (S01E06) War Horse.mp4` | working |

## The test card

`vod-premiumtv-test-card` is the one entry this repository authors: a
65-second synthetic clip (`scripts/vod_test_card.py`, CC0) committed at
`playlists/vod/media/premiumtv-test-card.mp4` with its poster beside it.
It exists so the shelf can be exercised in one play - a moving gold bar
proves the picture is advancing, the timecode proves the clock, the caption
proves text renders, and a beep on every whole second proves audio arrives.

Its `status` reads `unpublished` until the committed file reaches `main`:
the catalogue points at the repository's CDN copy, so the probe can only
answer once that copy exists. Re-run this script after the push and the
same probe turns it into `working`.

## What this proves

- **Sources exist.** Every entry resolves to a direct HTTPS MP4 with byte
  ranges, a poster and a traceable licence - the Archive's own metadata for
  its films, the committed CC0 clip for the test card.
- **The player already handles it.** MP4 plays in the existing ExoPlayer
  (Android) and the existing HLS/MP4 strategies (macOS); no second player
  or new dependency is needed.
- **The side player is the right home.** An on-demand item is just a stream
  with a title and a poster, so it opens in the same docked panel and
  expands to full screen the same way a channel does.
- **The bundle can carry it.** `android/tools/build_bundle.py` copies the
  catalogue into `bundle/vod-catalog.json` and into `meta.vod_catalog`,
  exactly like the team crests and the live schedule.

## What is deliberately not done yet

- No scraping of commercial catalogues: the test set is public domain only.
- No resume points, downloads or per-user watch state: that needs a store
  the apps do not have yet (the existing Recently watched shelf is keyed by
  stream URL and already works for these entries).
- No pagination: the test set fits one screen; a real library needs
  paging, search and per-show grouping before it ships at scale.

## Rights

Every item is public domain or published by the Internet Archive under a
licence that permits reuse. The licence URL from the item's own metadata is
kept in `vod-catalog.json` so the source of each film stays traceable.
