# PremiumTV 1.0.6.1 — Settings 2.0, Fresh Scrape, and the End of the Preview

**This is a small, incremental stable release.** It sits above 1.0.6 and below
every future 1.0.7/1.1 release, so nobody has to wait for a new minor version to
get a cleaner Settings screen or a repaired channel list.

Android `versionCode 100060001`. Both platforms are built from the same tree and
carry the same data scope: the USA lineup and the USA guide.

The macOS app is packaged as **1.0.7**, because electron-builder and macOS
require a three-part version number. The `.dmg` and `.pkg` installers therefore
appear on the **1.0.7** release; they are the same code as this one.

The same code is also published as **1.0.7** (Android `100070000`, installing
as `1.0.6.1`): apps shipped
before this release only read three-part versions, so 1.0.6.1 alone would be
invisible to their updater. 1.0.6.1 remains the recommended download and the
version named everywhere in the app; 1.0.7 is the compatibility twin that lets
1.0.4–1.0.6 update themselves. See
[`release-notes-1.0.7.md`](release-notes-1.0.7.md).

## Settings is now one compact screen

The old Settings tab had three headings, a dozen rows, two long explanations and
buttons scattered between them. 1.0.6.1 replaces it with:

- **One version card** — installed version, scope, channel/category/guide counts
  and the bundle build date, all visible at a glance.
- **Three one-tap actions** — **Force refresh**, **Check for update** and
  **Check for bugs** — plus **Download update / Install update** only when there
  really is an update.
- **A single status line** that reports whichever action ran last, instead of
  several competing messages.
- **A collapsible Details section** for the playlist/guide sources, URLs,
  guide window, refresh results and the reset button. Nothing is lost; it is
  just no longer in the way.

The Mac app gets the same treatment: a compact version/stat card, the same
actions in one row, and collapsible Details and About panels.

## New: Check for bugs

**Check for bugs** is a real, built-in diagnostic, not a link to GitHub. It runs
entirely on the device and never changes the cache:

- channel list: empty names, missing stream URLs, unusable schemes and duplicate
  URLs;
- categories: channels that name a category missing from the sidebar;
- TV guide: parse errors, still-loading guides, empty listings and coverage;
- data bundle: missing or non-HTTPS playlist/guide sources, count mismatches;
- refresh pipeline: a failed last attempt, or a refresh still running;
- app updates: a failed update check or a downloaded installer that no longer
  matches the offered version;
- installed version vs. the version the library was built for;
- on Mac, the bundled data files and the writable app-data folder.

Every check reports **OK**, **WARN** or **FAIL** with a specific sentence, so a
report can be acted on rather than just noticed. Press it again after a refresh
to confirm a fix.

## Fresh rescrape

The release build is cut from a fresh scrape of the published sources. The
scraper still tests every link, quarantines confirmed-dead entries, rebuilds the
category shelf and refreshes the guide before the APK is baked, so 1.0.6.1 ships
the current working lineup rather than a copy of the 1.0.6 list.

## The 1.1.x preview is retired and blocked

The **1.1.0 and 1.1.1 preview channel has been removed completely**:

- the `v1.1.1` GitHub release and its APK/DMG/PKG assets are deleted;
- the download page, the Netlify-style hub and every generated data file no
  longer list or link a preview;
- the repository no longer publishes preview-build switches or preview assets;
- anyone still running 1.1.0/1.1.1 sees a **BUILD RETIRED** banner at startup.
  Its button and the page at
  <https://cgyegcvcecvoc.github.io/PremiumTV1/blocked/> point at 1.0.6.1.

Android `100060001` is above the retired preview's `100010001` **and** it is
signed with the same long-lived update key, so the 1.0.6.1 APK installs straight
over 1.1.1 — no uninstall first. On Mac, open the 1.0.6.1 DMG and drag it to
Applications, replacing the preview.

## Older stable builds get a real upgrade path

The published notice document now targets three ranges:

| Installed | What the popup says | Can it update from the popup? |
|---|---|---|
| 0.0.0–1.0.3 | A newer stable is waiting; this is the last manual install; support ends **Nov 16, 2026** | No updater in these builds — install 1.0.6.1 by hand once |
| 1.0.4–1.0.6 | **1.0.6.1 is ready**; press Update now, then Download and Install in Settings → App updates; support for older builds ends Nov 16, 2026 | **Yes** on 1.0.5/1.0.6 (1.0.4 has the update centre but predates the popup; its Settings still offers 1.0.6.1) |
| 1.1.0–1.1.1 | This preview is retired and blocked; install 1.0.6.1 | Manual install over the preview |

The popup still returns every launch until the build is replaced, and its
wording, target range and support date remain published in
[`app-update-notice.json`](app-update-notice.json), so none of this needs another
release to change.

## Install

- Android: `PremiumTV-1.0.6.1-debug.apk` (`versionCode 100060001`), signed with
  the pinned update key from `android/keystore/`.
- macOS: `PremiumTV-1.0.6.1-mac-arm64.dmg` / `.pkg` and
  `PremiumTV-1.0.6.1-mac-x64.dmg` / `.pkg` (macOS 12 Monterey or later).

After installing 1.0.6.1, **Settings → Check for update** and the daily
background check keep it current. Only a published stable release above the
installed version is ever offered.
