# PremiumTV 1.0.4 — One Last Manual Install

PremiumTV 1.0.4 is the stable Android TV and macOS build that adds the
**in-app update center**. It is the last version that has to be downloaded by
hand: from this release on, Settings can check for, download and install every
later stable release.

## Updating from inside the app

- **Settings → App updates** shows the installed version, the newest stable
  release, the last check and the exact status.
- **Check for updates** asks GitHub immediately. The app also checks once a day
  at startup, sending its previous ETag so an unchanged release list is one
  tiny `304 Not Modified` response.
- **Download update** fetches only the installer for this device (the Android
  APK or the Mac DMG for Intel or Apple Silicon), verifies it against the
  release's published SHA-256 file, and keeps it until it is installed.
- **Install update** (Android) opens Android's normal package-installer
  confirmation. **Open installer** (Mac) opens the verified DMG so PremiumTV
  can be dragged to Applications.
- Pressing the button again after a download never downloads the same version
  twice: the verified file is reused.

## What counts as an update

Only a **published, non-pre-release** GitHub release whose version is
numerically above the installed app is offered. Drafts, previews, older
releases and releases whose installers are still uploading are ignored. An
installed preview such as 1.1.1 is ahead of stable 1.0.4 and is never offered
an older build. The release guard workflow rejects (and marks as a
pre-release) any stable release that is not above the current stable, so the
apps never have to guess.

## One clean install, then never again

Android refuses to install an update over an app signed by a different key.
Builds before 1.0.4 were each signed by a fresh key generated on the build
machine, which is why older versions could not update in place. 1.0.4 and all
later releases share one checked-in update key, and CI verifies the APK's
certificate on every build.

So: if you have 1.0.3 or older installed, **uninstall it once**, then install
1.0.4. Every release after this one installs directly over 1.0.4 from
**Settings → App updates**, with no uninstall and no full re-download of the
guide.

## Downloads (this release only)

- Android TV / Google TV / Fire TV / phone / tablet:
  `PremiumTV-1.0.4-debug.apk` (`versionCode 100000004`, derived from the
  version so every future release installs as an upgrade).
- Apple Silicon: `PremiumTV-1.0.4-mac-arm64.dmg` / `.pkg`.
- Intel Mac: `PremiumTV-1.0.4-mac-x64.dmg` / `.pkg`.
- Checksums: `SHA256SUMS-android.txt` and `SHA256SUMS-macos.txt`.

## Encore Preview unchanged

The pre-release keeps its name and scope: **1.1.1 Encore Preview** — global
checked lineup and cable-style Guide tab. It ships the same update center and
follows the same stable-only rule. A rebuilt 1.1.1 uses the derived
`versionCode 100010001`, so it remains installable above stable 1.0.4.

The usual gates still run before assets are attached: Android unit tests and
the emulator cold-start/Guide smoke test, and Mac unit tests plus packaged-app
smoke tests on Intel and Apple Silicon. Stream availability is upstream- and
region-dependent; a health check is a point-in-time probe, not a guarantee.
