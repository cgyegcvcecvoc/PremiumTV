# PremiumTV 1.1.17 — Indexed library, guarded playback

Android `1.1.17` / versionCode `101170000` · macOS `1.1.17`.

- Opening a channel no longer re-scans every channel name: one index per library, built off the UI thread.
- The Channels and Live Events tabs draw without the two full-library passes they ran in composition.
- Guarded the focus requests, guide cursor, feed list and stream setup that could stop the app mid-press.
- Duplicate playlist or catalogue rows are dropped before they can hand a lazy list two identical keys.
- Settings -> Check for bugs reports measured UI work: index build time, failures and the last channel open.
