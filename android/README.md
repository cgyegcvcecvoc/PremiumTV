# PremiumTV — Android TV app

A leanback-first Android app that carries this repository's channel list and
TV guide inside the APK. The default build is **1.0.2 stable** (`versionCode`
`7`) with the USA lineup. **1.1.0** (`versionCode` `8`) is a separate preview
build with the global checked lineup and an optional cable-style guide; it must
be distributed as a GitHub pre-release and is never the default. The guide is
built from the repository's curated per-country XMLTV feeds (iptv-epg.org and
epg.pw).

The 1.0.2 stable target is published as the `v1.0.2` release; the 1.1.0 build is
published with GitHub's pre-release flag. GitHub Actions can build either
version; the 1.1.0 release job requires that pre-release flag. Both versions
publish a debug-signed APK that installs as-is on supported devices.

Installs on an Android TV, Google TV, Amazon Fire TV stick, tablet or phone.
The same APK works everywhere — navigation is D-pad first, and touch works too.

## What ships inside the APK

| Build | Source playlist | Source guide | Preview metadata |
|---|---|---|---|
| **1.0.2 stable (default)** | `playlists/countries/USA.m3u` | `EPG/USA.xml` | `library_scope: usa`; no preview features |
| **1.1.0 pre-release** | `playlists/PremiumTV.m3u` | `EPG/PremiumTV.xml` | `library_scope: all`; `preview_features: ["cable-guide"]` |

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
- **Guide** — "what's on now" across every channel that has listings: current
  programme with a progress bar, plus what is next.
- **Cable (1.1.0 preview only)** — an optional 8-hour grid of channels against
  programme times, with a live marker. The tab is shown only when bundle
  metadata enables `cable-guide`; it is absent in stable 1.0.2.
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
the checked global pair for the 1.1.0 preview). It is an app-side data refresh:
it cannot run or trigger private GitHub Actions from a TV.

> **Current access limitation:** this repository is private, so an
> unauthenticated TV receives an access error from `raw.githubusercontent.com`.
> The app reports that result and keeps its bundled/cached data. Automatic and
> forced refreshes begin working when an owner-approved public mirror or public
> delivery URL is configured; no GitHub credential is stored in the app.

## Building

The bundle is generated from the repository, so build it first:

```bash
# Stable default (USA, 1.0.2)
python3 tools/build_bundle.py --scope usa --version 1.0.2
./gradlew -PpremiumTvVersion=1.0.2 -PpremiumTvVersionCode=7 assembleDebug

# Optional 1.1.0 pre-release data (global lineup + cable-guide flag)
python3 tools/build_bundle.py --scope all --version 1.1.0
./gradlew -PpremiumTvVersion=1.1.0 -PpremiumTvVersionCode=8 assembleDebug
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
APK and commits the build output to `build-out/`:

```text
build-out/PremiumTV-1.0.2-debug.apk   stable default (debug-signed, USA scope)
build-out/PremiumTV-1.1.0-debug.apk   only when the preview version is selected
build-out/SHA256SUMS-android.txt
build-out/build-log.txt               full Gradle output
```

The workflow only attaches 1.0.2 assets to the stable `v1.0.2` release and
1.1.0 assets to the pre-release `v1.1.0` release. Only the debug APK is
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
│       ├── HomeScreen.kt        channels, guide, settings and preview tabs
│       ├── CableGuide.kt        optional 8-hour cable-style preview grid
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

- Stable 1.0.2 intentionally bundles the USA library. The 1.1.0 pre-release
  selects the checked global playlist and merged guide.
- No favourites, search, or "continue watching" — browse, play and guide only.
- The bundled guide is a snapshot of what the repository had published at
  build time. It advances automatically only when the configured raw URLs are
  publicly readable; today the private repository blocks unauthenticated TVs.
- Android may defer background work, and force-stopping the app suspends its
  WorkManager jobs until the app is opened again.
- Dead upstream links are still in the playlist until the nightly link check
  drops them, so some channels will fail to play.

## Release launch gate

After baking the actual channel assets, CI runs `testDebugUnitTest` with
Robolectric (repository/cache and parser regression tests) and builds the debug APK.
`tools/smoke_apk.py` then installs that APK on an API 30 emulator, clears app
data for a cold launch, checks the channel count and visible cards, and repeats
a relaunch. Emulator boot failures block publication rather than being counted
as app test passes. Physical TV and upstream playback checks remain manual.
