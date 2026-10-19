# PremiumTV download site (`docs/`)

The public download page for PremiumTV: app installers, the best working M3U
playlist per country, and the project change log. It is a static site — no
server, no build step — published with GitHub Pages.

**Live URL:** https://cgyegcvcecvoc.github.io/PremiumTV1/

## What the page does

- **Download the apps.** The latest complete Stable release (currently 1.0.6.1 —
  Settings 2.0 + built-in bug check), with every asset (Android APK, macOS
  .dmg/.pkg for Intel and Apple Silicon), file sizes, SHA-256 checksums and
  install help — all linking at the GitHub release assets. The build is
  promoted only after its APK and all four Mac installers are published, so the
  page never replaces working downloads with empty links. Retired preview
  builds are never listed.
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

## Current stable: 1.0.6.1

Settings is now one compact screen: a version card, **Force refresh**, **Check
for update**, **Check for bugs**, and a collapsible details panel. The app
checks GitHub for a newer published stable release, downloads the installer
once, verifies its SHA-256 checksum and opens the platform installer. The
policy is documented in [`UPDATES.md`](UPDATES.md).

The **1.1.x Encore preview is retired and blocked**. Its release, installers and
download links were removed; any old link goes to
[`blocked/`](blocked/index.html), which points at 1.0.6.1 and explains how to
replace the preview without uninstalling on Android. The Netlify Drop hub under
`hub/` uses the same complete-release gate and no longer renders a preview
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
