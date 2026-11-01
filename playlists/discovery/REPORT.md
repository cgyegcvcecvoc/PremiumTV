# Monthly new-channel discovery

- **Run:** _monthly new-channel discovery_ (`monthly_discovery`; ID `discover-20261101T162015Z-2922`)
- **Last run:** 2026-11-01 11:21 AM EST (2026-11-01 16:21 UTC)
- **Outcome:** **SUCCESS**
- **Known channels in the published playlist:** 17037 from `PremiumTV_all.m3u`
- **Candidates:** 7 (evaluated 5, promoted 2, watch 2, rejected 2, skipped 2)
- **New working links found:** 45 (from active sources: 143)
- **Sources promoted for the next scrape:** ['VIP-m3u-playlist', 'israel-tv-plus']

## Candidate results

| Candidate | Found via | Channels | New links | Sample working | Score | Verdict |
|---|---|---:|---:|---:|---:|---|
| Fanmingming-Live | seed | 188 | 188 | 0/0 (0%) | 28.4 | **reject** |
| ↳ last checked 2026-10-01T15:38:44Z | | | | | | |
| Akiraleal-IPTV | seed | 42 | 23 | 12/12 (100%) | 67.9 | **watch** |
| TianmuTNT-IPTV | seed | 574 | 554 | 10/12 (83%) | 72.1 | **promote** |
| Public_Iptv_Channels | github_search | 35 | 35 | 0/0 (0%) | 49.0 | **watch** |
| ↳ last checked 2026-10-01T15:38:44Z | | | | | | |
| VIP-m3u-playlist | github_search | 212 | 111 | 11/12 (92%) | 74.3 | **promote** |
| israel-tv-plus | github_search | 276 | 204 | 10/12 (83%) | 84.1 | **promote** |
| mrgify-clean | github_search | 327 | 265 | 2/12 (17%) | 48.4 | **reject** |
| ↳ 2 working in sample (needs 3) | | | | | | |

## New channels from the active sources

| Source | Channels | New links | Sample working | Note |
|---|---:|---:|---:|---|
| local-channels | 4 | 0 | 0/0 (0%) | ok |
| priority-channels | 18 | 0 | 0/0 (0%) | ok |
| ae-networks | 53 | 0 | 0/0 (0%) | ok |
| aria | 287 | 0 | 0/0 (0%) | ok |
| doms9 | 888 | 143 | 5/8 (62%) | ok |
| xtemus | 0 | 0 | 0/0 (0%) | ok |
| iptv-org | 11388 | 0 | 0/0 (0%) | ok |
| free-tv | 2029 | 0 | 0/0 (0%) | ok |
| eja-tv-feed | 0 | 0 | 0/0 (0%) | no URL or url_env secret set |
| stepdaddylivehd-instance | 0 | 0 | 0/0 (0%) | no URL or url_env secret set |
| dlive-sx-feed | 0 | 0 | 0/0 (0%) | no URL or url_env secret set |

## Promoted source health

| Source | Status | Channels | Working sample | Note |
|---|---|---:|---:|---|
| m3u | ok | 834 | 67% |  |
| openstream | ok | 5428 | 100% |  |

## New working channels (sample)

45 new working links are in [`new-channels.m3u`](new-channels.m3u). First 20 by source:

- **Sky Racing 2** (体育) — Akiraleal-IPTV
- **World of Freesports** (体育) — Akiraleal-IPTV
- **FloRacing** (体育) — Akiraleal-IPTV
- **SportsGrid** (体育) — Akiraleal-IPTV
- **ACCDN** (体育) — Akiraleal-IPTV
- **Pac-12 Insider** (体育) — Akiraleal-IPTV
- **beIN Sports Xtra** (体育) — Akiraleal-IPTV
- **FashionTV Paris L'Original** (娱乐时尚) — Akiraleal-IPTV
- **Totalmusic Concerts** (娱乐时尚) — Akiraleal-IPTV
- **Graham Norton** (娱乐时尚) — Akiraleal-IPTV
- **Mystery TV** (娱乐时尚) — Akiraleal-IPTV
- **Estrella TV** (娱乐时尚) — Akiraleal-IPTV
- **1987年春晚** (Other) — TianmuTNT-IPTV
- **1993年春晚** (Other) — TianmuTNT-IPTV
- **2024年春晚** (Other) — TianmuTNT-IPTV
- **2026-11-01 18:25:26** (Other) — TianmuTNT-IPTV
- **AMC音乐** (Other) — TianmuTNT-IPTV
- **CCTV12** (Other) — TianmuTNT-IPTV
- **CCTV13** (Other) — TianmuTNT-IPTV
- **CCTV15** (Other) — TianmuTNT-IPTV

## Issues and diagnostics

None.

Promotion is not automatic publication: promoted sources are added to the next regular scrape, and every link is link-checked there before it can appear in `PremiumTV.m3u`. Roll back by removing or disabling an entry in `approved-sources.json`.
