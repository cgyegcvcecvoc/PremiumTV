# PremiumTV 1.1.0 — Preview: Global Lineup + Cable Guide

**This is a pre-release, not the default.** Stable users stay on 1.0.2. This
build is published with GitHub's pre-release flag so it is never handed out as
the recommended download.

## What is in the preview

- **Global checked lineup.** 9,788 channels across 89 categories from the
  checked global playlist, instead of the 2,133-channel USA library.
- **Cable guide tab.** A traditional channel-by-time grid: an 8-hour window in
  30-minute slots, one row per channel with listings, channel numbers, logos,
  programme titles with start times, a NOW marker and a gold highlight on the
  current programme. Horizontal scrolling is shared between the clock header and
  the rows, so the grid stays aligned.
- **The tab is metadata-gated.** The cable guide appears only when the bundle
  declares `preview_features: ["cable-guide"]`, which the global 1.1.0 bundle
  does and the stable USA bundle does not. The header shows a `PREVIEW` tag and
  Settings lists the library scope and preview features.

## Guide data

- Merged guide built from the repository's curated per-country EPG feeds:
  **105,319 programmes across 1,650 channels** in the 1.1.0 bundle.
- Runtime guide parsing over the refreshed network copy follows the same
  validation rules as 1.0.2: strict 14-digit timestamps with `±HHMM` offsets,
  impossible dates rejected, and non-positive durations repaired to 30 minutes.

## Everything from 1.0.2

This preview carries the same fixes: M3U names containing commas, strict XMLTV
validation, repaired programme durations, exact id+URL backup-stream selection
on Mac, correct proxy-session release, and channel-health evidence reconciled so
a newer successful probe supersedes an older quarantine entry.

## Validation

- 349 Python tests and 38 macOS Node tests pass on this commit.
- The strict verifier reports no structural problems and no published dead
  links across the 177 published playlists.
- Release CI builds the tagged commit for both platforms: Gradle unit tests and
  an emulator cold-launch/relaunch check for the APK, and real `.dmg`/`.pkg`
  packaging with packaged-app smoke tests on Apple Silicon and Intel.

A larger library is a larger promise: only 1,650 of the 9,788 channels currently
have listings, and dead upstream feeds remain possible between health checks.
Treat this preview as a test channel, not the default install.

## Downloads

- Android: `PremiumTV-1.1.0-debug.apk` (`versionCode 8`).
- Mac Apple Silicon: `PremiumTV-1.1.0-mac-arm64.dmg` / `.pkg`.
- Mac Intel: `PremiumTV-1.1.0-mac-x64.dmg` / `.pkg`.
- Checksums: `SHA256SUMS-android.txt` and `SHA256SUMS-macos.txt`.

Both platforms install side by side with the stable build (Android
`versionCode 8` upgrades `versionCode 7` in place). Mac installers are ad-hoc
signed, not notarized; Android stays debug-signed.

## Known limitations

The repository is private, so in-app refresh over unauthenticated raw GitHub
URLs cannot work from an installed app; the bundled global copy is what you get.
No credentials are embedded. Some upstream streams are geo-restricted or simply
offline.
