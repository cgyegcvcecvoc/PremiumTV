# Source hunt — 2026-11-25 (iptv-org `awesome-iptv` → Providers)

## Scope and method

The starting point was
<https://github.com/iptv-org/awesome-iptv/discussions/categories/providers>, read
through the GitHub GraphQL API rather than by eye: **149 discussions** in the
category, **86 of them labelled `Free`**, plus every pinned announcement. Each
free provider's own link was then opened - a repository tree read through the
API, or the site itself read through a page fetcher - and its playlists diffed
against this repository's own corpus.

Baseline: the corpus published by the **2026-11-25 09:58 UTC recheck** - 19,473
unique links, 13,347 published entries, 186 countries, and 24 sources in the run
(20 configured in `sources.json` plus 4 discovery-promoted ones).

Two limits are stated up front, because they are what the numbers below can and
cannot say:

- **No stream was played and no link was probed in this audit.** The sandbox
  reaches `github.com`/`api.github.com` only; raw files were read through the
  GitHub API and web pages through a page fetcher. Where a table says "new
  links" it is an URL-set difference against `playlists/PremiumTV_all.m3u`, not
  a promise those links answer. The scrape that follows is what decides.
- **Guide-only and paid listings were not considered importable.** A provider
  that sells subscriptions (Zorba, TryIPTV, Pillow, OrvenTV, Xtreme HD, Apollo,
  and the 40+ `Paid` records) publishes no static playlist to import, and a
  provider that publishes only XMLTV belongs in `epg_sources`, not `sources`.

## Verdict at a glance

| Provider (discussion) | What it actually is | Measured 2026-11-25 | Action |
|---|---|---|---|
| **M3UPT** [#656](https://github.com/iptv-org/awesome-iptv/discussions/656) | Portuguese playlist of public, official streams, GitHub-backed | 944 entries; TV group 159 (154 HTTPS), **71 new URLs**, 115 new tvg-ids | **added as `m3upt`** (`include_groups: ["TV"]`) |
| **TDTChannels** [#652](https://github.com/iptv-org/awesome-iptv/discussions/652) | Spanish TDT catalogue, 1.7k-star repo, stable list URLs | national/regional/local channels, several feeds each, `.TV` tvg-ids, own XMLTV | **added as `tdtchannels`** |
| **Nexonic IPTV** [#880](https://github.com/iptv-org/awesome-iptv/discussions/880) | Free-to-air playlists verified upstream 3×/day, CC0 data | 4,458 entries / 160 countries; **487 new URLs** (IN 169, US 58, RU 49) | **added as `nexonic-iptv`** |
| BuddyChewChew/pluto [#806](https://github.com/iptv-org/awesome-iptv/discussions/806) | Pluto TV M3U with session tokens | 459 entries, **2 new channel ids**; every URL is a per-session JWT | rejected (kept out) |
| FreeIPTV [#657](https://github.com/iptv-org/awesome-iptv/discussions/657) | "30,000+ channels", account gate | landing page unlocks a 24-hour account; **no static playlist** | rejected |
| Free-TV IPTV [#667](https://github.com/iptv-org/awesome-iptv/discussions/667) | Web front-end over iptv-org | community comment and page agree it is iptv-org | rejected (duplicate) |
| Grade TV [#769](https://github.com/iptv-org/awesome-iptv/discussions/769) | Browser catalogue + M3U export | ids are iptv-org ids (`00sReplay.us`, `3ABNEnglish.us`) | reference check only |
| Broadcast Atlas [#845](https://github.com/iptv-org/awesome-iptv/discussions/845) | Directory/player on iptv-org data | "each channel keeps its IPTV-org identifier" | reference check only |
| Open TV Atlas [#968](https://github.com/iptv-org/awesome-iptv/discussions/968) | Generator of iptv-org slices | every URL it can emit already arrives via `iptv-org` | reference check only |
| TV Explorer [#668](https://github.com/iptv-org/awesome-iptv/discussions/668) | Web player | page states the list comes from `iptv-org/iptv` | rejected (duplicate) |
| Globe TV [#659](https://github.com/iptv-org/awesome-iptv/discussions/659) | 839 channels + webcams + radio | YouTube thumbnails and embeds, no playlist | rejected |
| GlobeNow.tv [#868](https://github.com/iptv-org/awesome-iptv/discussions/868) | 647 channels on a globe | "using each broadcaster's official YouTube live stream" | rejected |
| FreeTV Garden [#724](https://github.com/iptv-org/awesome-iptv/discussions/724), FreeTV [#665](https://github.com/iptv-org/awesome-iptv/discussions/665), FluxCast [#662](https://github.com/iptv-org/awesome-iptv/discussions/662), Global Free TV [#639](https://github.com/iptv-org/awesome-iptv/discussions/639), CloudTVE [#658](https://github.com/iptv-org/awesome-iptv/discussions/658), Famelack [#663](https://github.com/iptv-org/awesome-iptv/discussions/663), TV Run [#660](https://github.com/iptv-org/awesome-iptv/discussions/660), EBK IPTV [#666](https://github.com/iptv-org/awesome-iptv/discussions/666), CineVid [#931](https://github.com/iptv-org/awesome-iptv/discussions/931), GDPlayer [#866](https://github.com/iptv-org/awesome-iptv/discussions/866) | Web players / app landing pages | no published M3U; several are iptv-org front-ends | rejected |
| Easy Web TV [#654](https://github.com/iptv-org/awesome-iptv/discussions/654), IPTVCat [#669](https://github.com/iptv-org/awesome-iptv/discussions/669), eja.tv [#763](https://github.com/iptv-org/awesome-iptv/discussions/763), xyzstreams [#856](https://github.com/iptv-org/awesome-iptv/discussions/856) | Already known here | tracked in `reference_checks` (or via `EJA_M3U_URL`) | no change |
| Free-TV/IPTV [#664](https://github.com/iptv-org/awesome-iptv/discussions/664), i.mjh.nz [#692](https://github.com/iptv-org/awesome-iptv/discussions/692) | Already configured | `free-tv` source, `matthuisman-mjh` discovery candidate | no change |
| FAST services: Pluto [#1021](https://github.com/iptv-org/awesome-iptv/discussions/1021), Tubi [#1022](https://github.com/iptv-org/awesome-iptv/discussions/1022), Samsung TV Plus [#1019](https://github.com/iptv-org/awesome-iptv/discussions/1019), Roku [#1023](https://github.com/iptv-org/awesome-iptv/discussions/1023), Plex [#1020](https://github.com/iptv-org/awesome-iptv/discussions/1020), Xumo [#1033](https://github.com/iptv-org/awesome-iptv/discussions/1033), STIRR [#1035](https://github.com/iptv-org/awesome-iptv/discussions/1035), LG Channels [#1026](https://github.com/iptv-org/awesome-iptv/discussions/1026), Vizio [#1027](https://github.com/iptv-org/awesome-iptv/discussions/1027), Google TV [#1028](https://github.com/iptv-org/awesome-iptv/discussions/1028), TCLtv+ [#1029](https://github.com/iptv-org/awesome-iptv/discussions/1029), Fawesome [#1031](https://github.com/iptv-org/awesome-iptv/discussions/1031), FilmRise [#1030](https://github.com/iptv-org/awesome-iptv/discussions/1030), Local Now [#1032](https://github.com/iptv-org/awesome-iptv/discussions/1032), Haystack [#1036](https://github.com/iptv-org/awesome-iptv/discussions/1036), ABEMA [#1047](https://github.com/iptv-org/awesome-iptv/discussions/1047) | Free ad-supported services | one record each, no playlist endpoint; `pluto-us` already carries Pluto and the XMLTV halves are wired | no new source |
| Guide-only: IPTV-EPG.org [#698](https://github.com/iptv-org/awesome-iptv/discussions/698), Open EPG [#697](https://github.com/iptv-org/awesome-iptv/discussions/697), EPGSHARE01 [#696](https://github.com/iptv-org/awesome-iptv/discussions/696), EPG.pw [#695](https://github.com/iptv-org/awesome-iptv/discussions/695), deepepg [#694](https://github.com/iptv-org/awesome-iptv/discussions/694), EPG TV XML [#877](https://github.com/iptv-org/awesome-iptv/discussions/877) | XMLTV providers | `epg.pw`, `iptv-epg.org` and Open EPG are already in `epg_sources` | no change |

## The three additions

### 1. `m3upt` — Portuguese public broadcasters

The file is `M3U/M3UPT.m3u` in <https://github.com/LITUATUI/M3UPT>, also served
as <https://m3upt.com/iptv>; the site and the repository are the same playlist.
It is *not* only television:

| Group in the file | Entries | What it is |
|---|---:|---|
| `TV` | 159 | linear channels - the part that belongs in a TV playlist |
| `Beachcam` | 194 | beach cameras |
| `PCNELID`, `Eixo do Mal`, `IEGCQT`, `O Planeta Vivo`, `100 ou Mais` | 290 | podcast/programme episodes (`media="true"`) |
| `Rádios` | 85 | radio (`radio="true"`) |
| `DRM test` | 6 | DRM test cards |

Measured on the TV group alone: **159 entries, 159 unique URLs, 154 HTTPS, 71
URLs new to this corpus, 115 tvg-ids it does not carry** - the `.pt` public
service (RTP 1/2/Notícias/Memória/Açores/Madeira/África/Mundo, SIC, SIC
Notícias, TVI, TVI Internacional, V+ TVI, CNN Portugal) plus international
public broadcasters with correct iptv-org-style ids (`DW.de@Espanol`,
`AlJazeera.qa`, `AfricanewsEnglish.fr`, `3CatInfo.es`). The 71 new URLs include
4 DASH (`.mpd`) manifests and 4 plain-HTTP feeds. Its header advertises two
XMLTV guides, and several streams need the `#EXTVLCOPT` Referer/Origin lines the
file ships - both already handled by the scraper (`Channel.headers()`).

Importing the whole file would have put 575 non-television entries into the
player playlist. That is the reason this hunt added `include_groups` support to
M3U sources: `"include_groups": ["TV"]` keeps the television half and the run
report records exactly what was dropped
(`group_filter_removed`, `group_filter_groups`).

### 2. `tdtchannels` — Spanish TDT

<https://www.tdtchannels.com/lists/tv.m3u> (and the identical `.m3u8`, which is
the mirror). The list was opened and parsed by hand: national channels (La 1,
La 2, Cuatro, Telecinco, TRECE, El Toro TV), the information block (24h,
3CatInfo, Euronews, El País, El Confidencial, Negocios TV), sport
(Teledeporte, Esport3, ETB Deportes) and then the regional and local stations,
each channel with several feeds - its own CDN, GEO variants and OTTera
ad-stitched variants - plus `#EXTVLCOPT` Referer lines where a broadcaster needs
one. The project also publishes `tv.json`, `tv_mpd.m3u8` and its own XMLTV
(<https://www.tdtchannels.com/epg/TV.xml.gz>).

Spain is already one of the better-covered countries (363 entries in the
corpus), so this is a *quality* import, not a volume one: it brings the project's
own `.TV` guide ids and its curated set of feeds for the same stations. Dead GEO
variants are dropped by the same check as every other source, and the run report
shows how many of its feeds answered.

### 3. `nexonic-iptv` — verified free-to-air, worldwide

The discussion links `Shahrukhalid/nexonic-iptv`, which now redirects to
<https://github.com/nexonic-technologies/nexonic-iptv>. Only
`playlists/all.m3u` is configured; the repository's `community/untested.m3u`
file is deliberately left out, because an unchecked queue is exactly what this
pipeline's own link check would have to redo.

Measured: **4,458 entries across 160 countries, 487 URLs new to this corpus.**
The gaps it fills, by count of new links: India 169, United States 58, Russia 49,
Peru 16, Vietnam 16, France 15, Spain 14, Italy 11, UK 10, Colombia 9,
Chile 8, Bolivia 7 - then a long tail. Upstream verifies streams three times a
day, excludes adult channels, and publishes code under MIT and data under CC0.

### The one that looked best and was still rejected

`BuddyChewChew/pluto` (8 upvotes, `[TV,EPG,Free]`) is an automatically updated
Pluto TV playlist with HD forcing and country grouping. Measured against the
corpus: **459 entries, 459 URLs "new" - but only 2 channel ids that the corpus
does not already carry.** Every URL is a per-session `ipv4.pluto.tv` stitcher
address carrying a signed JWT, session ID and client ID, so a scrape would
import 459 expiring addresses for channels already published from `pluto-us`
(whose own 458 entries show `alive 0` in the current report because those tokens
expire between runs). Adding it would double the Pluto rows, add churn, and
publish tokens that stop working - so it was **not** configured. The measurement
is recorded here so the question does not have to be re-opened.

## What this says about the provider directory

1. **The valuable entries are repositories, not websites.** All three additions
   publish a static file that a regenerator can fetch; the 20+ web players in the
   category are front-ends over iptv-org (several say so explicitly) and cannot
   be imported without scraping HTML that is not a playlist.
2. **Derivative catalogues are the majority.** Grade TV, Broadcast Atlas, Open TV
   Atlas, TV Explorer and Free-TV IPTV all re-publish iptv-org data with
   iptv-org ids. Importing any of them would re-fetch what `iptv-org` already
   delivers and inflate duplicate counts; they are tracked as reference checks
   instead, so their availability is still visible in the daily report.
3. **Mixed-purpose files need a filter.** M3UPT is a good source wrapped in
   radio, cameras and podcast episodes. A source-level `include_groups` /
   `exclude_groups` is the smallest honest way to take the TV half; guessing from
   names would have been the other option, and the worst one.
4. **Session-token feeds are not sources.** Pluto-style stitcher URLs are signed
   per session. A playlist of them is a snapshot of one machine's tokens, not a
   channel list - the same conclusion the 2026-10-13 deep check reached about
   variant URLs.

## What changed in the repository

- `sources.json`
  - `m3upt` (GitHub primary, `m3upt.com/iptv` and jsDelivr mirrors,
    `include_groups: ["TV"]`), `tdtchannels` (`.m3u` + `.m3u8`),
    `nexonic-iptv` (raw, Pages and jsDelivr addresses), each with the
    measurement in its note.
  - `reference_checks`: `gradetv`, `broadcast-atlas`, `open-tv-atlas` -
    reachability only, never imported.
- `scripts/scraper.py` — `filter_source_groups()`: M3U sources honour
  `include_groups` (exact) and `exclude_groups` (substring), the same two keys
  W3U sources already used. The run report records `group_filter_removed` and
  `group_filter_groups`, so a filtered source can never look like a source that
  shrank on its own.
- `tests/test_scraper.py` — the filter's behaviour on a mixed file (television
  kept, radio/camera/podcast/DRM dropped, no-group handling, substring exclude)
  and the configuration of the three new sources (declared filter, HTTPS,
  note, mirror).
- This document, and a link to it in `README.md`.

## Follow-ups this hunt did not do

- **Guides for the new sources.** M3UPT's XMLTV is `.xz` and TDTChannels'
  is `.gz` of a different id namespace (`La1.TV`); neither is wired. Wiring the
  TDTChannels guide would raise Spanish programme coverage, and it needs the
  `.xz` reader added first for M3UPT.
- **A periodic re-read of the provider directory.** The category grows by a few
  records a week; the cheap check is "does a new record link a repository with
  `.m3u` files", which is exactly what `scripts/discover.py` already does for
  GitHub - pointing its query list at this category is not possible through the
  API, so this stays a manual pass.
- **Pruning, not adding.** `xtemus` (31 alive of 317) and `aria-plus` (468 of
  2,039) remain the weakest configured sources; replacing them is worth more
  than a twenty-fourth source.
