# PremiumTV app updates

Version 1.0.4 is the last release that has to be installed by hand. From then
on, **Settings → App updates** checks GitHub, downloads the installer once,
verifies it against the release's SHA-256 file, and hands it to the platform's
normal installer.

## The rules every release follows

1. **Stable only.** The updater reads
   `https://api.github.com/repos/cgyegcvcecvoc/PremiumTV1/releases` and ignores
   drafts and pre-releases. Preview builds such as 1.1.1 are never offered to
   stable users, and an installed preview is never offered an older stable
   build.
2. **Strictly above the installed version.** Versions are compared numerically
   (`1.0.10` is above `1.0.9`). The release guard workflow fails a stable
   release whose version is not above the newest stable release and marks it
   as a pre-release, so no app will offer it.
3. **Complete for the platform.** The Android APK or the Mac DMG for this
   architecture must already be attached to the release. A release whose build
   jobs are still uploading is invisible until the file exists.
4. **One download per version.** A downloaded installer is kept in the app's
   data directory and reused. Pressing Download again, rechecking, or reopening
   Settings never downloads the same version twice. After the update is
   installed, the old installer is removed.
5. **No background downloads.** The daily check only reads the release list
   (and uses an ETag, so an unchanged list is one `304`). The installer
   download starts only when the user presses the button in Settings.
6. **Checksums are mandatory.** The APK/DMG is compared with the SHA-256 value
   published in that release before it is kept or opened.

## Android signing (why 1.0.4 is the clean install)

Android only installs an update over an existing app when both APKs carry the
same signing certificate. Every CI build before 1.0.4 generated a brand-new
debug key on the runner, so 1.0.0-1.0.3 could not update each other in place.
1.0.4 and every later build are signed with the checked-in long-lived key
`android/keystore/premiumtv-updates.p12`, and CI verifies the APK certificate
against `android/keystore/fingerprint.txt` before uploading.

If PremiumTV 1.0.3 (or older) is installed, uninstall it once before installing
1.0.4 by hand. After that, Android updates install straight over the previous
release - that is the whole point of 1.0.4.

## Android

`AppUpdateManager` stores its state in `premiumtv_app_update` preferences and
the verified APK in `files/updates/PremiumTV-<version>-debug.apk`. Installing
opens Android's package installer through a one-file `FileProvider`; Android 8
and newer may first ask the user to allow PremiumTV to install unknown apps.
The versionCode is derived by `scripts/release_version.py`
(`MAJOR * 100000000 + MINOR * 10000 + PATCH`), so every new release installs as
an upgrade over both stable and preview builds.

## macOS

`AppUpdater` stores its state in `update-state.json` in the app's user-data
directory and the verified DMG in `updates/`. Because builds are ad-hoc signed
(not notarized), macOS does not permit a silent in-place replacement; the app
opens the verified DMG and the user drags PremiumTV to Applications. The daily
check is throttled and the downloaded DMG is reused until it is installed.

## Publishing a new stable release

1. Bump the version and let CI build both platforms. Manual runs use
   *Actions → Build PremiumTV Android APK / macOS DMG + PKG → Run workflow*
   with the version (for example `1.0.5`) and channel `stable`.
2. Publish the GitHub release as a **full release** (not a pre-release) with
   the `v1.0.5` tag. The release guard checks the ordering; the build workflows
   attach the APK and all four Mac installers when the tag points at their
   commit.
3. The download site promotes the release only after the APK and all four Mac
   installers exist. Installed 1.0.4+ apps see it on their next daily check or
   immediately when the user presses **Check for updates**.

A preview is published with GitHub's pre-release flag and keeps its preview
name; it uses the global bundle scope and never becomes the default download.
