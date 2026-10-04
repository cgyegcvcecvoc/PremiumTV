# Merged TV guide build

- **Run:** nightly merged guide build (`20261004T110751Z-2742`)
- **Started:** 2026-10-04T11:07:51Z | **Finished:** 2026-10-04T11:11:03Z | **Duration:** 191.8s
- **Guide link (`.xml`):** `https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml`
- **Gzipped:** `https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml.gz`
- **Window:** 20261004050751 +0000 to 20261005171609 +0000 UTC (30.14h ahead, 6h back; trimmed from 48h to fit the size budget)

| Result | Value |
|---|---:|
| Guides merged | 83 of 94 |
| Playlist channels | 7908 |
| Channels with a guide | 2234 (28.2%) |
| Programmes in the guide | 90880 |
| Duplicate events merged | 259418 |
| Overlapping events dropped | 69453 |
| Events dropped (out of window / placeholder) | 4278842 |
| XML size | 60077 KB |
| Gzipped size | 7309 KB |

Published [`playlists/epg/PremiumTV.xml`](../epg/PremiumTV.xml) and [`playlists/epg/PremiumTV.xml.gz`](../epg/PremiumTV.xml.gz).

## Size trimming

- 83.2 MB over the 60 MB budget: window cut from 48h to 33.9h ahead
- 64.1 MB over the 60 MB budget: window cut from 34h to 31.1h ahead
- 60.2 MB over the 60 MB budget: window cut from 31h to 30.1h ahead

## Upstream guides

| Guide | Status | Channels seen | Matched | By id | By name | Programmes kept | Dropped | Read |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `epg_ripper_ALL_SOURCES1.xml.gz` | ok | 27386 | 3859 | 1474 | 2385 | 220785 | 2482930 | 196544 KB |
| `all.xml.gz` | ok | 2959 | 626 | 16 | 610 | 15089 | 55842 | 7069 KB |
| `all.xml.gz` | ok | 2637 | 615 | 91 | 524 | 5424 | 18352 | 2742 KB |
| `epg_ripper_IN1.xml.gz` | ok | 1166 | 392 | 326 | 66 | 24283 | 89834 | 4014 KB |
| `epg_ripper_IN4.xml.gz` | ok | 557 | 268 | 211 | 57 | 8647 | 12103 | 985 KB |
| `epg_ripper_PLEX1.xml.gz` | ok | 693 | 215 | 74 | 141 | 13350 | 63854 | 4664 KB |
| `TV.xml` | ok | 241 | 186 | 179 | 7 | 11037 | 13346 | 24337 KB |
| `epg_ripper_CZ1.xml.gz` | ok | 1087 | 182 | 37 | 145 | 9175 | 49067 | 6204 KB |
| `epg_ripper_RO1.xml.gz` | ok | 370 | 127 | 56 | 71 | 7819 | 37595 | 1802 KB |
| `epg_ripper_PL1.xml.gz` | ok | 636 | 123 | 27 | 96 | 11061 | 95730 | 8650 KB |
| `epg_ripper_UY1.xml.gz` | ok | 521 | 113 | 0 | 113 | 4036 | 26415 | 2509 KB |
| `epg_ripper_CH1.xml.gz` | ok | 751 | 110 | 4 | 106 | 8059 | 79031 | 6124 KB |
| `epg_ripper_BE2.xml.gz` | ok | 571 | 101 | 4 | 97 | 6931 | 55487 | 5680 KB |
| `epg_ripper_FR1.xml.gz` | ok | 574 | 97 | 36 | 61 | 7145 | 61838 | 5339 KB |
| `epg_ripper_HU1.xml.gz` | ok | 193 | 73 | 47 | 26 | 5168 | 18236 | 1846 KB |
| `epg_ripper_TR3.xml.gz` | ok | 287 | 71 | 37 | 34 | 5672 | 25860 | 1611 KB |
| `epg_ripper_UK1.xml.gz` | ok | 486 | 71 | 41 | 30 | 3396 | 38397 | 2844 KB |
| `guide.xml.gz` | ok | 343 | 69 | 5 | 64 | 4743 | 27839 | 2521 KB |
| `epg_ripper_RS1.xml.gz` | ok | 721 | 64 | 10 | 54 | 4978 | 78087 | 7357 KB |
| `epg_ripper_GR1.xml.gz` | ok | 318 | 61 | 21 | 40 | 3099 | 20743 | 1687 KB |
| `epg_ripper_DE1.xml.gz` | ok | 266 | 58 | 33 | 25 | 4285 | 17769 | 3581 KB |
| `epg_ripper_ES1.xml.gz` | ok | 373 | 52 | 28 | 24 | 2953 | 31212 | 3256 KB |
| `epg_ripper_RO2.xml.gz` | ok | 148 | 51 | 19 | 32 | 16 | 162 | 13 KB |
| `epg_ripper_IT1.xml.gz` | ok | 193 | 50 | 33 | 17 | 4377 | 15501 | 1620 KB |
| `epg_ripper_CO1.xml.gz` | ok | 138 | 47 | 14 | 33 | 2228 | 7666 | 582 KB |
| `epg_ripper_TR1.xml.gz` | ok | 178 | 39 | 14 | 25 | 2305 | 12865 | 166 KB |
| `epg_ripper_HR1.xml.gz` | ok | 213 | 38 | 8 | 30 | 2741 | 23978 | 1941 KB |
| `epg_ripper_NL1.xml.gz` | ok | 159 | 37 | 14 | 23 | 3405 | 19936 | 1862 KB |
| `epg_ripper_PT1.xml.gz` | ok | 178 | 37 | 8 | 29 | 2045 | 19593 | 1575 KB |
| `epg_ripper_PE1.xml.gz` | ok | 164 | 36 | 0 | 36 | 430 | 1926 | 138 KB |
| `epg_ripper_ID1.xml.gz` | ok | 269 | 35 | 12 | 23 | 1114 | 11564 | 125 KB |
| `epg_ripper_IE1.xml.gz` | ok | 175 | 34 | 0 | 34 | 2030 | 16033 | 2431 KB |
| `epg_ripper_SK1.xml.gz` | ok | 217 | 33 | 1 | 32 | 2003 | 19322 | 1568 KB |
| `epg_ripper_KR1.xml.gz` | ok | 258 | 32 | 12 | 20 | 1588 | 20993 | 598 KB |
| `epg_ripper_DK1.xml.gz` | ok | 217 | 30 | 4 | 26 | 1747 | 11616 | 1279 KB |
| `epg_ripper_KE1.xml.gz` | ok | 157 | 30 | 0 | 30 | 1442 | 15553 | 175 KB |
| `epg_ripper_AU1.xml.gz` | ok | 354 | 29 | 3 | 26 | 386 | 51287 | 3612 KB |
| `epg_ripper_AL1.xml.gz` | ok | 178 | 28 | 3 | 25 | 1281 | 8571 | 384 KB |
| `epg_ripper_BA1.xml.gz` | ok | 254 | 28 | 1 | 27 | 2359 | 25836 | 2267 KB |
| `epg_ripper_PH1.xml.gz` | ok | 134 | 28 | 1 | 27 | 0 | 0 | 1 KB |
| `epg_ripper_VN1.xml.gz` | ok | 151 | 28 | 13 | 15 | 1107 | 11374 | 221 KB |
| `epg_ripper_AT1.xml.gz` | ok | 144 | 27 | 5 | 22 | 2482 | 15413 | 3698 KB |
| `epg_ripper_SG1.xml.gz` | ok | 165 | 27 | 0 | 27 | 1763 | 13924 | 590 KB |
| `epg_ripper_DISTROTV1.xml.gz` | ok | 90 | 26 | 2 | 24 | 0 | 212 | 19 KB |
| `epg_ripper_DUMMY_CHANNELS.xml.gz` | ok | 165 | 26 | 8 | 18 | 1430 | 14410 | 86 KB |
| `epg_ripper_MT1.xml.gz` | ok | 192 | 26 | 1 | 25 | 1794 | 16200 | 1234 KB |
| `epg_ripper_NG1.xml.gz` | ok | 130 | 25 | 0 | 25 | 1182 | 12265 | 143 KB |
| `epg_ripper_FI1.xml.gz` | ok | 110 | 24 | 10 | 14 | 1773 | 8597 | 1043 KB |
| `epg_ripper_SA1.xml.gz` | ok | 97 | 24 | 0 | 24 | 0 | 0 | 1 KB |
| `za.xml` | ok | 161 | 24 | 0 | 24 | 1399 | 13562 | 8798 KB |
| `epg_ripper_SE1.xml.gz` | ok | 126 | 23 | 0 | 23 | 1752 | 11843 | 1378 KB |
| `epg_ripper_ZA1.xml.gz` | ok | 145 | 23 | 5 | 18 | 1515 | 15665 | 185 KB |
| `epg_ripper_MY1.xml.gz` | ok | 163 | 22 | 0 | 22 | 873 | 10729 | 516 KB |
| `epg_ripper_HK1.xml.gz` | ok | 143 | 21 | 1 | 20 | 1586 | 11853 | 604 KB |
| `epg_ripper_CY1.xml.gz` | ok | 94 | 19 | 3 | 16 | 1325 | 12076 | 538 KB |
| `epg_ripper_EG1.xml.gz` | ok | 238 | 19 | 2 | 17 | 0 | 1279 | 195 KB |
| `epg_ripper_LT1.xml.gz` | ok | 89 | 19 | 8 | 11 | 1272 | 7291 | 868 KB |
| `epg_ripper_LV1.xml.gz` | ok | 105 | 18 | 1 | 17 | 1198 | 12658 | 768 KB |
| `epg_ripper_NZ1.xml.gz` | ok | 100 | 17 | 2 | 15 | 960 | 8626 | 430 KB |
| `epg_ripper_BG1.xml.gz` | ok | 86 | 14 | 7 | 7 | 656 | 6537 | 217 KB |
| `epg_ripper_PH2.xml.gz` | ok | 130 | 14 | 1 | 13 | 18 | 328 | 16 KB |
| `epg_ripper_IL1.xml.gz` | ok | 119 | 8 | 4 | 4 | 515 | 9887 | 539 KB |
| `epg_ripper_RAKUTEN1.xml.gz` | ok | 1640 | 8 | 8 | 0 | 414 | 183474 | 9527 KB |
| `epg_ripper_NO1.xml.gz` | ok | 161 | 5 | 0 | 5 | 486 | 14429 | 1230 KB |
| `epg_ripper_SV1.xml.gz` | ok | 476 | 5 | 0 | 5 | 280 | 43499 | 1006 KB |
| `epg_ripper_BR1.xml.gz` | ok | 266 | 4 | 2 | 2 | 254 | 15271 | 661 KB |
| `epg_ripper_ASIANTELEVISION1.xml.gz` | ok | 54 | 3 | 0 | 3 | 257 | 6490 | 106 KB |
| `epg_ripper_DIRECTVSPORTS1.xml.gz` | ok | 4 | 3 | 0 | 3 | 122 | 55 | 3 KB |
| `epg_ripper_MX1.xml.gz` | ok | 178 | 3 | 1 | 2 | 91 | 16046 | 405 KB |
| `epg_ripper_TBNPLUS1.xml.gz` | ok | 17 | 3 | 0 | 3 | 0 | 340 | 28 KB |
| `epg_ripper_AR1.xml.gz` | ok | 82 | 2 | 0 | 2 | 142 | 10504 | 250 KB |
| `epg_ripper_CL1.xml.gz` | ok | 90 | 2 | 1 | 1 | 99 | 9447 | 255 KB |
| `epg_ripper_CR1.xml.gz` | ok | 117 | 2 | 0 | 2 | 62 | 11349 | 299 KB |
| `epg_ripper_DELUXEMUSIC1.xml.gz` | ok | 5 | 2 | 2 | 0 | 15 | 26 | 3 KB |
| `epg_ripper_FANDUEL1.xml.gz` | ok | 45 | 2 | 2 | 0 | 22 | 4558 | 122 KB |
| `epg_ripper_JP1.xml.gz` | ok | 133 | 2 | 0 | 2 | 151 | 9808 | 1171 KB |
| `guide.xml.gz` | ok | 2 | 1 | 1 | 0 | 30 | 82 | 3 KB |
| `epg_ripper_ALJAZEERA1.xml.gz` | ok | 2 | 1 | 0 | 1 | 48 | 176 | 4 KB |
| `epg_ripper_DRAFTKINGS1.xml.gz` | ok | 1 | 1 | 0 | 1 | 0 | 0 | 0 KB |
| `epg_ripper_EC1.xml.gz` | ok | 90 | 1 | 0 | 1 | 50 | 9783 | 236 KB |
| `epg_ripper_JM1.xml.gz` | ok | 25 | 1 | 0 | 1 | 144 | 2383 | 87 KB |
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

- Advertised the merged guide first in **175** playlists.
