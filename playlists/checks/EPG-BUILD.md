# Merged TV guide build

- **Run:** nightly merged guide build (`20261003T151015Z-2705`)
- **Started:** 2026-10-03T15:10:15Z | **Finished:** 2026-10-03T15:12:30Z | **Duration:** 134.3s
- **Guide link (`.xml`):** `https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml`
- **Gzipped:** `https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml.gz`
- **Window:** 20261003091015 +0000 to 20261004231020 +0000 UTC (32h ahead, 6h back; trimmed from 48h to fit the size budget)

| Result | Value |
|---|---:|
| Guides merged | 82 of 94 |
| Playlist channels | 7973 |
| Channels with a guide | 2229 (28.0%) |
| Programmes in the guide | 93519 |
| Duplicate events merged | 243555 |
| Overlapping events dropped | 64865 |
| Events dropped (out of window / placeholder) | 4286796 |
| XML size | 60259 KB |
| Gzipped size | 7073 KB |

Published [`playlists/epg/PremiumTV.xml`](../epg/PremiumTV.xml) and [`playlists/epg/PremiumTV.xml.gz`](../epg/PremiumTV.xml.gz).

## Size trimming

- 80.2 MB over the 60 MB budget: window cut from 48h to 35.2h ahead
- 62.7 MB over the 60 MB budget: window cut from 35h to 33.0h ahead
- 60.1 MB over the 60 MB budget: window cut from 33h to 32.0h ahead

## Upstream guides

| Guide | Status | Channels seen | Matched | By id | By name | Programmes kept | Dropped | Read |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `epg_ripper_ALL_SOURCES1.xml.gz` | ok | 27386 | 3752 | 1469 | 2283 | 209962 | 2485844 | 200011 KB |
| `all.xml.gz` | ok | 2959 | 628 | 16 | 612 | 15055 | 55630 | 7094 KB |
| `all.xml.gz` | ok | 2637 | 611 | 91 | 520 | 5476 | 18524 | 2735 KB |
| `epg_ripper_IN1.xml.gz` | ok | 1166 | 391 | 326 | 65 | 24300 | 88375 | 4072 KB |
| `epg_ripper_IN4.xml.gz` | ok | 557 | 267 | 211 | 56 | 7249 | 13488 | 979 KB |
| `epg_ripper_PLEX1.xml.gz` | ok | 693 | 216 | 75 | 141 | 13404 | 63439 | 4644 KB |
| `TV.xml` | ok | 240 | 189 | 185 | 4 | 10619 | 13483 | 24101 KB |
| `epg_ripper_CZ1.xml.gz` | ok | 1087 | 178 | 37 | 141 | 9211 | 49944 | 6412 KB |
| `epg_ripper_PL1.xml.gz` | ok | 636 | 119 | 27 | 92 | 10624 | 96077 | 8827 KB |
| `epg_ripper_RO1.xml.gz` | ok | 370 | 115 | 50 | 65 | 6987 | 37378 | 1799 KB |
| `epg_ripper_UY1.xml.gz` | ok | 521 | 103 | 0 | 103 | 3579 | 25889 | 2406 KB |
| `epg_ripper_CH1.xml.gz` | ok | 751 | 101 | 4 | 97 | 7150 | 80215 | 6273 KB |
| `epg_ripper_BE2.xml.gz` | ok | 571 | 93 | 4 | 89 | 6328 | 56265 | 5812 KB |
| `epg_ripper_FR1.xml.gz` | ok | 574 | 93 | 35 | 58 | 6861 | 62232 | 5507 KB |
| `epg_ripper_HU1.xml.gz` | ok | 193 | 73 | 47 | 26 | 5058 | 18321 | 1906 KB |
| `epg_ripper_TR3.xml.gz` | ok | 287 | 72 | 39 | 33 | 5842 | 26808 | 1685 KB |
| `epg_ripper_UK1.xml.gz` | ok | 486 | 72 | 45 | 27 | 3314 | 38527 | 2875 KB |
| `guide.xml.gz` | ok | 343 | 69 | 5 | 64 | 3475 | 28784 | 2487 KB |
| `epg_ripper_RS1.xml.gz` | ok | 721 | 62 | 10 | 52 | 4863 | 78315 | 7620 KB |
| `epg_ripper_GR1.xml.gz` | ok | 318 | 60 | 22 | 38 | 2957 | 21323 | 1765 KB |
| `epg_ripper_DE1.xml.gz` | ok | 266 | 59 | 35 | 24 | 4117 | 17924 | 3678 KB |
| `epg_ripper_ES1.xml.gz` | ok | 373 | 54 | 29 | 25 | 2981 | 31027 | 3233 KB |
| `epg_ripper_RO2.xml.gz` | ok | 148 | 48 | 19 | 29 | 29 | 169 | 15 KB |
| `epg_ripper_CO1.xml.gz` | ok | 138 | 44 | 14 | 30 | 2001 | 7908 | 587 KB |
| `epg_ripper_IT1.xml.gz` | ok | 193 | 41 | 26 | 15 | 3462 | 16509 | 1641 KB |
| `epg_ripper_TR1.xml.gz` | ok | 178 | 39 | 14 | 25 | 2313 | 12909 | 166 KB |
| `epg_ripper_IE1.xml.gz` | ok | 175 | 38 | 1 | 37 | 2020 | 15770 | 2438 KB |
| `epg_ripper_NL1.xml.gz` | ok | 159 | 37 | 14 | 23 | 3469 | 19591 | 1887 KB |
| `epg_ripper_HR1.xml.gz` | ok | 213 | 34 | 6 | 28 | 2029 | 23549 | 1878 KB |
| `epg_ripper_ID1.xml.gz` | ok | 269 | 34 | 12 | 22 | 1045 | 11532 | 125 KB |
| `epg_ripper_PT1.xml.gz` | ok | 178 | 34 | 8 | 26 | 1868 | 19986 | 1597 KB |
| `epg_ripper_PE1.xml.gz` | ok | 164 | 33 | 0 | 33 | 380 | 1953 | 141 KB |
| `epg_ripper_SK1.xml.gz` | ok | 217 | 33 | 1 | 32 | 2025 | 19113 | 1610 KB |
| `epg_ripper_KR1.xml.gz` | ok | 258 | 31 | 12 | 19 | 1468 | 21017 | 606 KB |
| `epg_ripper_KE1.xml.gz` | ok | 157 | 29 | 0 | 29 | 1354 | 15567 | 174 KB |
| `epg_ripper_AL1.xml.gz` | ok | 178 | 28 | 3 | 25 | 1333 | 8658 | 427 KB |
| `epg_ripper_AU1.xml.gz` | ok | 354 | 28 | 3 | 25 | 403 | 51270 | 3612 KB |
| `epg_ripper_DK1.xml.gz` | ok | 217 | 28 | 3 | 25 | 1499 | 11713 | 1292 KB |
| `epg_ripper_DUMMY_CHANNELS.xml.gz` | ok | 165 | 28 | 11 | 17 | 1540 | 14300 | 86 KB |
| `epg_ripper_BA1.xml.gz` | ok | 254 | 27 | 1 | 26 | 2225 | 26096 | 2293 KB |
| `epg_ripper_PH1.xml.gz` | ok | 134 | 27 | 1 | 26 | 0 | 0 | 1 KB |
| `epg_ripper_SG1.xml.gz` | ok | 165 | 27 | 0 | 27 | 1729 | 13815 | 607 KB |
| `epg_ripper_VN1.xml.gz` | ok | 151 | 27 | 13 | 14 | 912 | 11283 | 220 KB |
| `epg_ripper_AT1.xml.gz` | ok | 144 | 26 | 5 | 21 | 2261 | 15688 | 3790 KB |
| `epg_ripper_DISTROTV1.xml.gz` | ok | 90 | 26 | 2 | 24 | 0 | 212 | 19 KB |
| `epg_ripper_FI1.xml.gz` | ok | 110 | 25 | 12 | 13 | 1748 | 8615 | 1068 KB |
| `epg_ripper_NG1.xml.gz` | ok | 130 | 23 | 0 | 23 | 1093 | 12598 | 146 KB |
| `za.xml` | ok | 161 | 23 | 0 | 23 | 1321 | 13550 | 8754 KB |
| `epg_ripper_MT1.xml.gz` | ok | 192 | 22 | 1 | 21 | 1516 | 16481 | 1271 KB |
| `epg_ripper_SA1.xml.gz` | ok | 97 | 22 | 0 | 22 | 0 | 0 | 1 KB |
| `epg_ripper_ZA1.xml.gz` | ok | 145 | 22 | 5 | 17 | 1415 | 15691 | 186 KB |
| `epg_ripper_SE1.xml.gz` | ok | 126 | 21 | 0 | 21 | 1541 | 11900 | 1405 KB |
| `epg_ripper_EG1.xml.gz` | ok | 238 | 20 | 2 | 18 | 0 | 1279 | 195 KB |
| `epg_ripper_HK1.xml.gz` | ok | 143 | 20 | 1 | 19 | 1506 | 11924 | 640 KB |
| `epg_ripper_MY1.xml.gz` | ok | 163 | 20 | 0 | 20 | 853 | 10536 | 530 KB |
| `epg_ripper_LT1.xml.gz` | ok | 89 | 19 | 8 | 11 | 1246 | 7145 | 903 KB |
| `epg_ripper_CY1.xml.gz` | ok | 94 | 17 | 3 | 14 | 1159 | 12346 | 547 KB |
| `epg_ripper_LV1.xml.gz` | ok | 105 | 17 | 1 | 16 | 1129 | 12781 | 788 KB |
| `epg_ripper_NZ1.xml.gz` | ok | 100 | 15 | 2 | 13 | 832 | 8529 | 451 KB |
| `epg_ripper_BG1.xml.gz` | ok | 86 | 14 | 7 | 7 | 202 | 4055 | 147 KB |
| `epg_ripper_PH2.xml.gz` | ok | 130 | 14 | 1 | 13 | 15 | 393 | 19 KB |
| `epg_ripper_IL1.xml.gz` | ok | 119 | 8 | 4 | 4 | 535 | 10295 | 580 KB |
| `epg_ripper_RAKUTEN1.xml.gz` | ok | 1640 | 8 | 8 | 0 | 432 | 182341 | 9449 KB |
| `epg_ripper_SV1.xml.gz` | ok | 476 | 5 | 0 | 5 | 266 | 44436 | 1036 KB |
| `epg_ripper_BR1.xml.gz` | ok | 266 | 4 | 2 | 2 | 245 | 15430 | 672 KB |
| `epg_ripper_NO1.xml.gz` | ok | 161 | 4 | 0 | 4 | 449 | 14522 | 1208 KB |
| `epg_ripper_ASIANTELEVISION1.xml.gz` | ok | 54 | 3 | 0 | 3 | 257 | 6485 | 107 KB |
| `epg_ripper_DIRECTVSPORTS1.xml.gz` | ok | 4 | 3 | 0 | 3 | 126 | 73 | 3 KB |
| `epg_ripper_MX1.xml.gz` | ok | 178 | 3 | 1 | 2 | 94 | 16326 | 420 KB |
| `epg_ripper_TBNPLUS1.xml.gz` | ok | 17 | 3 | 0 | 3 | 0 | 289 | 26 KB |
| `epg_ripper_AR1.xml.gz` | ok | 82 | 2 | 0 | 2 | 144 | 10472 | 247 KB |
| `epg_ripper_CL1.xml.gz` | ok | 90 | 2 | 1 | 1 | 94 | 9038 | 251 KB |
| `epg_ripper_CR1.xml.gz` | ok | 117 | 2 | 0 | 2 | 68 | 11528 | 310 KB |
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
