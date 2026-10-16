# PremiumTV Download Hub (self-hosted)

A standalone download site for everything in this repository — **no GitHub Pages,
no GitHub Actions**. One Python process serves the page and every artifact:

- **Apps** — all Android TV / Fire TV APKs served straight from `build-out/`
  (with SHA-256 checksums computed at build time); macOS DMG/PKG installers link
  to the public GitHub release-asset URLs (direct browser downloads, no Pages).
- **Playlists** — the main playlist, USA lineup, priority/A&E lists, all 175
  country M3Us, and all three category shelves, each downloadable and with a
  copy-able permanent raw URL for IPTV players.
- **TV guides** — merged XMLTV guide (plain + gzip), the USA guide, and every
  per-country guide from `EPG/` (surfaced on each country card).
- **Bundles** — zips rebuilt by `build_data.py`: all countries, all categories,
  the USA pack, core playlists, and all EPGs.
- **Directions** — step-by-step setup for Fire TV, Android TV, macOS, VLC,
  TiviMate/Smarters, and Kodi, plus an About section.

## Run it

```bash
python3 hub/build_data.py   # scan the repo, hash APKs, build zips + dist/data.json
python3 hub/server.py 8000  # serve on 0.0.0.0:8000
```

Pure Python stdlib — no dependencies. Re-run `build_data.py` whenever playlists
or builds change; the server picks the new data up immediately.

## Layout

| Path | What |
|---|---|
| `server.py` | Threaded HTTP server: static front-end + whitelisted `/get/<zone>/…` file routes with Range support, traversal protection, and an extension allowlist. |
| `build_data.py` | Scans `playlists/`, `categories/`, `EPG/`, `build-out/`; counts channels, hashes APKs, zips bundles, writes `dist/data.json`. |
| `static/` | The site (single page: `index.html`, `assets/style.css`, `assets/app.js`, hero art). |
| `dist/` | Generated data + bundles (git-ignored; rebuild with `build_data.py`). |

> The sandbox this hub was built in cannot reach GitHub's release-asset CDN,
> so macOS installers are linked rather than mirrored. To fully self-host them,
> drop the DMG/PKG files into `hub/dist/mac/` and add a `mac` zone in
> `server.py` + entries in `build_data.py`.
