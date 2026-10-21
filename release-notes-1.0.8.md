# PremiumTV 1.0.8

> ⚠️ **CRASH WARNING — update to [1.0.9](release-notes-1.0.9.md) now.** This version can freeze on a black picture or crash when you open a channel (on Android the video surface stays attached to a released player after a server switch). 1.0.9 fixes it and installs in place. Do not stay on this build.

**Status: superseded by 1.0.9.** Android `versionCode 100080000` (derived by
`scripts/release_version.py`: `1.0.8` → `100080000` — above `1.0.7` /
`100070000` and every older build, so it installs in place over every previous
stable and the retired 1.1.x previews). Every 1.0.4+ app finds it in
Settings → App updates: check, download once, verify the SHA-256, install.

## The all-new look

- **Categories are a list — and every list sorts.** Everywhere categories are
  listed they read as one row per category: the name (and its drawn mark) on
  the left, the channel count small on the right.
  - **Android TV:** the Channels tab is now a two-level browser. The tab is a
    *category list* (personal shelves first, then one row per category); a
    **Sort** chip cycles **Published order → A-Z → Z-A → Most channels**.
    Clicking a row lands on that **category's page** — back to the list with
    one press, its own channel grid, and its own **Sort** chip cycling
    **Playlist order → A-Z → Z-A → Channel number**. Search filters the
    category page, or the whole library from the list.
  - **macOS:** the sidebar's category list gets the same four sort chips
    (Published / A-Z / Z-A / Biggest), a category page header with
    **◀ All categories** back, and channel-sort chips (Published / A-Z / Z-A /
    Number) on the category page.
  - **Download site:** the Channels section's category list gets the same
    sort chips. The hub's category rows are unchanged from 1.0.8-in-source.

## The side player

- **Watch while you browse.** On Android, **⤢ Side player** (or the player's
  Back key) tucks the channel into a corner card and brings the channel
  browser back up — the stream keeps playing, it never restarts. Clicking the
  corner picture (or its **⤢ Big screen** chip) grows it back to the big
  screen; its **✕ Close** chip is what stops playback.
- On macOS, **⧉ Side player** does the same: the same player element becomes a
  small corner card (Esc on the big screen tucks it, Esc in the corner stops),
  and clicking the picture grows it back.

## Live Events, revamped

- **Its own refresh button.** The Live Events tab has **⟳ Refresh live
  games**: it pulls the newest playlist (ended games drop out, new games
  appear) and then re-asks every game's feeds.
- **Live or not, per game.** Opening the tab — and every refresh — checks each
  game's feeds (six at a time) until one answers. The card's pill says
  **LIVE** (red) while a feed answers, **CHECKING** while the check runs, and
  **NO SIGNAL** (grey) when every feed timed out; the subtitle counts how many
  checked games are live. Any HTTP answer counts as answering, so geo-blocked
  edges are not called dead; only silence is.
- **Team badges.** A two-team matchup now shows each team with its own drawn
  crest — the team's initials in its own two colours, derived from the name so
  the same team always wears the same badge, with no network request and
  nothing to load in. Fight cards and other non-head-to-head titles keep the
  full event name.

## Unchanged on purpose

- No playlist, scraper, guide, or refresh-pipeline behaviour changes; the
  bundled data is still the USA lineup + USA guide.
- The 1.0.7 → 1.0.6.1 compatibility-alias mapping is historical and stays.
- Update policy is untouched: only a published full stable release above the
  installed version, with its platform installers attached, is ever offered.

## Verification

- `python3 scripts/release_version.py --code 1.0.8` prints `100080000`.
- Python suites: `tests/test_site_data.py` (category-list + sorting markers),
  `tests/test_app_updates.py`, `tests/test_macos_app.py`, and the Android
  bundle/refresh checks all pass.
- macOS app: `npm test` — 109 checks including the new team-badge, sorting,
  side-player and live-probe coverage.
- Android app: JVM tests for the sort cycles, team crests and matchup parsing
  (`SortingTest`, `TeamCrestTest`, extended `LiveEventsTest`), plus the CI
  emulator smoke test on the built APK.
