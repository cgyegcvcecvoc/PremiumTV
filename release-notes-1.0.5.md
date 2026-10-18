# PremiumTV 1.0.5 — Splash, Search, Live Games and Multi-Server Playback

PremiumTV 1.0.5 is the stable Android TV and macOS release. If you are on
1.0.4, you do not download this one by hand: **Settings → App updates** offers
it, downloads the installer once, verifies its SHA-256 and hands it to the
normal installer. Fresh installs use the APK / DMG / PKG attached here.

## A real launch screen

Both apps now open on the PremiumTV mark: the drawn television set, the
wordmark, a spinning gold loader while the library is read, and the build's
version pinned at the bottom of the screen — so a slow start says which build
is starting instead of showing a bare spinner.

## Search

- **Android TV:** a search field sits above the Channels tab. Type (or
  D-pad into it and use the on-screen keyboard) to filter every category by
  channel name, category, country or channel number; one press clears it.
- **macOS:** the sidebar search continues to cover Channels and the Guide,
  and now also searches the new Live Events tab.

## No more blank logos

A channel without a logo no longer shows two initials in an empty box. Every
logo-less channel gets a drawn picture of its category — a ball for Sports, a
smile for Comedy, a balloon for Kids, a music note, a film strip, a newspaper
for News, a cloud-and-sun for Weather and more — and a television set, the
app's own mark, for everything else. The same picture shows while a remote
logo is still loading and when a logo URL turns out to be dead.

## Live Events: what games are on, by sport

The new **Live Events** tab collects the live-game feeds the repository's
scrapers have on air right now and groups them by sport — Soccer, American
Football, College Football, NHL Hockey, Basketball, MLB, UFC/MMA, Boxing and
every other sport the scrapers tag. Each card shows the matchup, a LIVE pill
and how many streams carry the game. The games also appear in the Guide's
"what's on now" list with the matchup as their listing, and their cards in
the Channels tab say `LIVE · <sport>` instead of "no listing".

## Multi-server playback

When a game is published on more than one stream — or a channel has backup
feeds in the playlist — the player now treats them as servers:

- If a feed stops responding or refuses the connection, the next server takes
  over by itself. The player says which server is playing ("Server 2 of 3")
  and only shows the error card after every server has been tried.
- This works on Android (ExoPlayer) and macOS (hls.js/mpegts.js behind the
  loopback proxy) with no setting to turn on.

## Everyday polish

- The guide's dead ends are honest: channels no public schedule covers say
  "No listing published" instead of looking broken, and live-game feeds never
  say "nothing listed" while they are plainly playing a game.
- Android's loading screen keeps its rotating tips; the Mac activity panel is
  unchanged and still non-modal.

## What is in the box

- USA stable lineup and USA guide, baked into the app at build time, with the
  same automatic background refresh and Settings → App updates center as
  1.0.4.
- Android `versionCode 100000005`, signed with the long-lived update key, so
  it installs straight over 1.0.4 (and over the 1.1.1 preview, if you move
  back to stable).

The 1.1.1 Encore Preview is rebuilt from the same tree and carries every
feature above on top of its cable-style Guide.
