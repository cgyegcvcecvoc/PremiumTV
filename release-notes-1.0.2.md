# PremiumTV 1.0.2 — Stable Maintenance Release

The default release. Same USA lineup and USA guide as 1.0.1, with the parser,
playback and channel-health fixes from the 2026-10-14 deep check, plus the
Android build fix that had blocked the APK.

## Fixes

- **Android build restored.** The preview cable guide called `initialsOf()`,
  which was file-private to the shared components file, so `compileDebugKotlin`
  failed and no APK was produced. The helper is now module-internal and shared
  by both surfaces. The stable 1.0.2 build does not show the preview tab at all.
- **Channel names containing commas survive parsing.** Both the Android parser
  and the macOS parser split `#EXTINF` at the last comma, which truncated names
  such as `News, Local` and also corrupted the group when it contained a comma.
  Names are now read after the first comma outside quoted attribute values.
- **Guide timestamps are validated strictly.** XMLTV times must be a 14-digit
  stamp with an optional `±HHMM` offset; impossible calendar dates (for example
  `20261131…`) and year zero are rejected instead of being rolled forward, and
  out-of-range offsets are refused.
- **Non-positive programme durations are repaired.** A `stop` at or before
  `start` previously produced a zero- or negative-length listing; it is now
  rebuilt as a 30-minute block so the grid cannot render an inverted cell.
- **Mac backup streams play the backup.** Channel ids are EPG ids, so a channel
  and its backups share one. Selecting a backup now resolves the exact id+URL
  pair instead of silently reopening the primary feed.
- **Mac proxy sessions are released.** The renderer passed the loopback URL
  where the main process expected the session id, leaking one whitelisted
  session per playback. Release accepts either form.
- **Channel health evidence is reconciled.** A later confirmed media probe now
  supersedes an older quarantine entry, so streams re-proven playable are not
  reported or withheld as dead.
- Updated the macOS XML parser dependency and the release build configuration.

## Validation

- 349 Python tests, including the bundle builder, refresh wiring, packaging
  contracts and the strict playlist verifier.
- 38 macOS Node tests, covering cold start, guide loading, parser accuracy,
  duplicate-id playback selection and HTTP-level proxy behaviour.
- The strict verifier currently reports **177 playlists, 19,650 entries, zero
  structural problems, zero published dead links**, and 76 non-blocking
  EPG-coverage notes.
- Release CI builds the tagged commit: Gradle unit tests plus an emulator
  cold-launch/relaunch check for the APK, and real `.dmg`/`.pkg` packaging with
  packaged-app smoke tests on Apple Silicon and Intel for the Mac.

These are parsing, packaging and local playback-path checks. They are not a
promise that every third-party stream is online.

## Downloads

- Android: `PremiumTV-1.0.2-debug.apk` (`versionCode 7`).
- Mac Apple Silicon: `PremiumTV-1.0.2-mac-arm64.dmg` / `.pkg`.
- Mac Intel: `PremiumTV-1.0.2-mac-x64.dmg` / `.pkg`.
- Checksums: `SHA256SUMS-android.txt` and `SHA256SUMS-macos.txt`.

The build jobs attach these to this release page. Mac installers are ad-hoc
signed, not Developer ID notarized; macOS may require right-click → **Open**.
Android stays debug-signed: if Android reports a signing-key mismatch when
updating an older CI APK, uninstall that build first (this clears app settings
and cache).

## Known limitations

The repository is private, so unauthenticated raw GitHub refresh URLs are still
inaccessible from an installed app; the bundled channels work offline for
browsing and playback needs an internet connection. No credentials are embedded
in either app. A public delivery mirror requires separate owner-approved setup.
