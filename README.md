# PremiumTV1

A playlist builder for publicly listed TV streams. The scraper combines enabled sources, removes duplicate URLs, checks HTTP streams, and publishes the checked player playlist when the run passes its safety threshold.

**➡️ [Download site](https://cgyegcvcecvoc.github.io/PremiumTV1/)** — app installers (Android TV / Fire TV / macOS), the best working M3U playlist for **your** country, and the change log ([Atom feed](https://cgyegcvcecvoc.github.io/PremiumTV1/data/feed.xml)) — live at [`cgyegcvcecvoc.github.io/PremiumTV1`](https://cgyegcvcecvoc.github.io/PremiumTV1/) from [`docs/`](docs/README.md).

## Website hosting — automatic, no uploads

Use **[GitHub Pages](https://cgyegcvcecvoc.github.io/PremiumTV1/)** instead of the old Netlify Drop copy. The **[full download hub](https://cgyegcvcecvoc.github.io/PremiumTV1/hub/)** is built by the same Pages workflow. Hosting is free for this public repository. Changes to website code, published playlists/categories, guides and releases on `main` rebuild the site; completed automated data workflows rebuild it too (bot pushes alone do not trigger GitHub Actions). Feature-branch work must be merged before it changes the public site.

See [hosting instructions](hub/DEPLOY.md). Netlify Drop uploads are snapshots and do not follow GitHub pushes.

The download site's **Channels** section previews the current lineup — the number
of unique channels and backup feeds, categories and countries, quality labels,
familiar names, and a searchable category grid — and is generated from
`playlists/PremiumTV.m3u` by `scripts/build_site_data.py`, so the page cannot
advertise a channel the playlist does not carry.

## Change log

- [Detailed, editable change log (Google Doc)](https://docs.google.com/document/d/1anjXfhv6qXz9ZsSldHBMqsfDt8d44W8N_ayqYAloeNM/edit?usp=drivesdk) — historical PR milestones, all 79 run-history records available in the current snapshot, stream-health policy, and known limitations.
- [Repository change log](CHANGELOG.md) — concise GitHub copy and links to the live health reports.

## Load the playlist

Load this URL in an M3U-compatible player (VLC, TiviMate, IPTV Smarters, Kodi PVR IPTV Simple, etc.):

```text
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/PremiumTV.m3u
```

> **Public links.** Checked on 2026-10-15: `PremiumTV1` is a public repository, so the
> `raw.githubusercontent.com` playlist URLs and each playlist's `x-tvg-url` guide URLs load in
> any IPTV player without an account, and the apps' automatic refreshes can download them.

| File | Purpose |
|---|---|
| [`playlists/PremiumTV.m3u`](playlists/PremiumTV.m3u) | Confirmed working links from the latest successful checked run. |
| [`playlists/categories/`](playlists/categories/README.md) | The same channels split into one playlist per category — `Sports.m3u`, `Cartoons.m3u`, `PBS.m3u`, `Game_Shows.m3u`, `Fox_Channels.m3u`, … each with its own `*_Backups.m3u`. |
| [`playlists/checks/CATEGORIES.md`](playlists/checks/CATEGORIES.md) | Category audit: the published group order, how many channels each holds, and which ones have guide data. |
| [`categories/`](categories/README.md) | **The category shelf to point a player at:** [`categories/USA.m3u`](categories/USA.m3u) (every US channel, grouped by category and sorted), [`categories/USA/`](categories/USA) (one file per US category) and [`categories/All/`](categories/All) (one file per category for the whole library). |
| [`playlists/countries/`](playlists/countries/README.md) | Confirmed working playlists separated by country (`USA.m3u`, `China.m3u`, `UK.m3u`, `Canada.m3u`, `India.m3u`, etc.). |
| [`playlists/AE_Channels.m3u`](playlists/AE_Channels.m3u) | Dedicated playlist of confirmed working A&E and A+E Networks channels (linear & FAST). |
| [`playlists/PremiumTV_all.m3u`](playlists/PremiumTV_all.m3u) | All unique links found, including dead or unverified links. |
| [`playlists/STATUS.md`](playlists/STATUS.md) | Latest run outcome, source counts, country counts, A&E status, additions/removals, and diagnostics. |
| [`playlists/logs/scrape-log.txt`](playlists/logs/scrape-log.txt) | Complete plain-text (`.txt`) run report with source stats, A&E channels, country counts, and log edits. |
| [`playlists/logs/log-edits.txt`](playlists/logs/log-edits.txt) | Chronological plain-text (`.txt`) log of playlist edits (`+added` / `-removed` channels) and issues across runs. |
| [`playlists/logs/errors.txt`](playlists/logs/errors.txt) | Plain-text (`.txt`) error breakdown, source/run issues, and dead/unverified links. |
| [`playlists/logs/run-history.txt`](playlists/logs/run-history.txt) | Plain-text (`.txt`) tabular summary of all recorded runs. |
| [`playlists/report.json`](playlists/report.json) | Detailed latest JSON report, including failed sources, country counts, A&E channels, and dead/unverified URLs. |
| [`playlists/checks/LINK-CHECK.md`](playlists/checks/LINK-CHECK.md) | Nightly deep check: which published links are working, offline, unreachable, blocked, and what was patched out. |
| [`playlists/checks/CLEANUP.md`](playlists/checks/CLEANUP.md) | Biweekly repository housekeeping: logs trimmed, orphans removed, and whether every published artifact is actually current. |
| [`playlists/checks/LINK-CHECK-ARCHIVES.md`](playlists/checks/LINK-CHECK-ARCHIVES.md) | Biweekly deep check of the 218 playlists no daily run patches (priority, per-category, `categories/` shelf, source copies). |
| [`playlists/checks/VERIFY.md`](playlists/checks/VERIFY.md) | Offline verification of every playlist: the published categories and order, links the deep check called dead, header guide counts, and per-playlist EPG coverage. |
| [`playlists/checks/EPG-CHECK.md`](playlists/checks/EPG-CHECK.md) | Last remote EPG URL/status check (nightly); the checked-in snapshot predates the root-guide migration, while current country XML coverage is in EPG-BUILD. |
| [`EPG/PremiumTV.xml`](EPG/PremiumTV.xml) | **One merged, filtered XMLTV guide** for the whole library — load this `.xml` in an IPTV player. |
| [`EPG/`](EPG/README.md) | Separate, verified `.xml` EPG per country playlist (`EPG/USA.xml`, `EPG/UK.xml`, etc.). Each country M3U advertises only its own guide. |
| [`EPG/PremiumTV.xml.gz`](EPG/PremiumTV.xml.gz) | Gzipped copy of the all-country guide (for players that accept `.xml.gz`). |
| [`playlists/checks/EPG-BUILD.md`](playlists/checks/EPG-BUILD.md) | Guide build report: verified source guides, per-country channel/programme coverage, XML sizes and validation results. |
| [`playlists/checks/CHANNEL-HUNT.md`](playlists/checks/CHANNEL-HUNT.md) | Priority-channel hunt: every candidate found for Nickelodeon, NickToons, MeTV and MeTV Toons, and which ones actually played. |
| [`playlists/Priority_Channels.m3u`](playlists/Priority_Channels.m3u) | Ready-to-load playlist with only the verified priority channels (Nickelodeon, NickToons, MeTV, MeTV Toons, NFL Network, NFL RedZone) and the same guides as the main playlist. |
| [`playlists/run-history.jsonl`](playlists/run-history.jsonl) | Append-only, one-record-per-run history for regular checks, rechecks, final checks, and manual runs. |
| [`playlists/discovery/REPORT.md`](playlists/discovery/REPORT.md) | Latest monthly new-channel hunt: candidates, scores, verdicts, and promotions. |
| [`playlists/discovery/approved-sources.json`](playlists/discovery/approved-sources.json) | Sources vetted by monthly discovery and merged into the next regular scrape. |
| [`playlists/discovery/new-channels.m3u`](playlists/discovery/new-channels.m3u) | New working links found by the last monthly run, ready to try in a player. |
| `playlists/sources/*.m3u` | Normalized copies used as fallback caches when an upstream source is unavailable. |
| [`playlists/logs/resort-log.txt`](playlists/logs/resort-log.txt) | Result of the last `scripts/resort_playlists.py` run: what was re-sorted and which links were pruned. |

## PremiumTV apps and release channels

PremiumTV ships a native Android TV app and a macOS app. Release builds share
the same data scope and version policy:

| Channel | Version | Library | Release status |
|---|---|---|---|
| **Stable release** | **1.0.8 V1 Patch** `1.0.8.1` (Android `versionCode 100080001`) | USA lineup + USA guide | Default and only download; installs over every earlier build from Settings → App updates. Same 1.0.8 look plus V1 fixes: animated loading screen, hardened bug detection (patch chain, stream hygiene, guide freshness, library health) |
| Compatibility build | **1.0.9** (Android `versionCode 100090000`) | USA lineup + USA guide | Identical to 1.0.8.1, published so 1.0.4–1.0.6 can see and install it from Settings → App updates (V1's alias, like 1.0.7 for 1.0.6.1) |
| Previous stable | **1.0.8** (Android `versionCode 100080000`) | USA lineup + USA guide | Superseded by V1 Patch; installs in place over every earlier build |
| Archived stable | 1.0.4 / 1.0.5 / 1.0.6 / 1.0.6.1 / 1.0.7 | USA lineup + USA guide | Older builds warn to update; support for builds below 1.0.8 V1 ends Nov 19, 2026 |
| Next (in source) | **1.0.8 V1 Patch** `1.0.8.1` (Android `versionCode 100080001`) | USA lineup + USA guide | Marked as the default build version in source. Sets the V patch series in stone: V2=1.0.8.2, V3=1.0.8.3 … each V increments versionCode by 1 ([notes](release-notes-1.0.8.1.md)) |

The **1.1.0/1.1.1 Encore preview channel is retired**. Its release, installers
and download links were removed (old release-asset URLs now 404); every
retired-preview pointer the project controls, including the startup notice,
goes to the [blocked-build page](docs/blocked/index.html). A 1.1.1 install
shows a **BUILD RETIRED** notice at startup; on Android, 1.0.6.1 installs
straight over it because `100060001` is above `100010001` and both APKs share
the update key.

Versions are `MAJOR.MINOR.PATCH` or `MAJOR.MINOR.PATCH.HOTFIX`: 1.0.6.1 was a
small stable increment, not a new minor release; 1.0.8 V1 Patch is **1.0.8.1**
and uses the same rule — each future V increments the fourth number
(1.0.8.1, 1.0.8.2 …) and its `versionCode` by one, so every V installs in place
and orders above the last. Builds shipped before 1.0.6.1 only understand
three-part versions, so the same code was also published as an alias:
**1.0.7** for 1.0.6.1, **1.0.9** for 1.0.8.1 (V1), 1.0.10 for V2 … That mapping
is how an old updater still finds a V patch. See
[`release-notes-1.0.8.1.md`](release-notes-1.0.8.1.md),
[`release-notes-1.0.8.md`](release-notes-1.0.8.md),
[`release-notes-1.0.6.1.md`](release-notes-1.0.6.1.md) and its
[1.0.7 compatibility note](release-notes-1.0.7.md).

### What 1.0.8 V1 Patch adds on top of 1.0.8

- **More animated loading screen.** The Android and macOS launch splashes now
  breathe: a gold haze that drifts, a breathing halo around the TV mark, a
  sweeping shimmer underline, a segmented progress bar with a racing shine, and
  animated dots that tell the viewer the app is not frozen. All motion is
  transform/opacity only so it stays smooth on TV hardware.
- **Better bug detection.** Settings → **Check for bugs** now runs 11 checks
  (was 7): it still verifies channel list, categories, guide, bundle, refresh,
  updates and version, but adds **Patch chain** (V ordering that this patch
  sets in stone: V1=1.0.8.1, V2=1.0.8.2 …), **Stream hygiene** (spaces/malformed
  URLs that fail on players), **Guide freshness** (window age in days) and
  **Library health** (empty categories, oversized groups that stress low-memory
  sticks).
- **V patch versioning, locked in.** 1.0.8.1 displays as **1.0.8 V1 Patch** —
  and every follow-up V increments the fourth number (`1.0.8.2` = V2,
  `1.0.8.3` = V3 …) with alias releases (`1.0.9`, `1.0.10` …) so 1.0.4–1.0.6
  updaters still find them. No playlist, scraper or guide logic changed.

### What 1.0.8 added

- **Categories as a sorted list, with category pages.** Every category list
  (download site, Mac sidebar, Android Channels tab) is one row per category
  with the count small on the right and a **Sort** control (Published order,
  A-Z, Z-A, biggest first). Clicking a category opens that category's own
  page — Android gets a full drill-in page with a back button and its own
  channel sort (playlist order, A-Z, Z-A, channel number); the Mac category
  view gets an explicit **◀ All categories** back button and the same chips.
- **The side player.** **⤢ Side player** (Android) / **⧉ Side player** (Mac)
  tucks the running stream into a corner card while the browser stays up —
  the stream never restarts across the flip. Clicking the corner picture
  grows it back to the big screen; the card's close button stops playback.
- **Live Events, revamped.** The tab has its own **⟳ Refresh live games**
  button, and every game is live-checked: the card's pill reads LIVE,
  CHECKING or NO SIGNAL, with the checked-live count in the subtitle.
  Two-team matchups show drawn team crests — the team's initials in colours
  derived from its name, so the same team always wears the same badge, fully
  offline. See [`release-notes-1.0.8.md`](release-notes-1.0.8.md) and the V1
  follow-up [`release-notes-1.0.8.1.md`](release-notes-1.0.8.1.md).

### What earlier 1.0.x releases added

- **Launch splash** — the PremiumTV television mark, a spinner and the build's
  version pinned at the bottom while the library loads.
- **Channel search** — one field above the Channels tab (Android; the Mac
  sidebar keeps its own) that filters by name, category, country or channel
  number.
- **Category placeholders** — a channel with no logo gets a drawn picture of
  its category (a ball for Sports, a smile for Comedy, a balloon for Kids,
  a television set for everything else) instead of bare initials.
- **Live Events tab** — the scrapers' live-game feeds, grouped by sport
  (Soccer, American Football, College Football, NHL Hockey, and the rest),
  each card showing the matchup and how many streams carry it.
- **Multi-server playback** — a game published on more than one stream, and
  a channel with backup feeds, switch to the next server automatically when
  one feed dies; the player says which server is playing.

### App updates (1.0.4 and later)

**1.0.4 is the last version that needs a manual download.** From it on,
Settings → App updates shows the newest published stable release above the
installed app, downloads that release's installer once, verifies it against the
release's SHA-256 file, and opens the platform installer. The check runs at
most once a day using GitHub's ETag; nothing is downloaded in the background,
and a downloaded installer is reused rather than fetched again. Only full
stable releases count — previews, drafts, older tags and releases whose
installers are still uploading are ignored. The release guard workflow marks a
stable release that is not above the current stable as a pre-release, so the
apps never see an out-of-order version. Full policy and the release process:
[`docs/UPDATES.md`](docs/UPDATES.md).

### macOS app

The macOS app packages the channels and guide inside a `.dmg` (drag to
Applications) and a `.pkg` (installer) for **macOS 12 (Monterey) and later**, on
Intel and Apple Silicon.

| Item | Where |
|---|---|
| Project and build docs | [`macos/`](macos/README.md) |
| Stable target | `1.0.8.1` / **1.0.8 V1 Patch** — USA lineup; every 1.0.4+ build installs it from Settings → App updates (alias `1.0.9` for old updaters) |
| Build workflow | [`.github/workflows/macos-build.yml`](.github/workflows/macos-build.yml) |

The macOS regression suite covers startup data delivery, the cable-style guide
(grid layout, category filter, keyboard movement, stale-download handling),
parser accuracy, duplicate-ID playback selection, and proxy session cleanup.
Electron 43 retains macOS 12 support. Builds are ad-hoc signed, not notarized;
first launch may require right-click → **Open** or clearing the quarantine
attribute.

### Android TV app

The Android app carries the playlists and guide **inside the APK** — nothing
to configure in a player, no M3U file to side-load. It installs on Android TV,
Google TV, Fire TV stick, tablet and phone.

| Item | Where |
|---|---|
| Project and build docs | [`android/`](android/README.md) |
| Stable build target | `1.0.8.1` — **1.0.8 V1 Patch** (`versionCode 100080001`) — USA library |
| Build workflow | [`.github/workflows/android-build.yml`](.github/workflows/android-build.yml) |

The stable build bundles the USA playlist and guide. Both are built from curated
per-country EPG feeds (see [the guide build report](playlists/checks/EPG-BUILD.md)).

- **Channels** — one row per category, in published order; each card shows its
  logo (or its category's drawn placeholder) and current programme when the
  guide has one, with a search field above the rows.
- **Guide** — what's on now across every channel with listings, live-game feeds
  included (with the matchup as their listing), plus the next programme.
- **Automatic refresh** — Android WorkManager checks after repository publishing
  windows, using ETag/Last-Modified where possible.
- **Settings** — one compact version card with **Force refresh**, **Check for
  update** and **Check for bugs**, plus collapsible details, reset to bundled
  data and the **App updates** panel (check, download once, install).
- **Update popup for older builds** — a build inside the version range published
  in [`app-update-notice.json`](app-update-notice.json) is told at startup to go
  and get the newest release from GitHub, and what is waiting when it does. It is
  dismissible, because a TV remote can arrive mid-evening, but the dismissal
  lasts one launch and is never persisted, so it comes back until PremiumTV is
  updated. The wording, the targeted versions and the end-of-support date are all
  published, so none of them needs a new build to change.

Playback is ExoPlayer (Media3), and the app sends the referrer, origin and
user-agent a playlist entry publishes when it has one. Some upstream streams can
still fail between health checks; confirmed failures should be removed from the
player playlists, while transient or geo-blocked errors stay distinguishable.

**1.0.8 V1 Patch (1.0.8.1) is the current stable release** (`versionCode 100080001`, USA scope; alias `1.0.9` with `100090000` for old updaters).
1.0.4 was the last version that needed a manual download: every later build
upgrades from Settings → App updates, and 1.0.8 V1 installs over 1.0.8 and the
retired 1.1.x previews as well. A release is offered only when it is a
published full release above the installed version with its platform installer
already attached. The download site promotes only a complete published stable
release and no longer publishes preview builds.

**Builds below 1.0.8 V1 have an end-of-support date.** 1.0.5/1.0.6 show the
popup directly and can finish the upgrade from Settings. 1.0.4 has the update
centre but predates the popup; its Settings still offers the newest release. 1.0.0–1.0.3
ship no updater at all — the `v1.0.3` tree has neither `AppUpdateManager.kt` nor
`updater.js` — so they can only be reached through the one playlist they
refresh, and they need one manual install to join the self-updating line. 1.0.0–1.0.3 have no such route, which is why the feed they refresh carries the
message for them — and it has carried it since the first warning, not only
since the freeze.
`scripts/legacy_sunset.py` splits delivery in two: current builds read
[`playlists/live/USA.m3u`](playlists/live/), and 1.0.0–1.0.4 keep reading
`playlists/countries/USA.m3u`. While support lasts the two are identical. On the
`support_ends_utc` date published in
[`app-update-notice.json`](app-update-notice.json) — 30 days after the first
warning — the legacy feed is pinned to the last scraped channel list with one
sanctioned notice entry on top, and stops receiving scrape updates. `python
scripts/legacy_sunset.py status` reports the phase and the days left. See
[`docs/UPDATES.md`](docs/UPDATES.md) and [`playlists/live/README.md`](playlists/live/README.md).

### Keeping the categories and the order honest

The taxonomy below is not only applied at scrape time: `scripts/link_check.py --patch`
re-groups and re-orders a playlist after it removes dead links, and two offline tools exist
for the hours a nightly run cannot be waited for (neither needs the network):

```bash
python scripts/resort_playlists.py --dry-run   # report what would move, file by file
python scripts/resort_playlists.py             # re-group, re-order, prune deep-checked-dead links
python scripts/resort_playlists.py --max-feeds 3   # keep at most 3 feeds per channel, best first
python scripts/verify_playlists.py --strict    # audit every published playlist and its guide
```

`resort_playlists.py` never edits a URL: every link in a file before the run is still in it
afterwards - only a link the last deep check confirmed dead (`offline`/`invalid`, or in the
quarantine) is dropped - so tidying a playlist cannot break it. Before an upstream group such
as `Italy 🇮🇹` is replaced by a category, the country it carried is written back as
`tvg-country`, so the next run resolves the same country and the same category again.

A re-publish also resolves a repeated URL — the same stream listed twice under two channel
names. `verify_playlists.py` calls that a structural fault, so `rebuild_playlists.py` and
`resort_playlists.py` now keep one entry per URL (`categorize.dedupe_urls`), preferring the name
the URL actually supports and carrying over any metadata the duplicate held. That is the fault
the deep check found in `playlists/Priority_Channels.m3u`, where one Brazilian stream was
published as both *NickToons Brasil* and *Nickelodeon (Brazil)*.

`verify_playlists.py` answers, per playlist: is every group-title one the taxonomy would have
written, is the file in the published order, does it publish a link the deep check called dead,
how many guides does its header make a player download, and how many of its `tvg-id` values does
the advertised guide actually declare - and schedule. The result is published as
[`playlists/checks/VERIFY.md`](playlists/checks/VERIFY.md), and all three scheduled workflows run
it with `--strict`, so a playlist that drifts out of the taxonomy fails the run instead of quietly
staying wrong.

### Country-separated playlists & A&E channels

Every checked run automatically classifies all confirmed working channels by country (`tvg-country`, `tvg-id` country suffix, and `group-title` / channel metadata) and writes a separate playlist per country in [`playlists/countries/`](playlists/countries/README.md), plus a dedicated A&E Networks playlist at [`playlists/AE_Channels.m3u`](playlists/AE_Channels.m3u):

```text
# USA channels only
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/countries/USA.m3u

# China channels only
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/countries/China.m3u

# UK channels only
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/countries/UK.m3u

# Canada channels only
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/countries/Canada.m3u

# A&E and A+E Networks channels only
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/AE_Channels.m3u
```

See [`playlists/countries/README.md`](playlists/countries/README.md) for the complete table of all ~170+ country playlists.

### Channel categories and the published order

Every published playlist uses one fixed taxonomy, defined in
[`scripts/categorize.py`](scripts/categorize.py). The order below is the order
the groups appear in the file — change `CURATED_CATEGORIES` there and every
playlist follows:

| # | Category | What goes in it |
|---|---|---|
| 1 | **Sports** | NFL Network, NFL RedZone, ESPN, FS1, CBS Sports, beIN, league and event feeds — identified by the channel, not by the group the index shipped it in. |
| 2 | **Lifestyle** | HGTV, Food Network, TLC, Travel, Hallmark, home/food/travel/outdoor channels. |
| 3 | **Fox Channels** | Fox, Fox News, Fox Business, Fox Weather, Fox Soul and the Fox local stations. |
| 4 | **CBS** | CBS, CBS News 24/7, the CBS local stations. |
| 5 | **NBC** | NBC, CNBC, MSNBC, Bravo, USA, Syfy, Telemundo and the NBC local stations. |
| 6 | **NBC Sports Channels** | NBC Sports, the NBC Sports regional feeds, Golf Channel. |
| 7 | **Cartoons** | Cartoon Network, Boomerang, Adult Swim, Nicktoons, MeTV Toons, animation channels. |
| 8 | **PBS** | PBS, PBS Kids, PBS member stations. |
| 9 | **Game Shows** | Game Show Network, Buzzr, Family Feud, The Price Is Right. |
| — | **`<category> Backups`** | Every category is followed by its own backup group. A channel keeps one main link; the spare links that were previously scattered through the listing are named `… (Backup 1)`, `… (Backup 2)` and moved into that group, so a dead link has somewhere to fail over to. |
| — | *(then the rest)* | Music, News, Movies, Religious, Entertainment, Documentary, Kids, … sorted by size, with `Other` last. |

Two rules keep the listing usable:

* **the channel name decides the category**, not the group-title the public
  index happened to publish. That is why NFL Network is in Sports instead of the
  `TV` bucket it arrived in, and why 1647 `General` / 872 `Undefined` entries are
  gone;
* **when this index calls a channel `General` and three others call it `Music`,
  Music wins** — cross-source voting in `categorize.build_group_votes()`.

Anything still unidentifiable lands in a world region (`Europe`, `Asia`, …) or
in `Other`, and the whole library is kept — nothing is dropped to make the
category list short.

### The `categories/` shelf

[`categories/`](categories/README.md) is the folder a player is pointed at when the whole
playlist is more than you want to load at once. `categories/USA.m3u` is the headline file:
every working US channel, in the published category order, with each channel's spare feeds
next to it in its own `<category> Backups` group and the best quality first.

```text
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/USA.m3u          # every US channel, by category
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/USA/Sports.m3u   # just the US sports channels
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/All/Sports.m3u  # every sports channel in the library
```

| Folder | What it holds |
|---|---|
| [`categories/USA.m3u`](categories/USA.m3u) | Every published US channel in one file, in category order. |
| [`categories/USA/`](categories/USA) | The same list cut per category — `Sports.m3u`, `News.m3u`, `Movies.m3u`, `Cartoons.m3u`, … |
| [`categories/All/`](categories/All) | One file per category for the whole library (US channels first inside a category, because that is the published order). |
| [`categories/README.md`](categories/README.md) | The index: category order, channel counts, and the URLs above. |

Two properties make the shelf safe to hand to a player:

* **it is a slice of an already published playlist.** Same channels, same order, same
  `group-title` labels, same guide header — nothing is re-classified, so the shelf can never
  show a channel the playlist does not have (and never invents a category of its own);
* **it cannot drift.** `scripts/build_categories.py` rebuilds it after every scrape, quick
  update, guide build and deep check, a file is only rewritten when its channel list actually
  changed, and `scripts/verify_playlists.py --require-shelf` re-plans the shelf from the
  published playlists and fails the run when a committed file is stale or missing. Groups
  smaller than three channels keep no file of their own — they stay in the parent playlist,
  where nothing is lost.

### Local channels (Lancaster / Harrisburg, PA)

[`playlists/sources/local-channels.m3u`](playlists/sources/local-channels.m3u) is a curated source for the
Susquehanna Valley market, so the local stations are published in `PremiumTV.m3u` and
`playlists/countries/USA.m3u` like any other channel and re-checked on every scrape:

| Channel | Market | Feed |
|---|---|---|
| WGAL 8 (NBC) | Lancaster, PA | public Tubi feed |
| CBS 21 (WHP) | Harrisburg, PA | public Stirr feed |
| Fox 29 (WTXF) | Philadelphia, PA | Fox's public FAST feed |
| NBC 6 (WJAC) | Johnstown, PA | public Stirr feed |

WHTM 27 (ABC) and WPMT 43 (Fox) are the market's other stations, but they publish no free 24/7 stream —
abc27 and fox43 stream newscasts only inside their own sites and apps — so they are not listed. Add a line
to the file and the next scrape publishes and checks it; a feed that stops answering is dropped
automatically.

Each report compares the newly discovered links with the previous all-links playlist and records added/removed counts. A failed source refresh or a link-check run below the minimum working ratio is recorded, but does not replace the last good `PremiumTV.m3u`.

## TV guide (EPG) — root-level, country-specific XMLTV

The generated guides live in the repository-root [`EPG/`](EPG/README.md) folder, **not** inside
`playlists/`. There is one verified, filtered all-library file and a separate XMLTV `.xml` for each
country playlist. The channel-specific country M3Us automatically point to their matching country
guide, so an IPTV player can load one compact, relevant guide instead of downloading every upstream
country feed.

**All-library guide:**

```text
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/EPG/PremiumTV.xml
```

Examples for country playlists:

| Playlist | Country XMLTV guide |
|---|---|
| `playlists/countries/USA.m3u` | [`EPG/USA.xml`](EPG/USA.xml) |
| `playlists/countries/UK.m3u` | [`EPG/UK.xml`](EPG/UK.xml) |
| `playlists/countries/Canada.m3u` | [`EPG/Canada.xml`](EPG/Canada.xml) |
| Other country playlists | `https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/EPG/<Country>.xml` |

For manual setup, use the plain `.xml` raw URL in TiviMate, IPTV Smarters, Kodi PVR IPTV Simple,
VLC, or another XMLTV-capable player. The playlist's `x-tvg-url` already contains the right URL:
country playlist headers contain only their own country guide; the main/A&E/priority playlists put
`EPG/PremiumTV.xml` first and keep at most two verified source guides behind it as fallbacks
(`--max-header-guides`, `MAX_HEADER_GUIDES` in `scripts/scraper.py`). The merged guide already holds
every programme those fallbacks have, so trimming them from ~100 URLs stops a player from
downloading a hundred guides before it shows a single listing. `EPG/PremiumTV.xml.gz` is
also available when a player accepts gzip. For published playlists, channels missing a source
`tvg-id` receive a stable `premiumtv.<country>.<channel>` ID so their XMLTV channel entries can
still be addressed consistently; normalized source caches keep their upstream metadata unchanged.

[`scripts/epg_build.py`](scripts/epg_build.py) streams the upstream XMLTV sources that the nightly
guide check verified, matches channel IDs to the published M3Us, and writes all root-level EPG
files in the same run. The merged all-library guide declares **every** `tvg-id` in the
published playlists - channels with verified listings and channels that only have a catalogue
entry - so a channel is never missing from the guide, and coverage is reported honestly as
"declared" versus "with listings"
([`playlists/checks/VERIFY.md`](playlists/checks/VERIFY.md) shows both per playlist; the committed
`EPG/PremiumTV.xml` catches up on the next `epg-build` run, which is what writes the
declarations). Each country guide:

* declares only the `tvg-id` values present in its country playlist (including channels that have no
  public schedule, so missing guide coverage is visible rather than silently mis-mapped);
* includes programme entries only when a verified source matched that channel by ID or an
  unambiguous display name;
* preserves programme titles, descriptions, genres, episode numbers and ratings; merges duplicates,
  discards placeholders/poor overlaps, and uses explicit UTC timestamps in XMLTV format;
* is streamed and validated before publication. Reports list per-country channel counts, matched
  channels, programme totals, XML sizes and any build/validation failures.

**Curated upstream guide sources cover every country.** `sources.json` → `epg_sources` lists the
public XMLTV feeds every guide build merges ahead of the guides found in playlist headers:
[`iptv-epg.org`](https://iptv-epg.org/guides) (`epg-us.xml` and the other per-country `epg-<cc>.xml.gz`
files) and [`epg.pw`](https://epg.pw/xmltv.html?lang=en) (`epg.xml.gz` one-for-all plus `epg_<CC>.xml.gz`
per country). `scripts/epg_sources.py` expands one URL per published country playlist (345 curated
URLs across 172 countries in the current configuration). The nightly guide check verifies every one
of them (`playlists/checks/EPG-CHECK.md`), the merge matches them to playlist channels by ID and by
display name — fanning a schedule out to same-country backup feeds of one station — and the merged
guide is the only one advertised to players, so no player ever downloads the raw upstream files.

**Local stations are treated conservatively.** The curated Lancaster/Harrisburg/Johnstown/Philadelphia
feeds are in the USA playlist and are link-checked with the rest. A generic national `NBC.us` guide
is not copied onto WGAL and WJAC just because they share a network; the source must identify the
local affiliate or have a unique station-name match. When no public station-level listing is
available, the channel remains in the M3U and XMLTV channel catalogue but correctly has no fabricated
programme data. See [`playlists/sources/local-channels.m3u`](playlists/sources/local-channels.m3u) and
the per-country build table in [`playlists/checks/EPG-BUILD.md`](playlists/checks/EPG-BUILD.md).

When upstream EPG feeds are temporarily unreachable, the builder keeps the last good all-library
XMLTV in place and may reuse a successfully published, previously verified guide for country outputs
for up to 36 hours. If no recent verified guide is available, it publishes channel catalogues with no
programme entries rather than inventing schedules; the report clearly labels that fallback.

### Constant playlist and guide refresh

The scraper already checks and updates the M3U sources **seven times a day**, with a schedule guard
for delayed/dropped GitHub runs; the nightly deep check verifies streams end-to-end. EPG generation
runs twice daily, after nightly verification, and after scraper runs when the country-channel set has
changed. A guide freshness skip is allowed only when the guide-relevant M3U fingerprint and all
expected country XML files still match, so newly added/renamed channels trigger an immediate rebuild.

Run a manual checked refresh at any time:

```bash
python scripts/scraper.py --label "manual verified rescrape"  # refresh and check source streams
python scripts/epg_build.py --countries --patch --force         # rebuild every country XMLTV + playlist headers
python scripts/resort_playlists.py                              # re-sort the committed playlists into categories
python scripts/verify_playlists.py --strict                     # offline check: categories, order, dead links, EPG coverage
python scripts/audit_backups.py --strict                        # backup names, orphans, numbering, category files
```

The standard scrape safety threshold preserves the last good `PremiumTV.m3u` if a source/network
failure leaves too few confirmed working links. The XMLTV builder likewise leaves the previous
all-library file untouched if the verified harvest is implausibly small; every country output is
well-formed XMLTV and failures are shown in the build report. To request a workflow-run refresh
without opening Actions, use:

```bash
gh api -X POST repos/<owner>/<repo>/dispatches -f event_type=scrape-now \
  -f 'client_payload[label]=manual verified rescrape'
gh api -X POST repos/<owner>/<repo>/dispatches -f event_type=epg-build-now
```

Appending a line to [`playlists/logs/run-scrape.txt`](playlists/logs/run-scrape.txt) and pushing
runs a full checked scrape on that branch instead — the same switch the deep check
([`run-deep-check.txt`](playlists/logs/run-deep-check.txt)) and the guide build
([`run-epg-build.txt`](playlists/logs/run-epg-build.txt)) already use, and the only one of the
three that works from a branch other than `main` (a `repository_dispatch` always runs on the
default branch). None of the workflows writes to those files, so they cannot trigger themselves.

See [`playlists/checks/EPG-BUILD.md`](playlists/checks/EPG-BUILD.md) for current verified coverage,
source health and output metrics. Appending a line to
[`playlists/logs/run-epg-build.txt`](playlists/logs/run-epg-build.txt) and pushing also triggers a
build on that branch.

## Automatic checks and logs

The [GitHub Actions workflow](.github/workflows/scrape.yml) runs **seven times a day** in `America/New_York` — roughly every three hours, so a link that dies in the morning is out of the player playlist by the afternoon:

| Time | Cron | Run label |
|---|---|---|
| 3:07 AM | `7 3 * * *` | Regular daily scrape |
| 6:23 AM | `23 6 * * *` | Recheck |
| 9:41 AM | `41 9 * * *` | Recheck |
| 12:53 PM | `53 12 * * *` | Recheck |
| 4:41 PM | `41 16 * * *` | Final daily check |
| 8:17 PM | `17 20 * * *` | Recheck |
| 11:29 PM | `29 23 * * *` | Overnight recheck |

A separate [nightly workflow](.github/workflows/link-check.yml) runs the intensive deep check at 1:13 AM: it re-verifies every published link end to end, verifies every TV guide, and hunts for the priority channels. See [Deep link check, guide check and priority channels](#deep-link-check-guide-check-and-priority-channels).

A separate [guide workflow](.github/workflows/epg-build.yml) rebuilds the merged and country-specific XMLTV files twice a day at 5:47 AM and 5:47 PM; see [TV guide (EPG) — root-level, country-specific XMLTV](#tv-guide-epg--root-level-country-specific-xmltv).

A separate [monthly workflow](.github/workflows/discover.yml) hunts for new channels on the 1st of each month at 4:37 AM; see [Monthly new-channel discovery](#monthly-new-channel-discovery).

A separate [biweekly workflow](.github/workflows/biweekly-cleanup.yml) runs the slow, whole-repository
sweep at 7:43 AM on the 1st and the 15th of every month: it deep-checks the 218 playlists no daily run
ever patches (the priority playlist, the per-category playlists, the `categories/` shelf and the local
source copies), removes the dead channels they hold, rebuilds the guides, re-hunts the priority
channels, trims the append-only logs and reports anything the pipeline left stale. See
[Biweekly deep cleanup](#biweekly-deep-cleanup).

### Schedule reliability and the catch-up guard

GitHub does not promise to start a `schedule:` cron on time. Measured on this repository from
`playlists/run-history.jsonl` and the Actions API, every scheduled run between 2026-09-27 and
2026-09-29 started hours after its intended New York time, and three of the nine slots never
produced a run at all:

| Intended (New York) | Intended UTC | Actually started (UTC) | Delay |
|---|---|---|---|
| 2026-09-27 3:00 AM | 09-27 07:00 | never ran | **skipped** |
| 2026-09-27 6:00 AM | 09-27 10:00 | never ran | **skipped** |
| 2026-09-27 4:15 PM | 09-27 20:15 | 09-27 23:03 | +2h 48m |
| 2026-09-28 3:00 AM | 09-28 07:00 | 09-28 15:04 | +8h 04m |
| 2026-09-28 6:00 AM | 09-28 10:00 | 09-28 18:02 | +8h 02m |
| 2026-09-28 4:15 PM | 09-28 20:15 | 09-29 00:22 | +4h 07m |
| 2026-09-29 3:00 AM | 09-29 07:00 | 09-29 13:51 | +6h 51m |
| 2026-09-29 6:00 AM | 09-29 10:00 | 09-29 16:27 | +6h 27m |

The cron expressions and their `timezone:` keys were correct — GitHub supports timezone-aware
schedules — so this was the scheduler queueing and dropping runs under load, not a
misconfiguration. Each run still reported `success`, which is why the lateness was invisible
except in the timestamps. Two things now address it:

1. **Off-peak minutes.** The crons moved from minute 0/15 to 7, 23 and 41. GitHub's scheduler is
   most congested at the top of the hour, which is where two of the three slots used to sit.
2. **A catch-up guard.** [`.github/workflows/schedule-guard.yml`](.github/workflows/schedule-guard.yml)
   starts every 20 minutes and runs [`scripts/schedule_guard.py`](scripts/schedule_guard.py). It
   reads the crons straight out of `scrape.yml`, works out when each slot was due, and compares that
   with `playlists/run-history.jsonl`. If a slot that has already come due is still uncovered, it
   fires the existing `scrape-now` repository dispatch labelled with the slot it is catching up on.

The guard never scrapes or commits anything itself, so there is still exactly one code path that
publishes playlists. It is idempotent: a slot stops being overdue the moment the scrape it triggered
records itself in `run-history.jsonl`, and it will not dispatch while a scrape is queued, running, or
finished within the last 25 minutes. Only runs with outcome `success` or `warning` count as covering
a slot — a failed run, or an unchecked `--no-check` merge that never publishes `PremiumTV.m3u`,
leaves the slot open. A successful *checked* run within 45 minutes of a slot also covers it whatever
its run type, so a manual re-scrape next to a slot is not immediately repeated by a catch-up.

The trade-off is that a slot GitHub delays by many hours may end up scraped twice: once by the
guard's catch-up and once when GitHub's own run finally arrives. That costs about 20 minutes of
runner time and simply refreshes the playlist again, which beats the alternative of a day with no
verified refresh at all.

Every scheduled run now records how late it started. `STATUS.md` shows it directly under the run
label, `report.json` and `run-history.jsonl` carry `scheduled_for_utc` and `schedule_delay_minutes`,
and a start more than 15 minutes late is listed as a run issue, so lateness can no longer hide behind
a green check mark.

An offline regression suite runs before the scrape. All scheduled runs fetch every configured playlist source, deduplicate channels, and check every unique HTTP stream URL. The workflow adds the human-readable status to the Actions run summary and commits `STATUS.md`, `report.json`, source caches, and `run-history.jsonl` even if a failed health check prevents playlist publication. A failed scraper run still ends the Actions job as failed after its diagnostics have been saved.

Statuses distinguish **dead** responses from **unverified** results. For example, 401/403 access restrictions, rate limits, server errors, timeouts, and non-HTTP schemes are not represented as confirmed-working links; their reasons and next-step guidance are in `STATUS.md` and `report.json`. Per-host request limits and retries help reduce avoidable rate limiting. HTTP checks are only a reachability signal: they cannot guarantee playback from every region or that a stream is authorized for every viewer.

To run immediately, open **Actions → Scrape playlists → Run workflow**. Leave **Skip link checking** off for a verified refresh. Scheduled workflows run from the default branch (`main`); a manual run on another branch only updates that branch. To see the current schedule coverage without starting anything, run **Actions → Schedule guard → Run workflow** (dry run by default) or `python scripts/schedule_guard.py report`.

## Quick updates to playlists you already have

[`scripts/update_m3u.py`](scripts/update_m3u.py) is the fast path: point it at
any M3U file on disk — the one published here, one you downloaded, or a folder
full of them — and it re-checks every link concurrently, repairs what broke and
re-publishes the file in the curated category order.

```bash
python scripts/update_m3u.py my-list.m3u                       # check, repair, rewrite
python scripts/update_m3u.py my-list.m3u --dry-run             # report only
python scripts/update_m3u.py playlists/*.m3u \
    --pool playlists/PremiumTV_all.m3u "playlists/sources/*.m3u"
python scripts/update_m3u.py my-list.m3u --offline             # tidy categories only
python scripts/update_m3u.py my-list.m3u --deep                # prove a segment plays
```

What it does with a broken link, in order:

1. **a backup of the same channel in the same file** is promoted (the entry you
   see as `… (Backup 1)` in the `… Backups` group);
2. **a working candidate from `--pool`** is pulled in and tested first;
3. **only then** is the entry removed — and only when the run would not delete
   more than `--max-remove-ratio` (35% by default) of the file.

Links the deep check already quarantined (the "loads but never plays" ones) are
treated as broken too, so a shallow "server answered" never protects a dead
stream. Transient failures — timeouts, 5xx, 401/403 — are always kept.
[`.github/workflows/quick-update.yml`](.github/workflows/quick-update.yml) runs
it four times a day between the regular scrapes.

[`scripts/rebuild_playlists.py`](scripts/rebuild_playlists.py) is the offline
half: it never touches the network, re-classifies a playlist that is already on
disk, splits it into [`playlists/categories/`](playlists/categories/README.md)
and writes the [category audit](playlists/checks/CATEGORIES.md). The scraper
calls the same taxonomy, so a scrape cannot undo the order.

[`scripts/epg_match.py`](scripts/epg_match.py) fixes the "channel is missing
from the guide" problem: it reads the published XMLTV once and re-points every
channel at an id the guide actually declares — exact id first, then the base id
(`AE.us@East` → `AE.us`), then an unambiguous display-name match — so a channel
that had a guide entry under a different id now picks up its schedule.

## Deep link check, guide check and priority channels

The daily scrape is deliberately shallow: it reads the first few KB of a URL, which proves a server
answered but not that a player can play the stream. Three scripts cover the gap, and
[`.github/workflows/link-check.yml`](.github/workflows/link-check.yml) runs all three nightly at
**1:13 AM** (New York time). Each can also be run by hand from **Actions → Deep link and guide check
→ Run workflow**, or locally:

```bash
python scripts/link_check.py --all --patch     # re-verify every published link, drop dead ones
python scripts/epg_check.py  --all --patch     # verify every TV guide, drop dead ones
python scripts/channel_hunt.py --github-search # hunt the priority channels, NFL Network included
```

### `scripts/link_check.py` — the intensive M3U check

For every published link it fetches the URL with the headers a player would send, resolves an HLS
master playlist to its best variant, downloads a real media segment and checks it is media (TS sync
byte, fMP4 box, or enough bytes), checks DASH manifests are populated, and classifies the rest by
payload. That distinguishes the two cases a shallow check cannot tell apart:

| Result | Meaning | Patched? |
|---|---|---|
| `working` | answered **and** produced playable media | keep |
| `offline` | confirmed dead: 404/410, DNS failure, refused, HTML page, empty body | **removed** |
| `unreachable` | timeout, 5xx, connection reset — may recover | keep |
| `blocked` | 401 / 403 / 451 — needs auth or is geo-blocked | keep |
| `unsupported` | non-HTTP scheme (rtmp, acestream, …) that cannot be probed | keep |
| `invalid` | malformed or non-HTTP URL | **removed** |

Removals are also written to `playlists/checks/quarantine.json`, and `scraper.py` reads that file on
every run: a link that only fails the deep check is held back for 7 days, so the next shallow scrape
cannot put it straight back into the player playlist.

Only the two confirmed-dead buckets are ever removed, and two safety nets stop a bad network day
from gutting a good playlist: `--min-working-ratio` (default 20%) aborts the patch when too few
links worked overall, and `--max-remove-ratio` (default 35%) skips any single playlist that would
lose more than that share of its entries. Every removal is logged to
`playlists/logs/link-check-edits.txt` and summarised in
[`playlists/checks/LINK-CHECK.md`](playlists/checks/LINK-CHECK.md).

`--all` covers the playlists a player loads. **`--archives`** adds the 218 that no daily run patches -
the priority playlist, the 81 `playlists/categories/*.m3u` files, the `categories/` shelf and the
`playlists/sources/*.m3u` fallback copies - plus `playlists/PremiumTV_all.m3u`, which is checked but
never pruned because the file exists to hold every link ever found. The sweep the
[biweekly workflow](#biweekly-deep-cleanup) runs writes its own report
(`playlists/checks/LINK-CHECK-ARCHIVES.md`, via `--report-suffix=-archives`) so the
`link-check.json` the re-sort and the next scrape read back stays the player one, and it uses looser
limits (`--min-working-ratio 0.10 --max-remove-ratio 0.60 --quarantine-days 21`) because those files are
spares and caches rather than something a viewer is watching.

### `scripts/epg_check.py` — TV guide verification

Players download every guide in the playlist's `x-tvg-url` header on each refresh, so one dead guide
slows all of them down. This script fetches each guide the way a player does — decompressing
`.xml.gz` on the fly and only reading the first slice of what are often 100 MB files — and confirms
it is real XMLTV with channels and programmes in it. Guides that answer with an HTML error page,
JSON, or an empty body are `invalid`; guides that 404 are `offline`; both are dropped by `--patch`,
while `unreachable` and `blocked` guides are kept because they may recover. Results, channel counts
and the newest programme date are in
[`playlists/checks/EPG-CHECK.md`](playlists/checks/EPG-CHECK.md).

The guides this repository publishes for its own players (`EPG/PremiumTV.xml` and one
`EPG/<Country>.xml` per country, written by `scripts/epg_build.py`) are recorded with their real status
but flagged `own_repo`: they are never counted as upstream guides and never dropped from a header.
Without that distinction a *private* repository - where `raw.githubusercontent.com` answers 404 for
every one of its own files, see the note at the top of this README - looks like a total outage
(173 "dead" guides out of 175), which trips `--min-working-ratio` and silently disables guide patching.

### `scripts/epg_build.py` — merged and country-specific XMLTV

Verification tells you which upstream guides are alive; the builder turns the verified ones into
player-ready outputs. Its safety gate compares a fresh build against the channels of the published
guide that **still have a listing inside the new window** - not against the number of `<channel>` rows
in the file. A guide whose listings have all aged out protects nothing, and comparing against the old
row count let one held build block every build after it forever: 180 fresh channels refused in favour
of 8,521 expired ones, nightly, with the same file growing staler each day.
### `scripts/epg_build.py` — merged and country-specific XMLTV

Verification tells you which upstream guides are alive; the builder turns the verified ones into
player-ready outputs. It streams even very large compressed guides, matches channels to the current
M3Us, and writes the all-library `EPG/PremiumTV.xml` plus one `EPG/<Country>.xml` per
`playlists/countries/<Country>.m3u`. Country XMLs contain only their playlist's channel IDs and the
programmes verified for those channels. The detailed report lists source contributions, country
coverage, emitted programme counts, sizes, and XMLTV validation results in
[`playlists/checks/EPG-BUILD.md`](playlists/checks/EPG-BUILD.md).

### `scripts/channel_hunt.py` — priority channels

Coverage scrapes are good for volume and bad for a specific channel: if the index entry rots, the
channel silently disappears. This script inverts the process for the channels configured in
`sources.json` → `priority_channels` — Nickelodeon, NickToons, MeTV, MeTV Toons, and, since the
NFL Network kept breaking, **NFL Network** and **NFL RedZone**:

**NFL Network** is kept with up to six verified links and **NFL RedZone** with up to four. One
becomes the main link in **Sports**; the rest are published as `NFL Network (Backup 1…n)` in
**Sports Backups**, and `scripts/update_m3u.py` swaps a working one in automatically when the main
link stops playing. Every candidate is still verified end to end before anything is written.

1. **Collect** every candidate whose name or `tvg-id` matches a target — from the local corpus, from
   the configured upstream indexes, and (with `--github-search`) from public M3U files found by
   GitHub code search. A target whose name is a prefix of another target is excluded from it, so
   *MeTV* never collects *MeTV Toons* links.
2. **Verify** each candidate end to end with the deep checker.
3. **Publish** the survivors to `playlists/sources/priority-channels.m3u`, which `sources.json`
   enables as a normal source — so every scheduled scrape re-checks them, and a channel can only
   stay listed while it keeps playing.

Nothing is guessed: a link is only written after a media segment downloaded successfully. The hunt
reports every candidate it tested and the reason each one failed in
[`playlists/checks/CHANNEL-HUNT.md`](playlists/checks/CHANNEL-HUNT.md), so a channel with no working
public link is visible rather than silently missing.

Ranking favours the links worth keeping: the configured **`country`** first (`"us"` for all four
targets today, taken from the `tvg-id`/`tvg-name`), then an exact name match, then links **without**
a token or expiry in the URL. A signed link that plays today and 404s tomorrow is dropped entirely
whenever a stable link for the same channel plays (set `"allow_temporary": true` on a target to keep
them as a last resort). `blocklist` in the same config holds URL fragments that must never be collected, which is
how a feed several indexes list as "MeTV Toons" but which actually carries a different network stays
out. GitHub code search is best effort: it is rate limited (429) when the hunt runs more than about
once an hour, and every failure is recorded in the report's `notes` instead of being hidden.

## Biweekly deep cleanup

Every other scheduled run is a *publishing* run: it has to finish in a few minutes because seven
scrapes a day depend on it. [`.github/workflows/biweekly-cleanup.yml`](.github/workflows/biweekly-cleanup.yml)
is the slow one, twice a month at **7:43 AM on the 1st and the 15th** (New York time), that does the jobs
a quick run cannot afford. Start it by hand from **Actions → Biweekly deep cleanup → Run workflow**, or
by appending a line to [`playlists/logs/run-cleanup.txt`](playlists/logs/run-cleanup.txt) and pushing it
(the workflow never writes to that file, so it cannot trigger itself), or locally:

```bash
python scripts/link_check.py --all     --deep --patch --quarantine-days 14   # player playlists
python scripts/link_check.py --archives --deep --patch \
        --min-working-ratio 0.10 --max-remove-ratio 0.60 \
        --report-suffix=-archives                                            # everything else
python scripts/resort_playlists.py                                          # re-order + prune dead links
python scripts/build_categories.py                                          # rebuild the published shelf
python scripts/cleanup_repo.py --apply                                      # logs, orphans, quarantine
python scripts/verify_playlists.py --strict --require-shelf                 # audit the result
python scripts/audit_backups.py --strict                                    # backups + category slices
```

**The dead channels the daily runs miss.** `link_check.py --all` (nightly) checks the main playlist, the
A&E playlist and the country files; the four-times-a-day quick update re-checks the main and priority
playlists with a shallow probe. That leaves `playlists/Priority_Channels.m3u`, the 81
`playlists/categories/*.m3u` files, the 125 files of the `categories/` shelf a player is pointed at in
[the section above](#the-categories-shelf), and the 10 `playlists/sources/*.m3u` copies a scrape falls
back to when an index is down - 218 playlists in which a channel that died simply stays. `--archives`
adds exactly those to the sweep, with looser limits (they are mostly spares and fallbacks by design) and
its own report, `playlists/checks/LINK-CHECK-ARCHIVES.md`, so the `link-check.json` the next scrape reads
back is still the player one. `playlists/PremiumTV_all.m3u` is checked but never pruned: it is the
archive of *every* link found, dead ones included, and a link confirmed dead there is still added to the
quarantine, which is what stops the next scrape publishing it into a player.

**Why two dated slots rather than "every other week".** GitHub's cron cannot express a 14-day
interval, and the usual trick - a weekly trigger plus an even-week test - loses a whole month the moment
the scheduler drops the one run that mattered, which [this repository has measured it
doing](#schedule-reliability-and-the-catch-up-guard). Two dated slots are between 14 and 16 days apart and
each one covers for the other.

**Repository housekeeping** is [`scripts/cleanup_repo.py`](scripts/cleanup_repo.py), and it is the only
tool here that looks at the repository instead of the playlists:

| It does | Why it matters here |
|---|---|
| Trims the four append-only `playlists/logs/*-edits.txt` logs to the last `--keep-runs` runs (and `--max-log-lines` lines), at run-block boundaries, header banner intact | The logs record one line per removed link, so they passed a megabyte each within days and every clone carried that history |
| Removes `EPG/<Country>.xml` files whose country playlist is gone, plus swap files and byte-code caches a cut-off run left behind | `git` keeps every version of a 60 MB file it has ever seen |
| Drops quarantine entries past `--quarantine-days`, and reports the ones with no usable timestamp instead of removing them | The scraper *honours* an undated entry forever, so silently dropping one would re-publish a dead link |
| Checks that `STATUS.md`, `report.json` and every `checks/*.json` were refreshed recently, and that the published guide still has listings inside its window | A guide build held back by its own safety gate leaves every run green while players see an empty grid - nothing else in the pipeline notices |
| Refuses to touch `logs/run-*.txt` | Those files are push triggers; rewriting one from a workflow would start that workflow again |

It is read-only unless you pass `--apply`, and the cleanup run does not fail on a finding - the findings
are the point, and they are published in [`playlists/checks/CLEANUP.md`](playlists/checks/CLEANUP.md)
alongside the history in `playlists/logs/cleanup-edits.txt`.

## Monthly new-channel discovery

The daily schedule only refreshes the sources that are already configured, so new channels need their own hunt. The [monthly workflow](.github/workflows/discover.yml) runs [`scripts/discover.py`](scripts/discover.py) at **4:37 AM on the 1st of every month** (New York time) and can also be started manually from **Actions → Monthly discovery → Run workflow**.

Each monthly run:

1. Builds the corpus from the published `PremiumTV_all.m3u`, so "new" means "not in the playlist yet".
2. Collects candidates: the seeded repositories in `sources.json` plus public GitHub repositories found through repository search (`topic:iptv-m3u`, `#EXTM3U` in the README, and similar). For each repository the engine reads the file tree and picks the most likely static TV playlist, skipping series/movie/VOD/radio files.
3. Fetches and parses each candidate, then measures how many links it would actually **add**, how many are duplicates, and how many channel names are new.
4. Link-checks a host-balanced sample of those new links — 12 by default, spread across providers so one host cannot skew the result — and scores the candidate on working ratio, new-link volume, and freshness.
5. Reviews the already-configured sources the same way, so the report also shows new channels arriving from sources you already have.
6. Re-checks the health of previously promoted sources and flags any that have gone stale.

A candidate is promoted only when it clears every threshold in `sources.json` → `discovery.thresholds` (at least 25 new links, at least 3 of the sampled links working, a working ratio of at least 30%, and a score of at least 55). Promotions are capped at `max_promote_per_run` (2) per month and are written to `playlists/discovery/approved-sources.json`. The monthly workflow then runs a normal checked scrape so the new sources are integrated with every link verified, exactly like a regular run; otherwise the next daily scrape picks them up.

Promotion is not publication. A promoted source is still fetched, deduplicated, and link-checked by the regular scraper before anything can reach `PremiumTV.m3u`, promoted sources are marked 🌱 in `STATUS.md`, and the minimum-working-ratio safeguard still protects the last good playlist. To roll one back, set `"enabled": false` for it in `approved-sources.json` or delete the entry.

Candidates that were already measured and rejected are remembered in `playlists/discovery/state.json` and are not re-fetched until `recheck_after_days` (90) has passed, so a month of dead sources costs one fetch each. `--force` overrides this.

## Sources

Playlist sources are configured in [`sources.json`](sources.json). Active M3U/W3U feeds are fetched and their unique stream URLs are checked on every scheduled run.

| Source | Format | Integration |
|---|---|---|
| [`local-channels`](playlists/sources/local-channels.m3u) | M3U | Curated local channels for the Lancaster / Harrisburg / Lebanon / York market (`WGAL 8`, `CBS 21 (WHP)`, `Fox 29 (WTXF)`, `NBC 6 (WJAC)`); enabled and re-checked on every scrape. |
| [`ae-networks`](playlists/sources/ae-networks.m3u) | M3U | Curated A&E and A+E Networks linear & FAST M3U8 streams (`A&E`, `A&E Crime 360`, `The First 48`, `Storage Wars`, `Cold Case Files`, `60 Days In`, `Hoarders`, `Intervention`, `Dog the Bounty Hunter`, `Duck Dynasty`, `Home.Made.Nation`, `Crime + Investigation`, etc.); enabled. |
| [aria](https://github.com/aria-tv/aria/blob/main/aria.m3u) | M3U | Direct raw playlist; enabled. |
| [doms9/iptv](https://github.com/doms9/iptv) | M3U8 | `M3U8/TV.m3u8`; enabled. |
| [xtemus](https://xtemus.com/) | W3U | Enabled; only the selected live-TV groups are followed. Movie, series, radio, and highlight folders are excluded. |
| [iptv-org/iptv](https://github.com/iptv-org/iptv) | M3U | Added global playlist `https://iptv-org.github.io/iptv/index.m3u`. |
| [Free-TV/IPTV](https://github.com/Free-TV/IPTV) | M3U8 | Added `playlist.m3u8`. |
| [eja.tv](https://eja.tv/) | Website audit | The site is probed for reachability, but it is not treated as a static playlist. No direct M3U export was verified. It is not counted as imported channels unless a direct playlist URL is configured. |
| [StepDaddyLiveHD](https://github.com/gookie-dev/StepDaddyLiveHD) | Repository audit / optional instance playlist | The repository tree is checked for a static M3U. Its documented playlist is generated by a self-hosted app, so the repository itself is not a channel feed. |
| [dlive.sx](https://dlive.sx/24-7-channels.php) | Channel-index audit / optional direct playlist | The DaddyLiveHD 24/7 index is fetched and its catalogue counted, but no channel is imported: see below. Set `DLIVE_M3U_URL` to an authorized direct playlist to import and link-check it. |

`aria` and `doms9` were already active sources; the scraper now also scans `iptv-org` and `Free-TV/IPTV`. The eja.tv, StepDaddyLiveHD and dlive.sx references are checked and reported separately rather than falsely counted as channel feeds. To ingest an authorized direct M3U URL for any of them, add repository Actions secrets named `EJA_M3U_URL`, `STEPDADDYLIVEHD_PLAYLIST_URL` or `DLIVE_M3U_URL`. The StepDaddy secret should point to a running instance's `/playlist.m3u8`; without it, the repository audit still runs and the instance source is shown as `not_configured`.

If you have an authorized direct playlist for the same channels — for example an M3U generated by a
self-hosted proxy such as StepDaddyLiveHD — set the `DLIVE_M3U_URL` Actions secret. The `dlive-sx-feed`
source then imports it like any other feed, and every link is checked before it can appear in
`PremiumTV.m3u`. Until it is set, that source is reported as `not_configured` instead of failing the
run. Be aware that playlists and caches are committed to this repository, so only configure a feed
whose stream URLs are safe to publish.

To add another feed, add a `sources` entry with `name`, `type` (`m3u` or `w3u`), and `url`. For an optional URL supplied by an environment variable, use `url_env` and `optional: true`; the workflow's optional secrets are wired in `.github/workflows/scrape.yml`. W3U sources also support `include_groups`, `exclude_groups`, and `max_depth`. Playlist files and caches are committed to this repository, so only configure feeds whose resulting stream URLs are safe to publish—an Actions secret protects the feed URL from logs, but does not make output links private. Review source quality and permissions before publishing.

## Run locally

Python 3.9+ is required; there are no third-party dependencies.

```bash
python scripts/scraper.py                         # fetch, merge, check, and write reports
python scripts/scraper.py --no-check              # merge without checks; keep the checked player file untouched
python scripts/scraper.py --help                   # workers, timeout, retries, and other options
python scripts/discover.py                        # monthly new-channel hunt
python scripts/discover.py --no-search --max-candidates 3   # quick, seeded-only trial run
python scripts/discover.py --dry-run              # report only; never promote a source
python scripts/epg_check.py --all                  # verify every advertised TV guide
python scripts/resort_playlists.py --dry-run       # show the category re-sort without writing
python scripts/link_check.py --archives --deep --patch  # sweep the playlists no daily run patches
python scripts/link_check.py --archives --no-deep --dry-run --report-suffix=-archives
python scripts/cleanup_repo.py                          # report what needs housekeeping, change nothing
python scripts/cleanup_repo.py --apply --keep-runs 30   # trim logs, drop orphan guides, compact quarantine
python scripts/verify_playlists.py                 # offline playlist + EPG coverage report
python scripts/verify_playlists.py --require-shelf  # ... and the categories/ shelf with it
python scripts/build_categories.py --dry-run        # show what the shelf would contain
python scripts/epg_build.py --dry-run              # build the merged guide without publishing it
python scripts/epg_build.py --patch --force        # rebuild it and advertise it in the playlists
python scripts/schedule_guard.py report            # schedule coverage table, no side effects
python scripts/schedule_guard.py --dry-run check   # what the 20-minute guard would do right now
python scripts/categorize.py playlists/PremiumTV.m3u --show 0   # audit the category order
python scripts/rebuild_playlists.py --dry-run --report -        # same, plus the per-category split
python scripts/update_m3u.py my-list.m3u --dry-run              # re-check a file you already have
python scripts/epg_match.py --playlist playlists/PremiumTV.m3u  # guide coverage for a playlist
python -m unittest discover -s tests -v            # offline integration tests
```

Inspect `playlists/STATUS.md` and `playlists/report.json` after a run. `--no-check` leaves `PremiumTV.m3u` untouched, and the workflow has a second restore safeguard before committing.

## Disclaimer

This repository does not host video. It only collects and checks links published elsewhere. Verify that a stream is authorized for you to access and redistribute in your location before using it.
