# PremiumTV download site (`docs/`)

The public download page for PremiumTV: app installers, the best working M3U
playlist per country, and the project change log. It is a static site — no
server, no build step — published with GitHub Pages.

**Live URL:** https://cgyegcvcecvoc.github.io/PremiumTV1/

## What the page does

- **Download the apps.** Stable (1.0.2) and Preview (1.1.1) release channels,
  with every asset (Android APK, macOS .dmg/.pkg for Intel and Apple Silicon),
  file sizes, SHA-256 checksums and install help — all linking at the GitHub
  release assets.
- **The best working M3U for your country.** The page detects the visitor's
  country in their browser (ipwho.is / ipapi.co / country.is — nothing is sent
  to us), preselects it, and offers the country's confirmed-working playlist:
  copy URL, download `.m3u`, QR code, and that country's TV-guide URL. A
  multi-country bundle builder merges any set of country playlists into one
  downloadable `.m3u` (client-side, duplicates removed).
- **Change log.** Every change recorded in [`CHANGELOG.md`](../CHANGELOG.md)
  is shown as a timeline, with an [Atom feed](data/feed.xml) readers can subscribe
  to. The page also re-fetches `docs/data/changelog.json` from the repository
  and picks up entries added after the page was deployed.

## Files

| Path | What it is |
|---|---|
| `index.html` | The page. |
| `assets/style.css`, `assets/app.js` | Styles and logic (no frameworks). |
| `assets/qrcode.js` | Vendored [qrcode-generator](https://www.npmjs.com/package/qrcode-generator) 1.4.4 (MIT) for on-page QR codes. |
| `data/site-data.js` | Generated payload (countries, counts, app assets, stats) loaded via `<script>` so the page works even where `fetch` is blocked. |
| `data/site.json` | The same payload for tools. |
| `data/changelog.json`, `data/feed.xml` | Generated changelog timeline + Atom feed. |
| `data/releases.src.json` | GitHub release asset list (refresh: `gh api repos/cgyegcvcecvoc/PremiumTV1/releases > docs/data/releases.src.json`). |

## Regenerating the data

Every change to the repository is recorded in `CHANGELOG.md`, and the site data
is regenerated so the page and the feed show it:

```bash
python scripts/build_site_data.py           # rewrite docs/data/*
python scripts/build_site_data.py --check   # CI-style staleness check
```

The generator is offline: it reads the playlists, reports, release notes and
change log already in the repository.

## Deployment

`.github/workflows/pages.yml` deploys this directory to GitHub Pages on every
push to `main` that touches `docs/` (and on demand via *Run workflow*). The
first run also enables Pages for the repository automatically
(`actions/configure-pages` with `enablement: true`).
