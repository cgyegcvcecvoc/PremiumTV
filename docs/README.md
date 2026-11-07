# PremiumTV download site (`docs/`)

The public download page for PremiumTV: app installers, the best working M3U
playlist per country, and the project change log. It is a static site — no
server, no build step — published with GitHub Pages.

**Live URL:** https://cgyegcvcecvoc.github.io/PremiumTV/

## What the page does

- **Download the apps.** The latest complete Stable release (currently **1.1.5** — remote-first speed and focus on Android TV, a calmer real-progress startup screen, less work while a live channel plays, and a new 30/60/90-minute sleep timer in Settings. Every asset (Android APK, macOS .dmg/.pkg for Intel and Apple Silicon), file sizes, SHA-256 checksums and install help — all linking at the GitHub release assets. The build is promoted only after its APK and all four Mac installers are published, so the page never replaces working downloads with empty links. Retired preview builds are never listed.
- **The best working M3U for your country.** The page detects the visitor's
  country in their browser (ipwho.is / ipapi.co / country.is — nothing is sent
  to us), preselects it, and offers the country's confirmed-working playlist:
  copy URL, download `.m3u`, QR code, and that country's TV-guide URL. A
  multi-country bundle builder merges any set of country playlists into one
  downloadable `.m3u` (client-side, duplicates removed).
- **Channel-lineup preview.** A **Channels** section generated from
  `playlists/PremiumTV.m3u` shows the lineup at a glance: unique channel and
  backup-feed counts, categories and countries, quality labels, recognisable
  channels, and a searchable category grid with sample names and links to the
  matching category playlists. Every number comes from the published playlist,
  so the preview cannot drift from what the apps and players actually receive.
- **Change log.** Every change recorded in [`CHANGELOG.md`](../CHANGELOG.md)
  is shown as a timeline, with an [Atom feed](data/feed.xml) readers can subscribe
  to. The page also re-fetches `docs/data/changelog.json` from the repository
  and picks up entries added after the page was deployed.

## Current stable: 1.1.5

1.1.5 is the remote-first release. D-pad focus on a channel or event card no longer recomposes the card on every frame (the 3% lift is applied in the graphics layer with a 110 ms tween), the favourite star is no longer a second focus stop on every card — hold OK to favourite, or use the side player's ★ — the rail, channel grid, tabs and Live Events rows are focus groups that keep D-pad traversal inside the shelf you are browsing, and the guide folds held-direction repeats into one cursor move at a time. The startup screen is one calm composition with a real-progress gold bar (no invented trickle, no rotating tips), live playback stops polling a clock it never displays, the Guide tab stops remapping every channel once a minute, and Coil's logo cache is capped at 10% of the heap. Settings adds a new **Sleep timer** (Off/30/60/90 minutes) whose wall-clock deadline closes the player when it arrives, and the browser now respects the phone's safe area while narrow Settings rows stack instead of squeezing their values. The full-screen player, docked side player, category rail, automatic server backup and checksum-verified updater are unchanged. The policy is documented in [`UPDATES.md`](UPDATES.md) and the release notes in [`release-notes-1.1.5.md`](../release-notes-1.1.5.md).

It installs in place over every earlier build: Android `101050000` is above
every released versionCode, and the Mac DMG replaces the old copy. Builds from
1.1.0 on (and every 1.0.4–1.0.9 build through their own updater) find 1.1.5 in
**Settings → App updates**; the downloaded installer is checksum-verified before
it is opened.

### Previous release: 1.1.4

1.1.4 declutters the full-screen Android TV player: the bottom overlay buttons (Favorite, Side player, Close and server hop) no longer cover score bugs and other on-screen graphics while a game is on, so nothing unclickable sits in front of the stream — press Back to tuck the stream into the side player or close it back to the browser. The player's own controls — Mute/Unmute and the Audio track switcher — stay in the top corner and appear on interaction, fading away on their own. macOS is unchanged: its action bar already sits below the picture instead of over it, so it keeps its Favorite, side-player, Close and server buttons. It keeps the docked side player, category rail, automatic server backup, dead-channel filtering, amber pointer outlines, and compact Settings screen — a version card that shows **1.1.4**, plus **Force refresh**, **Check for update**, **Check for bugs**, the hidden-channel restore action and a collapsible details panel. The app checks GitHub for a newer published stable release, downloads the installer once, verifies its SHA-256 checksum and opens the platform installer. The policy is documented in [`UPDATES.md`](UPDATES.md) and the release notes in [`release-notes-1.1.4.md`](../release-notes-1.1.4.md).

It installs in place over every earlier build: Android `101040000` is above
every released versionCode, and the Mac DMG replaces the old copy. Builds from
1.1.0 on (and every 1.0.4–1.0.9 build through their own updater) find 1.1.4 in
**Settings → App updates**; the downloaded installer is checksum-verified before
it is opened.

The **1.1.x Encore preview is retired**. That preview's release, installers and
download links were removed; any old link goes to
[`blocked/`](blocked/index.html), which now points at the current stable release
and explains how to replace the preview without uninstalling on Android. **The
`1.1.0` and `1.1.1` names are ordinary stable releases** — the deleted preview
shared those names, and the project promoted them back, so a device on either is
on a supported build and simply updates to 1.1.5 in-app. The Netlify Drop hub
under `hub/` uses the same complete-release gate and never renders a preview
card. Rebuild and re-upload its export to refresh an existing Netlify
deployment.

## Files

| Path | What it is |
|---|---|
| `index.html` | The page. |
| `assets/style.css`, `assets/app.js` | Styles and logic (no frameworks). |
| `assets/qrcode.js` | Vendored [qrcode-generator](https://www.npmjs.com/package/qrcode-generator) 1.4.4 (MIT) for on-page QR codes. |
| `data/site-data.js` | Generated payload (countries, counts, channel lineup, app assets, stats) loaded via `<script>` so the page works even where `fetch` is blocked. |
| `data/site.json` | The same payload for tools. |
| `data/changelog.json`, `data/feed.xml` | Generated changelog timeline + Atom feed. |
| `data/releases.src.json` | Cached GitHub release asset list; Pages refreshes it from the Releases API before building the site. |

## Regenerating the data

Every requested change is recorded in `CHANGELOG.md`, and the site data is
regenerated so the page and the feed show it. The Pages workflow also runs for
changelog/release publications and after the scheduled/manual scrape, link-check,
EPG and cleanup workflows (whose bot commits do not trigger push workflows), so
live country counts and installer links do not sit stale between deployments:

```bash
python scripts/build_site_data.py           # rewrite docs/data/*
python scripts/build_site_data.py --check   # CI-style staleness check
```

The generator is offline: it reads the playlists, reports, release notes and
change log already in the repository.

## Deployment

`.github/workflows/pages.yml` deploys this directory to GitHub Pages on every
push to `main` that touches `docs/` (and on demand via *Run workflow*).

**One manual step is needed first**, because creating a Pages site is an admin
action GitHub does not allow `GITHUB_TOKEN` or app integration tokens to
perform: open **Settings → Pages** on the repository and set **Source** to
**GitHub Actions**. The workflow retries automatically and publishes the site
from then on (its failure message above repeats these instructions).
