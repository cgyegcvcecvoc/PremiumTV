# PremiumTV 1.1.16 — Crash diagnostics and hardened sources

Android `1.1.16` / versionCode `101160000` · macOS `1.1.16`.

- Settings now shows the last crash - class, message and stack - and can clear it.
- A crash is recorded on the device on Android and macOS; nothing is uploaded.
- The Android build compiles again: the crash card is a proper composable.
- The USA guide is built from the live feed, so it never lists a channel the app does not ship.
- Source playlist and guide fetches verify TLS; only live stream probes allow broken certificates.
