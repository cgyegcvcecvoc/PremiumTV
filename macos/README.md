# PremiumTV for Mac

A macOS app that does exactly what this repository is for — carry the checked
channel list and the TV guide **inside the app**, with nothing to configure —
packaged as a `.dmg` (drag to Applications) and a `.pkg` (installer) instead of
a script you have to run. Supports **macOS 12 (Monterey) and later**, on Intel
and Apple Silicon.

The second app build, **v1.0.0-mac2**, is built by GitHub Actions on a macOS
runner and attached to the [v1.0.0-mac2 pre-release](https://github.com/cgyegcvcecvoc/PremiumTV1/releases/tag/v1.0.0-mac2)
as `PremiumTV-1.0.0-mac2-mac-x64.dmg`, `...-arm64.dmg`, `...-x64.pkg` and
`...-arm64.pkg`, with `SHA256SUMS.txt`. It prevents overlapping refresh clicks
from causing duplicate downloads and keeps refresh failures visible in the app.
The v1.0.0-mac2 release bundle is rebuilt from the checked-in USA playlist and
guide after the manual verified repository scrape on 2026-10-12.

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
| **Guide** | "What's on now" for every channel with listings: current programme with a progress bar plus what is next. |
| **Settings** | Bundle provenance and counts, automatic-refresh state, next check, last success/result, **Force refresh all now**, and **Reset to the bundled copy**. |

Playback uses hls.js / mpegts.js behind a loopback proxy, so the referrer,
origin and user-agent a playlist entry publishes are sent — several public
feeds refuse the connection otherwise. A channel that will not play is almost
always a dead upstream link; the repository's nightly link check removes those
on its next run.

## Automatic refresh

Checks follow the repository's publishing jobs in `America/New_York`, 45
minutes after each slot, sending the last ETag/Last-Modified so an unchanged
playlist and guide cost two small `304` responses. Repeated in-flight refreshes
of the same kind are coalesced, and the Settings actions stay disabled while a
refresh is running. See `src/main/refresh-schedule.js`;
`tests/test_macos_app.py` fails the build if the in-app slots drift from
`scrape.yml` / `quick-update.yml` / `epg-build.yml`.

> **Access limitation:** this repository is private, so `raw.githubusercontent.com`
> returns an access error to an unauthenticated Mac. Refreshes report that
> result honestly and keep the bundled copy; they start working when an
> owner-approved public mirror exists. No GitHub credential is stored in the app.

## Building from source

```bash
cd macos/app
npm ci
npm run bundle     # bake playlists/countries/USA.m3u + EPG/USA.xml into resources/bundle
npm run assets     # vendor hls.js + mpegts.js into the renderer
npm test           # node unit tests + reference-builder cross-checks
npm run dist       # local .dmg/.zip (Linux can build dmg; .pkg needs macOS)
```

On macOS, `npx electron-builder --mac dmg pkg --x64 --arm64` produces both
installers and ad-hoc signs the `.app` via `tools/after-pack.cjs`.

Electron is pinned to **43.x**: Electron 44 dropped macOS 12 when Chromium did,
so while the supported floor is Monterey the major stays one behind. The floor
is declared in `electron-builder.yml` as `minimumSystemVersion: "12.0"`.
