# PremiumTV — Android TV app

A leanback-first Android app that carries this repository's channel list and
TV guide inside the APK. The default build target is **1.0.3 stable**
(`versionCode` `10`) with the USA lineup. The last published stable download is
still **1.0.2** (`versionCode` `7`) until the 1.0.3 release has its full asset
set. **1.1.1** (`versionCode` `9`) is the preview build with the global checked
lineup and a **cable-style Guide tab**; it must be distributed as a GitHub
pre-release and is never the default (it supersedes the 1.1.0 preview,
`versionCode` `8`). The guide is
built from the repository's curated per-country XMLTV feeds (iptv-epg.org and
epg.pw).

The next stable target is `v1.0.3`; `v1.0.2` remains the current published
stable release until the 1.0.3 Android and Mac assets are complete. The 1.1.x
builds are published with GitHub's pre-release flag. GitHub Actions can build
all supported versions; the 1.1.x release jobs require that pre-release flag.
Each published version carries a debug-signed APK that installs as-is on
supported devices.

Installs on an Android TV, Google TV, Amazon Fire TV stick, tablet or phone.
The same APK works everywhere — navigation is D-pad first, and touch works too.

## What ships inside the APK

| Build | Source playlist | Source guide | Preview metadata |
|---|---|---|---|
| **1.0.3 stable build target (default)** | `playlists/countries/USA.m3u` | `EPG/USA.xml` | `library_scope: usa`; no preview features |
| **1.1.1 pre-release** (and 1.1.0) | `playlists/PremiumTV.m3u` | `EPG/PremiumTV.xml` | `library_scope: all`; `preview_features: ["cable-guide"]` |

Both scopes are converted to JSON Lines by [`tools/build_bundle.py`](tools/build_bundle.py)
and read with `android.util.JsonReader`. This keeps the large XML source off the
TV's memory while channel playback is active. GitHub Actions generates the
bundle at build time, so the installed app never needs Python or another tool.
The `all` scope is an explicit preview input; it does not change the stable
default.

**How many channels have listings:** the merged guide declares every channel
the playlists publish, and real programme listings are attached to every
channel a verified upstream guide schedules. The per-country curated feeds
(iptv-epg.org's `epg-us.xml` family and epg.pw's `epg_US` family, merged ahead
of everything else) carry the long tail of FAST and international channels.
Channels no public guide schedules show "Nothing listed at this hour" or
"No listing" rather than an invented schedule; the current counts are in
[`playlists/checks/EPG-BUILD.md`](../playlists/checks/EPG-BUILD.md).

## Screens

- **Channels** — one row per category, in the order the repository publishes
  (`Sports`, `Lifestyle`, `Fox Channels`, `CBS`, `NBC`, …). Each card shows the
  channel logo and, when the guide covers it, what is on right now.
- **Guide (1.1.1 preview)** — a cable-style grid: channels down the left
  (number, logo, name, category), each channel's shows to the right sized by
  running time, half-hour times across the top for eight hours, a red NOW line,
  category headings, and a detail strip for the highlighted show. The grid is
  one focus stop with a cable-box highlight ([`GuideModel.kt`](app/src/main/kotlin/com/premiumtv/app/ui/GuideModel.kt)):
  ▲▼ keep the time column, ◀▶ step one show, OK watches, Back from the player
  returns to the same show, ▲ from the first row returns to the tabs, CH+/CH−
  page, and the remote's GUIDE key opens it. Touch drags both ways; tap plays.
  It is enabled by the APK's own bundle (`cable-guide`), never by downloaded
  data.
- **Guide (stable 1.0.3)** — "what's on now" across every channel that has
  listings: current programme with a progress bar, plus what is next.
- **Settings** — bundle provenance and counts, automatic-refresh state, next
  check, last success/result, **Force refresh all now**, and reset to the APK's
  bundled copy.

## Playback

ExoPlayer (Media3 1.4.1). HLS and progressive streams are both handled, and
when a playlist entry publishes a referrer, an origin or a user-agent through
`#EXTVLCOPT` / `#KODIPROP`, the app sends them — several public feeds refuse
the connection otherwise. Plain `http://` streams are allowed for the same
reason. A channel that will not play is almost always a dead upstream link:
the repository's nightly link check removes those on its next run.

## Automatic and forced refreshes (Beta 4)

The GitHub workflows publish channels throughout the day and the guide twice a
day. Beta 4 mirrors every daily slot from `scrape.yml`, `quick-update.yml` and
`epg-build.yml`, then asks Android WorkManager to check **45 minutes later** in
`America/New_York`. That grace gives the publishing job time to finish. A check
requires a connected network, runs while PremiumTV is in the background, and is
persisted across app exits and device reboots. WorkManager is intentionally
inexact, so Android can defer a run while a device sleeps or applies background
limits; the next slot is chained after every completed check.

Automatic checks send the last ETag and Last-Modified value. When neither file
changed, the server returns two small HTTP 304 responses instead of sending the
playlist and guide again. When data did change, both files are parsed and a
complete staging directory is swapped into place; interruption or a bad file
leaves the previous usable cache untouched.

Settings → **Force refresh all now** bypasses those validators and downloads
the playlist and guide named in the installed bundle metadata (USA for stable;
the checked global pair for the 1.1.x preview). It is an app-side data refresh
from the public repository; it never runs GitHub Actions. The guide is parsed
as it downloads (the global XML is ~38 MB), keeping only listings for channels
in the playlist.

A downloaded copy remembers the version and library scope it was refreshed
for. When a different APK is installed over it (1.0.2 → 1.1.1, say), the old
copy and its validators are discarded on the next start, so the new build's
bundled lineup and Guide show immediately.

## Building

The bundle is generated from the repository, so build it first:

```bash
# Stable build target (USA, 1.0.3)
python3 tools/build_bundle.py --scope usa --version 1.0.3
./gradlew -PpremiumTvVersion=1.0.3 -PpremiumTvVersionCode=10 assembleDebug

# 1.1.1 pre-release data (global lineup + cable-style Guide tab)
python3 tools/build_bundle.py --scope all --version 1.1.1
./gradlew -PpremiumTvVersion=1.1.1 -PpremiumTvVersionCode=9 assembleDebug
```

`app/src/main/assets/bundle/` is gitignored: it is derived data and would go
stale the moment the repository publishes a new scrape. Only developers need to
run the script; the APK built by CI already contains the bundle, and the app
itself never asks a viewer to run anything. If the required channel list is
unreadable, the app shows a retry action and a useful error; an unavailable
guide no longer prevents the channel browser from opening.

### Where the APKs come from

GitHub Actions builds them — [`.github/workflows/android-build.yml`](../.github/workflows/android-build.yml).
A plain sandbox cannot compile this project (no JDK, no Android SDK, no access
to Maven Central or `dl.google.com`). Every push that touches `android/`,
`playlists/countries/`, `EPG/` or the workflow rebuilds the installable debug
APK and commits the build output to `build-out/`. The stable bundle takes its
channels only from the checked USA playlist, not the unfiltered all-links
catalogue; the latest main-branch scrape and follow-up deep check on
2026-10-16 leave 2,694 published USA entries. The committed bundle metadata
records the exact counts and guide window used by each build:

```text
build-out/PremiumTV-1.0.3-debug.apk   stable build default (debug-signed, USA scope)
build-out/PremiumTV-1.1.1-debug.apk   only when the preview version is selected
build-out/SHA256SUMS-android.txt
build-out/build-log.txt               full Gradle output
```

The workflow attaches 1.0.3 assets only to the full stable `v1.0.3` release
(and can still rebuild the historical `v1.0.2` release), while 1.1.x assets go
to the matching pre-release (`v1.1.0`, `v1.1.1`). Only the debug APK is
published; an unsigned release APK cannot be installed on a TV or phone.

### Installing on a TV

1. Copy `PremiumTV-1.0.2-debug.apk` to the TV (USB stick, a file-sharing
   app, or `adb install -r PremiumTV-1.0.2-debug.apk` from a computer).
2. Allow installs from that source (*Install unknown apps*).
3. Open **PremiumTV**. The Channels tab should list the categories straight away.

## Project layout

```text
android/
├── app/src/main/kotlin/com/premiumtv/app/
│   ├── MainActivity.kt          entry point
│   ├── PremiumTvApplication.kt  repository, refresh schedule and image loader
│   ├── TvViewModel.kt           exposes load/refresh state and actions
│   ├── data/
│   │   ├── Model.kt             Channel, Programme, Library and refresh models
│   │   ├── Jsonl.kt             streaming reader for the bundled assets
│   │   ├── M3uParser.kt         playlist parser (mirrors build_bundle.py)
│   │   ├── XmlTvParser.kt       guide parser
│   │   └── TvRepository.kt      atomic cache + conditional/full network refresh
│   ├── update/
│   │   ├── AutomaticRefreshScheduler.kt  GitHub-aligned WorkManager slots
│   │   └── LibraryRefreshWorker.kt       connected background refresh worker
│   └── ui/
│       ├── AppRoot.kt           loading / error / home / player routing
│       ├── HomeScreen.kt        channels, guide and settings tabs
│       ├── CableGuide.kt        the cable-style Guide grid (preview builds)
│       ├── GuideModel.kt        grid rows, ordering and the remote's highlight
│       ├── PlayerScreen.kt      ExoPlayer + now-playing overlay
│       ├── Components.kt        D-pad correct cards, tabs, buttons
│       ├── Guide.kt             now/next helpers and clock formatting
│       └── Theme.kt             dark TV theme
├── art/app-icon.png             launcher icon source art (1024x1024)
└── tools/
    ├── build_bundle.py          repository data -> app assets
    └── make_icons.py            art -> mipmap folders
```

## Known limits

- Stable 1.0.3 intentionally bundles the USA library. The 1.1.x pre-releases
  select the checked global playlist and merged guide.
- No favourites, search, or "continue watching" — browse, play and guide only.
- The bundled guide is a snapshot of what the repository had published at
  build time; automatic refreshes keep it current after install.
- Android may defer background work, and force-stopping the app suspends its
  WorkManager jobs until the app is opened again.
- Dead upstream links are still in the playlist until the nightly link check
  drops them, so some channels will fail to play.

## Release launch gate

After baking the actual channel assets, CI runs `testDebugUnitTest` with
Robolectric (repository/cache and parser regression tests) and builds the debug APK.
`tools/smoke_apk.py` then installs that APK on an API 30 emulator, clears app
data for a cold launch, checks the channel count and visible cards, and repeats
a relaunch. It then opens the Guide tab: a preview build must show the grid
(times across the top, channels down the left, shows), follow D-pad moves,
open the player on OK and return to the guide on Back, and it saves
`build-out/android-guide*.png`; a stable build must show the list. Every adb call has an explicit timeout and the UI window is sized
for the global 1.1.x library (~21 MB of assets against ~6 MB for the stable USA
bundle), so a slow dump is retried instead of failing the build; a real failure
writes `build-out/smoke-log.txt`, which branch builds publish. Emulator boot
failures block publication rather than being counted as app test passes.
Physical TV and upstream playback checks remain manual.

### Updated Encore Preview builds

Ordinary pushes and manual builds default to stable 1.0.3 (Android code 10).
To request the updated 1.1.1 preview (code 11) without Actions-dispatch access,
append a timestamp to `.github/preview-build.txt` and push with
`[preview-build]` in the commit message. Both platform workflows build the global
preview and retain their normal smoke gates. Branch artifacts do not overwrite
an existing tagged release: release attachments remain exact-SHA guarded.
Only publish verified artifacts deliberately; label any rebuilt preview with its
actual source commit in the release notes. The original 1.1.1 tag is historical.
