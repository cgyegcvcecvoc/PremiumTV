# PremiumTV 1.1.15 — Crash diagnostics and hardened sources

Android `1.1.15` / versionCode `101150000` · macOS `1.1.15`.

- Settings now shows the last crash - class, message and stack - and can clear it.
- A crash is recorded on the device on Android and macOS; nothing is uploaded.
- The USA guide is built from the live feed, so it never lists a channel the app does not ship.
- Source playlist and guide fetches verify TLS; only live stream probes allow broken certificates.
- macOS player libraries are pinned to the same exact versions the web client already uses.
