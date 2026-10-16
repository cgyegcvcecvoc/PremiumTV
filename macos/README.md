# PremiumTV for Mac

A macOS app that does exactly what this repository is for — carry the checked
channel list and the TV guide **inside the app**, with nothing to configure —
packaged as a `.dmg` (drag to Applications) and a `.pkg` (installer) instead of
a script you have to run. Supports **macOS 12 (Monterey) and later**, on Intel
and Apple Silicon.

The release workflow prepares two separate channels:

- **1.0.3 stable build target (default):** USA playlist + USA guide. The
  published `v1.0.2` release stays available until all 1.0.3 installers are
  published.
- **1.1.1 pre-release:** global checked playlist + merged guide, and the Guide
  tab is a **cable-style grid**. This must be published with GitHub's
  pre-release flag; it never becomes the default build. (1.1.1 supersedes the
  1.1.0 preview, whose grid sat in a separate Cable tab.)

The current stable download is `v1.0.2`; the 1.1.x builds are pre-releases.
Once `v1.0.3` has its Android APK and all four Mac installers, the site promotes
it as the recommended stable download. Mac CI rebuilds both architectures from
the current checked USA playlist and guide whenever app, country-playlist,
bundle-tool or EPG inputs change. The latest main-branch scrape and follow-up
deep check on October 16, 2026 leave 2,705 published USA entries; refresh the
release build after any later data run.
Installers are named `PremiumTV-<version>-mac-x64.dmg`,
`...-arm64.dmg`, `...-x64.pkg` and `...-arm64.pkg`, with
`SHA256SUMS-macos.txt`. Third-party playback still depends on upstream feeds;
the installers are ad-hoc signed, not notarized.

## Installing

1. Download the `.dmg` for your architecture (Apple Silicon = `arm64`).
2. Open it and drag **PremiumTV** to Applications — or double-click the `.pkg`.
3. The build is ad-hoc signed, not notarized, so on first launch macOS will
   refuse to open it. Either right-click the app and choose **Open**, or run:

   ```bash
   xattr -dr com.apple.quarantine /Applications/PremiumTV.app
   ```

4. Open **PremiumTV**. The Channels list appears immediately from the bundled
   copy.

## What it does

| Screen | Behaviour (mirrors the Android app) |
|---|---|
| **Channels** | One card per channel, grouped in the repository's published category order (`Sports`, `Lifestyle`, `Fox Channels`, …). Each card shows the logo and, when the guide covers it, what is on right now. |
| **Guide (1.1.1 preview)** | A cable-style grid: channels down the left (sticky), each channel's shows to the right sized by running time, half-hour times across the top (sticky) for eight hours, a red NOW line and time pill, category headings, and a detail strip for the show under the pointer or keyboard focus. The sidebar categories filter it, search finds a channel or show, arrow keys move through it keeping the time column, click or Enter plays. Enabled by the bundle inside the .app (`cable-guide`), never by downloaded data. |
| **Guide (stable 1.0.3)** | "What's on now" for every channel with listings: current programme with a progress bar plus what is next. |
| **Settings** | Bundle provenance and counts, library scope/preview features, automatic-refresh state, next check, last success/result, **Force refresh all now**, and **Reset to the bundled copy**. |

Playback uses hls.js / mpegts.js behind a loopback proxy, so the referrer,
origin and user-agent a playlist entry publishes are sent — several public
feeds refuse the connection otherwise. An upstream feed may be unavailable or
refuse this connection; retrying the same feed will not necessarily help. Close the player to browse other channels.

## Automatic refresh

Checks follow the repository's publishing jobs in `America/New_York`, 45
minutes after each slot, sending the last ETag/Last-Modified so an unchanged
playlist and guide cost two small `304` responses. See
`src/main/refresh-schedule.js`; `tests/test_macos_app.py` fails the build if
the in-app slots drift from `scrape.yml` / `quick-update.yml` / `epg-build.yml`.

Refreshes download from the public repository on `raw.githubusercontent.com`;
no account or credential is involved. A downloaded copy remembers the version
and library scope it was refreshed for: when a different build is installed
over it, the copy and its validators are discarded on the next start, so the
new build's bundled lineup and Guide show immediately.

## Building from source

```bash
cd macos/app
npm ci
npm run bundle     # stable default: USA playlist + USA guide
npm run assets     # vendor hls.js + mpegts.js into the renderer
npm test           # unit tests + parser and preview-guide regression coverage

# Build preview data explicitly; the app version is selected by the workflow.
PREMIUMTV_SCOPE=all PREMIUMTV_VERSION=1.1.1 npm run bundle
npm run dist       # local .dmg/.zip (Linux can build dmg; .pkg needs macOS)
```

On macOS, `npx electron-builder --mac dmg pkg --x64 --arm64` produces both
installers and ad-hoc signs the `.app` via `tools/after-pack.cjs`.

Electron is pinned to **43.x**: Electron 44 dropped macOS 12 when Chromium did,
so while the supported floor is Monterey the major stays one behind. The floor
is declared in `electron-builder.yml` as `minimumSystemVersion: "12.0"`.

## Release launch gate

CI launches each packaged executable with `--smoke-test` using an isolated
throwaway user-data directory. It deliberately lets the renderer take an empty
snapshot before loading the real bundle, then verifies channels, the bridge,
vendored players, refreshed rows and reset. This does not fetch third-party
live streams or replace manual testing on supported macOS versions.
