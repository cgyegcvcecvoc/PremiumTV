# PremiumTV Web

**Your browser. Your television.** An independent static web edition of PremiumTV, not an Android/macOS release. Its own package version starts at `0.1.0`; the repository's native `VERSION` and release/tag/updater machinery are untouched.

## Run locally

Requires Node 20+ and Python 3.10+ (CI uses Node 22 / Python 3.12). No Python packages, Electron, account, API key or backend are needed.

```sh
cd web
npm ci
npm run build
npm start                 # http://localhost:3000
PORT=8080 npm start        # optional different port
```

The preview server binds `0.0.0.0` for the Arena proxy. All browser asset/data URLs are relative. There is no browser-to-localhost API call and no stream proxy.

## What is included

- Collapsible official viewing links for local news, public programming and sports; these open provider sites, not in-player feeds or automatic backups. Provider availability, subscriptions and blackout rules vary.
- The current checked USA channel library and published category order; category pages, search across name/category/country/channel number, sorting and incremental rendering (60 channel cards at a time).
- Favorites, recently watched, seven-day failed-feed memory and restore/clear controls. Storage failures fall back to session memory.
- Lazy-loaded XMLTV guide with on-now/next, progress, category/search filters and a horizontally scrollable six-hour timeline. Missing/stale listings are not invented.
- Live-event grouping, team badges and multi-server selection (kickoffs are omitted until a verified source is available), using the native apps' pure event logic. **Listed feeds are not labeled LIVE until played.** Browser CORS makes the native apps' arbitrary server probes unreliable, so the web UI does not pretend an opaque response proves playback.
- A **Movies & Shows** tab that currently shows a coming-soon page: the shared on-demand catalogue is paused while it is reworked. The title/genre/type filters, native MP4 playback, ±10-second controls, seeking and per-browser resume remain in the player for the catalogue's return.
- A persistent docked player that expands without replacing the video element; native fullscreen where available, picture-in-picture/AirPlay when the browser exposes them, mute/volume, audio-track selection and automatic/manual backup servers.
- Native inline HLS on iPhone/iPad, lazy HLS.js on MSE browsers, MPEG-TS.js only where supported. Playback begins from the user's tap; blocked autoplay gets an explicit play button.
- Persisted wall-clock sleep timer (30/60/90 minutes), 11 read-only diagnostics, library refresh, source/privacy details and an M3U download.
- Installable web-app manifest, home-screen instructions, offline app-shell/library cache and a no-JavaScript channel directory. **Offline mode does not make live streams available.** Suspended mobile browsers check the sleep deadline when resumed; the web cannot guarantee a background timer fires while the OS freezes the page.

The build copies `category-icons.js`, `live-events.js`, `personal.js` and `health.js` **unchanged** from the macOS renderer, and uses `android/tools/build_bundle.py` for M3U/XMLTV parsing. Web-specific storage, playback and responsive UI stay in `web/`; native source files are not edited.

## Honest browser compatibility

Target: current Safari (including iOS), Chrome, Edge, Firefox and other browsers with HTML5 video. The lightweight directory remains usable without JavaScript or modern APIs. There is no Electron-only API, framework, remote font, analytics service or mandatory service worker.

A playlist check is not a browser-playback guarantee. Providers may:

- deny cross-origin manifest/segment requests (CORS);
- require a particular Referer, Origin or User-Agent (browsers forbid setting these arbitrarily);
- publish HTTP streams that an HTTPS page blocks as mixed content;
- use AC-3/E-AC-3, DTS or other codecs the device cannot decode;
- go offline after the repository's last check.

The player tries available strategies and backup servers, then shows an actionable error and original-feed link. It never uses `no-cors` as a fake health check or routes arbitrary streams through an open proxy. Use the native apps for the broadest feed compatibility. AirPlay, PiP and fullscreen are feature-detected, not promised on every browser.

## Build and deploy separately from native releases

```sh
npm ci
npm test
npm run build
python3 tools/verify_export.py
npx playwright install --with-deps chromium webkit
WEBKIT_TESTS=1 npm run test:browser
```

`dist/` is the complete static site. Upload its **contents** to any static HTTPS host. For a standalone deployment use `web/` as the project root, `npm ci && npm run build` as the build command and `dist` as the publish directory. No environment variables or secrets are required. A plain static host works; `tools/serve.cjs` is an optional Node host with gzip, range requests and `/healthz`.

For nginx, serve `dist` as a normal static root. HTTPS is required for service workers/installability (localhost is exempt). Serve `.js` as JavaScript, `.json` as JSON, `.webmanifest` as `application/manifest+json`, and support MP4 Range requests. Do not rewrite missing API routes; there is no API. Pre-compressed `.gz` copies are optional; the included Node server uses them when the client accepts gzip.

### GitHub Pages

The existing download-site workflow builds this app into the ignored `docs/web/` directory and publishes it at:

**https://cgyegcvcecvoc.github.io/PremiumTV/web/**

That URL becomes live only after these changes reach `main` and the Pages workflow succeeds. The download page links to the web app separately from its native installer cards. GitHub Pages permits one site per repository, so this is a separate path/artifact within that site, **not a separate native release**. For a completely separate domain, upload `dist/` to another static host instead.

`.github/workflows/web-build.yml` runs unit tests, Chromium/touch/real WebKit smoke tests and export checks, then uploads `premiumtv-web-static`. It never creates a GitHub Release, changes `VERSION`, signs an installer or dispatches a native build. Data-publisher completions and manual dispatch can rebuild it independently.

### Refresh and cache policy

The web library is a deployment snapshot of the repository, not a live scrape executed in the visitor's browser. The existing Pages data triggers rebuild it after playlist/guide publications. **Refresh library** bypasses the HTTP cache and validates a new channel/group pair before replacing the old one. It does not claim to fetch unpublished repository changes.

Application/data URLs carry a content build ID. The service worker caches only same-origin public app/data files, never streams, logos or viewing history. A new build gets a new cache; old PremiumTV caches are removed on activation. **Reload web app** stops playback, clears this app's caches and reloads the deployment. Native app updates are never downloaded here.

## Tests and artifacts

- `npm test`: storage/sorting/search/resume/sleep/validation, diagnostics, shared native policies, iOS playback strategy selection and static-server gzip/range/path safety.
- `npm run test:browser`: desktop Chromium and iPhone-sized touch emulation by default; `WEBKIT_TESTS=1` adds real Playwright WebKit. Tests cover the Movies & Shows coming-soon page, player mode changes, personal shelves, guide/live listings, offline reload, diagnostics and honest provider failures.
- `tests/test_web.py` in the repository's Python suite: offline source/export isolation and native-release separation checks.
- `CHROMIUM_PATH` can point Playwright at a preinstalled compatible Chromium binary; normal CI installs its own engines.

Generated `dist/`, `node_modules/`, browser traces/reports and `docs/web/` are ignored. Only source, lockfile, tests and documentation belong in Git. The static artifact is roughly 13 MB including optional gzip copies; the channel payload is about 174 KB gzipped and the guide about 1.1 MB gzipped and lazy-loaded.

## Pull-request checks

Repository-owned gates are **Repository checks** (offline Python suite, version
sync, playlist/EPG/shelf invariants) and **PremiumTV Web checks and static
artifact** (Node tests, static export, Chrome desktop/touch, real WebKit, and
export isolation). Run them locally with:

```sh
python -m unittest discover -s tests
cd web
npm ci
npm test
npm run build
python tools/verify_export.py
npx playwright install chromium webkit
WEBKIT_TESTS=1 npm run test:browser
```

The Cloudflare **Workers Builds: premiumtv1** check is configured in the
Cloudflare dashboard, not in this repository (there is no Wrangler config here).
Its branch/preview build is an external deployment setting; a failure there does
not indicate a failing web export. Fix or disable that preview build in
Cloudflare Workers → premiumtv1 → Settings → Builds. Netlify deploy previews are
also external; the three Netlify rule checks may report “skipped/neutral” when
no rules changed.
