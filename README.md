# PremiumTV1

A playlist builder for publicly listed TV streams. The scraper combines enabled sources, removes duplicate URLs, checks HTTP streams, and publishes the checked player playlist when the run passes its safety threshold.

## Load the playlist

Load this URL in an M3U-compatible player (VLC, TiviMate, IPTV Smarters, Kodi PVR IPTV Simple, etc.):

```text
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/PremiumTV.m3u
```

| File | Purpose |
|---|---|
| [`playlists/PremiumTV.m3u`](playlists/PremiumTV.m3u) | Confirmed working links from the latest successful checked run. |
| [`playlists/PremiumTV_all.m3u`](playlists/PremiumTV_all.m3u) | All unique links found, including dead or unverified links. |
| [`playlists/STATUS.md`](playlists/STATUS.md) | Latest run outcome, source counts, additions/removals, and diagnostics. |
| [`playlists/report.json`](playlists/report.json) | Detailed latest report, including failed sources and dead/unverified URLs. |
| [`playlists/run-history.jsonl`](playlists/run-history.jsonl) | Append-only, one-record-per-run history for regular checks, rechecks, final checks, and manual runs. |
| [`playlists/discovery/REPORT.md`](playlists/discovery/REPORT.md) | Latest monthly new-channel hunt: candidates, scores, verdicts, and promotions. |
| [`playlists/discovery/approved-sources.json`](playlists/discovery/approved-sources.json) | Sources vetted by monthly discovery and merged into the next regular scrape. |
| [`playlists/discovery/new-channels.m3u`](playlists/discovery/new-channels.m3u) | New working links found by the last monthly run, ready to try in a player. |
| `playlists/sources/*.m3u` | Normalized copies used as fallback caches when an upstream source is unavailable. |

Each report compares the newly discovered links with the previous all-links playlist and records added/removed counts. A failed source refresh or a link-check run below the minimum working ratio is recorded, but does not replace the last good `PremiumTV.m3u`.

## Automatic checks and logs

The [GitHub Actions workflow](.github/workflows/scrape.yml) runs three times a day in `America/New_York`:

| Time | Cron | Run label |
|---|---|---|
| 3:07 AM | `7 3 * * *` | Regular daily scrape |
| 6:23 AM | `23 6 * * *` | Recheck |
| 4:41 PM | `41 16 * * *` | Final daily check |

A separate [monthly workflow](.github/workflows/discover.yml) hunts for new channels on the 1st of each month at 4:37 AM; see [Monthly new-channel discovery](#monthly-new-channel-discovery).

### Schedule reliability and the catch-up guard

GitHub does not promise to start a `schedule:` cron on time. Measured on this repository from
`playlists/run-history.jsonl` and the Actions API, every scheduled run between 2026-09-27 and
2026-09-29 started hours after its intended New York time, and three of the nine slots never
produced a run at all:

| Intended (New York) | Intended UTC | Actually started (UTC) | Delay |
|---|---|---|---|
| 2026-09-27 3:00 AM | 09-27 07:00 | never ran | **skipped** |
| 2026-09-27 6:00 AM | 09-27 10:00 | never ran | **skipped** |
| 2026-09-27 4:15 PM | 09-27 20:15 | 09-27 23:03 | +2h 48m |
| 2026-09-28 3:00 AM | 09-28 07:00 | 09-28 15:04 | +8h 04m |
| 2026-09-28 6:00 AM | 09-28 10:00 | 09-28 18:02 | +8h 02m |
| 2026-09-28 4:15 PM | 09-28 20:15 | 09-29 00:22 | +4h 07m |
| 2026-09-29 3:00 AM | 09-29 07:00 | 09-29 13:51 | +6h 51m |
| 2026-09-29 6:00 AM | 09-29 10:00 | 09-29 16:27 | +6h 27m |

The cron expressions and their `timezone:` keys were correct — GitHub supports timezone-aware
schedules — so this was the scheduler queueing and dropping runs under load, not a
misconfiguration. Each run still reported `success`, which is why the lateness was invisible
except in the timestamps. Two things now address it:

1. **Off-peak minutes.** The crons moved from minute 0/15 to 7, 23 and 41. GitHub's scheduler is
   most congested at the top of the hour, which is where two of the three slots used to sit.
2. **A catch-up guard.** [`.github/workflows/schedule-guard.yml`](.github/workflows/schedule-guard.yml)
   starts every 20 minutes and runs [`scripts/schedule_guard.py`](scripts/schedule_guard.py). It
   reads the crons straight out of `scrape.yml`, works out when each slot was due, and compares that
   with `playlists/run-history.jsonl`. If a slot that has already come due is still uncovered, it
   fires the existing `scrape-now` repository dispatch labelled with the slot it is catching up on.

The guard never scrapes or commits anything itself, so there is still exactly one code path that
publishes playlists. It is idempotent: a slot stops being overdue the moment the scrape it triggered
records itself in `run-history.jsonl`, and it will not dispatch while a scrape is queued, running, or
finished within the last 25 minutes. Only runs with outcome `success` or `warning` count as covering
a slot — a failed run, or an unchecked `--no-check` merge that never publishes `PremiumTV.m3u`,
leaves the slot open.

The trade-off is that a slot GitHub delays by many hours may end up scraped twice: once by the
guard's catch-up and once when GitHub's own run finally arrives. That costs about 20 minutes of
runner time and simply refreshes the playlist again, which beats the alternative of a day with no
verified refresh at all.

Every scheduled run now records how late it started. `STATUS.md` shows it directly under the run
label, `report.json` and `run-history.jsonl` carry `scheduled_for_utc` and `schedule_delay_minutes`,
and a start more than 15 minutes late is listed as a run issue, so lateness can no longer hide behind
a green check mark.

An offline regression suite runs before the scrape. All scheduled runs fetch every configured playlist source, deduplicate channels, and check every unique HTTP stream URL. The workflow adds the human-readable status to the Actions run summary and commits `STATUS.md`, `report.json`, source caches, and `run-history.jsonl` even if a failed health check prevents playlist publication. A failed scraper run still ends the Actions job as failed after its diagnostics have been saved.

Statuses distinguish **dead** responses from **unverified** results. For example, 401/403 access restrictions, rate limits, server errors, timeouts, and non-HTTP schemes are not represented as confirmed-working links; their reasons and next-step guidance are in `STATUS.md` and `report.json`. Per-host request limits and retries help reduce avoidable rate limiting. HTTP checks are only a reachability signal: they cannot guarantee playback from every region or that a stream is authorized for every viewer.

To run immediately, open **Actions → Scrape playlists → Run workflow**. Leave **Skip link checking** off for a verified refresh. Scheduled workflows run from the default branch (`main`); a manual run on another branch only updates that branch. To see the current schedule coverage without starting anything, run **Actions → Schedule guard → Run workflow** (dry run by default) or `python scripts/schedule_guard.py report`.

## Monthly new-channel discovery

The daily schedule only refreshes the sources that are already configured, so new channels need their own hunt. The [monthly workflow](.github/workflows/discover.yml) runs [`scripts/discover.py`](scripts/discover.py) at **4:37 AM on the 1st of every month** (New York time) and can also be started manually from **Actions → Monthly discovery → Run workflow**.

Each monthly run:

1. Builds the corpus from the published `PremiumTV_all.m3u`, so "new" means "not in the playlist yet".
2. Collects candidates: the seeded repositories in `sources.json` plus public GitHub repositories found through repository search (`topic:iptv-m3u`, `#EXTM3U` in the README, and similar). For each repository the engine reads the file tree and picks the most likely static TV playlist, skipping series/movie/VOD/radio files.
3. Fetches and parses each candidate, then measures how many links it would actually **add**, how many are duplicates, and how many channel names are new.
4. Link-checks a host-balanced sample of those new links — 12 by default, spread across providers so one host cannot skew the result — and scores the candidate on working ratio, new-link volume, and freshness.
5. Reviews the already-configured sources the same way, so the report also shows new channels arriving from sources you already have.
6. Re-checks the health of previously promoted sources and flags any that have gone stale.

A candidate is promoted only when it clears every threshold in `sources.json` → `discovery.thresholds` (at least 25 new links, at least 3 of the sampled links working, a working ratio of at least 30%, and a score of at least 55). Promotions are capped at `max_promote_per_run` (2) per month and are written to `playlists/discovery/approved-sources.json`. The monthly workflow then runs a normal checked scrape so the new sources are integrated with every link verified, exactly like a regular run; otherwise the next daily scrape picks them up.

Promotion is not publication. A promoted source is still fetched, deduplicated, and link-checked by the regular scraper before anything can reach `PremiumTV.m3u`, promoted sources are marked 🌱 in `STATUS.md`, and the minimum-working-ratio safeguard still protects the last good playlist. To roll one back, set `"enabled": false` for it in `approved-sources.json` or delete the entry.

Candidates that were already measured and rejected are remembered in `playlists/discovery/state.json` and are not re-fetched until `recheck_after_days` (90) has passed, so a month of dead sources costs one fetch each. `--force` overrides this.

## Sources

Playlist sources are configured in [`sources.json`](sources.json). Active M3U/W3U feeds are fetched and their unique stream URLs are checked on every scheduled run.

| Source | Format | Integration |
|---|---|---|
| [aria](https://github.com/aria-tv/aria/blob/main/aria.m3u) | M3U | Direct raw playlist; enabled. |
| [doms9/iptv](https://github.com/doms9/iptv) | M3U8 | `M3U8/TV.m3u8`; enabled. |
| [xtemus](https://xtemus.com/) | W3U | Enabled; only the selected live-TV groups are followed. Movie, series, radio, and highlight folders are excluded. |
| [iptv-org/iptv](https://github.com/iptv-org/iptv) | M3U | Added global playlist `https://iptv-org.github.io/iptv/index.m3u`. |
| [Free-TV/IPTV](https://github.com/Free-TV/IPTV) | M3U8 | Added `playlist.m3u8`. |
| [eja.tv](https://eja.tv/) | Website audit | The site is probed for reachability, but it is not treated as a static playlist. No direct M3U export was verified. It is not counted as imported channels unless a direct playlist URL is configured. |
| [StepDaddyLiveHD](https://github.com/gookie-dev/StepDaddyLiveHD) | Repository audit / optional instance playlist | The repository tree is checked for a static M3U. Its documented playlist is generated by a self-hosted app, so the repository itself is not a channel feed. |
| [dlive.sx](https://dlive.sx/24-7-channels.php) | Channel-index audit / optional direct playlist | The DaddyLiveHD 24/7 index is fetched and its catalogue counted, but no channel is imported: see below. Set `DLIVE_M3U_URL` to an authorized direct playlist to import and link-check it. |

`aria` and `doms9` were already active sources; the scraper now also scans `iptv-org` and `Free-TV/IPTV`. The eja.tv, StepDaddyLiveHD and dlive.sx references are checked and reported separately rather than falsely counted as channel feeds. To ingest an authorized direct M3U URL for any of them, add repository Actions secrets named `EJA_M3U_URL`, `STEPDADDYLIVEHD_PLAYLIST_URL` or `DLIVE_M3U_URL`. The StepDaddy secret should point to a running instance's `/playlist.m3u8`; without it, the repository audit still runs and the instance source is shown as `not_configured`.

### Why dlive.sx is audited rather than imported

[`https://dlive.sx/24-7-channels.php`](https://dlive.sx/24-7-channels.php) lists well over a
thousand 24/7 channels, so it looks like a source that could be scraped straight into the playlist.
It cannot, for two reasons that were verified against the site itself:

- Each channel links to `watch.php?id=<n>`, and the playable address is an **HTML player page**
  (`/stream/stream-<id>.php`, also mirrored under `/cast/`, `/watch/`, `/plus/`, `/casting/` and
  `/player/`). The stream URL is resolved by JavaScript at run time, so the page is not something a
  player can open and not something the link checker can verify. Importing those links would add
  hundreds of entries reported as `html page, not a stream` and would drag the working ratio down.
- The documented `daddyapi.php` endpoints (`channels`, `schedule`, `info`) are **key protected** —
  the site asks you to contact the operator for a key — and the site publishes no static M3U.

So the scraper treats it as a `website_channel_index` reference check. Every run fetches the page,
counts the catalogue, keeps a sample of channel names, records any playlist-looking link it finds,
and reports an `ingest_status` of `player_pages_only`, `static_playlist_found_not_configured` or
`no_channels_found`. The counts appear in the reference table of `STATUS.md` and in `report.json`,
so the site's reachability and size are visible without pretending its links are playable. Nothing
from the index can reach a playlist: the tests assert that.

If you have an authorized direct playlist for the same channels — for example an M3U generated by a
self-hosted proxy such as StepDaddyLiveHD — set the `DLIVE_M3U_URL` Actions secret. The `dlive-sx-feed`
source then imports it like any other feed, and every link is checked before it can appear in
`PremiumTV.m3u`. Until it is set, that source is reported as `not_configured` instead of failing the
run. Be aware that playlists and caches are committed to this repository, so only configure a feed
whose stream URLs are safe to publish.

To add another feed, add a `sources` entry with `name`, `type` (`m3u` or `w3u`), and `url`. For an optional URL supplied by an environment variable, use `url_env` and `optional: true`; the workflow's optional secrets are wired in `.github/workflows/scrape.yml`. W3U sources also support `include_groups`, `exclude_groups`, and `max_depth`. Playlist files and caches are committed to this repository, so only configure feeds whose resulting stream URLs are safe to publish—an Actions secret protects the feed URL from logs, but does not make output links private. Review source quality and permissions before publishing.

## Run locally

Python 3.9+ is required; there are no third-party dependencies.

```bash
python scripts/scraper.py                         # fetch, merge, check, and write reports
python scripts/scraper.py --no-check              # merge without checks; keep the checked player file untouched
python scripts/scraper.py --help                   # workers, timeout, retries, and other options
python scripts/discover.py                        # monthly new-channel hunt
python scripts/discover.py --no-search --max-candidates 3   # quick, seeded-only trial run
python scripts/discover.py --dry-run              # report only; never promote a source
python scripts/schedule_guard.py report            # schedule coverage table, no side effects
python scripts/schedule_guard.py --dry-run check   # what the 20-minute guard would do right now
python -m unittest discover -s tests -v            # offline integration tests
```

Inspect `playlists/STATUS.md` and `playlists/report.json` after a run. `--no-check` leaves `PremiumTV.m3u` untouched, and the workflow has a second restore safeguard before committing.

## Disclaimer

This repository does not host video. It only collects and checks links published elsewhere. Verify that a stream is authorized for you to access and redistribute in your location before using it.
