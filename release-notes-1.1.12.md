# PremiumTV 1.1.12 — Resilient playback

Android `1.1.12` / versionCode `101120000` · macOS `1.1.12` · web `0.2.0`.

- Android retries a dropped feed in place before spending its backup server.
- Android no longer leaves a one-feed channel spinning forever when it stalls.
- Android records a crash's class, message and stack for the next bug report.
- macOS now sends the `http-origin` a playlist publishes, and normalises it.
- Web: an optional, opt-in relay plays feeds a browser cannot reach directly.

## What each fix addresses

**Android choppiness and crashes.** A failed feed used to jump straight to the
next server. On a single-feed channel that meant the error card for a fault the
player could have survived. Network faults now get up to two reconnects and a
decoder fault gets one rebuild, while a permanent fault (bad HTTP status,
unsupported format, DRM) still walks on immediately. The buffering watchdog
reconnects once before moving on, and a channel with no backup finally says so
instead of showing a spinner indefinitely. `PlayerScreen` now keeps one stable
start-feed lambda, so a retry cannot re-run against stale captured state.
A last-chance handler stores the last crash in `last-crash.txt` and rethrows, so
the OS still receives a real crash but a report has something to go on.

**macOS streams that worked on Android.** Two concrete differences, now gone.
The Mac parser dropped `http-origin` — the bundle builder and the Android parser
both read it — so the same feed was requested with different headers. And an
`Origin` header is a scheme+host+port tuple, but playlists publish the embed
*page*; forwarding the page URL is a request a CDN refuses. Both apps now send
the normalised tuple.

**Web streams that would not play.** A browser cannot send a `Referer`, cannot
read a response without CORS, and cannot load `http://` media from an HTTPS
page: 771 of the 2,978 USA feeds are plain HTTP and 135 publish a required
header. `relay/` is a self-hostable Node service (no dependencies) that carries
exactly those cases for streams **in this repository's own playlist**. It ships
disabled, so GitHub Pages is unchanged; with one field set, the player uses it
only when this browser has a concrete reason to need it, and says so on screen.
An end-to-end test proves a referrer-gated feed becomes playable and that
private address ranges and unpublished URLs are still refused.

**Repository sweep.** The scheduled scrape and quick-update workflows had failed
three times each: they commit `playlists/` without regenerating
`playlists/local-channels.json`, so the offline suite failed the *next* run.
Both workflows now regenerate it before committing. The published site data was
advertising 11,941 channels against 12,353 in the playlist and has been rebuilt.
Two README sections still called 1.0.9 and 1.1.6 the current stable release.
