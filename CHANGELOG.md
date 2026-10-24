# PremiumTV1 change log

> **Detailed editable history:** [PremiumTV1 — Detailed Change Log (Google Doc)](https://docs.google.com/document/d/1anjXfhv6qXz9ZsSldHBMqsfDt8d44W8N_ayqYAloeNM/edit?usp=drivesdk). It backfills the available Git/PR history and all 79 records in the committed run-history snapshot, and documents stream-check policy, current metrics, and known limitations.

This GitHub file is the short index. The detailed Doc and the append-only [`playlists/run-history.jsonl`](playlists/run-history.jsonl) retain the run-by-run record; the per-run live reports remain under [`playlists/checks/`](playlists/checks/).

> **Change-log policy.** Every change made on request is recorded here the same
> day under a dated heading, and `python scripts/build_site_data.py` is re-run so
> the [download site](https://cgyegcvcecvoc.github.io/PremiumTV/) and its
> [Atom feed](https://cgyegcvcecvoc.github.io/PremiumTV/data/feed.xml) show it.
> If the site does not show a change, the generator was not re-run.

## 2026-10-24 — Version 1.1.2 is published; the release path and the download site are repaired

- **v1.1.2 is a complete published release.** Tag [`v1.1.2`](https://github.com/cgyegcvcecvoc/PremiumTV/releases/tag/v1.1.2) carries the APK (`15,564,521` bytes, `versionCode 101020000`) and all four Mac installers (`1.1.2` arm64/x64 DMG + PKG, `133–141 MB`), plus both `SHA256SUMS` files and build provenance. Before this, 1.1.2 existed only in the tree: no tag, no APK, no Mac installers — so no installed app could be offered it and the download page had fallen back to 1.0.9.
- **The Android release gate that blocked it is fixed.** `android-build.yml` failed on the 1.1.2 merge with *"the closed side player (live event) not seen within 90 seconds"*: the update popup is a dialog window, so it takes the remote's focus and Back key, and `AppRoot.kt` allowed it above a **docked** channel — exactly where Back is promised to the dock. The popup now shows only when nothing is playing (what `docs/UPDATES.md` already documented). The emulator gate now passes cold launch, Guide, a channel, the server hop, both side-player flips and the Live Events leg.
- **Every fielded version can reach 1.1.2.** Checked against the live release list with the updater's own policy: 1.0.0–1.0.3 (legacy playlist notice) and 1.0.4–1.1.1 (in-app updater) are all offered **1.1.2** on Android and macOS, and 1.1.2 is offered nothing. 1.0.8/1.0.8.1 keep the extreme crash warning, which now says **“Get the newest version”** and follows `/releases/latest` instead of pointing at the superseded `v1.0.9`.
- **Publishing is now a workflow.** New [`.github/workflows/publish-release.yml`](.github/workflows/publish-release.yml) publishes `VERSION` with its release notes, refuses an existing tag, and runs the version-drift check first. The version number could not reach the Releases page by hand any more.
- **The site promotes a release only when it is complete.** The release-triggered Pages job now waits (up to 45 minutes, in its own concurrency group) for the APK and all four Mac installers before redeploying; previously it redeployed immediately and left the previous stable card up until an unrelated data run happened to touch the site.
- **The download site is truthful again.** `docs/data/releases.src.json` was stuck at `v1.0.9`, so the stable card advertised a build two releases behind; it is refreshed (and now carries GitHub's own SHA-256 digests). `docs/blocked/index.html` claimed the **stable** 1.1.1 had been blocked and deleted and pointed at 1.1.0 — it now names the current stable, carries the right `versionCode` and download links, and says plainly that 1.1.0/1.1.1 are ordinary supported releases. `docs/README.md` (still “Current stable: 1.1.0”) and the hub landing page (“Stable 1.1.0”) now describe 1.1.2.
- **The published site address is `/PremiumTV/`.** The repository was renamed on 2026-10-21 and a project Pages URL does not survive a rename, so `/PremiumTV1/` served nothing. `PAGES_URL` (site payload + Atom feed id), `docs/README.md`, `hub/DEPLOY.md` and the workflow summary now use the canonical address; raw/API slugs stay on the old name because GitHub 301s them and installed builds have them baked in.
- **Drift can no longer ship.** `scripts/version_sync.py` also checks `docs/README.md`, `docs/blocked/index.html` and `hub/static/index.html`, and fails a blocked notice rule that links a fixed tag. `tests/test_site_data.py` verifies every download URL against the release cache, that the promoted card is the newest *complete* release, and that the published site address is the canonical one. The macOS suite caught the hub page mentioning a version it must not, which is what delayed the Mac installers by one build.
- **Validation:** emulator smoke gate green on both the branch and the tag; macOS suite `124/124` plus packaged-app smoke on Apple Silicon and Intel (Rosetta); Python suite `557` tests; `version_sync` clean; `verify_playlists.py --strict --require-shelf` 184 playlists, 0 problems; all 9 published download links return `302` (a name that does not exist returns `404`), and `/releases/latest` resolves to `v1.1.2`.

## 2026-10-23 — Version 1.1.2: side-player-first watching and the Movies & Shows test shelf (stable)

- **Stable 1.1.2 is prepared** for Android TV / Fire TV (`versionCode 101020000`) and macOS (`1.1.2`). It installs in place over 1.1.1 and every earlier build; tag `v1.1.2`. See [`release-notes-1.1.2.md`](release-notes-1.1.2.md).
- **A channel now opens in the side player.** `AppRoot.kt` sets `sidePlayer = true` when a channel is picked, so the docked right-hand panel appears first and the browser stays usable beside it; one click (or OK) on the picture, or **⤢ Big screen**, grows the same running stream to full screen. The macOS renderer's `openPlayer()` starts in the same docked state. Back tucks the big screen into the dock and closes the docked panel (it used to leave the app, since nothing listened for the key while docked); ✕ closes from either layout, and Esc does the same on macOS.
- **Movies & Shows becomes a working on-demand shelf.** The 1.1.1 coming-soon page is replaced by a poster grid on both platforms with All / Movies / TV Shows filters; an item plays in the same side player. New `ui/VodShelf.kt` (Android) and `renderMovies()` (macOS) read a bundled catalogue.
- **The catalogue is real and verified.** New `scripts/vod_catalog.py` resolves 10 public-domain Internet Archive films and classic TV episodes, probes each direct MP4 with a range request, and publishes `playlists/vod/vod-catalog.json`, `vod-health.json` and [`FEASIBILITY.md`](playlists/vod/FEASIBILITY.md). All 10 entries answered with playable, seekable media. It is kept separate from the M3U, country playlists and XMLTV guide.
- **Bundle and CSP.** `android/tools/build_bundle.py` ships the catalogue as `bundle/vod-catalog.json` and `meta.vod_catalog`; the macOS CSP allows poster images from `https://archive.org`.
- **Release plumbing.** All version surfaces move to `1.1.2` / `101020000`, `app-update-notice.json` targets every build below 1.1.1, and `build_site_data.py` no longer lists the published stable tags v1.1.0/v1.1.1 as retired.
- **Installers left Git.** The 13 historical APKs, the generated Android checksum and the stray 23 MB `premiumtv-hub-static-site.zip` are no longer tracked; `.gitignore` now carries `*.apk` and the zip rule. The Android workflow still uploads the APK and checksum to the matching release and to Actions, while committing back only the small logs, screenshots and bundle metadata (the log-commit path no longer force-adds the whole folder).
- **The version now has one source.** New [`VERSION`](VERSION) holds the only hand-edited copy. `scripts/version_sync.py` generates `android/version.properties` and the Mac package versions from it, and verifies the README, both app READMEs, `docs/UPDATES.md`, the update notice, the release-notes file, both build workflows, Gradle, `build_bundle.py` and `build_site_data.py`. `release_version.py --current` / `--current-code` expose it to scripts and CI, both build workflows default to it instead of a hardcoded number, and a new CI step plus `tests/test_version_single_source.py` fail on any disagreement.
- **Manual health run on this commit.** A full checked scrape (16,767 unique links, 11,911 working), `verify_playlists.py --strict`, `audit_backups.py --strict` and the offline test suite were run; the structural review is in [`docs/STRUCTURE-AUDIT-2026-10-23.md`](docs/STRUCTURE-AUDIT-2026-10-23.md).

## 2026-10-22 — Version 1.1.1: Live Events crests and countdowns, Movies & Shows (stable)

- **Stable 1.1.1 is published** for Android TV / Fire TV (`versionCode 101010000`) and macOS (`1.1.1`). It installs in place over 1.1.0 and every earlier build, including the retired 1.1.x preview (`101010000` > `100010001`). See [`release-notes-1.1.1.md`](release-notes-1.1.1.md).
- **Live Events now shows official club crests.** Every team name on the tab is paired with its official crest next to the name, on Android and macOS alike; teams without a published crest keep the drawn badge. New `ui/TeamLogo.kt` (Android) and `renderer/live-events.js` (Mac) load the crest with the drawn badge as fallback.
- **"Not live yet" with a real countdown.** Listed games that haven't kicked off stay on the tab with a "Not live yet" pill and a ticking countdown to the scheduled start (`playlists/live-schedule.json`, built by `scripts/build_live_schedule.py` and bundled with the app data by `android/tools/build_bundle.py`); after kickoff the pill reads "NO SIGNAL" until a feed answers, then "LIVE".
- **One card per game.** Feed copies ("… 1", "… 2") of the same matchup merge into a single game card with all of its streams as backups.
- **Movies & Shows (coming soon).** New tab on both platforms opening a polished coming-soon page for the on-demand section landing in a future release; channels and the guide are unchanged.
- **The update notice no longer blocks 1.1.1.** The `retired-preview-1-1` rule was removed from `app-update-notice.json` (a stable release cannot be blocked by a rule matching its own version), and `update-below-newest` now covers every build below 1.1.1, so 1.1.0 installs are nudged to update from Settings → App updates.
- **Validation:** the emulator smoke gate (cold launch, Guide, open a channel, server hop, both side-player flips, close, Live Events) plus the macOS renderer/health/personal suites and the repository Python suite run on this commit.

## 2026-10-22 — Version 1.1.0: side player docked right, automatic server backup, dead channels filtered (stable)

- **Stable 1.1.0 is published** for Android TV / Fire TV (`versionCode 101000000`) and macOS (`1.1.0`). It installs over 1.0.9 and every earlier build, and over the retired 1.1.x preview (`101000000` > `100010001`). See [`release-notes-1.1.0.md`](release-notes-1.1.0.md).
- **The side player is now a docked panel on the right.** `AppRoot.kt` composes the browser in a Row with a reserved dock slot and calls the *same* `PlayerScreen` at the *same* call site for both layouts, so growing the panel to full screen never rebuilds the ExoPlayer or restarts the stream. `PlayerScreen.kt` keeps one Column with a single video call site for the same reason; the panel shows the channel, the now-playing programme, the server it is on and how many automatic backups happened. Tap the picture (or **⤢ Big screen**) to expand; Back tucks it away.
- **Category rail beside the channel pane.** `HomeScreen.kt` replaces the two-level category page with a side-by-side browser: All channels / Recently watched / Favorites / every category on the left, the selected category's channels on the right, each pane with its own sort, and search across the whole library. Categories with nothing left drop out.
- **Automatic server backup, extracted and tested.** New `ServerFallback.kt` holds the walk rules (`autoNextServerIndex`, `hasBackupServer`, notices, status line, exhausted message) with unit tests. The player marks a failed feed (`ChannelHealthStore`), tries known-dead feeds last, advances on error or a 25 s stall, stops honestly at the last server, and hides the channel when every feed failed.
- **Dead channels are filtered out.** New `data/ChannelHealth.kt` records failed feed URLs for seven days, filters them from the browser, keeps a channel that still has a live backup, and exposes Settings → **Restore hidden channels**. The macOS app gains the same behaviour in `renderer/health.js` (localStorage), wired into `visibleChannels()` and the server walk.
- **One amber pointer outline.** `Theme.kt` adds `FocusRing` (`#FFB020`) and `Components.kt` adds `Modifier.focusOutline`, applied to channel cards, tabs, buttons, category rows, guide cells, search and the side player's picture — 3 dp with a soft glow, never confused with brand gold.
- **The animated loading screen is retired, the line bar stays.** Android's `LoadingScreen` and the macOS splash lose the breathing logo, spinner, shimmer, dots and keyframes; the gold bar remains and now reports the repository's real load stages (`TvRepository.loadProgress` → `LoadingScreen(progress = …)`). `app-update-notice.json` no longer blocks 1.1.0 (it only blocks the deleted 1.1.1 preview) and warns every stable build below 1.1.0.
- **The update notice cannot nag a current build.** `update-below-newest` now covers every stable build below 1.1.0 (1.0.4–1.0.9), so both implementations gained the same guard: a `warning`/`end_of_support` rule is skipped when the installed version is not older than the newest stable the updater found. `blocked` rules stay exempt — the deleted 1.1.1 preview is newer by name than 1.1.0 and must still be blocked.
- **Crash hardening.** Clamped server indices, a watchdog that only advances when a backup exists, guarded playback setup, and guarded dead-feed storage that recovers from corrupt or full storage.
- **Validation:** Gradle unit tests plus the emulator smoke gate (cold launch, Guide, open a channel, server hop, both side-player flips, close) must pass before the release is published; the macOS renderer/health/personal suites and the repository's Python suite run on the same commit.

## 2026-10-21 — Version 1.0.8.2 Bridge + Player Hardening + Updater UX Polish (1.0.9 still newest stable)

- **Bridge release 1.0.8.2 for stranded 1.0.8.1 users.** 1.0.8.1's frozen `COMPATIBILITY_ALIASES` listed `1.0.9 → 1.0.8.1`, so its Settings → App updates wrongly said “up to date”. 1.0.8.2 (`versionCode 100080002`, same fixed 1.0.9 code) is *not* in that alias table, so it *is* seen as newer and installs over 1.0.8.1; after it, 1.0.9 appears automatically. This is the last V-style tag — V patches remain retired otherwise. Tag `v1.0.8.2` at `9ca499c` with Android APK built from that commit; Mac has no crash bug and stays on 1.0.9. See [`release-notes-1.0.8.2.md`](release-notes-1.0.8.2.md).
- **Player hardening (non-crash).** `PlayerScreen.kt`: server fallback index now clamped with `coerceIn` so a rapid double-error cannot overshoot, and a 30-second buffering watchdog auto-advances to the next server if a feed stalls silently (geo-block timeout, stuck HLS). Retains the 1.0.9 single-player + surface-rebind invariant.
- **Updater UX polish for the crash cohort.** `UpdateNoticeDialog.kt` (Android) now shows an “Open download page” button for `blocked` builds — one tap opens the GitHub release in the browser, cutting through the “up to date” white lie. `macos/app/src/renderer/app.js` does the same: a `blocked` popup now calls `api.openExternal(releasesUrl)` instead of opening Settings that would lie. `app-update-notice.json` wording updated to mention the bridge and the new button.
- **Site data regenerated** after `v1.0.9` retag and `v1.0.8.2` publish.

## 2026-10-20 — Version 1.0.9: crash-on-watch fixed; V patches retired

- **Fixed: opening a channel could freeze on black or crash the app (Android).** The player created and released a whole media player per server while the video surface stayed attached to the first, already-released player — after a server fallback, a manual server hop or a side-player flip the picture was dead. 1.0.9 keeps one player per watch screen and swaps the stream inside it (`PlayerScreen.kt`), rebinds the surface on every flip, pauses on background, and only releases the player when you leave the screen. See [`release-notes-1.0.9.md`](release-notes-1.0.9.md).
- **1.0.9 is a real release, and the V-patch/alias scheme is retired.** 1.0.9 briefly existed as the same-code compatibility alias of 1.0.8.1; it now ships the fix as a normal three-part release (Android `1.0.9` / `versionCode 100090000`, Mac `1.0.9`). There will be no V2: every future fix is simply the next version. `COMPATIBILITY_ALIASES` keeps only the historical 1.0.7 → 1.0.6.1 mapping in `scripts/release_version.py`, `AppVersions.kt` and `macos/app/src/main/update-policy.js`; four-part versions are still parsed so old tags and installs resolve.
- **Extreme crash warning on 1.0.8 / 1.0.8.1.** `app-update-notice.json` gains a first-position, Android-only `blocked` rule (`crash-on-watch-1-0-8`, 1.0.8–1.0.8.1): affected builds show a red "update now" popup on launch that hard-codes 1.0.9 (their frozen updater reads 1.0.9 as an alias of itself, so `{newest}` would lie) and spells out the manual-install fallback. The v1.0.8/v1.0.8.1 release pages carry the same warning. Mac is excluded — its player never had the defect.
- **Mac: six dead controls fixed.** The ⧉ Side player button, category Sort toolbar, ◀ All categories back button + category-page toolbar, channel sort chips and ⟳ Refresh live games were never collected into the renderer's `els` map, so their `if (els.X)`-guarded handlers never attached and clicking did nothing since 1.0.8 (Escape still tucked the player, hiding it). Found by the new packaged-app watch test below; a regression test now requires every used `els.<name>` to be collected and present in the page.
- **The watch path is now gated on both platforms.** The Android emulator smoke test taps a channel, rides the automatic server fallback, hops servers, flips the side player both ways, closes it, and watches a live-event card; the Mac packaged-app smoke opens a channel and flips its side player too. This exact tap sequence is what shipped broken while every check was green.
- Note for 1.0.8.1 installs: Settings → App updates can wrongly say "up to date" (that build treats 1.0.9 as itself). Install `PremiumTV-1.0.9.apk` from the v1.0.9 release by hand; it installs in place.

## 2026-10-20 — Version 1.0.8 V1 Patch (1.0.8.1): animated loading, hardened diagnostics, V series in stone

- **Stable 1.0.8 V1 Patch is published** (Android `1.0.8.1` → `versionCode 100080001`, alias `1.0.9` → `100090000`; Mac `1.0.9` alias of `1.0.8.1`) and pushed through the in-app updaters: every 1.0.4+ build finds it in Settings → App updates, and 1.0.8 installs it in place over itself. See [`release-notes-1.0.8.1.md`](release-notes-1.0.8.1.md). This patch sets the V series in stone: V1=1.0.8.1, V2=1.0.8.2 … each V increments the fourth number and its versionCode by one and ships an alias (1.0.9, 1.0.10 …) so 1.0.4–1.0.6 updaters still see it.
- **More animated loading screen.** Both platforms now breathe: a drifting gold haze, a halo that pulses around the TV mark, a sweeping shimmer underline, a segmented progress bar with a racing highlight, and pulsing dots beside the title so the TV never looks frozen. Motion is transform/opacity only, so it stays smooth on TV sticks. Reduced-motion users get a static splash.
- **Better bug detection.** Settings → **Check for bugs** runs 11 checks (was 7): channel list, categories, guide, bundle, refresh, updates, version — plus new **Patch chain** (V ordering this patch establishes), **Stream hygiene** (spaces/malformed URLs), **Guide freshness** (window age in days) and **Library health** (empty/oversized categories).
- **Version plumbing:** `scripts/release_version.py` now understands V display (`--display 1.0.8.1` → `1.0.8 V1`), maps aliases for V1–V5 (1.0.9→1.0.8.1 …), and the Mac/Android updaters share the same alias table. The download page and change log now promote only a complete `v1.0.8.1` (with its alias) as the recommended build.
- **No playlist, scraper, guide or refresh logic changes** — the USA lineup + USA guide are unchanged, and the 1.0.7→1.0.6.1 alias mapping stays alongside the new V aliases.

## 2026-10-20 — Version 1.0.8: the all-new look, the side player, and a Live Events revamp (superseded by V1 Patch)

- **Stable 1.0.8 is published** (Android `versionCode 100080000`, Mac `1.0.8`)
  and pushed through the in-app updaters: every 1.0.4+ build finds it in
  Settings → App updates. See [`release-notes-1.0.8.md`](release-notes-1.0.8.md).
- **Categories are a list — and every list sorts.** The download site, the
  hub, the Mac sidebar and the Android Channels tab all read as one row per
  category (name left, small count right). The site's list, the Mac sidebar
  and the Android tab each get a **Sort** control (Published order, A-Z, Z-A,
  biggest first); a category's channels sort by playlist order, A-Z, Z-A or
  channel number.
- **Click a category and you're in it.** The Android Channels tab is a
  two-level browser now: a category list, then the category's own page with a
  back button and its own channel grid. The Mac category page gets an
  explicit **◀ All categories** back button and channel-sort chips.
- **The side player.** Android's **⤢ Side player** and the Mac's **⧉ Side
  player** tuck the running stream into a corner card while the channel
  browser stays up; clicking the corner picture grows it back to the big
  screen, and the card's close button stops playback. The stream never
  restarts across the flip.
- **Live Events gets its own refresh and tells live from dead.** The tab's
  **⟳ Refresh live games** pulls the newest playlist and re-checks every
  game's feeds; each card's pill reads LIVE (a feed answers), CHECKING, or
  NO SIGNAL (every feed silent), with the checked-live count in the subtitle.
  Two-team matchups show drawn team crests — initials in colours derived from
  the team name, so the same team always wears the same badge, offline.
- **Old-build notice wording goes generic.** `app-update-notice.json` now
  says "{newest}" instead of hard-coding 1.0.6.1, so the popup, the blocked
  preview banner and the end-of-support escalation all name whatever the
  newest stable actually is without another edit.

## 2026-10-19 — Missing channels restored: unverified links no longer delete channels (no version change)

- **Root cause:** the scraper published only links marked `alive`. A channel
  whose only feed timed out, answered 403 (geo/auth from the runner) or hit a
  transient 5xx in a single run was marked `unverified` and deleted from
  `PremiumTV.m3u`, every country/category playlist, the live USA feed the apps
  refresh from, and therefore the apps themselves. In the last checked run
  that was 2,710 unverified links; e.g. ESPN (United States), HBO (United
  States), Cartoon Network (United States) and HGTV (United States) had
  vanished, and NickToons hung on a single bare-IP feed.
- **Durable fix (`scripts/scraper.py`):** previously published links that a
  run can only mark unverified now stay published for a 7-day grace window
  (`--retention-days`, state in `playlists/checks/retention.json`, seeded
  from the run that first failed to verify them). Confirmed-dead links —
  including quarantine and deep-check verdicts — are still removed at once,
  and non-HTTP links are never retained. Reports now carry `retained` /
  `retained_links` so the kept-but-unverified set stays visible.
- **Restored now:** 2,237 feeds across ~2,190 stations that had lost every
  feed to an unverified verdict (and were not dead, quarantined or
  deep-check-dead) are back in `playlists/PremiumTV.m3u` (11,640 → 13,877
  entries) and in every derived country, category, A&E and live-USA file, so
  the next in-app refresh brings them back. `verify_playlists.py --strict`
  passes. NickToons is present in the main, Priority, live-USA, USA-shelf and
  Cartoons files with two US feeds.

## 2026-10-19 — Version 1.0.8 (in source): categories as a list, count small on the right

- **Version marked as 1.0.8 in source** (Android `versionCode 100080000`):
  the Gradle, bundle-tool, macOS package and both build-workflow defaults now
  build 1.0.8. It is not a published release yet — the download site promotes
  it only once a complete `v1.0.8` release exists, so 1.0.6.1 (alias 1.0.7)
  stays the recommended download until then. See
  [`release-notes-1.0.8.md`](release-notes-1.0.8.md).
- **Categories are now a list with the channel number small on the right:**
  the download site's category grid and the hub's category chips became
  one-row-per-category lists (name left, small count at the right edge), and
  the Android Channels category headers moved their small count to the right
  edge. The macOS sidebar already used this layout and is unchanged.

## 2026-10-19 — Version 1.0.6.1: Settings 2.0, Check for bugs, preview retired

- **Stable 1.0.6.1 is cut** (Android `versionCode 100060001`, Mac `1.0.6.1`) with
  a four-part version policy: `1.0.6.1` sorts above `1.0.6` and below `1.1.0`.
  The derived code is `MAJOR * 100000000 + MINOR * 1000000 + PATCH * 10000 +
  HOTFIX`, which is above the retired preview's `100010001`, so the new APK
  installs straight over 1.1.1.
- **A 1.0.7 compatibility build ships the same code.** The updater in
  1.0.4–1.0.6 reads only three-part versions, so 1.0.6.1 alone is invisible to
  it. The same tree is published as `v1.0.7` (`versionCode 100070000`) for those
  apps to find in Settings → App updates. `1.0.6.1` stays the recommended
  download; both updaters skip the alias when the installed build is already
  the canonical one. See [`release-notes-1.0.7.md`](release-notes-1.0.7.md).
- **Settings is one compact screen.** A single version/stat card replaces the
  old three headings; **Force refresh**, **Check for update** and **Check for
  bugs** sit in one action row; one status line replaces competing messages;
  sources, URLs, guide window and Reset moved into a collapsible Details panel.
  The Mac Settings screen gets the same structure.
- **New built-in bug check on both platforms.** Offline and read-only, it
  verifies channels, categories, guide, bundle provenance, refresh pipeline,
  update state, installed version and (on Mac) the bundled files and writable
  data folder, reporting every finding as OK / WARN / FAIL.
- **Fresh rescrape before the release.** The scrape workflow re-tested the
  published sources, rebuilt the category shelf and refreshed the guide before
  the release build baked its bundle.
- **The 1.1.x preview is retired.** The `v1.1.1` release and all of its
  installers are deleted, the download page and hub no longer list a preview,
  the `[preview-build]` switch is gone, and `release-notes-1.1.1.md` was removed.
  A new `docs/blocked/` page is the permanent banner for every old 1.1.1 link,
  and `app-update-notice.json` shows a **BUILD RETIRED** banner to anyone still
  running 1.1.0/1.1.1, with the 1.0.6.1 replacement path.
- **Older builds are warned and can upgrade.** Notices now target 0.0.0–1.0.3,
  1.0.4–1.0.6 and 1.1.0–1.1.1 separately. 1.0.5/1.0.6 users can press Update
  now and finish from Settings; support for builds below 1.0.6.1 ends
  **Nov 16, 2026**.
- **Release routing simplified.** Both build workflows default to `1.0.6.1`,
  keep the exact-SHA asset gate for every release, and no longer contain a
  special mutable-preview branch.

## 2026-10-18 — Version 1.0.6: click-to-search, personal shelves, manual server switching

- **Stable 1.0.6 is cut and becomes the default release** (Android
  `versionCode 100000006`); the **1.1.1 Encore Preview is rebuilt from the
  same tree** and stays a pre-release.
- **Search no longer activates on hover/focus.** The Mac field ships
  read-only until clicked (`/` or Enter also activates); the Android field
  only highlights on D-pad focus and opens editing on OK/click. Typing is
  debounced on Mac.
- **Manual server switching:** the player gains ◀ Server / Server ▶ on both
  platforms — jump between a live game's streams or a channel's backup feeds
  yourself (wrapping), on top of the existing automatic fallback.
- **Recently watched + Favorites shelves** lead the Channels tab/sidebar on
  both platforms, persist on-device, newest-first (30 max for Recents), and
  drop channels that leave the playlist.
- **Less stutter:** no 30 s full-grid rebuild on Mac, rAF-coalesced scroll
  paging, `content-visibility` on cards, no hover-lift repaint; gentler
  1.03× focus zoom on Android cards.

## 2026-10-18 — Version 1.0.5: splash, search, placeholder logos, Live Events and multi-server playback

- **Stable 1.0.5 is cut, and the 1.1.1 Encore Preview is rebuilt from the same
  tree.** Both apps open on a launch splash - the drawn PremiumTV television
  mark, a gold spinner and the build's version pinned at the bottom - instead
  of a bare progress wheel.
- **Android gets channel search** (the Mac sidebar already had one): a field
  above the Channels tab filters by name, category, country or channel number,
  and the Mac search now covers the new Live Events tab too.
- **Logo-less channels get a drawn category placeholder** - a ball for Sports,
  a smile for Comedy, a balloon for Kids, a newspaper for News, a cloud for
  Weather and a television set for everything else - on the cards, in the
  guide rows and in the cable grid, replacing the old two-initials fallback.
  The same art shows while remote logos load and when their URLs die.
- **A Live Events tab groups the scrapers' live-game feeds by sport**
  (Soccer, American Football, College Football, NHL Hockey, …): each card
  shows the matchup, a LIVE pill and how many streams carry the game. The
  games join the stable guide's "what's on now" list with the matchup as
  their listing - the event feeds share placeholder EPG ids, so no upstream
  guide ever schedules them - and their channel cards say `LIVE · <sport>`
  instead of "no listing".
- **Multi-server playback:** a game published on more than one stream, and
  any channel with backup feeds (same EPG id, same base name), switches to
  the next server automatically when a feed dies; the player shows "Server
  2 of 3" and only gives up after every server was tried. Implemented on
  ExoPlayer (Android) and the hls.js/mpegts.js chain (macOS).
- **Honest dead ends:** channels with no published schedule say "No listing
  published" instead of a blank, on both platforms.
- Guides: the merged guide already declares every playlist id and matches
  100% of entries exactly (verified against `EPG/PremiumTV.xml`), so this
  release improves what the apps *show* for uncovered channels rather than
  the harvest itself.

## 2026-10-18 — The popup is readable on a TV, and honest about 1.0.4

- **The buttons can no longer fall off the screen.** The first emulator
  screenshot of the popup on a short panel showed the card running past the
  bottom edge with the *Update now* and *Remind me next time* buttons clipped
  away — a message with no way to act on it. The card is now capped to the
  screen height, only the middle paragraph scrolls, and the buttons sit in a
  fixed footer, so the primary action is always one press away.
- **The copy fits, and says so when it does not.** A 1.0.4 build's message is
  shorter now, so the whole thing reads above the buttons on a short panel; when
  a longer notice still overflows, the card says *"D-pad up on the message for
  the rest"* instead of stopping mid-sentence, which read as a bug.
- **1.0.4 is no longer told a newer release is waiting.** Until 1.0.5 exists,
  the newest release on GitHub *is* 1.0.4, so the old single rule produced "You
  are on PremiumTV 1.0.4. The newest release on GitHub is 1.0.4." The notice
  document now carries two ordered rules: `legacy-upgrade` (0.0.0–1.0.3) names
  the release that is waiting, and `last-manual-install` (1.0.4) explains that
  this build is the one that updates itself and when its support ends, without
  claiming a download that does not exist yet.
- **The emulator gate exercises the popup instead of tripping over it.** It
  recognises the dialog, records `build-out/smoke-update-notice.png` as
  evidence, and presses the published dismiss button — read from
  `app-update-notice.json`, including the after-support-ends wording — so the
  gate keeps working on either side of the sunset.

## 2026-10-18 — The notice is actually delivered to installed 1.0.0–1.0.4

- **The warning now reaches builds that have no notice code.** Until today the
  notice only existed in builds made from this code: an installed 1.0.0–1.0.3 had
  nothing to read it, and 1.0.4 shipped before it existed. The one thing they all
  fetch is the USA playlist baked into their bundles, so
  `playlists/countries/USA.m3u` now carries one sanctioned entry — marked
  `tvg-notice="app-update"` — as the first row of the channel list:
  `⚠ UPDATE PremiumTV — support for 1.0.4 and older ends Nov 16, 2026 · the newest
  build updates itself: github.com/…/releases`. It appears under a `PremiumTV
  Notice` group on their next refresh and can be dismissed by updating, which is
  the point.
- **Verified against the shipped parser, not a copy of it.** The exact
  `parsers.js` from the `v1.0.4` tag parses the published file into 2,730
  channels with the notice first; the 1.0.5 parser drops the marker and sees the
  2,729 real channels. Android's parser gets the same behaviour with a Robolectric
  test, and `parseM3u` has a Node test for both cases.
- **Nothing treats the message as a channel.** `link_check.py` never probes the
  releases URL and can no longer patch the entry out as a dead link,
  `verify_playlists.py` excludes it from the group, order, id and dead-link
  checks, and `epg_build.py` never adds it to a guide. `legacy_sunset.py check`
  now fails a publishing run that drops the entry, so the warning cannot quietly
  disappear from the feed before the sunset.
- **The live feed stays clean.** `playlists/live/USA.m3u` — what 1.0.5+ and the
  bundle builder read — never carries the entry, so current builds see the proper
  popup and never a fake channel.
- **`main`'s pipeline is green again.** Two repeated URLs in
  `playlists/PremiumTV.m3u` (an otteravision stream and a UniversMotri feed) were
  failing the offline suite, the Android bundle check and the scrape itself; the
  repository's own dedupe removed them and the `categories/` shelf was rebuilt.
  The live USA feed was also re-synced from the last scrape, which is what the
  38-file shelf drift reported.

## 2026-10-17 — Older builds are told to update, and 1.0.0–1.0.4 get a sunset date

- **A startup popup sends an out-of-date build to GitHub.** Both apps now show a
  dialog when the installed version is inside a published notice's range: what is
  installed, what the newest release is, where to get it, and why it is worth it.
  On Android it floats above every screen except the player and takes focus on the
  primary button, so a remote needs one press; on macOS it is a modal that Esc
  dismisses. **Update now** opens Settings → App updates and re-checks GitHub —
  the installer still downloads only on the Settings button, so the "no background
  downloads" rule holds whichever button started it.
- **The surprise is the update center itself.** The copy says plainly that the
  newest build is the last one anybody has to install by hand: from there
  PremiumTV checks GitHub, downloads the installer once, verifies it against the
  release's SHA-256 file and hands it to the platform's normal installer.
- **Dismissible, but it comes back.** A TV remote can arrive mid-evening, so an
  app that refuses to run would turn "please update" into "your TV is broken". The
  dismissal lasts one launch and is deliberately never persisted — not in
  `SharedPreferences`, not in `update-state.json` — so the notice returns every
  launch until PremiumTV is updated, and one press cannot hide it for good.
- **The wording, the target versions and the sunset date are published, not
  compiled in.** `app-update-notice.json` at the root of the repository is read
  during the same daily check that reads the release list, and cached, so the
  popup is decided before any network call and still appears offline. Changing the
  message, the version range, or silencing every popup with `enabled: false` needs
  no new release. A notice that cannot be read, is oversized, or names a schema
  this build has never seen keeps the last good copy and can never fail the update
  check that already succeeded.
- **End of support escalates itself.** Each rule carries its `after_support_ends`
  wording, so on the day `support_ends_utc` passes the same notice turns from "a
  surprise is waiting" into "this build is frozen" and its accents turn red — with
  no fetch, no rebuild and no remote edit.
- **1.0.0–1.0.4 stop receiving scrape updates 30 days after the first warning.**
  None of them can show this popup: 1.0.0–1.0.3 ship no updater at all (the
  `v1.0.3` tree has neither `AppUpdateManager.kt` nor `updater.js`), and 1.0.4 has
  the update centre but was released before this notice existed. So they can only
  be reached through the one playlist they refresh. 1.0.4 can still escape on its
  own — its Settings → App updates will offer the next release — it just will not
  be told to look; 1.0.0–1.0.3 have no such route, which is why the frozen feed
  carries the message for them. `raw.githubusercontent.com` serves the same bytes to
  every caller and cannot look at a version, so delivery is split in two:
  `playlists/live/USA.m3u` for builds that can still update, and
  `playlists/countries/USA.m3u` for 1.0.0–1.0.4. While support lasts the two are
  identical; on the published date `scripts/legacy_sunset.py` pins the last
  scraped channel list to `playlists/legacy/USA.m3u` and rewrites the legacy feed
  from that pin with one sanctioned notice entry on top. Those builds keep the
  channels that worked that day, see `⚠ UPDATE PremiumTV — support for 1.0.4 and
  older ended Nov 16, 2026 · get the newest free version at github.com/…` as their
  first entry, and stop getting new ones. The frozen feed keeps advertising the
  live `EPG/USA.xml`: what ends is the channel scrape, not the listings.
- **The notice entry can never become a channel.** It is marked
  `tvg-notice="app-update"` and both apps' parsers drop an entry carrying that
  marker, so it cannot reach a channel list, a category, the `categories/` shelf or
  the download site of any build that understands it. Only builds too old to know
  the marker render it — which is exactly who it is for. A 1.0.3-era parser was run
  against a frozen feed to confirm it does.
- **Nothing that must stay current points at the pin.** `build_bundle.py`,
  `build_categories.py`, `build_site_data.py` and `verify_playlists.py` all resolve
  the USA list through `legacy_sunset.live_usa_path()`, so the shelf, the download
  site, the verifier and the next APK follow the live channels on the day the
  legacy feed freezes. Every publishing workflow runs `legacy_sunset.py apply`
  after the playlists are written and before the shelf is built, and
  `legacy_sunset.py check` fails a run when the sunset has been quietly undone.
- **Verification.** 470 Python tests (34 new for the sunset, 13 new for the popup
  contract, and the site-data contract updated for the live USA feed) and 82 Node
  tests (19 new: version targeting, the escalation, the offline startup path, and
  the launch-scoped dismissal).

## 2026-10-17 — PremiumTV 1.0.4: one last manual install, then updates from Settings

- **In-app update center on both platforms.** Settings → App updates now shows
  the installed version, the newest published stable release, the last check and
  a clear status, with **Check for updates**, **Download update** and
  **Install update** (Android) / **Open installer** (Mac). Checking is manual or
  once a day at startup; the installer downloads only when the user asks.
- **No repeated downloads.** A verified installer is stored once per version and
  reused on every later check or button press; after the update is installed,
  the old installer is pruned. The daily check sends GitHub its previous ETag,
  so an unchanged release list is a single `304 Not Modified` response.
- **Stable only, strictly newer, complete.** Both updaters ignore drafts and
  pre-releases, compare versions numerically (`1.0.10` > `1.0.9`), and require
  the platform installer to be attached. An installed preview (1.1.1) is ahead
  of stable 1.0.4 and is never offered an older build. The Mac updater verifies
  the DMG against `SHA256SUMS-macos.txt`; the Android updater verifies the APK
  against `SHA256SUMS-android.txt`, then hands it to Android's package installer
  through a one-file `FileProvider` (with the normal unknown-sources prompt).
- **One signing identity for every APK.** Android only installs an update over
  an app signed by the same certificate. Earlier CI builds each generated a
  fresh random debug key, so 1.0.0–1.0.3 could not update in place. From 1.0.4
  on, every APK is signed with the checked-in long-lived key
  `android/keystore/premiumtv-updates.p12`, and the Android workflow fails the
  build unless the APK certificate matches the pinned fingerprint. 1.0.4 is
  therefore a one-time clean install (uninstall 1.0.3 or older first); later
  releases install straight over it.
- **Release guard.** A new `Release version guard` workflow checks every
  published stable release against the newest stable release. A tag that is not
  above the current stable is converted to a pre-release (so no app can offer
  it) and the run fails with an explanation. Versions and Android versionCodes
  now come from one policy, `scripts/release_version.py`:
  `MAJOR * 100000000 + MINOR * 10000 + PATCH`. 1.0.4 is code `100000004`.
  The guard understands both the REST shape and the camelCase shape emitted by
  `gh release list --json` (`tagName`, `isPrerelease`, `isDraft`), so a release
  that is not above the current stable is actually caught and demoted.
- **Version 1.0.4 is the stable default.** Android and macOS defaults, both
  build workflows, the bundle builder and the download-site data all target
  1.0.4. Both build workflows accept future versions from the release tag or a
  manual version/channel dispatch, and every release builds both platforms.
  Stable builds use the USA scope; pre-releases use the global scope.
- **Encore Preview stays Encore Preview.** The 1.1.1 pre-release keeps its name,
  global lineup and cable-style Guide tab, and now carries the same update
  center. A rebuilt 1.1.1 uses the derived `versionCode 100010001`, so it stays
  installable above stable 1.0.4; the explicit `[preview-build]` switch still
  rebuilds only that existing pre-release.
- **Documentation and downloads.** Added `release-notes-1.0.4.md` and
  `docs/UPDATES.md` (policy plus the process for publishing the next stable
  release), updated both apps' READMEs, the download page and hub copy, and
  added 1.0.4 to the hub's asset mirror list.
- **Channel-lineup preview on the download site.** A new **Channels** section
  is generated from `playlists/PremiumTV.m3u`: unique channels and backup feeds,
  categories and countries, quality labels, a row of recognisable channels
  (ESPN, NFL Network, CNN, HBO, Nickelodeon, Cartoon Network, …), and a
  searchable category grid with sample names and direct links to each published
  category playlist. The counts are read from the playlist, so the page cannot
  advertise a channel the current lineup does not carry.
- **Backup integrity fixed and audited.** Backup feeds are now numbered per
  display name across every identity group, case-insensitively and in a stable
  identity-group order, so two feeds of the same station can no longer publish
  as “X (Backup 1)” and re-running the rebuild no longer renumbers them. The
  rebuild removed the duplicates for Billiard TV, World Poker Tour,
  Moviedome/MOVIEDOME, Pluto TV Sitcoms, Pluto TV Serie and Action Hollywood
  Movies, and rebuilding the result reproduces every name. All 1,424 backup names
  in `PremiumTV.m3u` are unique and each one has a primary channel. The main
  playlist still carries 11,444 entries (10,020 unique channels) with no
  duplicate URLs.
- **Category files cannot drift again.** `scripts/rebuild_playlists.py` now cuts
  every per-category playlist from the *published* order, not the parser’s
  pre-sort input, and deletes category files for groups that disappeared or fell
  below the three-channel threshold. This cleared seven stale playlists
  (`Public_TV`, `Public_TV_Backups`, `Tv_Reality`, `Tv_Reality_Backups`,
  `Online_TV_Backups`, `Family_Backups`, `Global_TV_Backups`) that still held
  channels and guide headers no longer in the lineup; the remaining 81 files
  match `PremiumTV.m3u` entry for entry.
- **Verification snapshot.** `scripts/verify_playlists.py --strict` reports 177
  playlists / 22,974 entries with 0 problems, 0 published links the deep check
  called dead, and all 132 files on the `categories/` shelf in step. Quality
  labels in the main playlist: 2,711 channels at 1080p, 8 at 4K, 2,314 at 720p,
  602 at 576p, 285 at 480p and 3,891 without a resolution tag; 924 channels have
  at least one spare feed.
- **Download checksums describe the file you actually get.** The download page
  preferred a checksum from the checked-in `build-out/` directory, which still
  described an earlier local 1.0.4 APK (16,079,074 bytes) while the published
  release asset is 16,090,467 bytes. `build_site_data.py` now trusts GitHub's
  release digest first and falls back to `build-out/` only when a release has no
  digest; a site test compares every published asset with its release digest.
- **Backup audit is now a repeatable check.** Added
  `scripts/audit_backups.py` and [`playlists/checks/BACKUP-AUDIT.md`](playlists/checks/BACKUP-AUDIT.md).
  It reports unique backup names, orphan feeds, continuous numbering, duplicate
  URLs, quality labels, and whether every `playlists/categories/*.m3u` file is
  an exact slice of the published playlist. Both the scrape and biweekly
  workflows run it with `--strict`, so a future duplicate backup name or a
  stale category file fails the verification step instead of shipping.

## 2026-10-16 — Everyday Polish + Encore Preview

- **Shared loading UX for stable 1.0.3 and preview 1.1.1.** Non-modal activity
  panels show loading/refresh stages, elapsed time, rotating offline tips and
  facts, then a 15-second result. Settings retains the last refresh outcome;
  failed downloads keep the current library. Refresh/reset controls are guarded
  while busy; Mac refresh requests coalesce instead of queueing duplicate work.
- **Encore Preview.** 1.1.1 is renamed “Encore Preview: Cable Guide + Everyday
  Polish”, retains the global cable guide and stays a pre-release. Its Android
  revision uses code 11, above stable code 10 and the original preview code 9.
  Android cannot downgrade code 11 to stable 10 without uninstalling first.
- **Release validation.** Added activity lifecycle, failure preservation,
  duplicate-request and non-modal renderer tests. Both platform build workflows
  retain their unit-test and packaged-app smoke gates. An explicit
  `[preview-build]` push switch rebuilds only the existing 1.1.1 pre-release,
  recording per-platform source manifests without moving the historical tag;
  stable attachments remain exact-SHA guarded.
- **Stable 1.0.3 published as Latest.** Android JVM/emulator checks and Mac
  unit/packaged-app smoke checks passed; the APK, all four Mac installers and
  platform checksums were attached before promoting the release.
- **Both download sites updated.** The Netlify hub now shares the published,
  complete-stable gate with the main site instead of hardcoding 1.0.2. Both
  explain Everyday Polish and Encore. Static APK downloads use release storage
  and authoritative release sizes rather than embedding stale local builds.
  Netlify Drop still requires uploading the rebuilt folder to the existing site.
- **Encore installers published.** The rebuilt APK and all four Mac installers
  passed their unit/emulator/packaged-app gates and replaced the existing 1.1.1
  pre-release assets. The preview remains separate from Latest stable 1.0.3.
- **Manual checked scrape completed.** Run `38969629022` checked 16,722 unique
  links and published 11,453 confirmed-working entries; 2,317 dead and 2,952
  unverified links were excluded. Verification reports zero structural playlist
  or shelf problems. The run carries a warning because three optional sources
  are not configured. An app refresh downloads published data; it is not a
  server scrape. These are point-in-time checks, not uptime guarantees.
- **Final local validation:** 375 Python tests and 46 Mac/website Node tests
  pass. Both versions also passed their Android and Mac CI smoke gates.

## 2026-10-16 — PremiumTV 1.0.3 maintenance + download-site reliability

- **Stable 1.0.3 build prepared.** The Android default now uses `versionName
  1.0.3` / `versionCode 10` (above preview code 9), the macOS package and
  bundle defaults are aligned, and both release workflows accept `v1.0.3` only
  as a full stable release. The USA lineup and list-style guide remain the
  stable scope; the 1.1.1 cable guide stays preview-only. The current published
  stable download remains 1.0.2 until 1.0.3 has its complete asset set.
- **Download site data stays current.** The Pages workflow now runs on
  `CHANGELOG.md`, playlist/report/country/EPG changes and published releases;
  it also runs after scheduled/manual data workflows because their bot commits
  do not trigger push workflows. It refreshes release asset metadata before
  rebuilding. The download page only
  promotes a stable release once the APK and all four Mac installers exist.
  Its live changelog refresh compares entry contents (so editing an existing
  entry also updates open pages), and generated data/Atom timestamps are
  reproducible so `build_site_data.py --check` can work reliably.
- **Public Pages status verified.** The repo is public, but GitHub Pages itself
  is not enabled: the Pages API returns 404, and this integration is denied
  permission to create the site (403). The workflow cannot change that admin
  setting; the owner must set **Settings → Pages → Source: GitHub Actions** once.
- **Manual checked scrape completed.** Run `20261016T103351Z-2912` finished at
  10:38 UTC on October 16. It confirmed 11,365 of 16,628 unique source links,
  reported 2,292 dead and 2,971 unverified candidates, and regenerated the
  175-country set; the scraper correctly marked this as a warning rather than
  claiming every source worked.
- **A full stream and guide check followed.** Deep HLS/segment checks covered
  11,365 unique links across the published playlists: 22,633 of 22,797 playlist
  entries (99.3%) returned playable media. It removed 22 confirmed-dead
  occurrences only, taking `PremiumTV.m3u` from 11,365 to 11,354 entries and
  the USA playlist from 2,682 to 2,679. The 128 unreachable and 14 blocked
  results were retained because a timeout/server error or geo/auth block is not
  proof that a stream is dead. Strict verification passed with no structural
  problems, no known-dead links left published, and all 134 category-shelf
  files in sync. The refreshed merged guide contains 116,992 programmes across
  1,757 of 9,769 playlist channels (18.0% coverage); guide coverage remains an
  upstream limitation, not an app defect.
- **The newest main scrape and post-merge deep check are verified.** The
  scheduled main report `20261016T174225Z-2917` (Actions run
  [38941630689](https://github.com/cgyegcvcecvoc/PremiumTV1/actions/runs/38941630689))
  confirmed 11,459 of 16,627 unique source links, with 2,216 reported dead and
  2,952 unverified across 175 country playlists. This newer scrape was kept
  when resolving PR #47's generated-data conflicts. The main-branch
  [deep-check run 38946889717](https://github.com/cgyegcvcecvoc/PremiumTV1/actions/runs/38946889717)
  then rechecked report `20261016T182340Z-2687`: 22,657 of 22,903 playlist
  entries were playable (98.9%). It removed 46 confirmed-dead occurrences and
  retained 186 unreachable / 14 blocked results. The final `PremiumTV.m3u`
  has 11,398 entries and the USA playlist 2,694. Strict verification found 0
  structural problems, 0 published known-dead links, and all 134
  category-shelf files in sync. The rebuilt merged guide has 113,236 programmes
  across 1,750 of 9,797 channels (17.9% coverage).
- **Final 1.0.3 app builds pass on main, with the APK and sidecar in sync.**
  The post-merge [Android CI run
  38951826549](https://github.com/cgyegcvcecvoc/PremiumTV1/actions/runs/38951826549)
  passed unit tests, emulator cold-launch/relaunch and stable list-Guide smoke
  tests, APK collection, and output publication. At build time,
  `build-out/PremiumTV-1.0.3-debug.apk` contains 2,694 USA channels, 61 groups,
  and 25,529 programmes (426 with guide listings). SHA-256:
  `8fc25ecaefb3148f82d73095d3297a5a5f6000e0fc7af9bb45b98f5e1e33f59c`;
  the sidecar metadata matches the embedded APK metadata. The [macOS CI run
  38949988204](https://github.com/cgyegcvcecvoc/PremiumTV1/actions/runs/38949988204)
  passed unit and packaged-app smoke tests on Apple Silicon and Intel/Rosetta,
  and produced the four x64/arm64 DMG/PKG installers in its Actions artifact.
  They are ad-hoc signed, not notarized. An earlier main Android build
  (38949988205) failed the emulator smoke gate and exposed a publisher bug that
  could update metadata without collecting an APK. PR #49 gated metadata
  publication on both smoke-test and APK-collection success; the subsequent
  main build above passed. These remain tested build outputs, not a published
  1.0.3 release; 1.0.2 remains the public stable-download fallback until a
  complete 1.0.3 release is published.

## 2026-10-15 — 1,999 missing channels restored + public download site

- **The missing channels are cleared out and fixed.** The 2026-10-13 deep
  check resolved HLS variants against the redirector's M3U URL instead of the
  URL that finally served the playlist, so redirector channels (1,344 `jmp2.uk`
  Pluto links plus ~655 others) were quarantined as `variant HTTP 414/404` and
  removed. The checker's writer was fixed that day, but
  `scraper.load_quarantine()` never applied the same rules, so every scrape
  still marked those links dead even when its own check found them alive —
  they could not come back.
  - `scraper.py` now owns the shared rules (`quarantine_reason_is_conclusive`,
    `quarantine_entry_proven_dead`) used by the scraper's reader, the deep
    check's writer and the cleanup's compactor, so the three can never disagree.
  - `playlists/checks/quarantine.json` was compacted under those rules
    (2,682 → 683 proven-dead entries). The 1,999 released links returned to a
    checked re-scrape, which re-verified each one over the network:
    **confirmed-working channels went 9,822 → 11,705 (+1,883 restored)**, dead
    links 3,995 → 2,060, and A&E channels 58 → 67. The deep check that
    followed then re-probed all 11,705 published links with the fixed
    HLS rules — **97.5% answered with playable media** — and patched the 416
    confirmed-dead entries out. Three channels in the briefly-revived Bermuda
    and San Marino playlists were confirmed truly gone (their variant
    playlists 403/404), so those two single-channel country files were cleared
    out again; 175 countries remain. Links that are genuinely gone are
    re-quarantined under the current rules and stay out.
- **New: the public download site** (`docs/`, GitHub Pages at
  [`cgyegcvcecvoc.github.io/PremiumTV1`](https://cgyegcvcecvoc.github.io/PremiumTV1/)):
  - **Apps**: every release asset for the Stable (1.0.2) and Preview (1.1.1)
    channels — Android APK, macOS `.dmg`/`.pkg` for Intel and Apple Silicon —
    with sizes, SHA-256 checksums, install help for Android TV/Fire TV and
    macOS, and links to older releases.
  - **Best working M3U for your country**: the page detects the visitor's
    country in the browser and hands them that country's confirmed-working
    playlist (copy URL, download `.m3u`, QR code, that country's guide URL),
    plus a custom bundle builder that merges any set of country playlists into
    one `.m3u`. All 175 country playlists are listed with live channel counts.
  - **Change log**: the timeline on the page, the Atom feed
    (`data/feed.xml`) to subscribe to, and a live re-fetch of
    `docs/data/changelog.json` so new entries appear without redeploying.
  - Deployed by `.github/workflows/pages.yml`, which regenerates the data and
    publishes `docs/` on every relevant change to `main`. **One manual step
    remains:** creating the Pages site is an admin action GitHub refuses
    `GITHUB_TOKEN` and integration tokens (`403 Resource not accessible by
    integration`), so the repository owner must open
    **Settings → Pages → Source: GitHub Actions** once; the workflow then
    publishes (and its failure summary repeats these instructions). Site data
    is regenerated offline by `python scripts/build_site_data.py`.
- **"Run it now" switches fire again.** The `playlists/logs/run-*.txt` push
  switches (`run-scrape.txt`, `run-deep-check.txt`, `run-epg-build.txt`,
  `run-cleanup.txt`) never triggered outside of `workflow_dispatch`: a push
  block with only `tags-ignore` and `paths` does not evaluate the paths filter
  on branch pushes. All four workflows now declare `branches: ["**"]` like the
  build workflows, which demonstrably fire.
- **Change-log discipline:** this entry is the first under the policy above —
  every future request is recorded here, and the site/feed are regenerated with
  it.

## 2026-10-15 — PremiumTV 1.1.1 pre-release: the Guide tab is a cable-style grid

- **The cable guide is real and visible now.** In the 1.1.1 preview the Guide
  tab of both apps *is* the cable-style grid: channels down the left (number,
  logo, name, category), each channel's shows to the right sized by running
  time, half-hour times across the top for eight hours, a red NOW line, the
  live show outlined, category headings, and a detail strip for the
  highlighted show. Stable 1.0.2 keeps the list-style Guide.
- **Why 1.1.0 did not show it:** its grid was a separate Cable tab gated on the
  *loaded* library's metadata, and an in-place upgrade kept the 1.0.x USA
  download in the cache, which loads before the bundle — so the app showed the
  old lineup and no Cable tab. Both apps now discard a downloaded copy written
  by another version or library scope (with its validators), and the preview
  features always come from the app's own bundle.
- **TV remote:** the grid is one focus stop with a cable-box highlight — up/down
  keep the time column, left/right step one show, OK plays, Back from the
  player returns to the same show, up from the first row returns to the tabs,
  CH+/CH− page, and the remote's GUIDE key opens the guide. Mac: hover and
  arrow keys, sidebar categories filter the grid.
- **Android refresh** parses the guide off the HTTP stream (the 38 MB global XML
  no longer becomes a ~200 MB String), keeps the published category order,
  and no longer blames a "private repository" (the repository is public).
- **Release gating:** `v1.1.1` builds only as a GitHub pre-release (Android
  `versionCode 9`, global scope); a stable-tagged `v1.1.1` is rejected. The
  emulator gate opens the Guide, checks times/channels/shows, drives the D-pad,
  OK and Back, and saves screenshots; the Mac gate opens the Guide grid.

### Maintenance (same day)

- **Deep link check removed working channels.** HLS variants and segments were
  resolved against the M3U link instead of the URL that finally served the
  playlist, so redirectors (jmp2.uk and the mjh.nz hosts) failed every variant
  with 414/404: the 2026-10-13 nightly run removed ~1,700 entries
  (`PremiumTV.m3u` 10,917 → 9,759) and quarantined them. Fixed, and the
  quarantine drops entries recorded under the old rules.
- **"Deep link and guide check" failed on 10-14 and 10-15.** A CDN answering 429
  to segment probes made working links "offline"; `verify_playlists --strict`
  then failed because they were still published. Rate limits, 5xx and timeouts
  one level below a working playlist are now "unreachable" (kept), matching the
  playlist-URL rules.
- **"Biweekly deep cleanup" failed on 10-15.** `--report-suffix "-archives"` was
  parsed by argparse as an option (exit code 2), so the archive sweep never ran;
  the workflow now passes `--report-suffix=-archives`.
- All workflows moved to Node 24 action majors (`checkout@v5`,
  `setup-python@v6`, `setup-node@v5`, `upload-artifact@v6`, `setup-gradle@v5`);
  the scheduled data jobs pin `ubuntu-24.04` ahead of the 2026-10-19
  `ubuntu-latest` → Ubuntu 26.04 move.
- Tests: 361 Python (12 new) and 42 macOS Node (4 new), plus new JVM/Robolectric
  Android tests for the guide model, stale caches and streaming XMLTV parsing.

## 2026-10-14 — PremiumTV 1.0.2 released, 1.1.0 published as a pre-release

- **1.0.2 is the published stable release.** It is the USA lineup + USA guide
  with Android `versionCode 7`, and it carries the parser, playback and
  channel-health fixes prepared earlier the same day (comma-safe `#EXTINF`
  names, strict XMLTV timestamps and repaired non-positive durations, exact
  id+URL backup-stream selection on Mac, correct proxy-session release, newer
  confirmed media probes superseding older quarantine entries).
- **1.1.0 is published as a GitHub pre-release.** Global checked lineup
  (9,788 channels, 89 categories) plus the merged guide (105,319 programmes
  across 1,650 channels) and the optional cable-style guide, which stays gated
  on `preview_features: ["cable-guide"]` so the stable build never shows it.
  Android `versionCode 8`. It must keep the pre-release flag and never becomes
  the default.
- **Android build fix.** The merged preview code called `initialsOf()` from
  `CableGuide.kt` while the helper was file-private in `Components.kt`, so
  `compileDebugKotlin` failed with "Cannot access 'fun initialsOf(...)': it is
  private in file" and the tagged release could not produce an APK. The helper
  is now `internal` and shared by the channel cards and the cable grid. This was
  a visibility-only change; the wire format, bundle and UI are unchanged.
- **Preview header fix, found by the release gate.** The 1.1.0 build passed
  Gradle but failed the emulator cold-launch check. The captured log showed the
  app alive and focused with the global cards on screen — and the header's
  status line missing entirely: with the extra Cable tab and the longer
  `1.1.0-debug · PREVIEW` plaque, the weighted `<count> channels · …` text was
  measured at zero width on a narrow screen. The title, plaque and status line
  now share the first row and the tabs get a scrollable row of their own, so the
  status line always renders and no tab can be clipped. The gate itself was
  resized for the global bundle (explicit adb timeouts, 240s UI window, retried
  dumps) and now saves `build-out/smoke-log.txt` on failure.
- Release CI builds both tagged versions from the release commit and attaches
  the APK, the `.dmg`/`.pkg` installers and the per-platform checksum manifests
  to the matching release page. Offline validation on the release commit: 349
  Python tests, 38 macOS Node tests, and the strict verifier reporting 177
  playlists / 19,650 entries with zero structural problems and zero published
  dead links.

## 2026-10-14 — Prepared 1.0.2 stable and 1.1.0 preview

- Kept **1.0.2** as the default stable target: Android `versionCode 7`, USA
  playlist/guide, and macOS package version 1.0.2. The 1.0.2 release is prepared
  but has not been published.
- Set up **1.1.0** as a separate GitHub pre-release target: Android
  `versionCode 8`, the checked global playlist and merged guide. Workflows only
  build that scope for the 1.1.0 preview and reject a stable-tagged 1.1.0.
- Added an optional cable-style, eight-hour EPG grid to both apps. The tab is
  controlled by bundle metadata (`preview_features: ["cable-guide"]`), so it is
  absent from the stable USA build.
- Fixed M3U display names containing commas and tightened XMLTV timestamp/end
  validation in the builder and app parsers. Fixed Mac duplicate-EPG-ID stream
  selection and reliable proxy-session release; added regression tests.
- Reconciled stale dead-link/quarantine evidence against a later successful
  deep channel-hunt result, so two streams re-proven playable are not falsely
  reported as dead. The verifier now lets newer confirmed media probes supersede
  older quarantine entries.
- Updated the macOS XML parser dependency and release-build configuration.
  Offline validation passes: 349 Python tests, 38 macOS Node tests, and the
  strict verifier (177 playlists, 19,650 entries, zero problems or published
  dead links). Android Gradle/emulator and macOS packaging remain platform-CI
  checks; Java is not available in this sandbox. No release was published.

## 2026-10-13 — PremiumTV 1.0.1 — channel-loading hotfix

- Fixed the Mac renderer retaining an empty startup snapshot after the main
  process finished loading channels. State/progress events now fetch the actual
  library, rebuild the guide index, and ignore stale IPC replies.
- Fixed Mac refresh validators being read from the wrong saved-state field;
  a corrupt cache fallback no longer sends validators for a discarded copy.
- HLS redirects now resolve relative segments and encryption keys against the
  final upstream URL, rather than the original pre-redirect URL.
- Added DOM regression tests, proxy HTTP coverage, five Android/Robolectric
  library tests, Android emulator cold-start/relaunch checks, and real packaged
  Electron smoke tests for Intel and Apple Silicon before installer uploads.
- Version 1.0.1 on both platforms; Android versionCode 6. Platform-specific
  checksum manifests avoid the two build jobs overwriting one shared file.
- Release CI fix (same day): the new Android emulator gate never booted —
  the runner had ~6.7 GB free while a default AVD data partition needs
  ~7.4 GB, so the emulator exited with "Not enough space to create userdata
  partition" and the APK collect/attach steps were silently skipped, leaving
  this release's draft without its Android APK. The Android workflow now
  frees the unused preinstalled toolchains and uses a 2048M AVD data
  partition; the cold-start/relaunch gate passes and the APK attaches.
- Upstream stream availability and private-repository refresh access remain
  external limitations; this patch does not promise every live feed is online.

## 2026-10-12 — PremiumTV 1.0.0 "Marquee" — the first official release

- **A guide for every channel.** New `sources.json` → `epg_sources` curated
  guide registry: `scripts/epg_sources.py` expands one upstream XMLTV URL per
  published country — `https://iptv-epg.org/files/epg-<cc>.xml.gz` (iptv-epg.org,
  76 countries) and `https://epg.pw/xmltv/epg_<CC>.xml.gz` (epg.pw, 21 countries)
  plus epg.pw's one-for-all `epg.xml.gz` and the `epg-us.xml` US guide that was
  picked out for the release — 345 curated feeds across 172 countries. The
  nightly guide check verifies every URL; the guide build merges the working
  ones ahead of the two or three guides a scraped M3U used to advertise, which
  is what left most channels without listings. Result on the release build:
  **1,658 channels with real listings (19.6%) and 99,079 programmes, up from
  172 channels and 10,090 programmes**, and every one of the 8,460 published
  channel ids is declared in the guide — including `epg-us.xml.gz` (13,373
  programmes) and epg.pw's `epg.xml.gz` (1,390 channels matched). Per-country
  guides grow the same way automatically as upstream families publish more
  `epg-<cc>` files; no listings are ever invented for channels no guide
  schedules.
- **Backup feeds share their station's schedule.** Display-name matching is now
  country-aware: when several published ids share one name and one country,
  all of them receive the same verified listings ("Nickelodeon" US backups get
  the US schedule), while same-name channels in other countries never do. The
  country of a per-country source file (`epg_DE.xml.gz`) counts even when the
  channel id has no `.de` suffix, three-letter names ("CNN", "TLC") match
  again, and cross-country names without any country signal stay unmatched
  rather than guessed.
- **Refreshes verified in both apps.** Settings' *Force refresh all now* and
  the automatic WorkManager/timer slots keep passing the contract tests on
  Android (`tests/test_android_refresh.py`) and macOS
  (`tests/test_macos_app.py`, `macos/app/test/*.test.js`): slots mirror the 13
  publishing windows, requests are conditional (ETag/Last-Modified) yet
  manually bypassable, serialized, and installed atomically with a backup
  rollback. Release verification: 343 Python tests + 25 Node tests green, and
  both CI release builds green (Gradle APK with the in-repo Android SDK
  Layoutlib toolchain; electron-builder DMG + PKG for Apple silicon and Intel).
- **Marquee UI on both platforms.** Cinema-gold-on-midnight theme with a
  playbill voice: marquee-plaque brand mark and version tag, gold-underlined
  tabs and category selection, ON-AIR style NOW badges, lifted channel cards,
  "No listing" honesty labels and gold primary actions. Same layouts, same
  D-pad/keyboard behavior, same hidden-overlay fix on the Mac.
- **One official release page.** `v1.0.0` carries the Android APK
  (`versionName 1.0.0`, `versionCode 5`) and the four Mac installers
  (dmg/pkg for Intel and Apple Silicon). Both build workflows attach to the
  same tag and only when the tag points at their own commit. Superseded
  release pages (beta 4, experimental.1) are removed; their Git tags remain.

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
