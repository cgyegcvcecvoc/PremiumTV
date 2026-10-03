# Merged TV guide build

- **Run:** nightly merged guide build (`20261003T144659Z-2767`)
- **Started:** 2026-10-03T14:46:59Z | **Finished:** 2026-10-03T14:50:12Z | **Duration:** 192.8s
- **Guide link (`.xml`):** `https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml`
- **Gzipped:** `https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml.gz`
- **Window:** 20261003084659 +0000 to 20261004212844 +0000 UTC (30.7h ahead, 6h back; trimmed from 48h to fit the size budget)

| Result | Value |
|---|---:|
| Guides merged | 82 of 94 |
| Playlist channels | 8015 |
| Channels with a guide | 2244 (28.0%) |
| Programmes in the guide | 92461 |
| Duplicate events merged | 251591 |
| Overlapping events dropped | 66798 |
| Events dropped (out of window / placeholder) | 4275061 |
| XML size | 60205 KB |
| Gzipped size | 7166 KB |

Published [`playlists/epg/PremiumTV.xml`](../epg/PremiumTV.xml) and [`playlists/epg/PremiumTV.xml.gz`](../epg/PremiumTV.xml.gz).

## Size trimming

- 82.3 MB over the 60 MB budget: window cut from 48h to 34.3h ahead
- 63.6 MB over the 60 MB budget: window cut from 34h to 31.7h ahead
- 60.0 MB over the 60 MB budget: window cut from 32h to 30.7h ahead

## Upstream guides

| Guide | Status | Channels seen | Matched | By id | By name | Programmes kept | Dropped | Read |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `epg_ripper_ALL_SOURCES1.xml.gz` | ok | 27386 | 3832 | 1483 | 2349 | 215966 | 2479840 | 200011 KB |
| `all.xml.gz` | ok | 2959 | 628 | 16 | 612 | 15055 | 55630 | 7094 KB |
| `all.xml.gz` | ok | 2637 | 610 | 91 | 519 | 5469 | 18531 | 2735 KB |
| `epg_ripper_IN1.xml.gz` | ok | 1166 | 393 | 328 | 65 | 24364 | 88311 | 4072 KB |
| `epg_ripper_IN4.xml.gz` | ok | 557 | 269 | 212 | 57 | 7451 | 13286 | 979 KB |
| `epg_ripper_PLEX1.xml.gz` | ok | 693 | 215 | 74 | 141 | 13394 | 63449 | 4644 KB |
| `TV.xml` | ok | 240 | 193 | 190 | 3 | 11008 | 13094 | 24101 KB |
| `epg_ripper_CZ1.xml.gz` | ok | 1087 | 188 | 37 | 151 | 9610 | 49545 | 6412 KB |
| `epg_ripper_PL1.xml.gz` | ok | 636 | 122 | 27 | 95 | 10783 | 95918 | 8827 KB |
| `epg_ripper_RO1.xml.gz` | ok | 370 | 115 | 50 | 65 | 7005 | 37360 | 1799 KB |
| `epg_ripper_UY1.xml.gz` | ok | 521 | 113 | 0 | 113 | 4005 | 25463 | 2406 KB |
| `epg_ripper_CH1.xml.gz` | ok | 751 | 110 | 4 | 106 | 7964 | 79401 | 6273 KB |
| `epg_ripper_BE2.xml.gz` | ok | 571 | 98 | 4 | 94 | 6720 | 55873 | 5812 KB |
| `epg_ripper_FR1.xml.gz` | ok | 574 | 96 | 35 | 61 | 7041 | 62052 | 5507 KB |
| `epg_ripper_UK1.xml.gz` | ok | 486 | 75 | 47 | 28 | 3440 | 38401 | 2875 KB |
| `epg_ripper_HU1.xml.gz` | ok | 193 | 74 | 47 | 27 | 5102 | 18277 | 1906 KB |
| `epg_ripper_TR3.xml.gz` | ok | 287 | 70 | 37 | 33 | 5743 | 26907 | 1685 KB |
| `guide.xml.gz` | ok | 343 | 68 | 5 | 63 | 3438 | 28821 | 2487 KB |
| `epg_ripper_RS1.xml.gz` | ok | 721 | 64 | 10 | 54 | 4991 | 78187 | 7620 KB |
| `epg_ripper_GR1.xml.gz` | ok | 318 | 60 | 21 | 39 | 3173 | 21107 | 1765 KB |
| `epg_ripper_DE1.xml.gz` | ok | 266 | 58 | 34 | 24 | 4064 | 17977 | 3678 KB |
| `epg_ripper_ES1.xml.gz` | ok | 373 | 53 | 29 | 24 | 2942 | 31066 | 3233 KB |
| `epg_ripper_IT1.xml.gz` | ok | 193 | 48 | 33 | 15 | 4270 | 15701 | 1641 KB |
| `epg_ripper_RO2.xml.gz` | ok | 148 | 48 | 19 | 29 | 29 | 169 | 15 KB |
| `epg_ripper_CO1.xml.gz` | ok | 138 | 44 | 14 | 30 | 2059 | 7850 | 587 KB |
| `epg_ripper_IE1.xml.gz` | ok | 175 | 44 | 2 | 42 | 2191 | 15599 | 2438 KB |
| `epg_ripper_TR1.xml.gz` | ok | 178 | 39 | 14 | 25 | 2321 | 12901 | 166 KB |
| `epg_ripper_HR1.xml.gz` | ok | 213 | 37 | 8 | 29 | 2350 | 23228 | 1878 KB |
| `epg_ripper_NL1.xml.gz` | ok | 159 | 37 | 14 | 23 | 3466 | 19594 | 1887 KB |
| `epg_ripper_SK1.xml.gz` | ok | 217 | 35 | 1 | 34 | 2170 | 18968 | 1610 KB |
| `epg_ripper_ID1.xml.gz` | ok | 269 | 34 | 12 | 22 | 1044 | 11533 | 125 KB |
| `epg_ripper_PT1.xml.gz` | ok | 178 | 34 | 8 | 26 | 1857 | 19997 | 1597 KB |
| `epg_ripper_PE1.xml.gz` | ok | 164 | 32 | 0 | 32 | 374 | 1959 | 141 KB |
| `epg_ripper_KR1.xml.gz` | ok | 258 | 31 | 12 | 19 | 1468 | 21017 | 606 KB |
| `epg_ripper_AU1.xml.gz` | ok | 354 | 29 | 3 | 26 | 503 | 51170 | 3612 KB |
| `epg_ripper_KE1.xml.gz` | ok | 157 | 29 | 0 | 29 | 1350 | 15571 | 174 KB |
| `epg_ripper_PH1.xml.gz` | ok | 134 | 29 | 1 | 28 | 0 | 0 | 1 KB |
| `epg_ripper_AL1.xml.gz` | ok | 178 | 28 | 3 | 25 | 1332 | 8659 | 427 KB |
| `epg_ripper_BA1.xml.gz` | ok | 254 | 28 | 1 | 27 | 2295 | 26026 | 2293 KB |
| `epg_ripper_DK1.xml.gz` | ok | 217 | 28 | 3 | 25 | 1520 | 11692 | 1292 KB |
| `epg_ripper_DUMMY_CHANNELS.xml.gz` | ok | 165 | 28 | 11 | 17 | 1540 | 14300 | 86 KB |
| `epg_ripper_SG1.xml.gz` | ok | 165 | 27 | 0 | 27 | 1730 | 13814 | 607 KB |
| `epg_ripper_VN1.xml.gz` | ok | 151 | 27 | 13 | 14 | 928 | 11267 | 220 KB |
| `epg_ripper_AT1.xml.gz` | ok | 144 | 26 | 5 | 21 | 2260 | 15689 | 3790 KB |
| `epg_ripper_DISTROTV1.xml.gz` | ok | 90 | 26 | 2 | 24 | 0 | 212 | 19 KB |
| `epg_ripper_FI1.xml.gz` | ok | 110 | 25 | 11 | 14 | 1780 | 8583 | 1068 KB |
| `epg_ripper_MT1.xml.gz` | ok | 192 | 25 | 1 | 24 | 1689 | 16308 | 1271 KB |
| `za.xml` | ok | 161 | 24 | 0 | 24 | 1420 | 13451 | 8754 KB |
| `epg_ripper_NG1.xml.gz` | ok | 130 | 23 | 0 | 23 | 1090 | 12601 | 146 KB |
| `epg_ripper_SE1.xml.gz` | ok | 126 | 23 | 0 | 23 | 1666 | 11775 | 1405 KB |
| `epg_ripper_ZA1.xml.gz` | ok | 145 | 23 | 5 | 18 | 1512 | 15594 | 186 KB |
| `epg_ripper_SA1.xml.gz` | ok | 97 | 22 | 0 | 22 | 0 | 0 | 1 KB |
| `epg_ripper_EG1.xml.gz` | ok | 238 | 20 | 2 | 18 | 0 | 1279 | 195 KB |
| `epg_ripper_HK1.xml.gz` | ok | 143 | 20 | 1 | 19 | 1506 | 11924 | 640 KB |
| `epg_ripper_LT1.xml.gz` | ok | 89 | 20 | 8 | 12 | 1300 | 7091 | 903 KB |
| `epg_ripper_MY1.xml.gz` | ok | 163 | 19 | 0 | 19 | 835 | 10554 | 530 KB |
| `epg_ripper_CY1.xml.gz` | ok | 94 | 17 | 3 | 14 | 1157 | 12348 | 547 KB |
| `epg_ripper_LV1.xml.gz` | ok | 105 | 17 | 1 | 16 | 1127 | 12783 | 788 KB |
| `epg_ripper_PH2.xml.gz` | ok | 130 | 16 | 1 | 15 | 15 | 393 | 19 KB |
| `epg_ripper_BG1.xml.gz` | ok | 86 | 15 | 7 | 8 | 242 | 4015 | 147 KB |
| `epg_ripper_NZ1.xml.gz` | ok | 100 | 15 | 2 | 13 | 827 | 8534 | 451 KB |
| `epg_ripper_IL1.xml.gz` | ok | 119 | 8 | 4 | 4 | 535 | 10295 | 580 KB |
| `epg_ripper_RAKUTEN1.xml.gz` | ok | 1640 | 8 | 8 | 0 | 434 | 182339 | 9449 KB |
| `epg_ripper_NO1.xml.gz` | ok | 161 | 5 | 0 | 5 | 629 | 14342 | 1208 KB |
| `epg_ripper_SV1.xml.gz` | ok | 476 | 5 | 0 | 5 | 265 | 44437 | 1036 KB |
| `epg_ripper_BR1.xml.gz` | ok | 266 | 4 | 2 | 2 | 245 | 15430 | 672 KB |
| `epg_ripper_ASIANTELEVISION1.xml.gz` | ok | 54 | 3 | 0 | 3 | 257 | 6485 | 107 KB |
| `epg_ripper_DIRECTVSPORTS1.xml.gz` | ok | 4 | 3 | 0 | 3 | 128 | 71 | 3 KB |
| `epg_ripper_TBNPLUS1.xml.gz` | ok | 17 | 3 | 0 | 3 | 0 | 289 | 26 KB |
| `epg_ripper_AR1.xml.gz` | ok | 82 | 2 | 0 | 2 | 145 | 10471 | 247 KB |
| `epg_ripper_CL1.xml.gz` | ok | 90 | 2 | 1 | 1 | 96 | 9036 | 251 KB |
| `epg_ripper_CR1.xml.gz` | ok | 117 | 2 | 0 | 2 | 70 | 11526 | 310 KB |
| `epg_ripper_DELUXEMUSIC1.xml.gz` | ok | 5 | 2 | 2 | 0 | 22 | 40 | 3 KB |
| `epg_ripper_FANDUEL1.xml.gz` | ok | 45 | 2 | 2 | 0 | 22 | 4345 | 137 KB |
| `epg_ripper_MX1.xml.gz` | ok | 178 | 2 | 1 | 1 | 42 | 16378 | 420 KB |
| `guide.xml.gz` | ok | 2 | 1 | 1 | 0 | 24 | 81 | 3 KB |
| `epg_ripper_ALJAZEERA1.xml.gz` | ok | 2 | 1 | 0 | 1 | 0 | 148 | 3 KB |
| `epg_ripper_DRAFTKINGS1.xml.gz` | ok | 1 | 1 | 0 | 1 | 0 | 0 | 0 KB |
| `epg_ripper_EC1.xml.gz` | ok | 90 | 1 | 0 | 1 | 44 | 9936 | 240 KB |
| `epg_ripper_JM1.xml.gz` | ok | 25 | 1 | 0 | 1 | 102 | 2451 | 92 KB |
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
