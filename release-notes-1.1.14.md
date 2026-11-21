# PremiumTV 1.1.14 — Crash diagnostics and hardened sources

Android `1.1.14` / versionCode `101140000` · macOS `1.1.14`.

- Settings now shows the last crash - class, message and stack - and can clear it.
- A crash is recorded on the device on Android and macOS; nothing is uploaded.
- Source playlist and guide fetches verify TLS; only live stream probes allow broken certificates.
- Configured source URLs must be http(s) without credentials; relative local files stay in-repo.
- macOS player libraries are pinned to the same exact versions the web client already uses.
