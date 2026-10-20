# PremiumTV 1.0.9 — Compatibility Build (identical to 1.0.8 V1 Patch / 1.0.8.1)

**1.0.9 is not a new feature release.** It is the **same application build** as
1.0.8 V1 Patch (`1.0.8.1`), published under a three-part version number for one
reason: apps distributed as 1.0.4–1.0.6 read only `MAJOR.MINOR.PATCH`, so a
`1.0.8.1` release is invisible to their updater. 1.0.9 is the release those
apps can find, download and install from **Settings → App updates** without a
manual APK or DMG download. It follows the same precedent as 1.0.7, the
compatibility build of 1.0.6.1.

- Android `versionCode 100090000`. The APK is named 1.0.9 so a three-part
  updater can find it, but it installs as **1.0.8.1** — the version Settings
  reports afterwards, shown as **1.0.8 V1 Patch**. That keeps the updated app
  on the canonical stable identity instead of calling itself a preview above
  it.
- Mac app version `1.0.9` (macOS packaging requires three parts).
- **The macOS `.dmg` and `.pkg` installers for 1.0.8 V1 live on this
  release.** macOS packaging rejects a four-part version, so the Mac build is
  packaged as 1.0.9 while staying the same application code as 1.0.8.1.
- Same code as 1.0.8.1: the all-new category list, the side player, the
  revamped Live Events tab, plus the V1 animated loading screen and the
  11-check **Check for bugs** diagnostics.
- The download page keeps **1.0.8.1** as the recommended build and shows this
  release's Mac installers as its own; 1.0.9 also exists for the updater.
- An install already running 1.0.8.1 ignores 1.0.9 (it is the same code behind
  a second name), so nobody is asked to download the same build twice.

## Who should use it

- **1.0.4 – 1.0.6:** install it through the in-app updater. This is the build
  your Settings screen can actually see. Support for builds below 1.0.8 V1
  ends **Nov 19, 2026**.
- **1.0.8 or 1.0.6.1 by hand:** use the updater or 1.0.8.1; there is no
  functional difference.
- **1.1.0 / 1.1.1 previews:** retired and blocked. Install 1.0.8.1 (or 1.0.9,
  which is the same code) — Android installs it straight over the preview.

Full release notes: [`release-notes-1.0.8.1.md`](release-notes-1.0.8.1.md).
