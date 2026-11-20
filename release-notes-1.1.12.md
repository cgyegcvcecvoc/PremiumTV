# PremiumTV 1.1.12 — Resilient playback

Android `1.1.12` / versionCode `101120000` · macOS `1.1.12`.

- Android, macOS and web retry recoverable playback faults before spending backup servers.
- A shared recovery policy keeps transient, media and permanent failures bounded.
- The opt-in web relay now handles extensionless HLS playlists and passes media through.
- Scheduled jobs self-heal generated data, local markets and the legacy freeze before tests.
- Android unit tests resolve Robolectric SDK 28 jars through Gradle, not Maven at runtime.
