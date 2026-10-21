# PremiumTV app updates

Version 1.0.4 was the last release that had to be installed by hand. From then
on, **Settings → App updates** checks GitHub, downloads the installer once,
verifies it against the release's SHA-256 file, and hands it to the platform's
normal installer. The current stable release is **1.0.9** — a plain three-part version. The V-patch scheme (1.0.8.1 = "1.0.8 V1", briefly aliased as 1.0.9) was retired at 1.0.9: every fix from now on is simply the next version number, with no four-part versions and no compatibility-alias twins.

## The rules every release follows

1. **Stable only.** The updater reads
   `https://api.github.com/repos/cgyegcvcecvoc/PremiumTV1/releases` and ignores
   drafts and pre-releases. The 1.1.x preview channel is retired: its release,
   installers and download links were removed, and installed previews see a
   blocked-build notice instead of an update offer.
2. **Strictly above the installed version.** Versions are compared numerically
   (`1.0.10` is above `1.0.9`, and `1.0.6.1` is above `1.0.6` without being
   mistaken for `1.0.7`). The release guard workflow fails a stable
   release whose version is not above the newest stable release and marks it
   as a pre-release, so no app will offer it.
3. **Complete for the platform.** The Android APK or the Mac DMG for this
   architecture must already be attached to the release. A release whose build
   jobs are still uploading is invisible until the file exists.
4. **One download per version.** A downloaded installer is kept in the app's
   data directory and reused. Pressing Download again, rechecking, or reopening
   Settings never downloads the same version twice. After the update is
   installed, the old installer is removed.
5. **No background downloads.** The daily check reads the release list (and uses
   an ETag, so an unchanged list is one `304`) plus the small
   `app-update-notice.json` document that drives the update popup. The installer
   download starts only when the user presses the button in Settings - and
   pressing **Update now** in the popup opens Settings and re-checks rather than
   downloading, so this rule holds whichever button started it.
6. **Checksums are mandatory.** The APK/DMG is compared with the SHA-256 value
   published in that release before it is kept or opened.

## The popup that sends an older build to GitHub

Settings is where an update is *managed*; the popup is where an out-of-date
build is *told*. Both apps show one at startup when the installed version is
inside the range a published notice targets.

Everything about it is published in **`app-update-notice.json`** at the root of
this repository, which both apps read from
`https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/app-update-notice.json`
during the same daily check that reads the release list:

| Field | What it decides |
|---|---|
| `enabled` | `false` silences every popup without a new release |
| `schema` | A build shows nothing for a schema it has never seen |
| `rules[].platforms` | `android`, `macos`, or both |
| `rules[].min_version` / `max_version` | The inclusive version range that is nagged |
| `rules[].title` / `message` / `surprise` | The wording, with `{version}`, `{newest}` and `{support_ends}` substituted |
| `rules[].action_label` / `dismiss_label` | The two buttons |
| `first_warning_utc` / `support_ends_utc` / `grace_days` | The end-of-support window |
| `rules[].after_support_ends` | The escalated wording used once that window closes |

The rules the popup follows:

1. **Dismissible, and it comes back.** A TV remote can arrive here mid-evening,
   so an app that refuses to run would turn "please update" into "your TV is
   broken". The dismissal lasts one launch and is never persisted - on Android it
   is kept out of `SharedPreferences`, on macOS out of `update-state.json` - so
   the notice returns every launch until PremiumTV is updated.
2. **Decided before any network call.** The document is cached, so the popup is
   resolved at startup from the last copy. An offline launch still shows it,
   which is exactly when an out-of-support build is most stuck.
3. **Never over a playing channel.** Android shows it above every screen except
   the player.
4. **A notice failure is invisible.** An unreachable, oversized (over 64 KB) or
   malformed document keeps the last good copy and can never fail the update
   check that already succeeded.
5. **The escalation needs no release.** On the day `support_ends_utc` passes, the
   same rule switches to its `after_support_ends` wording and its accent colour
   by itself - no fetch, no rebuild, no remote edit.

The "surprise" in the copy is the update centre itself: the newest build is the
last one anybody has to install by hand, because from there PremiumTV updates
itself.

## End of support for builds below 1.0.6.1

None of them can show this popup, so no code change can reach them. 1.0.0-1.0.3
ship no updater at all - the `v1.0.3` tree has neither `AppUpdateManager.kt` nor
`updater.js`. 1.0.4 does have the update centre (`AppUpdateManager.kt`,
`UpdateInstaller.kt`, `update-policy.js`), but it was released before this notice
existed, so it can never fetch one; it can still escape on its own, because its
Settings -> App updates will offer the next release - it simply will not be told to
look. 1.0.0-1.0.3 have no such route.

All of them do still refresh one playlist, baked into their bundles at build time,
and that is the only channel into them. `scripts/legacy_sunset.py` uses it:

| Feed | Path | Who reads it |
|---|---|---|
| **Live** | `playlists/live/USA.m3u` | PremiumTV 1.0.5+, the `categories/` shelf, the download site |
| **Legacy** | `playlists/countries/USA.m3u` | PremiumTV 1.0.0-1.0.4 only |

`raw.githubusercontent.com` serves the same bytes to every caller and cannot look
at a version, so the only way to stop feeding one set of builds is to give the
others a different address. While support lasts the two files carry the same
channels; the legacy one also carries the notice, and the live one never does.

* **First warning** (`first_warning_utc`) starts the countdown, and the first
  publishing run after it puts the sanctioned notice entry at the top of the
  legacy feed. That is the delivery: every installed 1.0.0-1.0.4 refreshes that
  playlist on its own schedule and renders the entry as the first channel in a
  `PremiumTV Notice` group. Builds that understand the marker drop it, so
  1.0.5+ is unaffected (they get the JSON popup instead).
* **End of support** (`support_ends_utc`, 30 days later) pins the last scraped
  channel list to `playlists/legacy/USA.m3u` and rewrites the legacy feed from
  that pin with one sanctioned notice entry on top. Builds 1.0.0-1.0.4 keep the
  channels that worked that day, see
  `⚠ UPDATE PremiumTV — support for 1.0.6 and older ended Nov 16, 2026 · get the
  newest free version at github.com/…` as the first entry in their channel list,
  and stop receiving scrape updates. The live feed carries on.

The frozen feed keeps advertising the live `EPG/USA.xml`: what ends is the
channel scrape, not the listings for the channels a legacy build still has.

`scripts/legacy_sunset.py apply` runs on every publishing pass: it refreshes the
live feed, attaches exactly one fresh notice entry to the legacy feed (replacing
any earlier one), and freezes on the published date. The deep check, the verifier
and the guide builder all skip that entry, so a message can never be counted as a
channel, probed as a dead link or added to a guide.

The notice entry is marked `tvg-notice="app-update"`, and both apps' parsers drop
an entry carrying that marker - so it can never reach a channel list, a category,
the shelf or the download site of a build that understands it. Only builds too
old to know the marker render it, which is exactly who it is for. Its URL is the
GitHub releases page rather than a stream: selecting it in an old build fails to
play, which is honest, because the row is a notice and its name is the message.

`python scripts/legacy_sunset.py status` reports the phase and the days left,
`apply` is what every publishing workflow runs, and `check` fails a run when the
sunset has been quietly undone - a legacy feed that is still live after its date,
a frozen feed that no longer matches its pin, or a live feed carrying a notice
entry.

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
(`MAJOR * 100000000 + MINOR * 1000000 + PATCH * 10000 + HOTFIX`), so every new
release installs as an upgrade over both stable and retired preview builds.
`1.0.6.1` is `100060001`, above 1.0.6's published `100000006` and the retired preview's
`100010001`; the APK and the preview share the same update signing key, so it
installs straight over 1.1.1 without uninstalling.

## macOS

`AppUpdater` stores its state in `update-state.json` in the app's user-data
directory and the verified DMG in `updates/`. Because builds are ad-hoc signed
(not notarized), macOS does not permit a silent in-place replacement; the app
opens the verified DMG and the user drags PremiumTV to Applications. The daily
check is throttled and the downloaded DMG is reused until it is installed.

## Publishing a new stable release

1. Bump the version and let CI build both platforms. Manual runs use
   *Actions → Build PremiumTV Android APK / macOS DMG + PKG → Run workflow*
   with the version (for example `1.0.9`) and channel `stable`. Versions are
   plain three-part numbers; the matching Android versionCode comes from
   `python3 scripts/release_version.py --code <version>`.
2. Publish the GitHub release as a **full release** (not a pre-release) with
   the tag (for example `v1.0.9`). The release guard checks the ordering;
   the build workflows attach the APK and all four Mac installers when the tag
   points at their commit. (`--display` still resolves the one historical V
   patch: `python3 scripts/release_version.py --display 1.0.8.1` → `1.0.8 V1`.)
3. The download site promotes the release only after its APK exists **and**
   all four Mac installers exist. Only the historical four-part releases
   (1.0.6.1, 1.0.8.1) borrow Mac installers from their alias release, since
   macOS packaging cannot carry a four-part version.
   Installed 1.0.4+ apps see the release on their next daily check or
   immediately when the user presses **Check for update**.
4. **No compatibility twin — that scheme is retired.** Four-part patch
   releases (1.0.6.1, 1.0.8.1) once needed a second, identical release one
   patch above them (1.0.7, briefly 1.0.9) because the updater in 1.0.4–1.0.6
   parses only `MAJOR.MINOR.PATCH`. From 1.0.9 on, publish **one** three-part
   release and nothing else: every updater still in the field can read it,
   and the download page promotes it directly. `COMPATIBILITY_ALIASES` keeps
   only the historical `1.0.7 → 1.0.6.1` entry so old tags and installs still
   resolve. One consequence to remember: installed 1.0.8.1 builds treat
   "1.0.9" as another name for themselves (their frozen alias table), so
   their in-app check can miss the real 1.0.9 — the crash-warning popup in
   `app-update-notice.json` tells those users to install the APK by hand.
5. Check `app-update-notice.json`. Its rules are read in order and the first
   one whose range contains the installed version is shown. The current
   document targets four ranges: `crash-on-watch-1-0-8` (Android 1.0.8–1.0.8.1,
   level `blocked` — the extreme update-now warning for the frozen-player bug,
   with 1.0.9 hard-coded because that cohort's `{newest}` would render as
   itself), `retired-preview-1-1` (1.1.0-1.1.1, level `blocked`, linking to
   the blocked page), `update-below-newest` (1.0.4–1.0.8,
   a warning whose action opens Settings so the normal updater finishes the
   job), and `legacy-upgrade-2026-11` (0.0.0-1.0.3, the last manual install).
   When a V patch ships, move that version's range to start above it (e.g.
   `max_version` 1.0.6 stays, newest becomes V1).

The 1.1.x preview channel is retired. There is no preview release, no preview
download and no preview rebuild switch; do not create a GitHub pre-release for
a 1.x build. The `all` bundle scope remains available for a future experimental
dispatch, but it does not become a published download unless this policy is
deliberately changed.
