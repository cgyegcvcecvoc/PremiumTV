# PremiumTV 1.1.1 — Encore Preview: Cable Guide + Everyday Polish

**This is a pre-release, not the default.** Stable users receive the recommended 1.0.4 release. Like
1.1.0, this build is published with GitHub's pre-release flag so it is never
handed out as the recommended download.

## Rebuilt with the in-app update center (same 1.1.1 name)

The preview now carries the same **Settings → App updates** center as stable
1.0.4: it checks GitHub once a day, offers only a published stable release
above the installed build, downloads the installer once, verifies its SHA-256
and reuses it until installed. Previews are never offered to stable users, and
an installed 1.1.1 preview is never downgraded to 1.0.4.

This rebuild is signed with PremiumTV's long-lived update key (versionCode
`100010001`), so later releases install in place. If you already have the
earlier 1.1.1 preview, uninstall it once before installing this build; after
that, in-app updates work normally.

## The Guide tab is now a cable-style guide

On both Android TV and Mac, the **Guide** tab of this preview is the grid you
know from a cable box:

- **Channels down the left** — channel number (when the playlist has one),
  logo, name and category, pinned while the grid scrolls sideways.
- **What each channel is playing to the right** — one block per show, as wide
  as its running time, the show on now outlined in gold.
- **Times across the top** — half-hour columns for the next eight hours from
  the current half hour, pinned while the channels scroll, with a red **NOW**
  line through the grid.
- **A detail strip above the grid** for the highlighted show: title and
  episode, start–end time, minutes left (or when it starts), category,
  description and channel.
- Channels follow the published category order (Sports first, as in the
  Channels tab) under category headings. A channel's backup feeds share its
  listings, so the guide shows the channel once.

### On a TV remote (Android)

- Select **Guide** and press OK: the highlight lands on the first channel's
  current show. The remote's **GUIDE** button opens it from anywhere.
- **▲ ▼** change channel and keep the same time column (the highlight does not
  drift sideways past long and short shows). **◀ ▶** step one show at a time;
  left of the first show is the channel itself.
- **OK** watches the highlighted channel. **Back** from the player returns to
  the same spot in the guide. **▲** from the first row goes back to the tabs;
  **Back** leaves the guide. **CH+ / CH−** page through the channels.
- On a touch screen, drag the grid in either direction and tap a show to watch.

### On a Mac

- Point at a show for its details, click to watch, or use the arrow keys.
- The sidebar categories filter the guide; the search box finds a channel or a
  show.

## Why 1.1.0 did not show it

1.1.0 put the grid in a separate **Cable** tab that only appeared when the
*loaded* data enabled it. Installing 1.1.0 over 1.0.x kept the copy the older
version had downloaded in the background, and that copy loaded first: the app
showed the old USA lineup and no Cable tab. 1.1.1 fixes both halves:

- The grid **is** the Guide tab — there is no extra tab to miss.
- A downloaded copy written by a different version or library scope is
  discarded on start (with its HTTP validators), and which preview features
  show is decided by the app's own bundle, never by downloaded data.

## Encore maintenance update

This refresh of the existing preview includes the same loading/activity panels,
real refresh stages, elapsed time, rotating offline tips and facts, completion
and failure feedback, and guarded refresh/reset controls as stable 1.0.3.
The global lineup and cable-style Guide remain preview-only. This is still
**1.1.1**, still a **pre-release**, and never the default download.

This rebuilt preview uses the derived `versionCode 100010001` (the original
1.1.1 used 9, the earlier maintenance build 11), so a future stable above 1.1.1
can install over it. It is signed with the same long-lived update key as stable
1.0.4; the earlier 1.1.1 builds used a different random debug key, so installing
over one of those needs a one-time uninstall. Mac installers keep version 1.1.1.

## Also in this build

- **Leaner refresh on TVs.** The global guide (~38 MB of XML) is parsed as it
  downloads instead of being held as text first, which needed roughly 200 MB
  of heap; listings for unknown channels or long-finished shows are skipped
  before their text is read.
- **Category order survives a refresh** (Android), so the Channels tab and the
  guide no longer re-sort by size after a background update.
- **Accurate refresh messages.** The repository is public and refreshes work;
  the old "this repository is private" explanations are gone from both apps.

## Rebuild provenance

The Encore maintenance installers replace the original 1.1.1 preview assets
without changing its historical source tag. `BUILD-SOURCE-android.txt` and
`BUILD-SOURCE-macos.txt` on the release record the exact updated source commit
and smoke-tested Actions run for each platform. Use those manifests, not the
historical tag, when inspecting the source of the rebuilt installers.

## Downloads

- Android: `PremiumTV-1.1.1-debug.apk` (`versionCode 100010001`) — signed with
  the long-lived update key; installs over stable 1.0.4 and future previews.
- Mac Apple Silicon: `PremiumTV-1.1.1-mac-arm64.dmg` / `.pkg`.
- Mac Intel: `PremiumTV-1.1.1-mac-x64.dmg` / `.pkg`.
- Checksums: `SHA256SUMS-android.txt` and `SHA256SUMS-macos.txt`.

Mac installers are ad-hoc signed, not notarized (first launch: right-click →
Open). The Android APK is signed with the pinned update key (see
`android/keystore/README.md`), so later releases install in place.

## Validation

- The Python repository tests and macOS Node tests run before publication; the Android
  build runs its JVM and Robolectric unit tests (guide ordering, remote-cursor
  movement, stale-cache discard, streaming XMLTV parsing) before packaging.
- The Android release gate installs the APK on an emulator, opens the Guide
  and checks the times across the top, the channels down the left and the
  shows; it then drives the D-pad, presses OK to open the player and Back to
  return to the same guide.
- The Mac release gate launches the packaged app on Apple Silicon and Intel
  (Rosetta), opens the Guide and checks the 16 half-hour columns, the channel
  rows, the shows and the NOW line.

## Known limitations

- The guide covers the channels that have listings — about 1,700 of the ~9,800
  in the global lineup. Every channel still plays from the Channels tab.
- The grid shows eight hours from the current half hour.
- Public streams come and go between health checks; a channel that will not
  play is usually a dead or geo-blocked upstream link.
