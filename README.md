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
| [`playlists/countries/`](playlists/countries/README.md) | Confirmed working playlists separated by country (`USA.m3u`, `China.m3u`, `UK.m3u`, `Canada.m3u`, `India.m3u`, etc.). |
| [`playlists/AE_Channels.m3u`](playlists/AE_Channels.m3u) | Dedicated playlist of confirmed working A&E and A+E Networks channels (linear & FAST). |
| [`playlists/PremiumTV_all.m3u`](playlists/PremiumTV_all.m3u) | All unique links found, including dead or unverified links. |
| [`playlists/STATUS.md`](playlists/STATUS.md) | Latest run outcome, source counts, country counts, A&E status, additions/removals, and diagnostics. |
| [`playlists/logs/scrape-log.txt`](playlists/logs/scrape-log.txt) | Complete plain-text (`.txt`) run report with source stats, A&E channels, country counts, and log edits. |
| [`playlists/logs/log-edits.txt`](playlists/logs/log-edits.txt) | Chronological plain-text (`.txt`) log of playlist edits (`+added` / `-removed` channels) and issues across runs. |
| [`playlists/logs/errors.txt`](playlists/logs/errors.txt) | Plain-text (`.txt`) error breakdown, source/run issues, and dead/unverified links. |
| [`playlists/logs/run-history.txt`](playlists/logs/run-history.txt) | Plain-text (`.txt`) tabular summary of all recorded runs. |
| [`playlists/report.json`](playlists/report.json) | Detailed latest JSON report, including failed sources, country counts, A&E channels, and dead/unverified URLs. |
| [`playlists/checks/LINK-CHECK.md`](playlists/checks/LINK-CHECK.md) | Nightly deep check: which published links are working, offline, unreachable, blocked, and what was patched out. |
| [`playlists/checks/EPG-CHECK.md`](playlists/checks/EPG-CHECK.md) | TV guide check: every advertised guide URL with its status, channel/programme counts, and dead guides removed. |
| [`playlists/epg/PremiumTV.xml`](playlists/epg/PremiumTV.xml) | **One merged, filtered TV guide** for every channel in the published playlists — load this `.xml` link in your player. |
| [`playlists/epg/PremiumTV.xml.gz`](playlists/epg/PremiumTV.xml.gz) | The same guide gzipped (about 10x smaller, same content). |
| [`playlists/checks/EPG-BUILD.md`](playlists/checks/EPG-BUILD.md) | Guide build report: which upstream guides merged, how many channels matched, events kept/merged/dropped, and the file size. |
| [`playlists/checks/CHANNEL-HUNT.md`](playlists/checks/CHANNEL-HUNT.md) | Priority-channel hunt: every candidate found for Nickelodeon, NickToons, MeTV and MeTV Toons, and which ones actually played. |
| [`playlists/Priority_Channels.m3u`](playlists/Priority_Channels.m3u) | Ready-to-load playlist with only the verified priority channels (Nickelodeon, NickToons, MeTV, MeTV Toons) and the same guides as the main playlist. |
| [`playlists/run-history.jsonl`](playlists/run-history.jsonl) | Append-only, one-record-per-run history for regular checks, rechecks, final checks, and manual runs. |
| [`playlists/discovery/REPORT.md`](playlists/discovery/REPORT.md) | Latest monthly new-channel hunt: candidates, scores, verdicts, and promotions. |
| [`playlists/discovery/approved-sources.json`](playlists/discovery/approved-sources.json) | Sources vetted by monthly discovery and merged into the next regular scrape. |
| [`playlists/discovery/new-channels.m3u`](playlists/discovery/new-channels.m3u) | New working links found by the last monthly run, ready to try in a player. |
| `playlists/sources/*.m3u` | Normalized copies used as fallback caches when an upstream source is unavailable. |

### Country-separated playlists & A&E channels

Every checked run automatically classifies all confirmed working channels by country (`tvg-country`, `tvg-id` country suffix, and `group-title` / channel metadata) and writes a separate playlist per country in [`playlists/countries/`](playlists/countries/README.md), plus a dedicated A&E Networks playlist at [`playlists/AE_Channels.m3u`](playlists/AE_Channels.m3u):

```text
# USA channels only
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/countries/USA.m3u

# China channels only
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/countries/China.m3u

# UK channels only
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/countries/UK.m3u

# Canada channels only
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/countries/Canada.m3u

# A&E and A+E Networks channels only
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/AE_Channels.m3u
```

See [`playlists/countries/README.md`](playlists/countries/README.md) for the complete table of all ~170+ country playlists.

### Local channels (Lancaster / Harrisburg, PA)

[`playlists/sources/local-channels.m3u`](playlists/sources/local-channels.m3u) is a curated source for the
Susquehanna Valley market, so the local stations are published in `PremiumTV.m3u` and
`playlists/countries/USA.m3u` like any other channel and re-checked on every scrape:

| Channel | Market | Feed |
|---|---|---|
| WGAL 8 (NBC) | Lancaster, PA | public Tubi feed |
| CBS 21 (WHP) | Harrisburg, PA | public Stirr feed |
| Fox 29 (WTXF) | Philadelphia, PA | Fox's public FAST feed |
| NBC 6 (WJAC) | Johnstown, PA | public Stirr feed |

WHTM 27 (ABC) and WPMT 43 (Fox) are the market's other stations, but they publish no free 24/7 stream —
abc27 and fox43 stream newscasts only inside their own sites and apps — so they are not listed. Add a line
to the file and the next scrape publishes and checks it; a feed that stops answering is dropped
automatically.

Each report compares the newly discovered links with the previous all-links playlist and records added/removed counts. A failed source refresh or a link-check run below the minimum working ratio is recorded, but does not replace the last good `PremiumTV.m3u`.

## TV guide (EPG) — one merged `.xml` file

Every playlist header advertises 90+ upstream guides, and a player downloads all of them on each
refresh. Those guides each use their own channel-id namespace, so most of the channels in these
playlists match nothing, and the events that *do* load belong to channels nobody can play. That is
what makes a guide grid useless for filtering.

This repository therefore publishes **one** guide, built from exactly those upstream guides and
reduced to exactly the channels the playlists carry:

```text
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml
```

| Guide | Use it when |
|---|---|
| [`playlists/epg/PremiumTV.xml`](playlists/epg/PremiumTV.xml) | Your player wants a plain `.xml` URL (TiviMate, IPTV Smarters, Kodi PVR IPTV Simple, VLC). |
| [`playlists/epg/PremiumTV.xml.gz`](playlists/epg/PremiumTV.xml.gz) | You would rather download 8x less (7.0 MB instead of 58.8 MB); identical content, gzipped. |

**What the last build produced** (from
[`playlists/checks/EPG-BUILD.md`](playlists/checks/EPG-BUILD.md), rebuilt 2026-10-02 23:58 UTC in
99 s): **2,283** of the **7,997** channels the playlists publish (**28.5%**) have a guide, carrying
**92,916** events — 6 h back and ~30 h ahead, trimmed from 48 h to fit the size budget — in
**58.8 MB** of XML (**7.0 MB** gzipped). 82 of the 94 advertised upstream guides contributed; the
other 12 answered but had no channel in common with these playlists, and every one is listed with
its reason in the report. Of those events, 74,586 carry a genre, 31,605 an episode number, 17,490
credits, 19,085 a `premiere` flag and 12,599 `previously-shown` — the metadata the filters run on.

The remaining 71.5% are mostly channels no public guide covers at all (regional and FAST channels
listed by an index but never in a listings feed). The build report names every guide that
contributed nothing, so the gap is visible rather than silent.

[`scripts/epg_build.py`](scripts/epg_build.py) builds it. "Filtered" is literal:

* **Only published channels.** A guide channel survives only when its id matches a `tvg-id` in
  `PremiumTV.m3u`, `AE_Channels.m3u` or `Priority_Channels.m3u` (plus the country playlists with
  `--countries`) — after
  normalising the `@variant` suffix (`AE.us@East`, `AE.us@West` and a guide's `AE.us` are the same
  channel), or, when the ids disagree entirely, by unambiguous display name. Everything else is
  discarded, so a player is not indexing events for channels it cannot play.
* **Aliases share one listing.** Both A&E feeds get the same events, and each channel carries the
  playlist's own name first in its `<display-name>` list, which is what name-matching players
  compare against.
* **UTC everywhere.** Every `start`/`stop` is rewritten to `YYYYMMDDHHMMSS +0000`, so time filtering
  behaves the same no matter which source an event came from.
* **A bounded window.** By default the next 48 hours plus the last 6, which is what a guide grid
  actually shows; `--ahead`/`--keep-past` change it.
* **No junk events.** Placeholder titles ("No Information", "Sign Off", "-", …) are dropped, and
  HTML entities and markup are cleaned out of titles and descriptions.
* **One track per channel.** Identical events from different guides are merged (the longest
  description and the union of the categories win), and events that overlap a better-sourced event
  are dropped — "better" means better described first, then from the guide that matched more of our
  channels.
* **Filterable metadata kept.** `sub-title`, `desc`, `category`, `episode-num`, `credits`, `icon`,
  `rating`, `star-rating` and the `new` / `live` / `premiere` / `previously-shown` flags are copied
  through, so genre and "new episode" filters keep working.

### Keeping the guide in step with the scrapes

| Trigger | What it does |
|---|---|
| [`epg-build.yml`](.github/workflows/epg-build.yml) — 5:47 AM and 5:47 PM (New York) | Full rebuild from the guides the nightly check verified, then advertises the merged guide first in every playlist's `x-tvg-url`. |
| [`link-check.yml`](.github/workflows/link-check.yml) — 1:13 AM, after the guide check | `--force` rebuild, so the guide is cut from the same verified guide list and covers the channels that survived the deep link check. |
| [`scrape.yml`](.github/workflows/scrape.yml) — every scrape slot | Freshness-guarded (`--max-age-hours 12`): most slots skip in under a second, and the guide is rebuilt only when it has gone stale, so it always covers whatever the automatic scrapes just published. |

Run it by hand any time — from **Actions → Build the merged TV guide → Run workflow**, or:

```bash
python scripts/epg_build.py --patch --force     # rebuild and advertise it in the playlists
python scripts/epg_build.py --ahead 24          # a shorter window, a smaller file
gh api -X POST repos/<owner>/<repo>/dispatches -f event_type=epg-build-now   # trigger the workflow
```

A build that comes back hollow refuses to publish: fewer than `--min-channels` (25) or
`--min-programmes` (1000) matched channels, or fewer than `--min-previous-ratio` (25%) of the
channels in the guide it would replace, leaves the previously published guide untouched and fails
the step. A bad network hour cannot wipe the guide. If the merged file would exceed `--max-mb`
(60 MB), the window is trimmed first — proportionally to the overshoot, and only for as long as
trimming still removes events — then events per channel, and every trim is recorded in
[`playlists/checks/EPG-BUILD.md`](playlists/checks/EPG-BUILD.md). `--max-mb` is the size/window
dial: 45 MB buys about 19 hours of listings, 60 MB about 30, 90 MB the full 48.

Every playlist the scraper writes — the three main ones and the ~180 country files — advertises
this guide **first** in its `x-tvg-url`, ahead of the upstream guides, so a player loads the guide
whose ids actually match and only falls back to the others for whatever it misses. Appending a line
to [`playlists/logs/run-epg-build.txt`](playlists/logs/run-epg-build.txt) and pushing rebuilds it on
that branch without opening the Actions tab.

## Automatic checks and logs

The [GitHub Actions workflow](.github/workflows/scrape.yml) runs **seven times a day** in `America/New_York` — roughly every three hours, so a link that dies in the morning is out of the player playlist by the afternoon:

| Time | Cron | Run label |
|---|---|---|
| 3:07 AM | `7 3 * * *` | Regular daily scrape |
| 6:23 AM | `23 6 * * *` | Recheck |
| 9:41 AM | `41 9 * * *` | Recheck |
| 12:53 PM | `53 12 * * *` | Recheck |
| 4:41 PM | `41 16 * * *` | Final daily check |
| 8:17 PM | `17 20 * * *` | Recheck |
| 11:29 PM | `29 23 * * *` | Overnight recheck |

A separate [nightly workflow](.github/workflows/link-check.yml) runs the intensive deep check at 1:13 AM: it re-verifies every published link end to end, verifies every TV guide, and hunts for the priority channels. See [Deep link check, guide check and priority channels](#deep-link-check-guide-check-and-priority-channels).

A separate [guide workflow](.github/workflows/epg-build.yml) rebuilds the merged TV guide twice a day at 5:47 AM and 5:47 PM; see [TV guide (EPG) — one merged `.xml` file](#tv-guide-epg--one-merged-xml-file).

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
leaves the slot open. A successful *checked* run within 45 minutes of a slot also covers it whatever
its run type, so a manual re-scrape next to a slot is not immediately repeated by a catch-up.

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

## Deep link check, guide check and priority channels

The daily scrape is deliberately shallow: it reads the first few KB of a URL, which proves a server
answered but not that a player can play the stream. Three scripts cover the gap, and
[`.github/workflows/link-check.yml`](.github/workflows/link-check.yml) runs all three nightly at
**1:13 AM** (New York time). Each can also be run by hand from **Actions → Deep link and guide check
→ Run workflow**, or locally:

```bash
python scripts/link_check.py --all --patch     # re-verify every published link, drop dead ones
python scripts/epg_check.py  --all --patch     # verify every TV guide, drop dead ones
python scripts/channel_hunt.py --github-search # hunt Nickelodeon, NickToons, MeTV, MeTV Toons
```

### `scripts/link_check.py` — the intensive M3U check

For every published link it fetches the URL with the headers a player would send, resolves an HLS
master playlist to its best variant, downloads a real media segment and checks it is media (TS sync
byte, fMP4 box, or enough bytes), checks DASH manifests are populated, and classifies the rest by
payload. That distinguishes the two cases a shallow check cannot tell apart:

| Result | Meaning | Patched? |
|---|---|---|
| `working` | answered **and** produced playable media | keep |
| `offline` | confirmed dead: 404/410, DNS failure, refused, HTML page, empty body | **removed** |
| `unreachable` | timeout, 5xx, connection reset — may recover | keep |
| `blocked` | 401 / 403 / 451 — needs auth or is geo-blocked | keep |
| `unsupported` | non-HTTP scheme (rtmp, acestream, …) that cannot be probed | keep |
| `invalid` | malformed or non-HTTP URL | **removed** |

Removals are also written to `playlists/checks/quarantine.json`, and `scraper.py` reads that file on
every run: a link that only fails the deep check is held back for 7 days, so the next shallow scrape
cannot put it straight back into the player playlist.

Only the two confirmed-dead buckets are ever removed, and two safety nets stop a bad network day
from gutting a good playlist: `--min-working-ratio` (default 20%) aborts the patch when too few
links worked overall, and `--max-remove-ratio` (default 35%) skips any single playlist that would
lose more than that share of its entries. Every removal is logged to
`playlists/logs/link-check-edits.txt` and summarised in
[`playlists/checks/LINK-CHECK.md`](playlists/checks/LINK-CHECK.md).

### `scripts/epg_check.py` — TV guide verification

Players download every guide in the playlist's `x-tvg-url` header on each refresh, so one dead guide
slows all of them down. This script fetches each guide the way a player does — decompressing
`.xml.gz` on the fly and only reading the first slice of what are often 100 MB files — and confirms
it is real XMLTV with channels and programmes in it. Guides that answer with an HTML error page,
JSON, or an empty body are `invalid`; guides that 404 are `offline`; both are dropped by `--patch`,
while `unreachable` and `blocked` guides are kept because they may recover. Results, channel counts
and the newest programme date are in
[`playlists/checks/EPG-CHECK.md`](playlists/checks/EPG-CHECK.md).

### `scripts/epg_build.py` — the merged guide

Verification tells you which guides are alive; it does not make them usable. This script downloads
the guides that survived the check, streams them (they are often 100 MB+ gzipped, so nothing is ever
held in memory whole), and folds the channels that match the published playlists into the single
`playlists/epg/PremiumTV.xml` described in
[TV guide (EPG) — one merged `.xml` file](#tv-guide-epg--one-merged-xml-file). What each upstream
guide contributed — channels seen, channels matched by id and by name, events kept and dropped,
bytes read, and the reason a guide contributed nothing — is in
[`playlists/checks/EPG-BUILD.md`](playlists/checks/EPG-BUILD.md).

### `scripts/channel_hunt.py` — priority channels

Coverage scrapes are good for volume and bad for a specific channel: if the index entry rots, the
channel silently disappears. This script inverts the process for the channels configured in
`sources.json` → `priority_channels` (Nickelodeon, NickToons, MeTV, MeTV Toons):

1. **Collect** every candidate whose name or `tvg-id` matches a target — from the local corpus, from
   the configured upstream indexes, and (with `--github-search`) from public M3U files found by
   GitHub code search. A target whose name is a prefix of another target is excluded from it, so
   *MeTV* never collects *MeTV Toons* links.
2. **Verify** each candidate end to end with the deep checker.
3. **Publish** the survivors to `playlists/sources/priority-channels.m3u`, which `sources.json`
   enables as a normal source — so every scheduled scrape re-checks them, and a channel can only
   stay listed while it keeps playing.

Nothing is guessed: a link is only written after a media segment downloaded successfully. The hunt
reports every candidate it tested and the reason each one failed in
[`playlists/checks/CHANNEL-HUNT.md`](playlists/checks/CHANNEL-HUNT.md), so a channel with no working
public link is visible rather than silently missing.

Ranking favours the links worth keeping: the configured **`country`** first (`"us"` for all four
targets today, taken from the `tvg-id`/`tvg-name`), then an exact name match, then links **without**
a token or expiry in the URL. A signed link that plays today and 404s tomorrow is dropped entirely
whenever a stable link for the same channel plays (set `"allow_temporary": true` on a target to keep
them as a last resort). `blocklist` in the same config holds URL fragments that must never be collected, which is
how a feed several indexes list as "MeTV Toons" but which actually carries a different network stays
out. GitHub code search is best effort: it is rate limited (429) when the hunt runs more than about
once an hour, and every failure is recorded in the report's `notes` instead of being hidden.

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
| [`local-channels`](playlists/sources/local-channels.m3u) | M3U | Curated local channels for the Lancaster / Harrisburg / Lebanon / York market (`WGAL 8`, `CBS 21 (WHP)`, `Fox 29 (WTXF)`, `NBC 6 (WJAC)`); enabled and re-checked on every scrape. |
| [`ae-networks`](playlists/sources/ae-networks.m3u) | M3U | Curated A&E and A+E Networks linear & FAST M3U8 streams (`A&E`, `A&E Crime 360`, `The First 48`, `Storage Wars`, `Cold Case Files`, `60 Days In`, `Hoarders`, `Intervention`, `Dog the Bounty Hunter`, `Duck Dynasty`, `Home.Made.Nation`, `Crime + Investigation`, etc.); enabled. |
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
python scripts/epg_check.py --all                  # verify every advertised TV guide
python scripts/epg_build.py --dry-run              # build the merged guide without publishing it
python scripts/epg_build.py --patch --force        # rebuild it and advertise it in the playlists
python scripts/schedule_guard.py report            # schedule coverage table, no side effects
python scripts/schedule_guard.py --dry-run check   # what the 20-minute guard would do right now
python -m unittest discover -s tests -v            # offline integration tests
```

Inspect `playlists/STATUS.md` and `playlists/report.json` after a run. `--no-check` leaves `PremiumTV.m3u` untouched, and the workflow has a second restore safeguard before committing.

## Disclaimer

This repository does not host video. It only collects and checks links published elsewhere. Verify that a stream is authorized for you to access and redistribute in your location before using it.
