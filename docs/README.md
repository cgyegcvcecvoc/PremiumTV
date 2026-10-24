# PremiumTV download site (`docs/`)

The public download page for PremiumTV: app installers, the best working M3U
playlist per country, and the project change log. It is a static site — no
server, no build step — published with GitHub Pages.

**Live URL:** https://cgyegcvcecvoc.github.io/PremiumTV/

## What the page does

- **Download the apps.** The latest complete Stable release (currently **1.1.2** — a channel opens in the docked side player first and grows to full screen on one press, Movies & Shows is a working on-demand shelf, plus the category rail, automatic server backup, dead channels filtered out, amber pointer outlines and every 1.0.9/1.1.0/1.1.1 fix), with every asset (Android APK, macOS .dmg/.pkg for Intel and Apple Silicon), file sizes, SHA-256 checksums and install help — all linking at the GitHub release assets. The build is promoted only after its APK and all four Mac installers are published, so the page never replaces working downloads with empty links. Retired preview builds are never listed.
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

## Current stable: 1.1.2

1.1.2 opens every channel in the docked side player first — the picture (or **⤢ Big screen**) grows the same running stream to full screen, Back tucks it into the dock and ✕ closes it — and turns Movies & Shows into a working on-demand shelf of ten public-domain films and classic TV episodes, verified by `scripts/vod_catalog.py`. It keeps the rest of the 1.1.x line: the category rail beside the channel list, automatic server backup when a feed dies, dead channels filtered out until Settings → Restore hidden channels, the same amber outline on every focusable control, a calm loading screen with the gold loading line bar, and a compact Settings screen — a version card that shows **1.1.2**, plus **Force refresh**, **Check for update**, **Check for bugs**, the hidden-channel restore action and a collapsible details panel. The app checks GitHub for a newer published stable release, downloads the installer once, verifies its SHA-256 checksum and opens the platform installer. The policy is documented in [`UPDATES.md`](UPDATES.md) and the release notes in [`release-notes-1.1.2.md`](../release-notes-1.1.2.md).

It installs in place over every earlier build: Android `101020000` is above
every released versionCode, and the Mac DMG replaces the old copy. Builds from
1.1.0 on (and every 1.0.4–1.0.9 build through their own updater) find 1.1.2 in
**Settings → App updates**; the downloaded installer is checksum-verified before
it is opened.

The **1.1.x Encore preview is retired**. That preview's release, installers and
download links were removed; any old link goes to
[`blocked/`](blocked/index.html), which now points at the current stable release
and explains how to replace the preview without uninstalling on Android. **The
`1.1.0` and `1.1.1` names are ordinary stable releases** — the deleted preview
shared those names, and the project promoted them back, so a device on either is
on a supported build and simply updates to 1.1.2 in-app. The Netlify Drop hub
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
