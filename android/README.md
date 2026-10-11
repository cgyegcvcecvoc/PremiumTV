# PremiumTV — Android TV app

A leanback-first Android app that carries this repository's channel list and
TV guide inside the APK. Version **1.0.0-beta**: the first installable build.

Installs on an Android TV, Google TV, Amazon Fire TV stick, tablet or phone.
The same APK works everywhere — navigation is D-pad first, and touch works too.

## What ships inside the APK

| Data | Source in this repository | Bundled size |
|---|---|---|
| 2,158 USA channels in 59 categories | `playlists/countries/USA.m3u` | ~816 KB |
| 9,058 guide listings for 158 channels | `EPG/USA.xml` | ~3.3 MB |

Both are converted to JSON Lines by [`tools/build_bundle.py`](tools/build_bundle.py)
and streamed into the app with `android.util.JsonReader`, so a TV stick never
holds a 10 MB XML document in memory next to a video decoder.

**Why only 158 of 2,158 channels have listings:** that is what the upstream
guides actually schedule. `EPG/USA.xml` declares 1,637 channels, but only 158
have real programme data behind them. The app shows "Nothing listed at this
hour" for the rest rather than inventing a schedule.

## Screens

- **Channels** — one row per category, in the order the repository publishes
  (`Sports`, `Lifestyle`, `Fox Channels`, `CBS`, `NBC`, …). Each card shows the
  channel logo and, when the guide covers it, what is on right now.
- **Guide** — "what's on now" across every channel that has listings: current
  programme with a progress bar, plus what is next.
- **Settings** — which bundle the app is showing, refresh from the repository's
  raw GitHub URLs, or reset back to the copy bundled in the APK.

## Playback

ExoPlayer (Media3 1.4.1). HLS and progressive streams are both handled, and
when a playlist entry publishes a referrer, an origin or a user-agent through
`#EXTVLCOPT` / `#KODIPROP`, the app sends them — several public feeds refuse
the connection otherwise. Plain `http://` streams are allowed for the same
reason. A channel that will not play is almost always a dead upstream link:
the repository's nightly link check removes those on its next run.

## Refresh from GitHub

Settings → **Refresh from GitHub** downloads `playlists/countries/USA.m3u` and
`EPG/USA.xml` from `raw.githubusercontent.com` and caches them, so a refresh
survives a restart. **This repository is private today**, so that download
returns HTTP 404 and the app says so plainly instead of pretending it worked.
It starts working the moment the repository is public or mirrored somewhere
public.

## Building

The bundle is generated from the repository, so build it first:

```bash
python3 tools/build_bundle.py          # writes app/src/main/assets/bundle
./gradlew assembleDebug                # -> app/build/outputs/apk/debug/app-debug.apk
./gradlew assembleRelease              # -> app/build/outputs/apk/release/app-release-unsigned.apk
```

`app/src/main/assets/bundle/` is gitignored: it is derived data and would go
stale the moment the repository publishes a new scrape. If it is missing, the
app opens with a message telling you to run the script.

### Where the APKs come from

GitHub Actions builds them — [`.github/workflows/android-build.yml`](../.github/workflows/android-build.yml).
A plain sandbox cannot compile this project (no JDK, no Android SDK, no access
to Maven Central or `dl.google.com`). Every push that touches `android/`,
`playlists/countries/`, `EPG/` or the workflow rebuilds both APKs and commits
them to `build-out/`:

```text
build-out/PremiumTV-1.0.0-beta-debug.apk             install as-is
build-out/PremiumTV-1.0.0-beta-release-unsigned.apk  sign before publishing
build-out/SHA256SUMS.txt
build-out/build-log.txt                              full Gradle output
```

### Signing for release

The release APK is intentionally **unsigned** so it can be signed with a key
you control:

```bash
apksigner sign --ks my-release-key.jks \
  --out PremiumTV-1.0.0-beta.apk \
  build-out/PremiumTV-1.0.0-beta-release-unsigned.apk
```

To have CI sign it, add these repository secrets and the workflow will pick
them up: `SIGNING_KEYSTORE_BASE64`, `SIGNING_KEYSTORE_PASSWORD`,
`SIGNING_KEY_ALIAS`, `SIGNING_KEY_PASSWORD`.

## Project layout

```text
android/
├── app/src/main/kotlin/com/premiumtv/app/
│   ├── MainActivity.kt          entry point
│   ├── TvViewModel.kt           exposes load state and refresh/reset
│   ├── data/
│   │   ├── Model.kt             Channel, Programme, Library, LoadState
│   │   ├── Jsonl.kt             streaming reader for the bundled assets
│   │   ├── M3uParser.kt         playlist parser (mirrors build_bundle.py)
│   │   ├── XmlTvParser.kt       guide parser
│   │   └── TvRepository.kt      bundled asset + cache + network refresh
│   └── ui/
│       ├── AppRoot.kt           loading / error / home / player routing
│       ├── HomeScreen.kt        channels, guide and settings tabs
│       ├── PlayerScreen.kt      ExoPlayer + now-playing overlay
│       ├── Components.kt        D-pad correct cards, tabs, buttons
│       ├── Guide.kt             now/next helpers and clock formatting
│       └── Theme.kt             dark TV theme
├── art/app-icon.png             launcher icon source art (1024x1024)
└── tools/
    ├── build_bundle.py          repository data -> app assets
    └── make_icons.py            art -> mipmap folders
```

## Known limits of the beta

- USA library only; the world library (9,864 channels) is not bundled yet.
- No favourites, search, or "continue watching" — browse, play and guide only.
- The bundled guide is a snapshot of the ~2 days the repository had published
  when the APK was built; it does not advance until you refresh or update.
- Dead upstream links are still in the playlist until the nightly link check
  drops them, so some channels will fail to play.
