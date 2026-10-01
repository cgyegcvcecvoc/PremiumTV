# Monthly new-channel discovery

- **Run:** _monthly new-channel discovery_ (`monthly_discovery`; ID `discover-20261001T153844Z-2391`)
- **Last run:** 2026-10-01 11:41 AM EDT (2026-10-01 15:41 UTC)
- **Outcome:** **WARNING**
- **Known channels in the published playlist:** 13515 from `PremiumTV_all.m3u`
- **Candidates:** 10 (evaluated 9, promoted 2, watch 2, rejected 4, skipped 0)
- **New working links found:** 59 (from active sources: 69)
- **Sources promoted for the next scrape:** ['m3u', 'openstream']

## Candidate results

| Candidate | Found via | Channels | New links | Sample working | Score | Verdict |
|---|---|---:|---:|---:|---:|---|
| Fanmingming-Live | seed | 188 | 188 | 0/12 (0%) | 28.4 | **reject** |
| ↳ 0 working in sample (needs 3) | | | | | | |
| Akiraleal-IPTV | seed | 34 | 24 | 11/12 (92%) | 61.1 | **watch** |
| TianmuTNT-IPTV | seed | 715 | 707 | 8/12 (67%) | 62.9 | **promote** |
| Public_Iptv_Channels | github_search | 35 | 35 | 6/12 (50%) | 49.0 | **watch** |
| BDIX-IPTV | github_search | 992 | 566 | 10/12 (83%) | 81.8 | **promote** |
| cathode | github_search | 1884 | 638 | 0/12 (0%) | 31.5 | **reject** |
| ↳ 0 working in sample (needs 3) | | | | | | |
| m3u | github_search | 827 | 662 | 10/12 (83%) | 88.3 | **promote** |
| openstream | github_search | 5548 | 2314 | 12/12 (100%) | 88.4 | **promote** |
| pluto-playlist | github_search | 0 | 0 | 0/0 (0%) | 0.0 | **reject** |
| ↳ response is not an M3U playlist | | | | | | |
| DF_IPTV | github_search | 3571 | 3474 | 2/12 (17%) | 37.7 | **reject** |
| ↳ 2 working in sample (needs 3) | | | | | | |

## New channels from the active sources

| Source | Channels | New links | Sample working | Note |
|---|---:|---:|---:|---|
| ae-networks | 53 | 0 | 0/0 (0%) | ok |
| aria | 395 | 0 | 0/0 (0%) | ok |
| doms9 | 452 | 69 | 5/8 (62%) | ok |
| xtemus | 0 | 0 | 0/0 (0%) | ok |
| iptv-org | 11129 | 0 | 0/0 (0%) | ok |
| free-tv | 2054 | 0 | 0/0 (0%) | ok |
| eja-tv-feed | 0 | 0 | 0/0 (0%) | no URL or url_env secret set |
| stepdaddylivehd-instance | 0 | 0 | 0/0 (0%) | no URL or url_env secret set |
| dlive-sx-feed | 0 | 0 | 0/0 (0%) | no URL or url_env secret set |

## Promoted source health

| Source | Status | Channels | Working sample | Note |
|---|---|---:|---:|---|
| _no promoted sources yet_ | | | | |

## New working channels (sample)

59 new working links are in [`new-channels.m3u`](new-channels.m3u). First 20 by source:

- **湖南卫视4K** (卫视) — Akiraleal-IPTV
- **浙江卫视4K** (卫视) — Akiraleal-IPTV
- **凤凰中文** (香港) — Akiraleal-IPTV
- **凤凰香港** (香港) — Akiraleal-IPTV
- **翡翠台** (香港) — Akiraleal-IPTV
- **公视高清** (台湾) — Akiraleal-IPTV
- **耀才财经** (香港) — Akiraleal-IPTV
- **WildEarth** (文旅) — Akiraleal-IPTV
- **Love Nature 4K** (文旅) — Akiraleal-IPTV
- **CGTN Documentary** (文旅) — Akiraleal-IPTV
- **Reuters** (国际) — Akiraleal-IPTV
- **1987年春晚** (Other) — TianmuTNT-IPTV
- **1993年春晚** (Other) — TianmuTNT-IPTV
- **2024年春晚** (Other) — TianmuTNT-IPTV
- **2026-09-25 18:28:23** (Other) — TianmuTNT-IPTV
- **AMC音乐** (Other) — TianmuTNT-IPTV
- **CCTV12** (Other) — TianmuTNT-IPTV
- **CCTV13** (Other) — TianmuTNT-IPTV
- **CCTV15** (Other) — TianmuTNT-IPTV
- **Hiii** (HimelOp) — Public_Iptv_Channels

## Issues and diagnostics

None.

Promotion is not automatic publication: promoted sources are added to the next regular scrape, and every link is link-checked there before it can appear in `PremiumTV.m3u`. Roll back by removing or disabling an entry in `approved-sources.json`.
