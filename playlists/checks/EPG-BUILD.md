# Merged TV guide build

- **Run:** scheduled guide build (`20261004T145840Z-2153`)
- **Started:** 2026-10-04T14:58:40Z | **Finished:** 2026-10-04T15:01:28Z | **Duration:** 168.4s
- **Guide link (`.xml`):** `https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml`
- **Gzipped:** `https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml.gz`
- **Window:** 20261004085840 +0000 to 20261005221824 +0000 UTC (31.33h ahead, 6h back; trimmed from 48h to fit the size budget)

| Result | Value |
|---|---:|
| Guides merged | 83 of 94 |
| Playlist channels | 7916 |
| Channels with a guide | 2220 (28.0%) |
| Programmes in the guide | 92100 |
| Duplicate events merged | 251381 |
| Overlapping events dropped | 67596 |
| Events dropped (out of window / placeholder) | 4289794 |
| XML size | 60354 KB |
| Gzipped size | 7267 KB |

Published [`playlists/epg/PremiumTV.xml`](../epg/PremiumTV.xml) and [`playlists/epg/PremiumTV.xml.gz`](../epg/PremiumTV.xml.gz).

## Size trimming

- 81.1 MB over the 60 MB budget: window cut from 48h to 34.8h ahead
- 63.3 MB over the 60 MB budget: window cut from 35h to 32.3h ahead
- 60.2 MB over the 60 MB budget: window cut from 32h to 31.3h ahead

## Upstream guides

| Guide | Status | Channels seen | Matched | By id | By name | Programmes kept | Dropped | Read |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `epg_ripper_ALL_SOURCES1.xml.gz` | ok | 27386 | 3799 | 1470 | 2329 | 214867 | 2488848 | 196544 KB |
| `all.xml.gz` | ok | 2959 | 628 | 16 | 612 | 15042 | 55624 | 7069 KB |
| `all.xml.gz` | ok | 2637 | 615 | 91 | 524 | 5319 | 18103 | 2716 KB |
| `epg_ripper_IN1.xml.gz` | ok | 1166 | 394 | 328 | 66 | 24508 | 89609 | 4014 KB |
| `epg_ripper_IN4.xml.gz` | ok | 557 | 268 | 211 | 57 | 7320 | 13430 | 985 KB |
| `epg_ripper_PLEX1.xml.gz` | ok | 693 | 215 | 74 | 141 | 13338 | 63866 | 4664 KB |
| `TV.xml` | ok | 241 | 186 | 181 | 5 | 11048 | 13335 | 24337 KB |
| `epg_ripper_CZ1.xml.gz` | ok | 1087 | 177 | 37 | 140 | 9125 | 49117 | 6204 KB |
| `epg_ripper_RO1.xml.gz` | ok | 370 | 126 | 56 | 70 | 7727 | 37687 | 1802 KB |
| `epg_ripper_PL1.xml.gz` | ok | 636 | 121 | 29 | 92 | 10803 | 95988 | 8650 KB |
| `epg_ripper_UY1.xml.gz` | ok | 521 | 103 | 0 | 103 | 3692 | 26759 | 2509 KB |
| `epg_ripper_CH1.xml.gz` | ok | 751 | 100 | 4 | 96 | 7052 | 80038 | 6124 KB |
| `epg_ripper_BE2.xml.gz` | ok | 571 | 96 | 4 | 92 | 6523 | 55895 | 5680 KB |
| `epg_ripper_FR1.xml.gz` | ok | 574 | 94 | 35 | 59 | 6860 | 62123 | 5339 KB |
| `epg_ripper_HU1.xml.gz` | ok | 193 | 73 | 47 | 26 | 5181 | 18223 | 1846 KB |
| `epg_ripper_UK1.xml.gz` | ok | 486 | 73 | 44 | 29 | 3508 | 38285 | 2844 KB |
| `epg_ripper_TR3.xml.gz` | ok | 287 | 71 | 37 | 34 | 5656 | 25876 | 1611 KB |
| `guide.xml.gz` | ok | 343 | 69 | 5 | 64 | 4718 | 27864 | 2521 KB |
| `epg_ripper_RS1.xml.gz` | ok | 721 | 62 | 10 | 52 | 4813 | 78252 | 7357 KB |
| `epg_ripper_GR1.xml.gz` | ok | 318 | 61 | 21 | 40 | 3100 | 20742 | 1687 KB |
| `epg_ripper_DE1.xml.gz` | ok | 266 | 59 | 34 | 25 | 4319 | 17735 | 3581 KB |
| `epg_ripper_ES1.xml.gz` | ok | 373 | 52 | 29 | 23 | 2927 | 31238 | 3256 KB |
| `epg_ripper_RO2.xml.gz` | ok | 148 | 51 | 19 | 32 | 13 | 165 | 13 KB |
| `epg_ripper_CO1.xml.gz` | ok | 138 | 45 | 14 | 31 | 2103 | 7791 | 582 KB |
| `epg_ripper_IT1.xml.gz` | ok | 193 | 42 | 26 | 16 | 3441 | 16437 | 1620 KB |
| `epg_ripper_TR1.xml.gz` | ok | 178 | 39 | 14 | 25 | 2283 | 12887 | 166 KB |
| `epg_ripper_IE1.xml.gz` | ok | 175 | 38 | 1 | 37 | 2177 | 15886 | 2431 KB |
| `epg_ripper_ID1.xml.gz` | ok | 269 | 37 | 13 | 24 | 1287 | 11391 | 125 KB |
| `epg_ripper_NL1.xml.gz` | ok | 159 | 37 | 14 | 23 | 3343 | 19998 | 1862 KB |
| `epg_ripper_PT1.xml.gz` | ok | 178 | 37 | 8 | 29 | 2023 | 19615 | 1575 KB |
| `epg_ripper_HR1.xml.gz` | ok | 213 | 35 | 5 | 30 | 2374 | 24345 | 1941 KB |
| `epg_ripper_PE1.xml.gz` | ok | 164 | 33 | 0 | 33 | 405 | 1951 | 138 KB |
| `epg_ripper_KR1.xml.gz` | ok | 258 | 32 | 12 | 20 | 1604 | 20977 | 598 KB |
| `epg_ripper_SK1.xml.gz` | ok | 217 | 32 | 1 | 31 | 1978 | 19347 | 1568 KB |
| `epg_ripper_AU1.xml.gz` | ok | 354 | 30 | 3 | 27 | 379 | 51294 | 3612 KB |
| `epg_ripper_KE1.xml.gz` | ok | 157 | 30 | 0 | 30 | 1442 | 15553 | 175 KB |
| `epg_ripper_DK1.xml.gz` | ok | 217 | 29 | 3 | 26 | 1678 | 11685 | 1279 KB |
| `epg_ripper_AL1.xml.gz` | ok | 178 | 28 | 3 | 25 | 1163 | 8689 | 384 KB |
| `epg_ripper_VN1.xml.gz` | ok | 151 | 28 | 13 | 15 | 963 | 11518 | 221 KB |
| `epg_ripper_AT1.xml.gz` | ok | 144 | 27 | 5 | 22 | 2496 | 15399 | 3698 KB |
| `epg_ripper_BA1.xml.gz` | ok | 254 | 27 | 1 | 26 | 2204 | 25991 | 2267 KB |
| `epg_ripper_PH1.xml.gz` | ok | 134 | 27 | 1 | 26 | 0 | 0 | 1 KB |
| `epg_ripper_SG1.xml.gz` | ok | 165 | 27 | 0 | 27 | 1785 | 13902 | 590 KB |
| `epg_ripper_DISTROTV1.xml.gz` | ok | 90 | 26 | 2 | 24 | 0 | 212 | 19 KB |
| `epg_ripper_DUMMY_CHANNELS.xml.gz` | ok | 165 | 26 | 8 | 18 | 1430 | 14410 | 86 KB |
| `epg_ripper_MT1.xml.gz` | ok | 192 | 25 | 1 | 24 | 1653 | 16341 | 1234 KB |
| `epg_ripper_NG1.xml.gz` | ok | 130 | 25 | 0 | 25 | 1192 | 12255 | 143 KB |
| `epg_ripper_FI1.xml.gz` | ok | 110 | 24 | 10 | 14 | 1736 | 8634 | 1043 KB |
| `epg_ripper_SA1.xml.gz` | ok | 97 | 24 | 0 | 24 | 0 | 0 | 1 KB |
| `za.xml` | ok | 161 | 24 | 0 | 24 | 1399 | 13562 | 8798 KB |
| `epg_ripper_ZA1.xml.gz` | ok | 145 | 23 | 5 | 18 | 1513 | 15667 | 185 KB |
| `epg_ripper_SE1.xml.gz` | ok | 126 | 22 | 0 | 22 | 1668 | 11927 | 1378 KB |
| `epg_ripper_HK1.xml.gz` | ok | 143 | 21 | 1 | 20 | 1653 | 11786 | 604 KB |
| `epg_ripper_MY1.xml.gz` | ok | 163 | 21 | 0 | 21 | 874 | 10728 | 516 KB |
| `epg_ripper_CY1.xml.gz` | ok | 94 | 19 | 3 | 16 | 1323 | 12078 | 538 KB |
| `epg_ripper_EG1.xml.gz` | ok | 238 | 19 | 2 | 17 | 0 | 1279 | 195 KB |
| `epg_ripper_LT1.xml.gz` | ok | 89 | 19 | 8 | 11 | 1265 | 7298 | 868 KB |
| `epg_ripper_LV1.xml.gz` | ok | 105 | 18 | 1 | 17 | 1207 | 12649 | 768 KB |
| `epg_ripper_NZ1.xml.gz` | ok | 100 | 17 | 2 | 15 | 1013 | 8573 | 430 KB |
| `epg_ripper_PH2.xml.gz` | ok | 130 | 14 | 1 | 13 | 14 | 332 | 16 KB |
| `epg_ripper_BG1.xml.gz` | ok | 86 | 13 | 7 | 6 | 603 | 6590 | 217 KB |
| `epg_ripper_IL1.xml.gz` | ok | 119 | 8 | 4 | 4 | 519 | 9883 | 539 KB |
| `epg_ripper_RAKUTEN1.xml.gz` | ok | 1640 | 8 | 8 | 0 | 421 | 183467 | 9527 KB |
| `epg_ripper_NO1.xml.gz` | ok | 161 | 5 | 0 | 5 | 511 | 14404 | 1230 KB |
| `epg_ripper_SV1.xml.gz` | ok | 476 | 5 | 0 | 5 | 287 | 43492 | 1006 KB |
| `epg_ripper_BR1.xml.gz` | ok | 266 | 4 | 2 | 2 | 246 | 15279 | 661 KB |
| `epg_ripper_ASIANTELEVISION1.xml.gz` | ok | 54 | 3 | 0 | 3 | 256 | 6491 | 106 KB |
| `epg_ripper_DIRECTVSPORTS1.xml.gz` | ok | 4 | 3 | 0 | 3 | 121 | 56 | 3 KB |
| `epg_ripper_MX1.xml.gz` | ok | 178 | 3 | 1 | 2 | 94 | 16043 | 405 KB |
| `epg_ripper_TBNPLUS1.xml.gz` | ok | 17 | 3 | 0 | 3 | 0 | 340 | 28 KB |
| `epg_ripper_AR1.xml.gz` | ok | 82 | 2 | 0 | 2 | 147 | 10499 | 250 KB |
| `epg_ripper_CL1.xml.gz` | ok | 90 | 2 | 1 | 1 | 95 | 9451 | 255 KB |
| `epg_ripper_CR1.xml.gz` | ok | 117 | 2 | 0 | 2 | 60 | 11351 | 299 KB |
| `epg_ripper_DELUXEMUSIC1.xml.gz` | ok | 5 | 2 | 2 | 0 | 15 | 26 | 3 KB |
| `epg_ripper_FANDUEL1.xml.gz` | ok | 45 | 2 | 2 | 0 | 22 | 4558 | 122 KB |
| `epg_ripper_JP1.xml.gz` | ok | 133 | 2 | 0 | 2 | 150 | 9809 | 1171 KB |
| `guide.xml.gz` | ok | 2 | 1 | 1 | 0 | 24 | 88 | 3 KB |
| `epg_ripper_ALJAZEERA1.xml.gz` | ok | 2 | 1 | 0 | 1 | 47 | 177 | 4 KB |
| `epg_ripper_DRAFTKINGS1.xml.gz` | ok | 1 | 1 | 0 | 1 | 0 | 0 | 0 KB |
| `epg_ripper_EC1.xml.gz` | ok | 90 | 1 | 0 | 1 | 48 | 9785 | 236 KB |
| `epg_ripper_JM1.xml.gz` | ok | 25 | 1 | 0 | 1 | 135 | 2392 | 87 KB |
| `epg_ripper_JP2.xml.gz` | ok | 244 | 1 | 0 | 1 | 0 | 0 | 4 KB |
| `epg_ripper_RALLY_TV1.xml.gz` | ok | 1 | 1 | 0 | 1 | 0 | 0 | 0 KB |
| `epg_ripper_BEIN1.xml.gz` | nomatch | 80 | 0 | 0 | 0 | 0 | 3268 | 35 KB |
| `epg_ripper_DO1.xml.gz` | nomatch | 56 | 0 | 0 | 0 | 0 | 4912 | 163 KB |
| `epg_ripper_PA1.xml.gz` | nomatch | 106 | 0 | 0 | 0 | 0 | 10726 | 271 KB |
| `epg_ripper_PK1.xml.gz` | nomatch | 8 | 0 | 0 | 0 | 0 | 0 | 0 KB |
| `epg_ripper_SA2.xml.gz` | nomatch | 41 | 0 | 0 | 0 | 0 | 4628 | 103 KB |
| `epg_ripper_SPORTKLUB1.xml.gz` | nomatch | 16 | 0 | 0 | 0 | 0 | 927 | 33 KB |
| `epg_ripper_SSPORTPLUS1.xml.gz` | nomatch | 1 | 0 | 0 | 0 | 0 | 71 | 1 KB |
| `epg_ripper_THESPORTPLUS1.xml.gz` | nomatch | 3 | 0 | 0 | 0 | 0 | 75 | 1 KB |
| `epg_ripper_US_SPORTS1.xml.gz` | nomatch | 267 | 0 | 0 | 0 | 0 | 19595 | 223 KB |
| `epg_ripper_VOA1.xml.gz` | nomatch | 10 | 0 | 0 | 0 | 0 | 0 | 0 KB |
| `epg_ripper_viva-russia.ru.xml.gz` | nomatch | 1 | 0 | 0 | 0 | 0 | 222 | 3 KB |

## Guides that contributed nothing

| Guide | Status | Reason |
|---|---|---|
| `https://epgshare01.online/epgshare01/epg_ripper_BEIN1.xml.gz` | nomatch | 80 channels, none matched the published playlists |
| `https://epgshare01.online/epgshare01/epg_ripper_DO1.xml.gz` | nomatch | 56 channels, none matched the published playlists |
| `https://epgshare01.online/epgshare01/epg_ripper_PA1.xml.gz` | nomatch | 106 channels, none matched the published playlists |
| `https://epgshare01.online/epgshare01/epg_ripper_PK1.xml.gz` | nomatch | 8 channels, none matched the published playlists |
| `https://epgshare01.online/epgshare01/epg_ripper_SA2.xml.gz` | nomatch | 41 channels, none matched the published playlists |
| `https://epgshare01.online/epgshare01/epg_ripper_SPORTKLUB1.xml.gz` | nomatch | 16 channels, none matched the published playlists |
| `https://epgshare01.online/epgshare01/epg_ripper_SSPORTPLUS1.xml.gz` | nomatch | 1 channels, none matched the published playlists |
| `https://epgshare01.online/epgshare01/epg_ripper_THESPORTPLUS1.xml.gz` | nomatch | 3 channels, none matched the published playlists |
| `https://epgshare01.online/epgshare01/epg_ripper_US_SPORTS1.xml.gz` | nomatch | 267 channels, none matched the published playlists |
| `https://epgshare01.online/epgshare01/epg_ripper_VOA1.xml.gz` | nomatch | 10 channels, none matched the published playlists |
| `https://epgshare01.online/epgshare01/epg_ripper_viva-russia.ru.xml.gz` | nomatch | 1 channels, none matched the published playlists |

## Playlist headers

- Advertised the merged guide first in **0** playlists.
