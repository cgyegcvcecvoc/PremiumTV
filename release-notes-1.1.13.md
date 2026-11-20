# PremiumTV 1.1.13 — Hardened sources

Android `1.1.13` / versionCode `101130000` · macOS `1.1.13`.

- Source playlist and guide fetches verify TLS; only live stream probes allow broken certificates.
- Configured source URLs must be http(s) without credentials; relative local files stay in-repo.
- macOS player libraries are pinned to the same exact versions the web client already uses.
- CI Node setup matches the Mac workflow, and discovery will not promote this repository.
