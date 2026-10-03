# Merged TV guide build

- **Run:** nightly merged guide build (`20261003T150005Z-2795`)
- **Started:** 2026-10-03T15:00:05Z | **Finished:** 2026-10-03T15:03:13Z | **Duration:** 187.7s
- **Guide link (`.xml`):** `https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml`
- **Gzipped:** `https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml.gz`
- **Window:** 20261003090005 +0000 to 20261004235704 +0000 UTC (32.95h ahead, 6h back; trimmed from 48h to fit the size budget)

| Result | Value |
|---|---:|
| Guides merged | 82 of 94 |
| Playlist channels | 7997 |
| Channels with a guide | 2233 (27.9%) |
| Programmes in the guide | 94927 |
| Duplicate events merged | 243787 |
| Overlapping events dropped | 64827 |
| Events dropped (out of window / placeholder) | 4286386 |
| XML size | 61145 KB |
| Gzipped size | 7150 KB |

Published [`playlists/epg/PremiumTV.xml`](../epg/PremiumTV.xml) and [`playlists/epg/PremiumTV.xml.gz`](../epg/PremiumTV.xml.gz).

## Size trimming

- 80.3 MB over the 60 MB budget: window cut from 48h to 35.2h ahead
- 62.7 MB over the 60 MB budget: window cut from 35h to 32.9h ahead

## Upstream guides

| Guide | Status | Channels seen | Matched | By id | By name | Programmes kept | Dropped | Read |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `epg_ripper_ALL_SOURCES1.xml.gz` | ok | 27386 | 3752 | 1473 | 2279 | 210137 | 2485669 | 200011 KB |
| `all.xml.gz` | ok | 2959 | 628 | 16 | 612 | 15055 | 55630 | 7094 KB |
| `all.xml.gz` | ok | 2637 | 611 | 91 | 520 | 5476 | 18524 | 2735 KB |
| `epg_ripper_IN1.xml.gz` | ok | 1166 | 392 | 328 | 64 | 24517 | 88158 | 4072 KB |
| `epg_ripper_IN4.xml.gz` | ok | 557 | 267 | 211 | 56 | 7260 | 13477 | 979 KB |
| `epg_ripper_PLEX1.xml.gz` | ok | 693 | 216 | 75 | 141 | 13411 | 63432 | 4644 KB |
| `TV.xml` | ok | 240 | 190 | 186 | 4 | 10675 | 13427 | 24101 KB |
| `epg_ripper_CZ1.xml.gz` | ok | 1087 | 178 | 37 | 141 | 9209 | 49946 | 6412 KB |
| `epg_ripper_PL1.xml.gz` | ok | 636 | 119 | 27 | 92 | 10619 | 96082 | 8827 KB |
| `epg_ripper_RO1.xml.gz` | ok | 370 | 115 | 50 | 65 | 6977 | 37388 | 1799 KB |
| `epg_ripper_UY1.xml.gz` | ok | 521 | 103 | 0 | 103 | 3584 | 25884 | 2406 KB |
| `epg_ripper_CH1.xml.gz` | ok | 751 | 101 | 4 | 97 | 7152 | 80213 | 6273 KB |
| `epg_ripper_FR1.xml.gz` | ok | 574 | 94 | 36 | 58 | 6880 | 62213 | 5507 KB |
| `epg_ripper_BE2.xml.gz` | ok | 571 | 93 | 4 | 89 | 6325 | 56268 | 5812 KB |
| `epg_ripper_HU1.xml.gz` | ok | 193 | 73 | 47 | 26 | 5059 | 18320 | 1906 KB |
| `epg_ripper_TR3.xml.gz` | ok | 287 | 72 | 39 | 33 | 5840 | 26810 | 1685 KB |
| `epg_ripper_UK1.xml.gz` | ok | 486 | 71 | 45 | 26 | 3293 | 38548 | 2875 KB |
| `guide.xml.gz` | ok | 343 | 69 | 5 | 64 | 3485 | 28774 | 2487 KB |
| `epg_ripper_RS1.xml.gz` | ok | 721 | 62 | 10 | 52 | 4863 | 78315 | 7620 KB |
| `epg_ripper_GR1.xml.gz` | ok | 318 | 60 | 22 | 38 | 2957 | 21323 | 1765 KB |
| `epg_ripper_DE1.xml.gz` | ok | 266 | 59 | 35 | 24 | 4112 | 17929 | 3678 KB |
| `epg_ripper_ES1.xml.gz` | ok | 373 | 54 | 29 | 25 | 2981 | 31027 | 3233 KB |
| `epg_ripper_RO2.xml.gz` | ok | 148 | 48 | 19 | 29 | 29 | 169 | 15 KB |
| `epg_ripper_CO1.xml.gz` | ok | 138 | 44 | 14 | 30 | 2003 | 7906 | 587 KB |
| `epg_ripper_IT1.xml.gz` | ok | 193 | 41 | 26 | 15 | 3461 | 16510 | 1641 KB |
| `epg_ripper_TR1.xml.gz` | ok | 178 | 39 | 14 | 25 | 2315 | 12907 | 166 KB |
| `epg_ripper_IE1.xml.gz` | ok | 175 | 38 | 1 | 37 | 2020 | 15770 | 2438 KB |
| `epg_ripper_NL1.xml.gz` | ok | 159 | 37 | 14 | 23 | 3470 | 19590 | 1887 KB |
| `epg_ripper_HR1.xml.gz` | ok | 213 | 34 | 6 | 28 | 2028 | 23550 | 1878 KB |
| `epg_ripper_ID1.xml.gz` | ok | 269 | 34 | 12 | 22 | 1046 | 11531 | 125 KB |
| `epg_ripper_PE1.xml.gz` | ok | 164 | 33 | 0 | 33 | 379 | 1954 | 141 KB |
| `epg_ripper_PT1.xml.gz` | ok | 178 | 33 | 8 | 25 | 1791 | 20063 | 1597 KB |
| `epg_ripper_SK1.xml.gz` | ok | 217 | 33 | 1 | 32 | 2024 | 19114 | 1610 KB |
| `epg_ripper_KR1.xml.gz` | ok | 258 | 31 | 12 | 19 | 1471 | 21014 | 606 KB |
| `epg_ripper_DUMMY_CHANNELS.xml.gz` | ok | 165 | 29 | 12 | 17 | 1595 | 14245 | 86 KB |
| `epg_ripper_KE1.xml.gz` | ok | 157 | 29 | 0 | 29 | 1354 | 15567 | 174 KB |
| `epg_ripper_AL1.xml.gz` | ok | 178 | 28 | 3 | 25 | 1333 | 8658 | 427 KB |
| `epg_ripper_AU1.xml.gz` | ok | 354 | 28 | 3 | 25 | 402 | 51271 | 3612 KB |
| `epg_ripper_BA1.xml.gz` | ok | 254 | 27 | 1 | 26 | 2229 | 26092 | 2293 KB |
| `epg_ripper_DK1.xml.gz` | ok | 217 | 27 | 3 | 24 | 1462 | 11750 | 1292 KB |
| `epg_ripper_PH1.xml.gz` | ok | 134 | 27 | 1 | 26 | 0 | 0 | 1 KB |
| `epg_ripper_SG1.xml.gz` | ok | 165 | 27 | 0 | 27 | 1731 | 13813 | 607 KB |
| `epg_ripper_VN1.xml.gz` | ok | 151 | 27 | 13 | 14 | 912 | 11283 | 220 KB |
| `epg_ripper_AT1.xml.gz` | ok | 144 | 26 | 5 | 21 | 2258 | 15691 | 3790 KB |
| `epg_ripper_DISTROTV1.xml.gz` | ok | 90 | 26 | 2 | 24 | 0 | 212 | 19 KB |
| `epg_ripper_FI1.xml.gz` | ok | 110 | 25 | 12 | 13 | 1747 | 8616 | 1068 KB |
| `epg_ripper_NG1.xml.gz` | ok | 130 | 23 | 0 | 23 | 1094 | 12597 | 146 KB |
| `za.xml` | ok | 161 | 23 | 0 | 23 | 1324 | 13547 | 8754 KB |
| `epg_ripper_MT1.xml.gz` | ok | 192 | 22 | 1 | 21 | 1516 | 16481 | 1271 KB |
| `epg_ripper_SA1.xml.gz` | ok | 97 | 22 | 0 | 22 | 0 | 0 | 1 KB |
| `epg_ripper_ZA1.xml.gz` | ok | 145 | 22 | 5 | 17 | 1416 | 15690 | 186 KB |
| `epg_ripper_SE1.xml.gz` | ok | 126 | 21 | 0 | 21 | 1541 | 11900 | 1405 KB |
| `epg_ripper_EG1.xml.gz` | ok | 238 | 20 | 2 | 18 | 0 | 1279 | 195 KB |
| `epg_ripper_HK1.xml.gz` | ok | 143 | 20 | 1 | 19 | 1507 | 11923 | 640 KB |
| `epg_ripper_MY1.xml.gz` | ok | 163 | 20 | 0 | 20 | 854 | 10535 | 530 KB |
| `epg_ripper_LT1.xml.gz` | ok | 89 | 19 | 8 | 11 | 1246 | 7145 | 903 KB |
| `epg_ripper_CY1.xml.gz` | ok | 94 | 17 | 3 | 14 | 1158 | 12347 | 547 KB |
| `epg_ripper_LV1.xml.gz` | ok | 105 | 17 | 1 | 16 | 1128 | 12782 | 788 KB |
| `epg_ripper_NZ1.xml.gz` | ok | 100 | 15 | 2 | 13 | 832 | 8529 | 451 KB |
| `epg_ripper_BG1.xml.gz` | ok | 86 | 14 | 7 | 7 | 202 | 4055 | 147 KB |
| `epg_ripper_PH2.xml.gz` | ok | 130 | 14 | 1 | 13 | 15 | 393 | 19 KB |
| `epg_ripper_IL1.xml.gz` | ok | 119 | 8 | 4 | 4 | 536 | 10294 | 580 KB |
| `epg_ripper_RAKUTEN1.xml.gz` | ok | 1640 | 8 | 8 | 0 | 432 | 182341 | 9449 KB |
| `epg_ripper_SV1.xml.gz` | ok | 476 | 5 | 0 | 5 | 266 | 44436 | 1036 KB |
| `epg_ripper_BR1.xml.gz` | ok | 266 | 4 | 2 | 2 | 245 | 15430 | 672 KB |
| `epg_ripper_NO1.xml.gz` | ok | 161 | 4 | 0 | 4 | 450 | 14521 | 1208 KB |
| `epg_ripper_ASIANTELEVISION1.xml.gz` | ok | 54 | 3 | 0 | 3 | 257 | 6485 | 107 KB |
| `epg_ripper_DIRECTVSPORTS1.xml.gz` | ok | 4 | 3 | 0 | 3 | 126 | 73 | 3 KB |
| `epg_ripper_MX1.xml.gz` | ok | 178 | 3 | 1 | 2 | 94 | 16326 | 420 KB |
| `epg_ripper_TBNPLUS1.xml.gz` | ok | 17 | 3 | 0 | 3 | 0 | 289 | 26 KB |
| `epg_ripper_AR1.xml.gz` | ok | 82 | 2 | 0 | 2 | 144 | 10472 | 247 KB |
| `epg_ripper_CL1.xml.gz` | ok | 90 | 2 | 1 | 1 | 94 | 9038 | 251 KB |
| `epg_ripper_CR1.xml.gz` | ok | 117 | 2 | 0 | 2 | 69 | 11527 | 310 KB |
| `epg_ripper_DELUXEMUSIC1.xml.gz` | ok | 5 | 2 | 2 | 0 | 22 | 40 | 3 KB |
| `epg_ripper_FANDUEL1.xml.gz` | ok | 45 | 2 | 2 | 0 | 22 | 4345 | 137 KB |
| `guide.xml.gz` | ok | 2 | 1 | 1 | 0 | 23 | 82 | 3 KB |
| `epg_ripper_ALJAZEERA1.xml.gz` | ok | 2 | 1 | 0 | 1 | 0 | 148 | 3 KB |
| `epg_ripper_DRAFTKINGS1.xml.gz` | ok | 1 | 1 | 0 | 1 | 0 | 0 | 0 KB |
| `epg_ripper_EC1.xml.gz` | ok | 90 | 1 | 0 | 1 | 43 | 9937 | 240 KB |
| `epg_ripper_JM1.xml.gz` | ok | 25 | 1 | 0 | 1 | 103 | 2450 | 92 KB |
| `epg_ripper_JP1.xml.gz` | ok | 133 | 1 | 0 | 1 | 43 | 9638 | 1174 KB |
| `epg_ripper_RALLY_TV1.xml.gz` | ok | 1 | 1 | 0 | 1 | 0 | 0 | 0 KB |
| `epg_ripper_BEIN1.xml.gz` | nomatch | 80 | 0 | 0 | 0 | 0 | 3124 | 33 KB |
| `epg_ripper_DO1.xml.gz` | nomatch | 56 | 0 | 0 | 0 | 0 | 4973 | 167 KB |
| `epg_ripper_JP2.xml.gz` | nomatch | 244 | 0 | 0 | 0 | 0 | 0 | 4 KB |
| `epg_ripper_PA1.xml.gz` | nomatch | 106 | 0 | 0 | 0 | 0 | 10585 | 267 KB |
| `epg_ripper_PK1.xml.gz` | nomatch | 8 | 0 | 0 | 0 | 0 | 0 | 0 KB |
| `epg_ripper_SA2.xml.gz` | nomatch | 41 | 0 | 0 | 0 | 0 | 4863 | 110 KB |
| `epg_ripper_SPORTKLUB1.xml.gz` | nomatch | 16 | 0 | 0 | 0 | 0 | 973 | 36 KB |
| `epg_ripper_SSPORTPLUS1.xml.gz` | nomatch | 1 | 0 | 0 | 0 | 0 | 80 | 2 KB |
| `epg_ripper_THESPORTPLUS1.xml.gz` | nomatch | 3 | 0 | 0 | 0 | 0 | 75 | 1 KB |
| `epg_ripper_US_SPORTS1.xml.gz` | nomatch | 267 | 0 | 0 | 0 | 0 | 19783 | 225 KB |
| `epg_ripper_VOA1.xml.gz` | nomatch | 10 | 0 | 0 | 0 | 0 | 0 | 0 KB |
| `epg_ripper_viva-russia.ru.xml.gz` | nomatch | 1 | 0 | 0 | 0 | 0 | 222 | 3 KB |

## Guides that contributed nothing

| Guide | Status | Reason |
|---|---|---|
| `https://epgshare01.online/epgshare01/epg_ripper_BEIN1.xml.gz` | nomatch | 80 channels, none matched the published playlists |
| `https://epgshare01.online/epgshare01/epg_ripper_DO1.xml.gz` | nomatch | 56 channels, none matched the published playlists |
| `https://epgshare01.online/epgshare01/epg_ripper_JP2.xml.gz` | nomatch | 244 channels, none matched the published playlists |
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

- Advertised the merged guide first in **176** playlists.
