# Source reliability follow-up — 2026-11-12

## Scope and limitations

This is a continuation on a fresh branch from main. The earlier session's
unmerged branch was not available here, so its work has been reconstructed in
this checkout rather than assumed to exist. The repository contains automated
scraping, deduplication, link checks, EPG generation and publication under
`scripts/` and `.github/workflows/`; Android, macOS and the independent web app
consume generated playlist/guide data. Sources are configured in `sources.json`;
local curated files are preferred, with remote and GitHub API fallback paths.

The last **checked-in** report (`playlists/HEALTH.txt`, 2026-11-12 08:26 UTC)
recorded 11,809 reachable, 2,484 failed and 2,665 unverified unique links. A
reachability probe is neither a playback nor quality guarantee. The checked-in
live-event audit reported 0/26 *grouped entries* meeting its policy of three
confirmed feeds across two origin families. Those 26 are not necessarily unique
real-world games: differing sport labels can split the same matchup. The earlier
audit inferred reachability from absence in the failure lists. This has now
been replaced with exact-URL SHA-256 evidence from completed scrapes; the old
snapshot predates that evidence, so its unknown URLs are no longer counted as
confirmed. None of these figures is a fresh test.

The sandbox permits outbound requests only to selected package and GitHub hosts.
Provider pages below were discovered through search results, not exercised in a
real browser or player. Stream availability, embedding permission, ownership,
CORS, geographic restrictions, login, DRM, latency and segment playback were
not verified here. Do not add these page URLs to M3U playlists or treat them as
confirmed stream backups. The web app instead offers explicit links to the
providers. Provider policies and pricing can change.

## Official viewing paths added to the web app

| Provider / use | Evidence and qualification |
| --- | --- |
| [WNEP](https://www.wnep.com/watch) | Station's watch page advertises news and on-demand content. |
| [abc27 WHTM](https://www.abc27.com/viewing-options/) | Station says its newscasts stream free; this is not a promise of full ABC programming. |
| [Very Local / WGAL](https://www.verylocal.com/cities/susquehanna-valley/) | Promotes free WGAL news/weather in its app, not the full linear station. |
| [PBS Kids](https://www.pbs.org/video/pbs-kids-youre-watching-pbs-kids2/) | PBS describes live TV and viewing options; local station/availability varies. |
| [MeTV](https://www.metv.com/wheretowatch/) and [MeTV Toons](https://www.metvtoons.com/wheretowatch/) | Channel/provider finders, including antenna and paid services; not direct streams. |
| [A&E](https://support.aetv.com/hc/en-us/articles/4416565615383-Why-can-t-I-access-Live-TV-in-the-A-E-app) | Official guidance describes US-only live access with a participating TV provider. |
| [NASA ways to watch](https://www.nasa.gov/ways-to-watch/) and [live schedule](https://www.nasa.gov/live/) | NASA describes free NASA+ and schedules live coverage; not all times have live events. |
| [NFL+](https://support.nfl.com/hc/en-us/articles/39796576862996-Which-NFL-plan-is-right-for-me) | Paid plans; live local/primetime games are phone/tablet limited, RedZone is in Premium. |
| [NBA League Pass](https://www.nba.com/league-pass-purchase) | Paid, primarily out-of-market; local and national blackouts apply. |
| [MLB.TV](https://www.mlb.com/live-stream-games/subscribe) | Paid out-of-market package; blackout restrictions apply. |
| [NHL Blackhawks broadcast guide](https://www.nhl.com/blackhawks/team/broadcast) | Example league/team guide explains in- and out-of-market options, not universal game coverage. |

These are alternatives a viewer can investigate, not a solution for every
channel or fixture, nor replacements for actual independent in-player feeds.
They do not change Android/macOS UI or modify existing channel playlist streams.

## Fixes and remaining work

- Removed fixture-order-based kickoff guesses. All games remain in the schedule
  index with `kickoff_utc: null`; apps can still handle verified times if a
  future fixture-level source is integrated. Regenerated the published index.
- Updated the three curated-source raw URL and GitHub API fallback repository
  names from `PremiumTV1` to `PremiumTV`; local file paths are unchanged.
- Scrapes now record exact URL hashes for reachable recognized event feeds. The
  event audit counts only matching hashes from a completed scrape as reachable;
  legacy reports and other published URLs remain unconfirmed. Hashes omit raw
  URL credentials, but are not a substitute for protecting predictable URLs.
  This is still point-in-time evidence, not proof of current playback.
- For genuine playback redundancy: identify authorized stable media feeds;
  verify rights, exact content and origin diversity; probe manifest **and** media
  segments, browser CORS/mixed-content, headers, codecs, latency, regional
  access and multiple devices; then integrate only successful candidates and
  monitor for expiry. Provider landing pages alone are insufficient.
- Resolve identity mismatches between event sport/league labels before drawing
  real-world fixture conclusions from the grouping report. A reliable schedule
  integration needs fixture-level team/competition/date matching, timezone
  handling, provenance and expiry; never infer time from order.
- Run browser/UI and actual provider playback tests from an unrestricted device,
  including Android TV and macOS. Static browser smoke tests do not prove live
  source quality or permissions.
