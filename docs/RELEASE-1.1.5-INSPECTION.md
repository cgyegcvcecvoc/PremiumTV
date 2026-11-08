# PremiumTV 1.1.5 — repository inspection and readiness notes

**Inspection date:** 2026-11-08
**Working branch:** `arena/35971af4-premiumtv`
**Scope:** manual source/history review and Android 1.1.5 readiness follow-up. No playlist or EPG scrape was run; generated channel data was left untouched.

## What PremiumTV is

PremiumTV is a self-refreshing IPTV project with a data pipeline, two clients and a download site. The pipeline combines enabled public playlist sources, normalizes and deduplicates streams, probes their availability, builds channel categories and XMLTV programme listings, then publishes M3U playlists, guides and health/run-history reports. Android and macOS clients bundle a library so they can open before a refresh succeeds, then keep a downloaded copy current. The GitHub Pages site promotes only complete releases and data artifacts.

## Architecture map

| Layer | Main paths | Responsibilities / stack |
|---|---|---|
| Data pipeline | `scripts/scraper.py`, `categorize.py`, `link_check.py`, `epg_build.py`, `verify_playlists.py`, `build_site_data.py` | Python 3, primarily standard library. Fetches configured sources; normalizes, checks and categorizes streams; compiles XMLTV; applies publication safety checks; generates site data. |
| Published data | `playlists/`, `categories/`, `EPG/` | Main and per-country/per-category M3U files, the category shelf, merged/per-country XMLTV guides, run history and health reports. Android and Mac bundle builders consume the same published sources. |
| Shared bundle | `android/tools/build_bundle.py`; Android `data/` | Packages channel, group, guide and metadata snapshots. Android reads JSONL snapshots and can publish channels before the guide finishes parsing. |
| Android client | `android/app/src/main/kotlin/com/premiumtv/app/` | Kotlin + Jetpack Compose. `MainActivity` hosts `AppRoot`; `TvViewModel` coordinates flows/background actions; `TvRepository` loads a bundled or refreshed library; `HomeScreen` composes category/channel shelves, Events, VOD, Guide and Settings; `PlayerScreen` uses Media3/ExoPlayer with backup-feed and audio-track recovery. Coil handles artwork; WorkManager schedules refresh; the updater verifies packages against the pinned signing key. Targets Android TV/Google TV/Fire TV and touch devices. |
| macOS client | `macos/app/src/main/`, `src/renderer/` | Electron. The main process owns repository, updater, IPC and local stream proxy; the renderer is HTML/CSS/JavaScript and uses native playback, hls.js and mpegts.js strategies. |
| Download site | `docs/`, `hub/`, `scripts/build_site_data.py` | GitHub Pages metadata and download links. The release-data generator waits for a complete set of version-matched installers before promoting a stable version. |
| Automation | `.github/workflows/` | CI, scheduled scrape/guide jobs, Android emulator smoke gate, macOS builds, Pages deployment and a manual release-publish workflow. |

### Core user functionality

- Browse channel categories and a lazy channel grid; search, sort, mark favourites and revisit recent channels.
- Open a docked or full-screen live player with backup-server failover, programme details and multi-track audio recovery.
- Browse live/upcoming events, Movies & Shows, and a channel guide; use Settings for refresh, diagnostics, app updates and the sleep timer.
- Continue from bundled data offline or during a failed refresh; a successful refresh is stored locally and re-used on subsequent launches.

## 1.1.5 release facts

- `VERSION` is `1.1.5`; Android version code is `101050000`; `macos/app/package.json` is `1.1.5`; version synchronization is enforced by `scripts/version_sync.py`.
- The detailed release contract is [`release-notes-1.1.5.md`](../release-notes-1.1.5.md). The merged release-preparation PR is #114 (`Release/1.1.5`). Its relevant commit headlines cover Android TV input/smoke-gate fixes, a supported forced-null-root switch for the emulator smoke test, and choosing an on-screen channel in that gate. PR #113 immediately before it widened backup-feed coverage.
- **Publication check:** at this inspection, GitHub listed `v1.1.4` as Latest; `v1.1.5` had no tag or published release. The 1.1.5 source surfaces and release notes are prepared in-tree, not yet published. `docs/data/releases.src.json` intentionally remains at v1.1.4 until a release is actually published. The local clone is shallow (the checked-out commit is `e239b3b`, the #114 merge), so the GitHub PR/API history was consulted for context.
- `.github/workflows/publish-release.yml` is a manual, guarded action. It checks the version and notes, refuses an existing tag, creates the release from `main`, then dispatches Android/macOS builds and waits for all expected installers before requesting the Pages refresh. This branch's code must merge before that publish workflow can build the complete release.

## Previously prepared for 1.1.5

The release notes and source tests already cover the focus-lift graphics layer, hold-OK favourites, D-pad focus groups, contrast-aware focus rings, guide repeat coalescing, less frequent live/guide work, memoized shelves, bounded Coil memory cache, safe areas/narrow Settings, real-stage startup progress and the persisted Android sleep timer. These were inspected as existing release work; the readiness follow-up does not duplicate them.

## Readiness follow-up in this branch

- Added direct Android channel-number tuning using numeric `tvg-chno` values, including decimal subchannels (through the remote's period key): number-key repeats are ignored, OK commits immediately, a short idle tunes automatically, Back/D-pad cancels, missing numbers are surfaced, and an active search field retains its input. Numeric duplicates resolve in playlist order; alphanumeric `tvg-chno` labels are not quick-tune targets. Pure key/lookup logic has JVM unit tests and the UI contract is pinned by the offline suite.
- Added `focusRestorer()` to the tab row, category rail, channel grid and Live Events rows so focus returns to the previous item when D-pad traversal re-enters those groups.
- Keyed the player's lifecycle observer to the active channel as well as the shared ExoPlayer, preventing a channel switch from saving VOD position under a stale channel id.
- Removed the Android startup bar's continuous shimmer loop. The determinate bar still follows real repository progress, but does not schedule repeated draw invalidations while the library is loading.

## Validation before publishing

- Run the full offline Python suite and `python scripts/version_sync.py --check`.
- Run `cd macos/app && npm test`; Android changes do not alter the Mac renderer, but the shared release bundle and version surfaces remain part of the release gate.
- Run Android Gradle unit tests and the emulator smoke workflow on GitHub Actions. This workspace has no local Java/Android SDK, so a local Gradle/emulator result cannot be claimed here.
- Re-run `python scripts/build_site_data.py` after the same-day CHANGELOG entry; verify generated outputs with `python scripts/build_site_data.py --check`.
- Publish only after the branch is merged and the guarded workflow has completed the Android and macOS installer gates.
