# PremiumTV — Android TV app

A leanback-first Android app that carries this repository's channel list and
TV guide inside the APK. The default build target is **1.1.4**
(`versionCode` `101040000`) with the USA lineup: a channel opens in the docked
side player with built-in transport and audio-track controls and one press on
the picture goes full screen, an expanded **Movies & Shows** on-demand shelf of
public-domain films and classic TV with search and genre pills, FFmpeg broadcast
audio decoding (`AC-3`, `E-AC-3`, `DTS`, `MP2`), a moving gold startup loading
bar, channel search, category placeholder logos, a **Live Events** tab grouped
by sport with team crests and kickoff countdowns, automatic multi-server
playback, and a compact Settings screen with **Force refresh**, **Check for
update** and an expanded **Check for bugs** (11 checks). 1.1.4 installs over
1.1.3 and every earlier build, including the retired 1.1.x preview. 1.0.9 is the crash-on-watch fix: earlier, opening a channel could
freeze on black after a server fallback because the video surface stayed
attached to a released player; the player now lives for the whole watch
screen. (1.0.9 briefly existed as the same-code alias of 1.0.8.1; that
scheme is retired — see the version policy below.)

Versions and versionCodes come from one policy, `scripts/release_version.py`.
Versions are `MAJOR.MINOR.PATCH`; the code is
`MAJOR * 100000000 + MINOR * 1000000 + PATCH * 10000 + HOTFIX`, so `1.0.9`
is `100090000` — above `1.0.8.1` (the one historical V patch, `100080001`),
1.0.8 and the retired preview's `100010001`. Four-part "V patch" versions
are retired: the parser still reads them so old tags resolve, but no new
one is ever published — a fix takes the next plain version.
Only a published full release above the installed version is offered, and a
stable release that is not above the current stable is converted to a
pre-release by the release guard. Each published version carries an APK signed
with the long-lived update key in `android/keystore/` (verified against a
pinned certificate on every build), so the next release installs in place from
Settings. Builds before 1.0.4 used a fresh random debug key on every CI run, so
upgrading from one of those needs one uninstall + install; 1.0.4 onward update
in place.

Installs on an Android TV, Google TV, Amazon Fire TV stick, tablet or phone.
The same APK works everywhere — navigation is D-pad first, and touch works too.

## What ships inside the APK

| Build | Source playlist | Source guide | Bundle metadata |
|---|---|---|---|
| **1.0.9 build target (default)** | `playlists/live/USA.m3u` | `EPG/USA.xml` | `library_scope: usa`; no optional features · crash-on-watch player fix; animated splash + hardened bug detection from 1.0.8.1 |

Both scopes are converted to JSON Lines by [`tools/build_bundle.py`](tools/build_bundle.py)
and read with `android.util.JsonReader`. This keeps the large XML source off the
TV's memory while channel playback is active. GitHub Actions generates the
bundle at build time, so the installed app never needs Python or another tool.
The `all` scope remains available to a future experimental dispatch; it does not
change the stable default and no published release uses it today.

**How many channels have listings:** the merged guide declares every channel
the playlists publish, and real programme listings are attached to every
channel a verified upstream guide schedules. The per-country curated feeds
(iptv-epg.org's `epg-us.xml` family and epg.pw's `epg_US` family, merged ahead
of everything else) carry the long tail of FAST and international channels.
Channels no public guide schedules show "Nothing listed at this hour" or
"No listing" rather than an invented schedule; the current counts are in
[`playlists/checks/EPG-BUILD.md`](../playlists/checks/EPG-BUILD.md).

## Screens

- **Launch splash** — the drawn PremiumTV television mark with a breathing
  gold halo, sweeping shimmer bar and pulsing dots, plus the build's version
  pinned at the bottom while the library loads.
- **Channels** — one row per category, in the order the repository publishes
  (`Sports`, `Lifestyle`, `Fox Channels`, `CBS`, `NBC`, …). Each card shows the
  channel logo — or its category's drawn placeholder when it has none — and,
  when the guide covers it, what is on right now. A search field above the rows
  filters by name, category, country or channel number.
- **Live Events** — the scrapers' live-game feeds grouped by sport (Soccer,
  American Football, College Football, NHL Hockey, …): each card shows the
  matchup, a LIVE pill and how many streams carry it. A game with more than one
  stream, and any channel with backup feeds, switches to the next server
  automatically when one feed dies.
- **Guide (optional cable-style bundle)** — a cable-style grid: channels down the left
  (number, logo, name, category), each channel's shows to the right sized by
  running time, half-hour times across the top for eight hours, a red NOW line,
  category headings, and a detail strip for the highlighted show. The grid is
  one focus stop with a cable-box highlight ([`GuideModel.kt`](app/src/main/kotlin/com/premiumtv/app/ui/GuideModel.kt)):
  ▲▼ keep the time column, ◀▶ step one show, OK watches, Back from the player
  returns to the same show, ▲ from the first row returns to the tabs, CH+/CH−
  page, and the remote's GUIDE key opens it. Touch drags both ways; tap plays.
  It is enabled by the APK's own bundle (`cable-guide`), never by downloaded
  data, and the published stable 1.0.8 build does not enable it.
- **Guide** — "what's on now" across every channel that has
  listings: current programme with a progress bar, plus what is next. The
  live-game feeds join the list with their matchup as the listing.
- **Settings** — one compact version card (installed version, scope, counts,
  build date), **Force refresh**, **Check for update**, **Check for bugs**,
  a collapsible Details panel with sources/URLs/refresh state and Reset, and
  **App updates**: newest stable release, one-time verified download, install.

## App updates

Settings → App updates is the only place a release is downloaded. The manager
keeps its state in `premiumtv_app_update` preferences and exactly one verified
APK in `files/updates/`. It checks GitHub at most once a day (with an ETag, so
an unchanged list is a `304`), ignores drafts and pre-releases, and requires
the release's exact `PremiumTV-<version>-debug.apk` to be attached. The
downloader verifies `SHA256SUMS-android.txt` before keeping the file; a second
press reuses it instead of downloading again. Installation goes through a
one-file `FileProvider` and Android's normal package installer, so the user
confirms the update. Android 8+ may ask once for permission to install unknown
apps. See [`docs/UPDATES.md`](../docs/UPDATES.md).

## The update popup

Settings is where an update is managed; the popup is where an out-of-date build
is told. `UpdateNotice` resolves `app-update-notice.json` — published at the root
of the repository and read from `main` during the same daily check — against this
APK's version, and `AppRoot` shows `UpdateNoticeDialog` above every screen except
the player.

The document decides the wording, the targeted version range, and the
end-of-support date, so all three can change without another release. The popup
is dismissible (a remote can arrive mid-evening, and an app that refuses to run
turns "please update" into "your TV is broken"), but the dismissal is launch-scoped
and never written to `SharedPreferences`, so the notice returns every launch. The
document is cached, so the popup is decided before any network call and still
appears offline. On the day `support_ends_utc` passes, the same rule escalates to
its `after_support_ends` wording and turns its accents red by itself.

A notice that cannot be read, is oversized, or names a schema this build has never
seen keeps the last good copy and can never fail the update check that already
succeeded. **Update now** opens Settings and re-checks GitHub; the installer still
downloads only on the Settings button.

`M3uParser` also drops an entry marked `tvg-notice="app-update"` — the sanctioned
notice row `scripts/legacy_sunset.py` puts in the frozen legacy feed for builds
too old to carry a popup. It is a message, never a channel.

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

Settings → **Force refresh** bypasses those validators and downloads the
playlist and guide named in the installed bundle metadata (USA for stable). It is an app-side data refresh
from the public repository; it never runs GitHub Actions. The guide is parsed
as it downloads (the global XML is ~38 MB), keeping only listings for channels
in the playlist.

A downloaded copy remembers the version and library scope it was refreshed
for. When a different APK is installed over it (1.0.6 → 1.0.6.1, say), the old
copy and its validators are discarded on the next start, so the new build's
bundled lineup and Guide show immediately.

## Building

The bundle is generated from the repository, so build it first:

```bash
# Stable build target (USA, 1.0.9, versionCode 100090000)
python3 tools/build_bundle.py --scope usa --version 1.0.9
./gradlew -PpremiumTvVersion=1.0.9 -PpremiumTvVersionCode=100090000 assembleDebug
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
build-out/PremiumTV-1.0.8-debug.apk     stable build (debug-signed, USA scope)
build-out/SHA256SUMS-android.txt
build-out/build-log.txt               full Gradle output
```

The workflow attaches an APK only to the release tag that points at the exact
commit it built. Stable tags (`v1.0.4` and later) are full releases. Only the debug APK is
published; an unsigned release APK cannot be installed on a TV or phone.

### Installing on a TV

1. Copy `PremiumTV-1.0.6.1-debug.apk` to the TV (USB stick, a file-sharing
   app, or `adb install -r PremiumTV-1.0.6.1-debug.apk` from a computer).
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
│   │   ├── UpdateNotice.kt        the published "go and update" notice policy
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

- The stable build intentionally bundles the USA library. The 1.1.x
  pre-releases select the checked global playlist and merged guide.
- No favourites or "continue watching" — browse, search, play and guide only.
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
for a large optional bundle (~21 MB of assets against ~6 MB for the stable USA
bundle), so a slow dump is retried instead of failing the build; a real failure
writes `build-out/smoke-log.txt`, which branch builds publish. Emulator boot
failures block publication rather than being counted as app test passes.
Physical TV and upstream playback checks remain manual.

### Stable build publication

Ordinary pushes and manual builds default to stable `1.0.9`
(Android code 100090000). The V-patch/compatibility-alias scheme is retired:
publish one three-part release and no twin. (Historically, `1.0.7` was the
alias of `1.0.6.1`, and `1.0.9` briefly of `1.0.8.1`; the alias mapping for
1.0.7 remains in the policy so those tags still resolve.)
The `[preview-build]` switch and `.github/preview-build.txt` were removed when
the 1.1.x preview channel was retired; there is no preview build to dispatch.
Both platform workflows build the stable lineup and retain their normal smoke
gates. Every release attachment remains exact-SHA guarded, and
per-platform BUILD-SOURCE manifests record the commit and Actions URL.
