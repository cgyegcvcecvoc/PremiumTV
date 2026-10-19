# PremiumTV 1.0.7 — Compatibility Build (identical to 1.0.6.1)

**1.0.7 is not a new feature release.** It is the **same application build** as
1.0.6.1, published under a three-part version number for one reason: apps that
were distributed before 1.0.6.1 read only `MAJOR.MINOR.PATCH`, so a `1.0.6.1`
release is invisible to their updater. 1.0.7 is the release those apps can find,
download and install from **Settings → App updates** without a manual APK or
DMG download.

- Android `versionCode 100070000`. The APK is named 1.0.7 so a three-part
  updater can find it, but it installs as **1.0.6.1** — the version Settings
  reports afterwards. That keeps the updated app on the canonical stable
  identity instead of calling itself a preview above it.
- Mac app version `1.0.7` (macOS packaging requires three parts).
- **The macOS `.dmg` and `.pkg` installers for 1.0.6.1 live on this release.**
  macOS packaging rejects a four-part version, so the Mac build is packaged as
  1.0.7 while staying the same application code.
- Same code as 1.0.6.1: compact Settings, **Force refresh**, **Check for
  update**, **Check for bugs**, the USA lineup and the USA guide.
- The download page keeps **1.0.6.1** as the recommended build and shows this
  release's Mac installers as its own; 1.0.7 also exists for the updater.
- An install already running 1.0.6.1 ignores 1.0.7 (it is the same code behind a
  second name), so nobody is asked to download 19 MB twice.

## Who should use it

- **1.0.4 – 1.0.6:** install it through the in-app updater. This is the build
  your Settings screen can actually see. Support for older builds ends
  **Nov 16, 2026**.
- **1.0.6.1, 1.0.5, 1.0.4 by hand:** use 1.0.6.1; there is no functional
  difference.
- **1.1.0 / 1.1.1 previews:** retired and blocked. Install 1.0.6.1 (or 1.0.7,
  which is the same code) — Android installs it straight over the preview.

Full release notes: [`release-notes-1.0.6.1.md`](release-notes-1.0.6.1.md).
