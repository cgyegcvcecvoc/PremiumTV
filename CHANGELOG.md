# PremiumTV1 change log

> **Detailed editable history:** [PremiumTV1 — Detailed Change Log (Google Doc)](https://docs.google.com/document/d/1anjXfhv6qXz9ZsSldHBMqsfDt8d44W8N_ayqYAloeNM/edit?usp=drivesdk). It backfills the available Git/PR history and all 79 records in the committed run-history snapshot, and documents stream-check policy, current metrics, and known limitations.

This GitHub file is the short index. The detailed Doc and the append-only [`playlists/run-history.jsonl`](playlists/run-history.jsonl) retain the run-by-run record; the per-run live reports remain under [`playlists/checks/`](playlists/checks/).

## 2026-10-12 — release consolidation and Mac experimental display fix

- The Mac player's `#player { display: flex }` and error panel's `display: grid`
  overrode the browser's `[hidden]` display rule. On launch they covered the
  channel browser with the error text and Try Again button. Explicitly honor
  `[hidden]` and test both elements' initial hidden state. Playback now uses
  the original feed URL as a format hint rather than the extensionless loopback
  URL, so HLS and MPEG-TS are tried before native playback where appropriate.
- Publish one **Mac experimental pre-release** (`v1.0.0-experimental.1`) and
  one **Android beta download** (`v1.0.0-beta4`, the default/latest download).
  Superseded release pages are removed, but historical Git tags remain.
  Neither platform is claimed to be a hardware-verified final/stable build;
  the Mac installer is not the default release.
- Build workflows only attach artifacts to their own platform's matching tag
  and commit, so later branch builds cannot silently replace a release asset.

## 2026-10-12 — macOS app (v1.0.0-mac1 preview; historical)

- **A native installer, not a script.** New `macos/` Electron app packaged as a
  `.dmg` and a `.pkg` for macOS 12+ on Intel and Apple Silicon, built by
  `.github/workflows/macos-build.yml` and published to the
  [v1.0.0-mac1 pre-release](https://github.com/cgyegcvcecvoc/PremiumTV1/releases/tag/v1.0.0-mac1).
- **Same behaviour as the Android app.** Channels / Guide / Settings screens,
  bundled USA playlist + guide, loopback playback proxy that sends each entry's
  published referrer/origin/user-agent, and a GitHub-aligned automatic refresh
  (45 min after every publishing slot, ETag/Last-Modified conditional, atomic
  staging swap, force-refresh and reset-to-bundled).
- **Electron pinned to 43.** Electron 44 dropped macOS 12, so the app stays on
  43 and declares `minimumSystemVersion: "12.0"`. Ad-hoc signed, not notarized.
- **Guarded by tests.** `tests/test_macos_app.py` and `macos/app/test/*.test.js`
  cross-check the parsers against `build_bundle.py` and the refresh slots
  against the publishing workflows.

## 2026-10-11 — Android TV beta 4 (v1.0.0-beta4 preview)

- **GitHub-aligned automatic refresh.** Android WorkManager now schedules a
  connected-network check 45 minutes after every daily playlist scrape,
  quick-update and EPG publication slot. The next one-time job is chained after
  each run and survives app exits/reboots; Android may defer it under normal
  background limits.
- **Low-cost unchanged checks.** Automatic runs retain ETag and Last-Modified
  validators, so unchanged playlist/guide files use HTTP 304 instead of being
  transferred up to 13 times per day. A changed playlist forces a complete
  guide read so newly added channel IDs can receive listings immediately.
- **Force refresh all.** Settings now has a true force action that bypasses
  validators and downloads both the complete USA playlist and complete guide.
  It shows in-progress state, next automatic check, last successful refresh and
  the latest result.
- **Safe cache publication.** Foreground and worker operations share one mutex.
  A refresh writes a staging directory and atomically swaps it into place only
  after both files parse; interrupted, partial and malformed updates keep the
  last usable data. Reset clears validators so the next check cannot mistake
  bundled data for an already-downloaded copy.
- **Honest private-repository behavior.** 401/403/404 results retain current
  data and do not trigger rapid retries. Transient timeouts, 408/425/429 and 5xx
  failures receive two WorkManager backoff retries. No GitHub credential is
  embedded or requested.
- **Version/release status.** Source is `1.0.0-beta4`, `versionCode 4`, and CI
  targets the [v1.0.0-beta4 pre-release](https://github.com/cgyegcvcecvoc/PremiumTV1/releases/tag/v1.0.0-beta4).
  **Beta 3 is the current default release; Beta 4 is the new preview** until its
  background behavior is smoke-tested on TV hardware.

## 2026-10-11 — Android TV beta 3 (v1.0.0-beta3; current default release)

- **Channels open sooner.** The repository reads the channel list first and
  publishes the Channels screen while it parses the larger programme guide on
  the IO dispatcher. Guide parsing no longer blocks the first usable channel
  rows.
- **Guide failures are isolated.** Missing or damaged metadata/categories use
  safe fallbacks; an unreadable guide shows a clear notice without taking down
  the channel list. A failure to read the required channel data now offers a
  visible retry action.
- **Smoother browsing.** Channel rows are D-pad focus groups; controls expose
  button semantics and retain the latest click callback. Channel logos share a
  small disk cache and skip per-image fades to reduce repeated work on TV sticks.
- **Version** — `1.0.0-beta3`, `versionCode 3`. The Android build workflow now
  targets the `v1.0.0-beta3` release tag.
- **Release status** — Beta 3 is the
  [current default release](https://github.com/cgyegcvcecvoc/PremiumTV1/releases/tag/v1.0.0-beta3)
  with a CI-built APK. Beta 4 continues separately as the new pre-release.

## 2026-10-11 — Android TV beta 2 (v1.0.0-beta2; superseded by beta 3)

- **Fixed: channels did not load on launch.** The bundled channel list and guide
  were in the APK, but the reader looped on `JsonReader.hasNext()` past the end
  of each file and threw on the last line. The app then reported the data as
  missing and asked for a Python command, which a TV cannot run. Each line is
  now read on its own, a damaged download falls back to the bundled copy, and
  the app's messages no longer mention Python.
- **Version** — `1.0.0-beta2`, `versionCode 2`. Install
  `PremiumTV-1.0.0-beta2-debug.apk`.
- **Unsigned release APK dropped.** An unsigned APK cannot be installed on a
  device, so CI publishes only the debug APK, which installs as-is.
- Rebuilt bundle: 2,217 USA channels in 59 categories; about 9,950 guide
  listings for 167 channels.

## 2026-10-11 — first Android TV app (v1.0.0 beta, superseded by beta 2)

The repository now builds an installable Android app that carries the channel
list and the guide inside the APK, so a TV needs no separate player setup.

- **Project** — [`android/`](android/README.md): Kotlin + Jetpack Compose,
  targeting leanback (Android TV / Google TV / Fire TV) and handhelds from one
  APK. `minSdk 23`, `targetSdk 34`.
- **Bundled data** — 2,158 confirmed-working USA channels in the 59 published
  categories and every guide listing available at build time (about 8,900
  listings covering 158 channels). [`android/tools/build_bundle.py`](android/tools/build_bundle.py)
  converts `playlists/countries/USA.m3u` + `EPG/USA.xml` into JSON Lines the
  app streams with `android.util.JsonReader`, so a TV stick never holds a
  10 MB XML document in memory beside a video decoder.
- **Screens** — category rows, a what's-on-now guide with now/next and
  progress, and settings that refresh from the repository's raw URLs or reset
  to the bundled copy.
- **Playback** — ExoPlayer (Media3), honouring the referrer, origin and
  user-agent a playlist entry publishes through `#EXTVLCOPT` / `#KODIPROP`.
- **D-pad correctness** — focus, the centre/enter keys and taps are each wired
  once, so a card can never be focused-but-unopenable or fire twice on one
  press.
- **Build** — [`.github/workflows/android-build.yml`](.github/workflows/android-build.yml)
  compiles in GitHub Actions: a plain sandbox has no JDK, no Android SDK and no
  route to Maven Central or `dl.google.com`. It publishes a debug-signed,
  installable APK and an unsigned release APK to `build-out/` and to the
  release.
- **Tests** — `tests/test_android_bundle.py` (18 checks) covers header capture,
  timezone normalisation, group ordering, the already-finished listings rule,
  and referential integrity between the bundle's channels and programmes.
  Full suite: 311 passing.

Known limits: USA library only; the world library is not bundled yet. Guide
coverage is whatever the upstream XMLTV sources publish — 158 of 2,158
channels have real listings and the app says so rather than padding. Refresh
returns HTTP 404 while the repository is private.

## 2026-10-10 — verified playlist maintenance and history backfill

The existing deep-check workflow was reviewed as the safe mechanism for pruning broken player feeds. It probes HLS variants and actual media segments, removes only confirmed-dead/invalid links, and protects working streams with minimum-working and maximum-removal thresholds. Timeouts, 5xx responses, resets, and auth/geo blocks are not treated as dead based on one observation. The user-facing player playlist is built from confirmed-working links; the all-links catalogue and source caches remain diagnostic/fallback data, not clean player feeds.

Baseline captured from scraper run `20261010T202102Z-2648` (20:21–20:24 UTC):

- 21,547 source entries; 17,230 unique URLs.
- 10,946 confirmed working; 1,915 confirmed dead; 4,369 unverified.
- 176 country playlists; A&E playlist: 62 confirmed working of 71 unique candidates.
- The same commit's offline verification: 179 published playlists, 0 structural problems, 0 known-dead links present, and 131/131 category-shelf files in sync.
- The latest saved live deep check before this baseline (11:08–11:11 UTC) removed 156 confirmed-dead entries across 27 playlists; it retained 48 unreachable and 12 blocked entries rather than risking false removals. The next live check's results are recorded in the updated Actions report.
- The refreshed merged XMLTV guide declares 9,281 channel IDs but has programme listings for 192 channels (2.1%); guide coverage remains a follow-up item.

### Historical milestones

| Date | Change | Summary |
|---|---|---|
| 2026-09-27 | PRs #1–2 | Scheduled M3U scraper, checked player playlist, all-links catalogue, source snapshots, publication safety threshold, and setup documentation. |
| 2026-09-28 | PRs #3–4 | Append-only run history and diagnostics; separate confirmed-dead from transient/unverified; source audits and monthly discovery with scoring, caps, cooldown, and rollback. |
| 2026-09-29–30 | PRs #5–6 | Country-specific playlists, curated A&E feeds, plain-text logs, steadier New York schedules, and URL/W3U parsing fixes. |
| 2026-10-01 | PR #7 | Tried a single master list with country sections; subsequent taxonomy and country-playlist changes define the current output format. |
| 2026-10-02 | PR #8 | Deep HLS/DASH checks, EPG checks, quarantining, safe dead-link pruning, priority-channel hunting, and stable-link ranking. |
| 2026-10-03 | PRs #10–11 | Guide/workflow integration, live deep audit, and curated Lancaster/Harrisburg-area local channel source. |
| 2026-10-04 | PRs #12, #14 | Merged and country XMLTV guides; canonical categories and backup groups; quick repair/replacement path; NFL Network/RedZone targets. |
| 2026-10-05 | PR #15 | Reconciled branch conflicts into one taxonomy/order; strict verification, safer in-place resorting, guide-header limits, and honest EPG coverage. |
| 2026-10-07 | PRs #16–18 | Generated category shelf; URL deduplication and workflow branch isolation; fixed padded IDs, malformed `+https` URLs, placeholder EPG programmes, orphan guides, and stale shelf files. |
| 2026-10-10 | PR #19 | Added the biweekly archive/deep-clean workflow: check archived/source playlists, rebuild guides and category shelf, re-hunt priority channels, rotate logs, compact quarantine, prune orphans, then verify strictly. |
| 2026-10-11 | app/ | First Android TV app (v1.0.0 beta): bundled USA channel list and guide, D-pad first Compose UI, Media3 playback, GitHub Actions APK build. |

PRs #9 and #13 were superseded/closed rather than discarded: merged-guide work was reconciled into #11/#12, and the taxonomy work from #13 was reconciled with #14 by #15.

## Link quality and safe pruning

- **Keep:** streams that answer and produce playable media; preserve their URLs during re-sorting.
- **Remove:** only confirmed offline or invalid URLs, including links that answer with HTML/empty content or an HLS playlist with no playable media. A repeated-URL duplicate is collapsed to one correctly named entry, not treated as another stream.
- **Recheck, don't guess:** transient network failures and geo/auth restrictions are not equivalent to dead streams. Quarantine and retry help catch persistent failures without losing a stream that works elsewhere or recovers.
- **Protect the file:** `--min-working-ratio` and `--max-remove-ratio` prevent bad network days or unexpectedly large removals from replacing a known-good playlist. Backup promotion is checked before replacement.
- **Current health reports:** [scraper status](playlists/STATUS.md) · [deep link check](playlists/checks/LINK-CHECK.md) · [strict playlist verification](playlists/checks/VERIFY.md) · [guide build](playlists/checks/EPG-BUILD.md).

## Access and limitations

GitHub currently reports this repository as **private**. Its `raw.githubusercontent.com` playlist and guide links cannot be consumed by unauthenticated IPTV players. This change intentionally does not alter repository visibility or sharing; an owner-approved public delivery endpoint is required before using those links in a player. Also, “confirmed working” is a time- and location-specific test, and the 4,369 unverified baseline candidates must not be conflated with confirmed-dead feeds.

The local Git history in this checkout covers 2026-09-27 through 2026-10-10 (151 commits); the Google Doc contains the full available run-history backfill. Some verbose per-URL text logs have been rotated by the repository's cleanup policy, so the append-only JSONL and Git snapshots are the durable audit sources.
