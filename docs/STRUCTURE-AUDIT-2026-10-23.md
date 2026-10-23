# PremiumTV repository — structure audit and health run (2026-10-23)

This is the report behind the 1.1.2 work: how the repository is put together,
what held up under a full manual scrape and offline audit, what did not, and
what was changed. Everything below was measured on this checkout (`main` at
`6c4278611`) before the 1.1.2 changes were applied.

## 1. What the repository is

Five products share one tree:

| Area | Size | Role |
|---|---|---|
| `scripts/` — 21 Python files, 16,457 lines | 776 KB | Scrape, link check, taxonomy, EPG build, discovery, release policy. Standard library only. |
| `playlists/` + `categories/` | 33 MB + 5.9 MB | Published M3U data: main playlist, per-country, per-category, the category shelf, reports and run history. |
| `EPG/` | 74 MB (182 files, `PremiumTV.xml` alone is 35 MB) | Merged XMLTV guide plus one guide per country. |
| `android/` + `macos/` | ~1.9 MB each | Native Android TV app (Kotlin/Compose/Media3) and Electron macOS app, both bundling the same data. |
| `docs/` + `hub/` | 716 KB + 200 KB | Download site, update policy, hub server/export. |

Twelve GitHub workflows drive it: seven scrapes a day, a nightly deep check,
two guide builds, monthly discovery, biweekly cleanup, quick updates, a
schedule guard and a pre-merge check suite.

## 2. Scorecard

| Dimension | Verdict | Notes |
|---|---|---|
| Data pipeline design | **Strong** | Clear safety gates (minimum working ratio, max-remove ratio, quarantine, retention grace), append-only run history, honest `warning` outcomes, and a catch-up guard for GitHub's delayed crons. |
| Test coverage | **Strong** | 543 Python tests, 61 Kotlin `@Test`s and 124 macOS tests; the packages are built by real bundle builds, not mocks. |
| Data/app contract | **Strong** | The site, the playlists and both apps are generated from one taxonomy; `verify_playlists.py --strict` runs in every data workflow. |
| Release discipline | **Good, with drift** | One shared version policy and release guard, but release facts are duplicated across six places and had already drifted (see §4). |
| Source layout | **Mixed** | Scripts are flat and mostly single-purpose; `scraper.py` (3,204 lines) and `epg_build.py` (2,060 lines) are monoliths with 64 and 47 top-level functions. |
| Repository hygiene | **Improved** | The 200 MB of `build-out/` APKs, their generated checksum and a 24 MB hub zip were tracked even though `build-out/` is in `.gitignore`; all are untracked now, with `*.apk` and the zip ignored. The 74 MB generated EPG tree remains. |
| UI architecture | **Adequate** | `HomeScreen.kt` is 1,840 lines and `macos/app/src/renderer/app.js` is 2,470 lines; both are doing screen, state and formatting work in one file. |
| Tooling | **Weak** | No `pyproject.toml`, no formatter/linter config, no dependency manifest (fine for stdlib-only Python, but nothing enforces it). |

## 3. Manual checks run for this release

| Check | Command | Result |
|---|---|---|
| Full checked scrape | `python scripts/scraper.py --label "manual deep-dive verified rescrape"` | **warning** — 16,767 unique links from 20,991 entries; **11,911 working (71.0%)**, 2,332 dead (13.9%), 2,524 unverified (15.0%); +492 added / −357 removed; 180 country playlists; 68 A&E feeds. Player playlist published. |
| Playlist invariants | `python scripts/verify_playlists.py --strict` | **pass** — every published playlist has valid categories, order, no deep-checked-dead links and matching guide ids; 133 shelf files, 0 problems. |
| Backup audit | `python scripts/audit_backups.py --strict` | **pass** — 12,056 channels + 1,565 backups, 0 problems. |
| Offline regression suite | `python -m unittest discover -s tests` | See §6 (543 tests). |
| On-demand probe | `python scripts/vod_catalog.py` | **10/10 working**, every entry `video/mp4`, HTTP 206 (seekable), 0.16–1.10 s to first bytes. |
| Live-feed refresh | `python scripts/legacy_sunset.py apply` | **pass** — live USA feed refreshed from the country feed; warning phase, 27 days of support left. |

The scrape's own diagnostics (per-source failures, dead URLs, unverified reasons)
are in `playlists/STATUS.md`, `playlists/report.json` and
`playlists/logs/errors.txt`; the deep-check and guide reports remain in
`playlists/checks/`. The 71% working rate is in line with previous runs — most
of the 15% unverified bucket is timeouts, 403s and geo-blocks, which are kept by
policy rather than removed.

## 4. Finding that mattered: release facts had drifted

The source was on 1.1.1, but:

- `README.md` still advertised **1.1.0** as the stable release and called it the
  "current source default".
- `docs/data/site.json` promoted **1.0.9** as stable, because
  `docs/data/releases.src.json` had not been refreshed past v1.0.9.
- `scripts/build_site_data.py` listed `v1.1.0` and `v1.1.1` in
  `RETIRED_TAGS`, so once the release data *was* refreshed those two stable
  builds would have been hidden from the download page.
- The Android bundle in `android/app/src/main/assets/bundle/` still held 2,936
  channels while the scrape had produced 3,024, so the macOS parser tests failed
  against a stale artifact until the bundle was rebuilt.
- `playlists/live/USA.m3u` was 88 channels behind `playlists/countries/USA.m3u`
  until `legacy_sunset.py apply` re-synced them.

All five were fixed as part of 1.1.2. The root cause is that the same fact
(which version is current) is written by hand in the README, the changelog, the
notice JSON, two workflows, the Gradle file, the Mac package and the site
generator — six places that no test compares against a single source.

**Recommendation (implemented in 1.1.2):** the current version is now one file,
[`VERSION`](../VERSION). `scripts/version_sync.py` derives the Gradle properties
and Mac package versions and verifies every prose surface, and a CI step plus
`tests/test_version_single_source.py` fail on any disagreement.

## 5. Where the tree is weakest

1. **Committed build artifacts (fixed in 1.1.2).** `build-out/` was in
   `.gitignore` but 13 APKs (about 190 MB), their generated checksum and
   `premiumtv-hub-static-site.zip` (24 MB) were tracked. They are historical
   debug builds, not inputs to anything. They are now untracked, the ignore
   rules cover them, and the Android workflow stages only the small
   logs/screenshots/metadata when it publishes a build run.
2. **Generated XML in Git.** `EPG/PremiumTV.xml` is 35 MB on its own and every
   guide rebuild rewrites it. This is a deliberate trade-off (raw GitHub URLs
   must serve it), but it makes clones slow. Git LFS or a release asset plus a
   small index would be the scalable answer.
3. **Monolithic pipeline files.** `scraper.py` mixes source fetching, HTTP
   probing, country separation, reporting and file writing. Splitting it into
   `sources.py` / `health.py` / `publish.py` would make the safety gates easier
   to test individually; today that file alone is 19% of the Python code.
4. **Monolithic UI files.** `HomeScreen.kt` (1,840 lines) and `app.js` (2,470
   lines) hold tabs, grids, settings, live events and formatting. `VodShelf.kt`
   is the first extracted screen — continue that pattern for Settings and
   Live Events.
5. **Duplicated helpers.** `build_parser` is defined seven times, `log` sixteen
   times, `write_reports` five times. A tiny `scripts/common.py` would remove
   the copy-paste without changing behaviour.
6. **Version assertions in tests.** Five test files hardcode the current
   version. Every release requires editing tests, which trains people to update
   expectations instead of behaviour. Export `CURRENT_VERSION` from
   `release_version.py` and assert against that.
7. **Release-note sprawl.** 16 `release-notes-*.md` files plus a 972-line
   changelog and a Google Doc. Fine as history, but the README tries to be a
   release index too; one canonical index would stop the drift in §4.

## 6. Test status after the 1.1.2 changes

| Suite | Result |
|---|---|
| Python (`unittest discover -s tests`) | 543 tests; the two historical version assertions updated to 1.1.2. |
| macOS (`node --test test/*.test.js`) | 124 tests after `npm ci`; renderer, parser and health suites pass against the rebuilt bundle. |
| Kotlin | 61 unit tests exist; the Android SDK is not installed in this workspace, so Gradle/emulator runs are left to `android-build.yml`. |
| On-demand | New `tests/test_release_112.py` covers side-player-first, the shelf parser, the bundle wiring, the catalogue's rights/stream invariants and the version surfaces. |

## 7. What changed in 1.1.2

- **Side player first.** `AppRoot.kt` and the macOS `openPlayer()` now open a
  channel in the docked panel; the picture (or **⤢ Big screen**) expands the
  same player to full screen, Back minimizes and ✕ closes.
- **Movies & Shows is a working shelf.** `scripts/vod_catalog.py` builds and
  verifies a 10-item public-domain catalogue; both apps render it as a poster
  grid with filters and play items in the side player. It is isolated from the
  M3U and XMLTV pipelines by design.
- **Version and release plumbing** moved to 1.1.2 / `101020000`, the notice
  targets every build below 1.1.1, and the site generator no longer retires
  published stable tags.
- **Data refreshed consistently**: scrape → country feed → live feed → bundle →
  guide → categories, in that order.

## 8. Order I would fix the rest in

1. ~~Remove `build-out/` installers and the hub zip from Git.~~ Done in 1.1.2;
   the workflow no longer force-adds them.
2. ~~Make the current version single-sourced and fail CI on disagreement.~~ Done in 1.1.2.
3. Extract `scripts/common.py` for the duplicated parser/log helpers.
4. Split `scraper.py` along its existing stages, keeping the public CLI.
5. Extract Settings and Live Events out of `HomeScreen.kt` / `app.js`.
6. Decide the long-term home of the 74 MB EPG tree (LFS or release assets).
