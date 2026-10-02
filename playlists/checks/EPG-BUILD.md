# Merged TV guide build

- **Run:** scheduled guide build (`20261002T233610Z-2113`)
- **Started:** 2026-10-02T23:36:10Z | **Finished:** 2026-10-02T23:39:04Z | **Duration:** 174.5s
- **Guide link (`.xml`):** `https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml`
- **Gzipped:** `https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml.gz`
- **Window:** 20261002173610 +0000 to 20261003113610 +0000 UTC (48h ahead, 6h back)

| Result | Value |
|---|---:|
| Guides merged | 82 of 94 |
| Playlist channels | 7997 |
| Channels with a guide | 2283 (28.5%) |
| Programmes in the guide | 51122 |
| Duplicate events merged | 247258 |
| Overlapping events dropped | 67008 |
| Events dropped (out of window / placeholder) | 4282611 |
| XML size | 33884 KB |
| Gzipped size | 4626 KB |

Published [`playlists/epg/PremiumTV.xml`](../../epg/PremiumTV.xml) and [`playlists/epg/PremiumTV.xml.gz`](../../epg/PremiumTV.xml.gz).

## Size trimming

- 82 MB over the 40 MB budget: window cut to 42h ahead
- 74 MB over the 40 MB budget: window cut to 36h ahead
- 66 MB over the 40 MB budget: window cut to 30h ahead
- 58 MB over the 40 MB budget: window cut to 24h ahead
- 50 MB over the 40 MB budget: window cut to 18h ahead
- 42 MB over the 40 MB budget: window cut to 12h ahead

## Upstream guides

| Guide | Status | Channels seen | Matched | By id | By name | Programmes kept | Dropped | Read |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `epg_ripper_ALL_SOURCES1.xml.gz` | ok | 27386 | 3785 | 1477 | 2308 | 213734 | 2483906 | 200605 KB |
| `all.xml.gz` | ok | 2959 | 628 | 16 | 612 | 15321 | 56116 | 7202 KB |
| `all.xml.gz` | ok | 2637 | 611 | 91 | 520 | 5378 | 18316 | 2734 KB |
| `epg_ripper_IN1.xml.gz` | ok | 1166 | 395 | 331 | 64 | 24481 | 87567 | 4069 KB |
| `epg_ripper_IN4.xml.gz` | ok | 557 | 266 | 210 | 56 | 8527 | 12244 | 992 KB |
| `epg_ripper_PLEX1.xml.gz` | ok | 693 | 216 | 75 | 141 | 13399 | 63388 | 4674 KB |
| `epg_ripper_CZ1.xml.gz` | ok | 1087 | 195 | 41 | 154 | 9632 | 49523 | 6412 KB |
| `TV.xml` | ok | 240 | 190 | 188 | 2 | 10768 | 13349 | 24209 KB |
| `epg_ripper_PL1.xml.gz` | ok | 636 | 118 | 27 | 91 | 11067 | 95634 | 8827 KB |
| `epg_ripper_RO1.xml.gz` | ok | 370 | 117 | 49 | 68 | 7132 | 37233 | 1799 KB |
| `epg_ripper_UY1.xml.gz` | ok | 521 | 106 | 0 | 106 | 3863 | 25605 | 2406 KB |
| `epg_ripper_CH1.xml.gz` | ok | 751 | 102 | 4 | 98 | 7244 | 80121 | 6273 KB |
| `epg_ripper_BE2.xml.gz` | ok | 571 | 96 | 4 | 92 | 6276 | 56317 | 5812 KB |
| `epg_ripper_FR1.xml.gz` | ok | 574 | 93 | 34 | 59 | 6881 | 62389 | 5504 KB |
| `epg_ripper_HU1.xml.gz` | ok | 193 | 75 | 47 | 28 | 5170 | 18209 | 1906 KB |
| `epg_ripper_UK1.xml.gz` | ok | 486 | 67 | 40 | 27 | 3049 | 38792 | 2875 KB |
| `guide.xml.gz` | ok | 343 | 66 | 5 | 61 | 4039 | 28220 | 2487 KB |
| `epg_ripper_RS1.xml.gz` | ok | 721 | 64 | 10 | 54 | 4849 | 77720 | 7601 KB |
| `epg_ripper_GR1.xml.gz` | ok | 318 | 61 | 21 | 40 | 3146 | 21134 | 1765 KB |
| `epg_ripper_TR3.xml.gz` | ok | 287 | 60 | 32 | 28 | 2573 | 28634 | 1547 KB |
| `epg_ripper_DE1.xml.gz` | ok | 266 | 59 | 35 | 24 | 4147 | 22572 | 4378 KB |
| `epg_ripper_ES1.xml.gz` | ok | 373 | 53 | 29 | 24 | 2821 | 31195 | 3130 KB |
| `epg_ripper_IT1.xml.gz` | ok | 193 | 49 | 33 | 16 | 4487 | 15484 | 1641 KB |
| `epg_ripper_RO2.xml.gz` | ok | 148 | 48 | 19 | 29 | 37 | 161 | 15 KB |
| `epg_ripper_CO1.xml.gz` | ok | 138 | 46 | 15 | 31 | 2150 | 7759 | 587 KB |
| `epg_ripper_HR1.xml.gz` | ok | 213 | 40 | 9 | 31 | 2773 | 22805 | 1878 KB |
| `epg_ripper_ID1.xml.gz` | ok | 269 | 39 | 17 | 22 | 1300 | 11402 | 127 KB |
| `epg_ripper_SK1.xml.gz` | ok | 217 | 37 | 1 | 36 | 2256 | 18833 | 1631 KB |
| `epg_ripper_NL1.xml.gz` | ok | 159 | 35 | 14 | 21 | 3565 | 19519 | 1927 KB |
| `epg_ripper_PE1.xml.gz` | ok | 164 | 33 | 0 | 33 | 374 | 1962 | 138 KB |
| `epg_ripper_TR1.xml.gz` | ok | 178 | 33 | 11 | 22 | 2082 | 13104 | 166 KB |
| `epg_ripper_IE1.xml.gz` | ok | 175 | 31 | 2 | 29 | 1637 | 16164 | 2476 KB |
| `epg_ripper_KR1.xml.gz` | ok | 258 | 31 | 12 | 19 | 1439 | 20458 | 599 KB |
| `epg_ripper_PT1.xml.gz` | ok | 178 | 31 | 6 | 25 | 1837 | 20017 | 1597 KB |
| `epg_ripper_AL1.xml.gz` | ok | 178 | 29 | 3 | 26 | 1363 | 8506 | 399 KB |
| `epg_ripper_KE1.xml.gz` | ok | 157 | 29 | 0 | 29 | 1380 | 15541 | 174 KB |
| `epg_ripper_PH1.xml.gz` | ok | 134 | 29 | 1 | 28 | 0 | 0 | 1 KB |
| `epg_ripper_AU1.xml.gz` | ok | 354 | 28 | 3 | 25 | 708 | 50965 | 3612 KB |
| `epg_ripper_DK1.xml.gz` | ok | 217 | 27 | 3 | 24 | 1516 | 11704 | 1327 KB |
| `epg_ripper_SG1.xml.gz` | ok | 165 | 27 | 0 | 27 | 1698 | 13715 | 607 KB |
| `epg_ripper_VN1.xml.gz` | ok | 151 | 27 | 13 | 14 | 1598 | 10597 | 220 KB |
| `epg_ripper_BA1.xml.gz` | ok | 254 | 26 | 0 | 26 | 2189 | 26132 | 2293 KB |
| `epg_ripper_DISTROTV1.xml.gz` | ok | 90 | 26 | 2 | 24 | 0 | 212 | 19 KB |
| `epg_ripper_DUMMY_CHANNELS.xml.gz` | ok | 165 | 26 | 10 | 16 | 1430 | 14410 | 87 KB |
| `epg_ripper_AT1.xml.gz` | ok | 144 | 25 | 4 | 21 | 2107 | 15842 | 3790 KB |
| `epg_ripper_MT1.xml.gz` | ok | 192 | 25 | 1 | 24 | 1693 | 16317 | 1240 KB |
| `epg_ripper_NG1.xml.gz` | ok | 130 | 24 | 0 | 24 | 1123 | 12568 | 146 KB |
| `za.xml` | ok | 161 | 24 | 0 | 24 | 1412 | 13397 | 8727 KB |
| `epg_ripper_FI1.xml.gz` | ok | 110 | 23 | 10 | 13 | 1622 | 8713 | 1084 KB |
| `epg_ripper_SA1.xml.gz` | ok | 97 | 23 | 0 | 23 | 0 | 0 | 1 KB |
| `epg_ripper_ZA1.xml.gz` | ok | 145 | 23 | 5 | 18 | 1501 | 15605 | 186 KB |
| `epg_ripper_MY1.xml.gz` | ok | 163 | 21 | 0 | 21 | 838 | 10635 | 521 KB |
| `epg_ripper_SE1.xml.gz` | ok | 126 | 21 | 0 | 21 | 1505 | 11876 | 1439 KB |
| `epg_ripper_EG1.xml.gz` | ok | 238 | 20 | 2 | 18 | 0 | 1279 | 195 KB |
| `epg_ripper_LT1.xml.gz` | ok | 89 | 20 | 8 | 12 | 1322 | 7295 | 944 KB |
| `epg_ripper_HK1.xml.gz` | ok | 143 | 19 | 1 | 18 | 1385 | 11984 | 661 KB |
| `epg_ripper_LV1.xml.gz` | ok | 105 | 17 | 1 | 16 | 1093 | 12817 | 788 KB |
| `epg_ripper_CY1.xml.gz` | ok | 94 | 16 | 3 | 13 | 1168 | 12337 | 547 KB |
| `epg_ripper_PH2.xml.gz` | ok | 130 | 16 | 1 | 15 | 3 | 306 | 14 KB |
| `epg_ripper_BG1.xml.gz` | ok | 86 | 15 | 7 | 8 | 373 | 3884 | 147 KB |
| `epg_ripper_NZ1.xml.gz` | ok | 100 | 15 | 2 | 13 | 863 | 8374 | 460 KB |
| `epg_ripper_IL1.xml.gz` | ok | 119 | 8 | 4 | 4 | 549 | 9917 | 615 KB |
| `epg_ripper_RAKUTEN1.xml.gz` | ok | 1640 | 8 | 8 | 0 | 444 | 181725 | 9465 KB |
| `epg_ripper_NO1.xml.gz` | ok | 161 | 5 | 0 | 5 | 547 | 14424 | 1208 KB |
| `epg_ripper_SV1.xml.gz` | ok | 476 | 5 | 0 | 5 | 249 | 44575 | 1015 KB |
| `epg_ripper_BR1.xml.gz` | ok | 266 | 4 | 2 | 2 | 255 | 15267 | 663 KB |
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
| `epg_ripper_JM1.xml.gz` | ok | 25 | 1 | 0 | 1 | 109 | 2550 | 90 KB |
| `epg_ripper_JP1.xml.gz` | ok | 133 | 1 | 0 | 1 | 36 | 9645 | 1174 KB |
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

- Advertised the merged guide first in **3** playlists.
