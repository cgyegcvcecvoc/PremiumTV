# PremiumTV 1.0.1 — Channels Back on Air

A focused follow-up to the Marquee release: fix the empty Mac channel browser and add release gates that launch the actual apps.

## Fixes

- **Mac channels load on cold launch.** The renderer previously kept the empty snapshot it received before the bundled library loaded. It now fetches the current library on state and channel-progress events, updates channel cards and guide listings, and ignores out-of-order IPC replies.
- **Refreshed channels and listings appear without restarting.** The same fix updates the displayed library after a refresh or reset.
- **Mac conditional refresh works correctly.** Saved HTTP validators are read from their actual persisted location and are not reused after falling back from a corrupt cache to the bundle.
- **Redirected HLS feeds resolve correctly.** Relative video segments and encryption keys now use the final redirected playlist URL.
- **Separate platform checksums.** Android and macOS no longer overwrite each other's checksum manifest.

## Validation

- 343 Python tests covering playlist processing, bundles, refresh wiring and packaging contracts.
- 32 Node tests, including reproduced cold-start failures, guide loading, stale IPC responses, refreshed cards, cache recovery and an HTTP-level proxy test.
- Release CI runs five Android/Robolectric tests using the actual bundled assets and Android JSON reader, then installs and cold-launches/relaunches the built APK in an emulator.
- Release CI launches the packaged Electron apps for both Apple Silicon and Intel (under Rosetta), verifying the preload bridge, loaded channel cards, bundled players, library updates and reset.

These are channel-loading and local playback-path checks, not a guarantee that every third-party stream is online. Physical Android TV devices and all supported macOS versions are not covered by this CI matrix.

## Downloads

- Android: `PremiumTV-1.0.1-debug.apk` (versionCode 6).
- Mac Apple Silicon: `PremiumTV-1.0.1-mac-arm64.dmg` / `.pkg`.
- Mac Intel: `PremiumTV-1.0.1-mac-x64.dmg` / `.pkg`.
- Checksums: `SHA256SUMS-android.txt` and `SHA256SUMS-macos.txt`.

Mac installers are ad-hoc signed, not Developer ID notarized; macOS may require right-click → Open. Android remains a debug-signed build; if Android reports a signing-key mismatch when updating an older CI APK, uninstall that build before installing (this clears app settings/cache).

## Known limitations

The repository is private: unauthenticated raw GitHub refresh URLs are still inaccessible from an installed app. The bundled channels work offline for browsing; actual playback needs an internet connection. No credentials are embedded in either app. A public delivery mirror requires a separate owner-approved setup.
