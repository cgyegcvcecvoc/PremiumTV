# Merged TV guide build

- **Run:** scheduled guide build (`20261002T235708Z-2032`)
- **Started:** 2026-10-02T23:57:08Z | **Finished:** 2026-10-02T23:58:47Z | **Duration:** 98.7s
- **Guide link (`.xml`):** `https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml`
- **Gzipped:** `https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml.gz`
- **Window:** 20261002175708 +0000 to 20261004061505 +0000 UTC (30.3h ahead, 6h back; trimmed from 48h to fit the size budget)

| Result | Value |
|---|---:|
| Guides merged | 82 of 94 |
| Playlist channels | 7997 |
| Channels with a guide | 2283 (28.5%) |
| Programmes in the guide | 92916 |
| Duplicate events merged | 247033 |
| Overlapping events dropped | 66986 |
| Events dropped (out of window / placeholder) | 4282973 |
| XML size | 60229 KB |
| Gzipped size | 7169 KB |

Published [`playlists/epg/PremiumTV.xml`](../epg/PremiumTV.xml) and [`playlists/epg/PremiumTV.xml.gz`](../epg/PremiumTV.xml.gz).

## Size trimming

- 82.3 MB over the 60 MB budget: window cut from 48h to 34.3h ahead
- 64.4 MB over the 60 MB budget: window cut from 34h to 31.3h ahead
- 60.2 MB over the 60 MB budget: window cut from 31h to 30.3h ahead

## Upstream guides

| Guide | Status | Channels seen | Matched | By id | By name | Programmes kept | Dropped | Read |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `epg_ripper_ALL_SOURCES1.xml.gz` | ok | 27386 | 3785 | 1477 | 2308 | 213557 | 2484083 | 200605 KB |
| `all.xml.gz` | ok | 2959 | 628 | 16 | 612 | 15321 | 56116 | 7202 KB |
| `all.xml.gz` | ok | 2637 | 611 | 91 | 520 | 5378 | 18316 | 2734 KB |
| `epg_ripper_IN1.xml.gz` | ok | 1166 | 395 | 331 | 64 | 24477 | 87571 | 4069 KB |
| `epg_ripper_IN4.xml.gz` | ok | 557 | 266 | 210 | 56 | 8493 | 12278 | 992 KB |
| `epg_ripper_PLEX1.xml.gz` | ok | 693 | 216 | 75 | 141 | 13412 | 63375 | 4674 KB |
| `epg_ripper_CZ1.xml.gz` | ok | 1087 | 195 | 41 | 154 | 9619 | 49536 | 6412 KB |
| `TV.xml` | ok | 240 | 190 | 188 | 2 | 10765 | 13352 | 24209 KB |
| `epg_ripper_PL1.xml.gz` | ok | 636 | 118 | 27 | 91 | 11073 | 95628 | 8827 KB |
| `epg_ripper_RO1.xml.gz` | ok | 370 | 117 | 49 | 68 | 7144 | 37221 | 1799 KB |
| `epg_ripper_UY1.xml.gz` | ok | 521 | 106 | 0 | 106 | 3861 | 25607 | 2406 KB |
| `epg_ripper_CH1.xml.gz` | ok | 751 | 102 | 4 | 98 | 7228 | 80137 | 6273 KB |
| `epg_ripper_BE2.xml.gz` | ok | 571 | 96 | 4 | 92 | 6266 | 56327 | 5812 KB |
| `epg_ripper_FR1.xml.gz` | ok | 574 | 93 | 34 | 59 | 6867 | 62403 | 5504 KB |
| `epg_ripper_HU1.xml.gz` | ok | 193 | 75 | 47 | 28 | 5162 | 18217 | 1906 KB |
| `epg_ripper_UK1.xml.gz` | ok | 486 | 67 | 40 | 27 | 3050 | 38791 | 2875 KB |
| `guide.xml.gz` | ok | 343 | 66 | 5 | 61 | 4020 | 28239 | 2487 KB |
| `epg_ripper_RS1.xml.gz` | ok | 721 | 64 | 10 | 54 | 4845 | 77724 | 7601 KB |
| `epg_ripper_GR1.xml.gz` | ok | 318 | 61 | 21 | 40 | 3149 | 21131 | 1765 KB |
| `epg_ripper_TR3.xml.gz` | ok | 287 | 60 | 32 | 28 | 2554 | 28653 | 1547 KB |
| `epg_ripper_DE1.xml.gz` | ok | 266 | 59 | 35 | 24 | 4138 | 22581 | 4378 KB |
| `epg_ripper_ES1.xml.gz` | ok | 373 | 53 | 29 | 24 | 2809 | 31207 | 3130 KB |
| `epg_ripper_IT1.xml.gz` | ok | 193 | 49 | 33 | 16 | 4496 | 15475 | 1641 KB |
| `epg_ripper_RO2.xml.gz` | ok | 148 | 48 | 19 | 29 | 37 | 161 | 15 KB |
| `epg_ripper_CO1.xml.gz` | ok | 138 | 46 | 15 | 31 | 2147 | 7762 | 587 KB |
| `epg_ripper_HR1.xml.gz` | ok | 213 | 40 | 9 | 31 | 2770 | 22808 | 1878 KB |
| `epg_ripper_ID1.xml.gz` | ok | 269 | 39 | 17 | 22 | 1298 | 11404 | 127 KB |
| `epg_ripper_SK1.xml.gz` | ok | 217 | 37 | 1 | 36 | 2256 | 18833 | 1631 KB |
| `epg_ripper_NL1.xml.gz` | ok | 159 | 35 | 14 | 21 | 3559 | 19525 | 1927 KB |
| `epg_ripper_PE1.xml.gz` | ok | 164 | 33 | 0 | 33 | 372 | 1964 | 138 KB |
| `epg_ripper_TR1.xml.gz` | ok | 178 | 33 | 11 | 22 | 2071 | 13115 | 166 KB |
| `epg_ripper_IE1.xml.gz` | ok | 175 | 31 | 2 | 29 | 1638 | 16163 | 2476 KB |
| `epg_ripper_KR1.xml.gz` | ok | 258 | 31 | 12 | 19 | 1438 | 20459 | 599 KB |
| `epg_ripper_PT1.xml.gz` | ok | 178 | 31 | 6 | 25 | 1836 | 20018 | 1597 KB |
| `epg_ripper_AL1.xml.gz` | ok | 178 | 29 | 3 | 26 | 1363 | 8506 | 399 KB |
| `epg_ripper_KE1.xml.gz` | ok | 157 | 29 | 0 | 29 | 1384 | 15537 | 174 KB |
| `epg_ripper_PH1.xml.gz` | ok | 134 | 29 | 1 | 28 | 0 | 0 | 1 KB |
| `epg_ripper_AU1.xml.gz` | ok | 354 | 28 | 3 | 25 | 706 | 50967 | 3612 KB |
| `epg_ripper_DK1.xml.gz` | ok | 217 | 27 | 3 | 24 | 1512 | 11708 | 1327 KB |
| `epg_ripper_SG1.xml.gz` | ok | 165 | 27 | 0 | 27 | 1698 | 13715 | 607 KB |
| `epg_ripper_VN1.xml.gz` | ok | 151 | 27 | 13 | 14 | 1588 | 10607 | 220 KB |
| `epg_ripper_BA1.xml.gz` | ok | 254 | 26 | 0 | 26 | 2188 | 26133 | 2293 KB |
| `epg_ripper_DISTROTV1.xml.gz` | ok | 90 | 26 | 2 | 24 | 0 | 212 | 19 KB |
| `epg_ripper_DUMMY_CHANNELS.xml.gz` | ok | 165 | 26 | 10 | 16 | 1430 | 14410 | 87 KB |
| `epg_ripper_AT1.xml.gz` | ok | 144 | 25 | 4 | 21 | 2101 | 15848 | 3790 KB |
| `epg_ripper_MT1.xml.gz` | ok | 192 | 25 | 1 | 24 | 1689 | 16321 | 1240 KB |
| `epg_ripper_NG1.xml.gz` | ok | 130 | 24 | 0 | 24 | 1122 | 12569 | 146 KB |
| `za.xml` | ok | 161 | 24 | 0 | 24 | 1405 | 13404 | 8727 KB |
| `epg_ripper_FI1.xml.gz` | ok | 110 | 23 | 10 | 13 | 1626 | 8709 | 1084 KB |
| `epg_ripper_SA1.xml.gz` | ok | 97 | 23 | 0 | 23 | 0 | 0 | 1 KB |
| `epg_ripper_ZA1.xml.gz` | ok | 145 | 23 | 5 | 18 | 1502 | 15604 | 186 KB |
| `epg_ripper_MY1.xml.gz` | ok | 163 | 21 | 0 | 21 | 835 | 10638 | 521 KB |
| `epg_ripper_SE1.xml.gz` | ok | 126 | 21 | 0 | 21 | 1502 | 11879 | 1439 KB |
| `epg_ripper_EG1.xml.gz` | ok | 238 | 20 | 2 | 18 | 0 | 1279 | 195 KB |
| `epg_ripper_LT1.xml.gz` | ok | 89 | 20 | 8 | 12 | 1320 | 7297 | 944 KB |
| `epg_ripper_HK1.xml.gz` | ok | 143 | 19 | 1 | 18 | 1382 | 11987 | 661 KB |
| `epg_ripper_LV1.xml.gz` | ok | 105 | 17 | 1 | 16 | 1092 | 12818 | 788 KB |
| `epg_ripper_CY1.xml.gz` | ok | 94 | 16 | 3 | 13 | 1168 | 12337 | 547 KB |
| `epg_ripper_PH2.xml.gz` | ok | 130 | 16 | 1 | 15 | 3 | 306 | 14 KB |
| `epg_ripper_BG1.xml.gz` | ok | 86 | 15 | 7 | 8 | 372 | 3885 | 147 KB |
| `epg_ripper_NZ1.xml.gz` | ok | 100 | 15 | 2 | 13 | 867 | 8370 | 460 KB |
| `epg_ripper_IL1.xml.gz` | ok | 119 | 8 | 4 | 4 | 548 | 9918 | 615 KB |
| `epg_ripper_RAKUTEN1.xml.gz` | ok | 1640 | 8 | 8 | 0 | 445 | 181724 | 9465 KB |
| `epg_ripper_NO1.xml.gz` | ok | 161 | 5 | 0 | 5 | 547 | 14424 | 1208 KB |
| `epg_ripper_SV1.xml.gz` | ok | 476 | 5 | 0 | 5 | 249 | 44575 | 1015 KB |
| `epg_ripper_BR1.xml.gz` | ok | 266 | 4 | 2 | 2 | 256 | 15266 | 663 KB |
| `epg_ripper_ASIANTELEVISION1.xml.gz` | ok | 54 | 3 | 0 | 3 | 250 | 6486 | 104 KB |
| `epg_ripper_DIRECTVSPORTS1.xml.gz` | ok | 4 | 3 | 0 | 3 | 140 | 71 | 3 KB |
| `epg_ripper_MX1.xml.gz` | ok | 178 | 3 | 1 | 2 | 108 | 16312 | 420 KB |
| `epg_ripper_TBNPLUS1.xml.gz` | ok | 17 | 3 | 0 | 3 | 0 | 304 | 27 KB |
| `epg_ripper_AR1.xml.gz` | ok | 82 | 2 | 0 | 2 | 153 | 10463 | 247 KB |
| `epg_ripper_CL1.xml.gz` | ok | 90 | 2 | 1 | 1 | 109 | 9023 | 251 KB |
| `epg_ripper_CR1.xml.gz` | ok | 117 | 2 | 0 | 2 | 66 | 11682 | 307 KB |
| `epg_ripper_DELUXEMUSIC1.xml.gz` | ok | 5 | 2 | 2 | 0 | 23 | 60 | 3 KB |
| `epg_ripper_FANDUEL1.xml.gz` | ok | 45 | 2 | 2 | 0 | 26 | 4090 | 133 KB |
| `guide.xml.gz` | ok | 2 | 1 | 1 | 0 | 47 | 58 | 3 KB |
| `epg_ripper_ALJAZEERA1.xml.gz` | ok | 2 | 1 | 0 | 1 | 0 | 148 | 3 KB |
| `epg_ripper_DRAFTKINGS1.xml.gz` | ok | 1 | 1 | 0 | 1 | 0 | 0 | 0 KB |
| `epg_ripper_EC1.xml.gz` | ok | 90 | 1 | 0 | 1 | 30 | 10080 | 235 KB |
| `epg_ripper_JM1.xml.gz` | ok | 25 | 1 | 0 | 1 | 108 | 2551 | 90 KB |
| `epg_ripper_JP1.xml.gz` | ok | 133 | 1 | 0 | 1 | 37 | 9644 | 1174 KB |
| `epg_ripper_RALLY_TV1.xml.gz` | ok | 1 | 1 | 0 | 1 | 0 | 0 | 0 KB |
| `epg_ripper_BEIN1.xml.gz` | nomatch | 80 | 0 | 0 | 0 | 0 | 3124 | 33 KB |
| `epg_ripper_DO1.xml.gz` | nomatch | 56 | 0 | 0 | 0 | 0 | 4973 | 162 KB |
| `epg_ripper_JP2.xml.gz` | nomatch | 244 | 0 | 0 | 0 | 0 | 0 | 4 KB |
| `epg_ripper_PA1.xml.gz` | nomatch | 106 | 0 | 0 | 0 | 0 | 10585 | 267 KB |
| `epg_ripper_PK1.xml.gz` | nomatch | 8 | 0 | 0 | 0 | 0 | 0 | 0 KB |
| `epg_ripper_SA2.xml.gz` | nomatch | 41 | 0 | 0 | 0 | 0 | 4863 | 110 KB |
| `epg_ripper_SPORTKLUB1.xml.gz` | nomatch | 16 | 0 | 0 | 0 | 0 | 950 | 35 KB |
| `epg_ripper_SSPORTPLUS1.xml.gz` | nomatch | 1 | 0 | 0 | 0 | 0 | 80 | 2 KB |
| `epg_ripper_THESPORTPLUS1.xml.gz` | nomatch | 3 | 0 | 0 | 0 | 0 | 77 | 1 KB |
| `epg_ripper_US_SPORTS1.xml.gz` | nomatch | 267 | 0 | 0 | 0 | 0 | 19994 | 226 KB |
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

- Advertised the merged guide first in **0** playlists.
