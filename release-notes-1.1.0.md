# PremiumTV 1.1.0 — Stable: the side player, done right

**This is the stable release.** It ships as the default download for Android TV /
Fire TV and macOS. It installs over every earlier stable build (1.0.9 and below)
and over the retired 1.1.x preview channel.

## The side player now works like a cable box

- **The player is docked on the right.** Opening a channel and pressing Back
  tucks the picture into a fixed panel on the right of the window. The category
  rail and channel list fill the rest of the screen, so you can keep watching
  while you browse — the IPTV Smarters Pro arrangement, not a card floating over
  the bottom corner.
- **One press goes full screen.** Press OK on the small picture (or the
  **⤢ Big screen** button) and the same stream grows to the whole screen; press
  Back to tuck it away again. The stream never restarts during the flip: the
  screen keeps one ExoPlayer for its whole life, and the big-screen and
  side-player layouts share the same video surface.
- **The picture shows where the remote is.** The docked panel carries the
  channel name, what is on now, which server is carrying it, and how many
  automatic backups have happened this session.

## Categories, side by side

- The Channels tab is now a **category rail on the left and the selected
  category's channels beside it**, instead of a full-page list you had to leave
  and re-enter. *All channels*, *Recently watched*, *Favorites* and every
  published category sit in the rail with their counts.
- Each pane has its own sort control; search is library-wide and works from any
  category.
- Categories with nothing left to show drop out of the rail automatically.

## Automatic server backup

- When a feed fails, stalls for 25 seconds, or is already known to be dead, the
  player moves to the **next server by itself** and says so on screen. The walk
  never wraps around on its own, so it cannot loop forever on a dead first feed.
- **Feeds already seen failing are tried last**, so an open channel leads with a
  server that was working.
- Manual **◀ Server / Server ▶** hopping still wraps, for a live event that
  needs a nudge.
- If every feed fails, the player says so honestly and the channel is hidden
  until the next refresh instead of being offered again.

## Dead channels are filtered out

- The app remembers a feed the player watched fail (seven days) and removes a
  channel from the browser once **every** feed for it has failed. A channel with
  a live backup feed stays, reached through that backup.
- *Settings → Restore hidden channels* forgets the recordings and puts every
  published channel back, in case a link came back.
- The repository's nightly link check still removes dead links from the
  published playlists; this is the app's own safety net between checks.

## Focus you cannot lose

- Every focusable thing — channel cards, category rows, tabs, buttons, guide
  cells, the side player's picture — now draws the **same amber outline**, 3 dp
  wide with a soft glow. It is deliberately hotter than the brand gold, so
  "where is the remote" never gets confused with a decorative accent.

## A calm loading screen

- The animated splash is gone: no breathing logo, orbiting spinner, shimmer
  sweep or pulsing dots. What is left is the mark, the tagline, the version — and
  **the gold loading line bar**, which now reports the loader's real stages
  (channels, then guide) instead of looping for decoration.
- The same change is in the macOS app.

## Crash hardening

- One ExoPlayer per player screen, with a single video call site for both
  layouts, so a side-player flip or server hop can never leave the view bound to
  a released player.
- Every server index is clamped; the automatic walk stops at the last server
  instead of overshooting; the buffering watchdog only advances when a backup
  exists and otherwise says the truth.
- Dead-feed storage recovers quietly from corrupt or full storage and can never
  break playback.
- The library is filtered and re-grouped only when the dead-feed set changes, so
  a long session cannot build up repeated full-list copies.

## Everything from 1.0.9

The crash-on-watch fix, M3U names containing commas, strict XMLTV validation,
repaired programme durations, exact id+URL backup-stream selection on Mac,
correct proxy-session release, the revamped Live Events tab with live checks,
and channel-health evidence reconciled so a newer successful probe supersedes
an older quarantine entry.

## Upgrading

| You are on | What to do |
|---|---|
| 1.0.9 or earlier stable | It installs straight over the top — Settings → App updates finds 1.1.0 automatically, or fetch the installer from the release. |
| Old 1.1.0 / 1.1.1 preview | That channel is retired and its name equals this release, so the in-app updater will not offer 1.1.0. Install it by hand once: Android accepts it over the preview (`versionCode 101000000` > `100010001`), and the Mac DMG replaces the preview copy. |

## Validation

- The Android build must pass Gradle unit tests **and** an emulator cold-launch
  smoke gate that opens a channel, exercises the server hop, tucks the player
  into the side panel, grows it back, and closes it — with screenshots saved for
  review. If that gate fails, this release is held back rather than published.
- The macOS app's renderer, storage and updater test suites run on every build.
- The repository's Python suite (playlists, guide, site data, release policy)
  runs on the same commit.

## Downloads

- Android: `PremiumTV-1.1.0-debug.apk` — `versionCode 101000000`, signed with the
  pinned PremiumTV update key so it installs over every earlier build.
- Mac Apple Silicon: `PremiumTV-1.1.0-mac-arm64.dmg` / `.pkg`.
- Mac Intel: `PremiumTV-1.1.0-mac-x64.dmg` / `.pkg`.
- Checksums: `SHA256SUMS-android.txt` and `SHA256SUMS-macos.txt`.

## Known limitations

- Some upstream streams are geo-restricted or simply offline; the dead-channel
  memory hides one only after the player has watched every feed for it fail.
- The macOS app's dead-feed memory is stored per machine, like its shelves.
- A channel whose only feed dies while the app is closed is still listed until
  the repository's next published playlist refresh removes it.
