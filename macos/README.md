# PremiumTV for Mac

A macOS app that does exactly what this repository is for — carry the checked
channel list and the TV guide **inside the app**, with nothing to configure —
packaged as a `.dmg` (drag to Applications) and a `.pkg` (installer) instead of
a script you have to run. Supports **macOS 12 (Monterey) and later**, on Intel
and Apple Silicon.

The release workflow prepares one published channel:

- **1.1.2 stable build (default):** USA playlist + USA guide. A channel opens
  in the docked side player and one click on the picture grows it to the full
  window, and **Movies & Shows** is a working on-demand shelf of public-domain
  films and classic TV episodes (bundled from `playlists/vod/vod-catalog.json`).
- **1.0.9 (superseded):** USA playlist + USA guide,
  with the animated launch splash (breathing gold halo, sweeping shimmer bar,
  pulsing dots), the compact Settings screen, the hardened bug check (11 checks:
  patch chain, stream hygiene, guide freshness, library health plus the original
  7), category placeholder logos, the Live Events tab and automatic multi-server
  playback. 1.0.4 was the last release that needed a manual download; from
  there on Settings → App updates checks GitHub, downloads the DMG for this Mac
  once, verifies its SHA-256 checksum, and opens the installer. 1.0.9 is the
  crash-on-watch fix (an Android player defect; the Mac player was unaffected,
  but its packaged smoke test now opens a channel too). The V-patch/alias
  scheme is retired: 1.0.8.1 was the only V patch, and fixes now take the next
  plain version.
- **The 1.1.x preview is retired.** Its release, installers and download links
  were removed; the `cable-guide` bundle scope still exists for a future
  experimental build, but no preview is published. An installed 1.1.x build
  sees a blocked-build notice and is sent to
  [`docs/blocked/`](../docs/blocked/index.html).

The current stable download is `v1.1.2`. (Historically, `v1.0.8.1` — shown as
**1.0.8 V1 Patch** — was packaged as `1.0.9` on macOS and briefly published as a
same-code alias release so the three-part updater in 1.0.4–1.0.6 could find it;
the fixed 1.0.9 replaced that build, so a Mac already reporting 1.0.9 should
reinstall from the current `v1.0.9` release to get the fixed code.) Only a published
full release above the installed version is offered, and a downloaded DMG is
reused until it is installed. Mac CI rebuilds and smoke-tests both architectures
against the current checked USA playlist and guide whenever app,
country-playlist, bundle-tool or EPG inputs change. Refresh the release build
after any later data run.
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
| **Channels** | One card per channel, grouped in the repository's published category order (`Sports`, `Lifestyle`, `Fox Channels`, …). Each card shows the logo — or its category's drawn placeholder (a ball for Sports, a smile for Comedy, a TV set for the rest) — and, when the guide covers it, what is on right now. |
| **Live Events** | The scrapers' live-game feeds grouped by sport (Soccer, American Football, College Football, NHL Hockey, …): matchup, LIVE pill and stream count per card. A game with several streams, and any channel with backup feeds, switches to the next server automatically when one feed dies; a badge shows which server is playing. |
| **Guide (optional cable bundle)** | A cable-style grid: channels down the left (sticky), each channel's shows to the right sized by running time, half-hour times across the top (sticky) for eight hours, a red NOW line and time pill, category headings, and a detail strip for the show under the pointer or keyboard focus. The sidebar categories filter it, search finds a channel or show, arrow keys move through it keeping the time column, click or Enter plays. Enabled by the bundle inside the .app (`cable-guide`), never by downloaded data. |
| **Guide (stable 1.0.8 V1)** | "What's on now" for every channel with listings: current programme with a progress bar plus what is next. Live-game feeds join the list with their matchup as the listing. |
| **Settings** | One compact version/stat card (shows **1.0.8 V1 Patch** for 1.0.8.1), then **Force refresh**, **Check for update** and **Check for bugs** (now 11 checks), a single status line, a collapsible bug report, App updates, and a Details panel with sources, URLs, refresh state and **Reset to bundled copy**. |

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

## The update popup

`src/main/update-notice.js` is the same policy the Android app implements in
`UpdateNotice.kt`, reading the same published `app-update-notice.json` from the
root of the repository. `AppUpdater` fetches it during the daily check, caches it
in `update-state.json`, and resolves the popup for this build before any network
call — so it appears at startup, offline included.

The renderer paints it into `#update-notice` with `textContent` only: the wording
is remote, so it is never parsed as HTML. Esc and the dismiss button hide it for
this launch; the dismissal is deliberately kept out of the state file, so the
notice returns every launch until PremiumTV is updated. Once the published
`support_ends_utc` passes, the same rule escalates to its end-of-support wording
and turns red without a new build.

`src/main/parsers.js` drops an entry marked `tvg-notice="app-update"` — the
sanctioned notice row in the frozen legacy feed, aimed at builds too old to carry
a popup. See [`../docs/UPDATES.md`](../docs/UPDATES.md).

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
npm test           # unit tests + parser and cable-guide regression coverage

# Build the optional global bundle explicitly (no preview is published).
PREMIUMTV_SCOPE=all npm run bundle
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
