# PremiumTV 1.0.3 — Stable Maintenance Release

PremiumTV 1.0.3 is the next stable Android TV and macOS maintenance build. It
keeps the stable USA lineup and the list-style TV guide; the global cable-style
guide remains preview-only in 1.1.1.

## Maintenance

- **Refreshed bundled data.** CI bakes the latest checked USA playlist and USA
  XMLTV guide into each installer. The app remains usable from its bundled
  library at first launch and can refresh from the public repository afterward.
- **Safe Android upgrade numbering.** Android uses `versionName 1.0.3` and
  `versionCode 10`, above the 1.1.1 preview's code 9, so installing stable over
  either 1.0.2 or the preview is an in-place update rather than a downgrade.
- **Stable-only release routing.** Both platform workflows accept `v1.0.3` only
  as a full release, keep the USA scope for stable, and continue to reject
  stable-tagged 1.1.x previews.
- **Download site freshness.** The site refreshes published release assets,
  promotes a stable release only after the APK and all four Mac installers are
  available, and regenerates its country picker, counts, changelog and Atom
  feed from the repository inputs.

## Downloads

- Android TV / Google TV / Fire TV / phone / tablet:
  `PremiumTV-1.0.3-debug.apk` (`versionCode 10`).
- Apple Silicon: `PremiumTV-1.0.3-mac-arm64.dmg` / `.pkg`.
- Intel Mac: `PremiumTV-1.0.3-mac-x64.dmg` / `.pkg`.
- Checksums: `SHA256SUMS-android.txt` and `SHA256SUMS-macos.txt`.

The CI release gates run Android unit tests and an emulator cold-start/Guide
smoke test, and macOS unit tests plus packaged-app smoke tests on Intel and
Apple Silicon. Stream availability is upstream- and region-dependent; a health
check is a point-in-time probe, not a guarantee that every public feed will
remain online.
