# PremiumTV1 change log

> **Detailed editable history:** [PremiumTV1 — Detailed Change Log (Google Doc)](https://docs.google.com/document/d/1anjXfhv6qXz9ZsSldHBMqsfDt8d44W8N_ayqYAloeNM/edit?usp=drivesdk). It backfills the available Git/PR history and all 79 records in the committed run-history snapshot, and documents stream-check policy, current metrics, and known limitations.

This GitHub file is the short index. The detailed Doc and the append-only [`playlists/run-history.jsonl`](playlists/run-history.jsonl) retain the run-by-run record; the per-run live reports remain under [`playlists/checks/`](playlists/checks/).

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
