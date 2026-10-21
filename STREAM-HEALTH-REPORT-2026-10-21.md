# PremiumTV stream health audit — 2026-10-21

Manual checked scrape requested via the `run-scrape.txt` switch and executed on
GitHub Actions (run `20261021T170203Z-3330`, verification re-run 17:24 UTC).
This sandbox cannot reach stream hosts directly (only GitHub/npm/PyPI egress),
so the checks ran where they have full network, exactly like the scheduled ones.

## Headline numbers (manual run, 17:05 UTC)

| Metric | Value |
|---|---|
| Unique links found | 16,703 (from 20,942 entries) |
| Confirmed working | **11,544 (69.1%)** |
| Dead (confirmed failure) | 2,629 |
| Unverified (timeout/403/transient) | 2,530 (+1,876 retained within grace) |
| Published player playlist | 13,402 channels — updated |
| Outcome | WARNING (normal for this pipeline) |
| Change vs baseline | +35 added / −14 removed |

## 🔴 Critical — fixed in PR #85: the repo rename broke the pipeline

The repository was renamed `PremiumTV1` → `PremiumTV` today between **15:20 and
16:46 UTC**. From then on, every scrape workflow run failed its offline test
gate (`test_epg_build.BuildTest.test_report_and_files`, `3 != 2`): the EPG
build identifies its own published guides by `$GITHUB_REPOSITORY`-derived URL
prefixes, so guide URLs under the old slug were no longer recognized as "ours"
and the build counted/re-ingested its own output. **Tonight's 16:41 ET
scheduled run would have failed too.** Fix (match every historical repo slug)
implemented in `scripts/epg_check.py` / `scripts/epg_build.py`, 496/496 tests
pass in a runner-identical env, and the push-triggered verification run
(17:19 UTC) went fully green end to end. **Merge PR #85 before the next slot.**

## 🔴 App-facing problems

1. **NFL RedZone has 0 working feeds in the app.** Its one verified priority
   feed (`[Sports] NFL RedZone (OVO)`) now serves "html page, not a stream";
   it was dropped from `PremiumTV.m3u` and `live/USA.m3u`. The last channel
   hunt found 26 candidates — all other 25 dead or auth-blocked. NFL Network
   is fine (5 verified feeds in the app feed).
2. **2 of 4 curated Susquehanna Valley locals dead** (both HTTP 404 on
   Sinclair `frequency.stream`): **CBS 21 (WHP) Harrisburg** and
   **NBC 6 (WJAC) Johnstown**. WGAL 8 (NBC Lancaster) and Fox 29 (WTXF) still
   play. These 404s are consistent across runs today — the Stirr/Frequency
   links for those stations appear to be gone, they need replacements.
3. **A&E US Eastern Feed (HD & SD, tvpass.org)** — DNS lookup failures,
   quarantined since 10-20. The dedicated A&E playlist still holds 67/72.
4. **Guide coverage in the app is thin: 20.6%** — only 449 of 2,179
   `tvg-id`s in `live/USA.m3u` have actual programme listings in the merged
   guide. The upstream US guides are 100% healthy and fresh (iptv-epg.org US
   stretches to 2026-11-19); the ids used by FAST/aggregator channels simply
   match nothing upstream.

## 🟡 Source quality

| Source | Working / Unique | Verdict |
|---|---:|---|
| xtemus (w3u) | **29 / 317 (9%)** | Effectively dead upstream — 233 confirmed dead. Candidate to disable or re-review. |
| doms9 | 218 / 584 (37%) | Degraded: 319 unverified, mostly HTTP 403 + timeouts (anti-bot). |
| iptv-org | 7,898 / 11,352 (70%) | Back-bone; steady. |
| free-tv | 1,120 / 1,999 (56%) | 537 dead — normal churn. |
| openstream 🌱 | 5,084 / 5,447 (93%) | Discovery-promoted; in great shape. |
| m3u 🌱 | 655 / 823 (80%) | Discovery-promoted; fine. |
| priority-channels | 18 / 19 | Only the NFL RedZone feed lost. |
| ae-networks | 50 / 53 | tvpass.org pair dead (see above). |
| aria / local | 221 / 311, 2 / 4 | aria typical churn; locals see above. |
| eja / StepDaddy / dlive | not configured | Optional feeds never configured — no impact. |

## 🟡 Top failure modes this run

1. **HTTP 403 — 1,287 links** (largest unverified bucket). Pirate event/sports
   hosts (`khala.futlivehd.com`, `envivosenhd.beer`, `fubo18.com`, `ftlly.com`,
   `freeott.top`) bot-block the checker; ~500 of them are US/sports links kept
   only by the grace retention. Expect these to flap.
2. **HTTP 404 — 1,020 links.** Genuinely gone; purged or quarantined.
3. **Timeouts — 901 links**, concentrated on whole dead hosts
   (`57.128.231.171:8080` ×101, `31.148.48.15` ×96, `hls127.freeott.top` ×96,
   `103.250.28.74:8000` ×60, `playlist.xtemus.com` ×30).
4. "html page, not a stream" — 366 links (feed replaced by a website).

## Trends worth watching

- Slow decline since the Oct-15 quarantine fix released ~1,999 links:
  working 11,717 (10-18) → **11,545 today**; dead 2,062 → 2,597. No cliff,
  but the drift is all in the –100/day range this week.
- **GitHub scheduler remains unreliable:** all seven daily slots started
  **4.5–9.6 h late** over the last 10 days (`schedule_delay_minutes` in
  run-history). The schedule guard catches them, so nothing is lost — but
  "7×/day" in practice means "7 times per day, at random hours".
- Deep link check (this morning): published playlists **85.4% working**
  (22,810/26,710 entries); 1,732 blocked (geo/auth), 2,100 unreachable.
  App feed: ~93% of 2,896 entries playable.
- Structure is clean: 0 playlist problems in VERIFY, 0 dead links published,
  backup/category shelves in sync.

## Recommendations

1. **Merge PR #85 immediately** — the scheduled pipeline is red until then.
2. Re-run `channel_hunt.py` for **NFL RedZone** before Sunday; consider
   temporarily widening retries/hosts for it.
3. Replace the two dead Sinclair locals (CBS 21 WHP, NBC 6 WJAC) in
   `playlists/sources/local-channels.m3u`, or drop the entries until a working
   public feed exists.
4. Decide on `xtemus`: 9% yield costs ~30 dead entries in every report;
   either disable it in `sources.json` or re-audit its group filters.
5. Follow-up rename sweep: `PremiumTV1` still hard-coded in
   `scraper.py` (countries README links, `SELF_EPG_URL` default),
   `legacy_sunset.py`, `build_categories.py`, `build_site_data.py`. All work
   via GitHub's redirect, but the headers now write the new slug, so the two
   names coexist — do the deliberate migration while PR #85's alias logic
   keeps both sides safe.
6. Optional feeds (`EJA_M3U_URL`, `STEPDADDYLIVEHD_PLAYLIST_URL`,
   `DLIVE_M3U_URL`) have never been configured — configure or remove them
   from the source table to quiet the report.
