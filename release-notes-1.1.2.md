# PremiumTV 1.1.2 — channel opens in the side player, Movies & Shows test shelf (stable)

Published 2026-10-23. Android `1.1.2` / `versionCode 101020000`, macOS `1.1.2`.

It installs straight over 1.1.1, 1.1.0 and every earlier build — no uninstall
needed — and Settings → App updates offers it to every build below it.

## The side player comes first

- **Clicking a channel docks it on the right.** The channel list, the category
  rail and the Guide stay usable beside the picture, so picking the next
  channel does not mean leaving what is already playing.
- **One click on the picture goes full screen.** The same running stream grows
  to the full window — the player is never rebuilt, so playback does not
  restart or flash black. The **⤢ Big screen** button does the same thing.
- **Back tucks it away; ✕ closes it.** From full screen, Back returns the
  channel to the dock instead of stopping it. Closing the panel stops playback
  and returns to the tab you left.
- **Works from every list.** Channels, Guide listings, Live Events cards and
  the new on-demand shelf all open the same way.

## Movies & Shows is a working shelf

- **The coming-soon page is gone.** The tab is now a poster grid of films and
  classic TV episodes with **All / Movies / TV Shows** filters, a runtime and
  genre line, and a short plot summary.
- **Public domain only.** The test catalogue is 10 Internet Archive items —
  five films (*Night of the Living Dead*, *Plan 9 from Outer Space*,
  *Nosferatu*, *His Girl Friday*, *Carnival of Souls*) and five TV episodes
  (*The Beverly Hillbillies*, *Dragnet*, *The Lone Ranger*, *Sherlock Holmes*).
  Every item resolves to a direct HTTPS MP4 with a poster and the licence from
  the source's own metadata.
- **Same player, same panel.** An on-demand item is one finite stream, so it
  opens in the side player exactly like a channel and expands the same way.
- **Verified, not assumed.** `scripts/vod_catalog.py` resolves each item,
  probes the stream the way a player opens it, and writes
  [`playlists/vod/FEASIBILITY.md`](playlists/vod/FEASIBILITY.md) plus
  `vod-health.json`. On this release all 10 entries answered with playable
  media, seekable byte ranges and a poster.
- **Separate by design.** The catalogue never enters the M3U, the country
  playlists or the XMLTV guide, so a film cannot appear as a channel and the
  live lineup is unchanged.

## Under the hood

- The on-demand catalogue ships in the app bundle as `bundle/vod-catalog.json`
  on Android and `meta.vod_catalog` on macOS, next to the team crests and the
  live schedule.
- The macOS renderer's Content-Security-Policy now allows poster images from
  `archive.org`; no other policy changed.
- Version plumbing: `1.1.2` / Android `101020000` / macOS `1.1.2`, release tag
  `v1.1.2`. `app-update-notice.json` covers every build below 1.1.1, and the
  download site no longer retires a tag that is a published stable release.
- **One source for the version.** [`VERSION`](VERSION) is now the only
  hand-edited version; `scripts/version_sync.py` derives
  `android/version.properties` and the Mac package versions, and fails CI when
  the README, update notice, Gradle wiring, site generator or release notes
  disagree. The build workflows default to `release_version.py --current`
  instead of embedding a number.
- Validation on this commit: the repository Python suite (including the new
  1.1.2 and on-demand tests), the macOS renderer/parser/health suites and a
  fresh bundle build. The Android compile and emulator smoke gate run in
  `.github/workflows/android-build.yml` before an APK is published.

See [`CHANGELOG.md`](CHANGELOG.md) for the full history and
[`docs/UPDATES.md`](docs/UPDATES.md) for how the in-app updater delivers it.
