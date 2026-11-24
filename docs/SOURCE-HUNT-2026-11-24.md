# Source hunt — 2026-11-24

## Scope and limitations

A deep pass over five externally supplied sources, measured against the
repository's own published corpus rather than judged by eye:

1. <https://github.com/HerbertHe/iptv-sources>
2. <https://iptvcat.net/united_states_of_america__1>
3. <https://iptvcat.net/home_7>
4. <https://i.mjh.nz/>
5. <https://raw.githubusercontent.com/doms9/iptv/refs/heads/default/M3U8/base.m3u8>

The comparison baseline is the corpus from the 2026-11-24 21:28 UTC run:
**19,621 unique links** (12,525 working, 2,341 confirmed dead, 4,755
unverified), **13,340 published** entries across 176 countries.

This sandbox reaches `github.com`, `api.github.com`, `codeload.github.com`,
`registry.npmjs.org` and PyPI only. Raw `curl` to `raw.githubusercontent.com`,
`iptvcat.net` and `i.mjh.nz` returns nothing here, so GitHub content was read
through the API and web pages through a page-fetch tool. **No stream was played
in a real player, and no stream was link-checked by this audit.** Where a number
below says "would add N links", it is an URL-set difference, not a promise that
those links work; the daily link check and the monthly discovery sample check
are the things that decide that. Nothing here was imported on the strength of
this document alone.

Nothing in this hunt is about WGAL or any other single named channel.

## Verdict at a glance

| Source | What it actually is | New links vs corpus | Action |
|---|---|---:|---|
| HerbertHe/iptv-sources | TypeScript generator, no M3U in the repo | 0 directly | Evaluated its 21 upstreams instead; one added as a discovery candidate |
| iptvcat.net (US + index) | HTML catalogue, per-channel wrapper playlists only | 0 usable | Added as a reference check (visibility), not a source |
| i.mjh.nz | EPG host + a small NZ/AU generated playlist | likely some | Playlist added as a discovery candidate; guides already wired |
| doms9 `M3U8/base.m3u8` | 178-link subset of the already-configured `TV.m3u8` | **0 of 178** | Documented and rejected; `sources.json` note added |

The honest headline: **four of the five sources add nothing that the existing
20-source pipeline does not already have.** The one real opportunity is
`i.mjh.nz`, and it is an Oceania gap fill, not a US one.

## 1. HerbertHe/iptv-sources

A Node/TypeScript project, not a playlist repository: the recursive tree has 80
blobs and **zero `.m3u` files**. It reads 21 upstream playlist URLs
(`src/sources/*.ts`), rewrites them, and publishes the output to GitHub Pages at
`https://m3u.ibert.me/` (`o_all.m3u` 10,281 entries, `o_cn.m3u` 155,
`o_s_cn.m3u` 350, `cn.m3u` 165, `all.m3u` 800).

So the useful question is not "what is in this repo" but "what are its upstreams,
and is any of them a source PremiumTV does not already have". All 21 were
downloaded and diffed:

| Upstream | Entries | What it carries | Result |
|---|---:|---|---|
| `iptv-org` index / `cn*` | — | already configured | duplicate — 0 new |
| `fanmingming/live` | — | already a discovery candidate (rejected 2026-11-01 at 0/0 sample) | duplicate |
| `YueChan/Live` `IPTV.m3u` | 96 | all `rtp://239.3.1.*` multicast | unusable — not routable off-LAN |
| `YanG-1989/m3u` `Gather.m3u` | 123 | 80 `cdn.ttvb.eu.org` esports restreams + 42 Migu + 1 misc | **123 new URLs** → discovery candidate |
| `YanG-1989/m3u` `Migu.m3u` | 43 | 42 China Mobile Migu streams | subset of the above risk, not added separately |
| `qwerttvv/Beijing-IPTV` ×4 | 135 each | `http://192.168.123.1:23234/rtp/...` | unusable — private LAN |
| `joevess/IPTV` | 8 bytes | `#EXTM3U` header only | dead upstream |
| `cymz6/AutoIPTV-Hotel` | — | repository returns 404, deleted/renamed | dead upstream |
| `epg.pw` ×5 | — | China guides; `epg.pw` already in `epg_sources.fixed` | duplicate |

Two upstreams are structurally unusable for this project, not merely low value:
`rtp://` multicast (the scraper already classifies `rtp` as non-HTTP) and
`192.168.x.x` LAN addresses can never answer a public HTTP probe, so importing
them would add hundreds of guaranteed-dead rows to every run's failure count and
drag the published-strength number down for no viewer benefit.

`YanG-1989/m3u` is the only genuine addition. It is not general television
(CCTV/China channels are already covered many times over); it is a proxy layer
for China Mobile's Migu sports and movie-rotation tiers plus esports livestreams
of Bilibili/Huya/Douyu. All 123 URLs are new to the corpus. It was added as a
**discovery candidate, not a source**, because the value depends entirely on
whether those proxies answer from outside China — which the sample check will
answer honestly and this audit cannot.

## 2. iptvcat.net — US pages and the `home_7` index

`home_7` is the same index as `home_22`: **14,018 channels worldwide, 13,716
online, 302 offline**, by country/region. The US slice is 1,621 total, 1,593
online, 28 offline, across 5 pages.

The blocking problem is delivery, and it was checked rather than assumed:

- Every row's download link is a **single-channel** wrapper playlist:
  `https://list.iptvcat.net/my_list/s/<32-hex>.m3u8`. Fetching one
  (`30A Georgia Hollywood Review TV`) returned exactly one entry:
  `https://30a-tv.com/gh.m3u8?checkedby:iptvcat.net`.
- The site's "Download this list" / "Add to list" actions are built client-side
  from a session-scoped list. There is **no static country or bulk M3U URL** —
  confirmed by inspecting the page source and by search, matching the earlier
  finding recorded in this repo.
- Every stream URL carries a `?checkedby:iptvcat.net` query marker that has to be
  stripped before any dedupe, or the whole catalogue reads as "new".

So a real import would mean fetching 5 HTML pages, resolving ~1,600 hash
wrappers one at a time, and stripping the marker — ~1,600 extra fetches per run
to land at a catalogue that is **smaller than what is already published**: 1,621
US vs ~2,900 published US, 14,018 worldwide vs 19,621 in the corpus. The
spot-check confirms the direction: `30a-tv.com` appears 16 times in
`PremiumTV_all.m3u` (14 published), including the `gh.m3u8` path without the
marker, so this catalogue's content is already arriving through existing
sources.

Action taken: added as **`iptvcat` reference check** (reachability + visibility,
never imported), with the delivery limitation and the size comparison written
into its note so the next person does not repeat the 5-page investigation.

## 3. i.mjh.nz

An Apache directory index over matthuisman's generators. The distinction that
matters here is guide vs playlist:

- **Provider folders** (`PlutoTV/`, `SamsungTVPlus/`, `Plex/`, `Roku/`, `MeTV/`,
  `PBS/`, …) contain **XMLTV only** — e.g. `PlutoTV/us.xml.gz` 986 KB,
  `SamsungTVPlus/us.xml.gz` 521 KB, `Plex/us.xml.gz` 2.9 MB. There is no M3U in
  them and the `matthuisman/i.mjh.nz` repo tree has zero `.m3u` files, so there
  is nothing to scrape for streams there.
- **The guides are already wired**: `epg_sources.fixed` in this repo already
  lists matthuisman's PlutoTV US and SamsungTVPlus US XML, so that half of this
  source is fully exploited.
- **`all/raw-tv.m3u8`** (114,617 B) and **`world/raw-tv.m3u8`** (1,490 B) are the
  only playlists. They are New Zealand/Australia linear feeds — Sky NZ, Mood,
  Three, Bravo, Whakaata Māori, Sky Open, RUSH, Warner Bros FAST — served
  through the `https://i.mjh.nz/.r/` redirector, generally with an Apple TV
  user-agent.

That is a real gap, not a duplicate: the published lineup has **2 Oceania
entries (plus 1 backup)** and **15 Australian (plus 1 backup**, with 32 in the
`Australia` country playlist), and only **4 `mjh-` tvg-ids** are in the corpus
at all. Action taken: added **`matthuisman-mjh` as a discovery
candidate**, with the user-agent caveat written into the note, so the monthly
engine sample-checks it and promotes it only if the redirector actually answers.

## 4. doms9 `M3U8/base.m3u8`

Fully diffed. The file is 178 entries — a US-heavy curated subset with
tokenised `cdnlivetv.tv` URLs and `23.237.104.106:8080/USA_*` feeds — and is a
different file from the `TV.m3u8` (573 entries) already configured as the
`doms9` source.

Result: **178 of 178 URLs are already in `TV.m3u8` and in
`PremiumTV_all.m3u`; 0 new URLs.** 176 of the 178 `tvg-id`s are already in the
corpus. Only 5 normalised names are absent (Bravo TV, Crime & Investigation
Network, E! Entertainment, Fox Sports 1, Turner Classic Movies) — name variants
of channels that are already carried, not missing channels. Configuring
`base.m3u8` as a second source would add zero links and double-fetch a strict
subset of what the `doms9` source already delivers. Action taken: **not
configured**; a note was added to the `doms9` entry in `sources.json` recording
the measurement so the question is closed rather than re-opened.

## What changed in the repository

- `sources.json`
  - `doms9` — note recording that `base.m3u8` is a 178/178 duplicate subset.
  - `reference_checks` — new `iptvcat` entry (reachability only, never imported).
  - `discovery.candidates` — new `matthuisman-mjh` (`i.mjh.nz/all/raw-tv.m3u8`)
    and `YanG-Gather` (`YanG-1989/m3u`), each with the reason it is a candidate
    rather than a source.
- This document.

No playlist, guide or generated file was touched, no source was force-imported,
and the published lineup is unchanged by this hunt. The two new candidates reach
`playlists/discovery/approved-sources.json` only if the monthly engine's sample
check passes them, exactly like every other candidate.

## What this says about overall development

The audit's real finding is that **source discovery has hit diminishing returns
and the constraint has moved**. Twenty sources already yield 19,621 unique links
and 13,340 published channels; four of five hand-picked external sources added
nothing. The bottleneck is no longer "find more lists":

1. **Quality, not count.** 63.8% reachable overall (12,525 of 19,621) is the
   number that decides what a viewer sees. The biggest single group of
   unverified links is HTTP 403 (bot-blocked pirate sports hosts) — a
   *verification* problem that more sources make worse, not better.
2. **Weak sources cost real work.** `xtemus` returned 31 working of 317 (under
   10%) and `aria-plus` 474 of 1,983. Each keeps failing daily, inflating every
   run's failure list. Pruning or replacing them is worth more than adding a
   twenty-first source.
3. **Guide coverage is the visible gap, not channel count.** ~20.6% of
   `tvg-id`s in the US lineup have real programme data. `i.mjh.nz` matters far
   more as the guide host already in use than as a playlist source — which is
   why the playlist half is a *candidate* and the guide half was already wired.
4. **Regional thinness is real but narrow.** A 2-entry Oceania section and
   15 primary Australian channels are genuine holes; that is what the `i.mjh.nz` and
   `YanG` candidates address. Most other regions are already well covered.
5. **The pipeline sorts itself out.** Every finding above was decideable from
   the corpus diff plus one sample fetch. That is the right shape: the useful
   work now is keeping the corpus honest and the guides matched, not collecting
   more entry points.
