# PremiumTV 1.0.8 V1 Patch — 1.0.8.1

> ⚠️ **CRASH WARNING — update to [1.0.9](release-notes-1.0.9.md) now.** This version can freeze on a black picture or crash when you open a channel (on Android the video surface stays attached to a released player after a server switch). 1.0.9 fixes it and installs in place. Do not stay on this build.

**Status: superseded by 1.0.9 — the only V patch ever cut; the V series is retired.** Android `versionCode 100080001` (`1.0.8.1` → `100080001`; alias `1.0.9` → `100090000` for 1.0.4–1.0.6 updaters), Mac `1.0.9` (alias of `1.0.8.1`, both carry the same code). Every 1.0.4+ app finds it in Settings → App updates: check, download once, verify the SHA-256, install. It installs in place over every previous stable and the retired 1.1.x previews.

> **V naming, locked in.** `1.0.8 V1` is `1.0.8.1`, `V2` is `1.0.8.2`, `V3` is `1.0.8.3` … each V increments the fourth number and its `versionCode` by one, so every V installs over the last and orders above it. Old three-part updaters (1.0.4–1.0.6) see the same code under its alias (`1.0.9`, `1.0.10` …), just as `1.0.7` was the alias for `1.0.6.1`. The real `1.0.9` has since shipped as the crash-on-watch fix, retiring this naming scheme — there is no V2.

## The more animated loading screen

- **Android:** the launch splash now breathes — a drifting gold haze circles the TV mark, a halo ring pulses around the logo, a sweeping shimmer underline races endlessly, a segmented progress bar carries a racing highlight, and three dots beside the title pulse in sequence so the TV never looks frozen. All motion is transform/opacity only, so it stays smooth on low-end sticks. Tips still fade every 8 s, and the bottom plaque now reads `Version 1.0.8 V1 Patch` with the raw code underneath.
- **macOS:** the same language — breathing logo, orbiting ring, sweeping gold sweep across the window, shimmer bar and pulsing dots — plus a `Patched · V1` chip in the foot. Reduced-motion users get a static splash (no animation, no transition).

## Better bug detection — 11 checks, not 7

Settings → **Check for bugs** stays offline and read-only, but now reports:

1. **Channel list** — blank names/URLs, bad schemes, duplicate URLs
2. **Categories** — empty shelf, ungrouped channels
3. **TV guide** — loading/error/coverage
4. **Data bundle** — missing HTTPS URLs, declared vs loaded count
5. **Refresh pipeline** — in-progress, failed-last-attempt
6. **App updates** — error, stale downloaded installer
7. **Version** — installed vs library build, with V display (`1.0.8 V1` for `1.0.8.1`)
8. **Patch chain** *(new)* — validates the V ordering this patch establishes: `Patch V1 of 1.0.8 — chain intact, next V is V2.` Future Vs must keep increasing the fourth number.
9. **Stream hygiene** *(new)* — flags spaces in stream URLs and malformed logo URLs that fail on players.
10. **Guide freshness** *(new)* — how old the window start is, in days; warns after 7 days, urges refresh after 14.
11. **Library health** *(new)* — warns on empty categories and on oversized groups (>5000) that stress low-memory devices.

Both Android and macOS share the same four new checks, so a report from either platform reads the same.

## Unchanged on purpose

- No playlist, scraper, guide, or refresh-pipeline behaviour changes; the bundled data is still the USA lineup + USA guide (`playlists/live/USA.m3u` + `EPG/USA.xml`).
- The 1.0.7 → 1.0.6.1 alias mapping is historical and stays, and the V series adds its own (1.0.9 → 1.0.8.1, 1.0.10 → 1.0.8.2 …).
- Update policy is untouched: only a published full stable release above the installed version, with its platform installers attached, is ever offered; drafts, pre-releases and releases with missing assets are ignored.

## Verification

- `python3 scripts/release_version.py --code 1.0.8.1` prints `100080001`; `--display 1.0.8.1` prints `1.0.8 V1`; `--macos 1.0.8.1` prints `1.0.9`.
- `python3 scripts/release_version.py --canonical 1.0.9` prints `1.0.8.1`; `is_compatibility_alias` confirms the mapping.
- Python suites: `tests/test_release_version.py` (including V alias tests), `tests/test_site_data.py`, `tests/test_app_updates.py`, `tests/test_macos_app.py`, and the Android bundle/refresh checks all pass.
- macOS app: `npm test` — updated diagnostics and animation coverage.
- Android app: JVM tests for sorting, team crests and matchup parsing (`SortingTest`, `TeamCrestTest`, extended `LiveEventsTest`) plus new `Diagnostics` V chain tests; CI emulator smoke test on the built APK.

## Downloads (after release publish)

- Android: `PremiumTV-1.0.8.1-debug.apk` (`versionCode 100080001`) + alias `PremiumTV-1.0.9-debug.apk` (`100090000`) for old updaters
- Mac Apple Silicon: `PremiumTV-1.0.9-mac-arm64.dmg` / `.pkg` (alias of `1.0.8.1`)
- Mac Intel: `PremiumTV-1.0.9-mac-x64.dmg` / `.pkg` (alias of `1.0.8.1`)
- Checksums: `SHA256SUMS-android.txt` and `SHA256SUMS-macos.txt`

Both platforms install side by side with the stable build and over the retired previews. Mac installers are ad-hoc signed, not notarized.
