# PremiumTV download site (`docs/`)

The public download page for PremiumTV: app installers, the best working M3U
playlist per country, and the project change log. It is a static site — no
server, no build step — published with GitHub Pages.

**Live URL:** https://cgyegcvcecvoc.github.io/PremiumTV/

## What the page does

- **Download the apps.** The latest complete Stable release (currently **1.1.26** — honest releases and steadier sources, on Android TV, macOS, Linux and web). Every asset (Android APK, macOS .dmg/.pkg for Intel and Apple Silicon, Linux AppImage/.deb/tarball), file sizes, SHA-256 checksums and install help — all linking at the GitHub release assets. The build is promoted only after its APK and all four Mac installers are published, so the page never replaces working downloads with empty links. Retired preview builds are never listed.
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

## Current stable: 1.1.26

1.1.26 makes the release pages honest and the sources steadier. The download page promotes only the newest complete published stable release — never a pre-release — and the stale copy that still called 1.1.4 the previous release is gone. The web player's tabs now keep real history, so Back and Forward move between Channels, Live, TV guide and Settings. Live events gain doms9's dedicated hourly events playlist, mirrored on GitHub and GitLab. Full notes: [`release-notes-1.1.26.md`](../release-notes-1.1.26.md).

It installs in place over every earlier build: Android `101260000` is above
every released versionCode, and the Mac DMG replaces the old copy. Builds from
1.1.0 on (and every 1.0.4–1.0.9 build through their own updater) find 1.1.26 in
**Settings → App updates**; the downloaded installer is checksum-verified before
it is opened.

**1.1.25 is a pre-release, not this stable line.** Its release page describes a
Spotify preview while this tree's 1.1.25 retired the Movies & Shows tab, so the
download page and the in-app updater both skip it. 1.1.26 supersedes it and
installs over it in place.

### Previous release: 1.1.24

1.1.24 adds broken-feed reports: the player error card opens a prefilled GitHub
issue with the channel, server position, URL, app version and platform, and
`playlists/HEALTH.txt` names the failing servers and channels rather than only
totals. It also files BBC America under Entertainment. Full notes:
[`release-notes-1.1.24.md`](../release-notes-1.1.24.md).

The **1.1.x Encore preview is retired**. That preview's release, installers and
download links were removed; any old link goes to
[`blocked/`](blocked/index.html), which now points at the current stable release
and explains how to replace the preview without uninstalling on Android. **The
`1.1.0` and `1.1.1` names are ordinary stable releases** — the deleted preview
shared those names, and the project promoted them back, so a device on either is
on a supported build and simply updates to 1.1.26 in-app. The Netlify Drop hub
under `hub/` uses the same complete-release gate and never renders a preview
card. Rebuild and re-upload its export to refresh an existing Netlify
deployment.

### Earlier releases

1.1.4 declutters the full-screen Android TV player only — macOS keeps its action bar below the picture — and is recorded in [`release-notes-1.1.4.md`](../release-notes-1.1.4.md).

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
