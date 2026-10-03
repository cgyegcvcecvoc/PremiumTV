# Merged TV guide build

- **Run:** scheduled guide build (`20261003T143037Z-2140`)
- **Started:** 2026-10-03T14:30:37Z | **Finished:** 2026-10-03T14:33:27Z | **Duration:** 169.8s
- **Guide link (`.xml`):** `https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml`
- **Gzipped:** `https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml.gz`
- **Window:** 20261003083037 +0000 to 20261004215726 +0000 UTC (31.45h ahead, 6h back; trimmed from 48h to fit the size budget)

| Result | Value |
|---|---:|
| Guides merged | 82 of 94 |
| Playlist channels | 8088 |
| Channels with a guide | 2264 (28.0%) |
| Programmes in the guide | 94545 |
| Duplicate events merged | 252647 |
| Overlapping events dropped | 66881 |
| Events dropped (out of window / placeholder) | 4273263 |
| XML size | 61401 KB |
| Gzipped size | 7304 KB |

Published [`playlists/epg/PremiumTV.xml`](../epg/PremiumTV.xml) and [`playlists/epg/PremiumTV.xml.gz`](../epg/PremiumTV.xml.gz).

## Size trimming

- 83.0 MB over the 60 MB budget: window cut from 48h to 34.0h ahead
- 63.6 MB over the 60 MB budget: window cut from 34h to 31.4h ahead

## Upstream guides

| Guide | Status | Channels seen | Matched | By id | By name | Programmes kept | Dropped | Read |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `epg_ripper_ALL_SOURCES1.xml.gz` | ok | 27386 | 3851 | 1496 | 2355 | 216849 | 2478957 | 200011 KB |
| `all.xml.gz` | ok | 2959 | 627 | 16 | 611 | 15022 | 55663 | 7094 KB |
| `all.xml.gz` | ok | 2637 | 610 | 91 | 519 | 5469 | 18531 | 2735 KB |
| `epg_ripper_IN1.xml.gz` | ok | 1166 | 396 | 330 | 66 | 24579 | 88096 | 4072 KB |
| `epg_ripper_IN4.xml.gz` | ok | 557 | 269 | 212 | 57 | 7463 | 13274 | 979 KB |
| `epg_ripper_PLEX1.xml.gz` | ok | 693 | 215 | 75 | 140 | 13320 | 63523 | 4644 KB |
| `TV.xml` | ok | 240 | 196 | 193 | 3 | 11148 | 12954 | 24101 KB |
| `epg_ripper_CZ1.xml.gz` | ok | 1087 | 190 | 37 | 153 | 9711 | 49444 | 6412 KB |
| `epg_ripper_PL1.xml.gz` | ok | 636 | 123 | 28 | 95 | 10827 | 95874 | 8827 KB |
| `epg_ripper_RO1.xml.gz` | ok | 370 | 116 | 50 | 66 | 7055 | 37310 | 1799 KB |
| `epg_ripper_UY1.xml.gz` | ok | 521 | 113 | 0 | 113 | 4008 | 25460 | 2406 KB |
| `epg_ripper_CH1.xml.gz` | ok | 751 | 108 | 4 | 104 | 7718 | 79647 | 6273 KB |
| `epg_ripper_BE2.xml.gz` | ok | 571 | 98 | 4 | 94 | 6547 | 56046 | 5812 KB |
| `epg_ripper_FR1.xml.gz` | ok | 574 | 96 | 35 | 61 | 7043 | 62050 | 5507 KB |
| `epg_ripper_HU1.xml.gz` | ok | 193 | 75 | 47 | 28 | 5152 | 18227 | 1906 KB |
| `epg_ripper_UK1.xml.gz` | ok | 486 | 75 | 47 | 28 | 3436 | 38405 | 2875 KB |
| `epg_ripper_TR3.xml.gz` | ok | 287 | 70 | 37 | 33 | 5750 | 26900 | 1685 KB |
| `guide.xml.gz` | ok | 343 | 68 | 5 | 63 | 3449 | 28810 | 2487 KB |
| `epg_ripper_RS1.xml.gz` | ok | 721 | 65 | 10 | 55 | 5037 | 78141 | 7620 KB |
| `epg_ripper_GR1.xml.gz` | ok | 318 | 61 | 22 | 39 | 3182 | 21098 | 1765 KB |
| `epg_ripper_DE1.xml.gz` | ok | 266 | 58 | 34 | 24 | 4066 | 17975 | 3678 KB |
| `epg_ripper_ES1.xml.gz` | ok | 373 | 55 | 31 | 24 | 3101 | 30907 | 3233 KB |
| `epg_ripper_IT1.xml.gz` | ok | 193 | 48 | 33 | 15 | 4276 | 15695 | 1641 KB |
| `epg_ripper_RO2.xml.gz` | ok | 148 | 48 | 19 | 29 | 29 | 169 | 15 KB |
| `epg_ripper_CO1.xml.gz` | ok | 138 | 45 | 15 | 30 | 2063 | 7846 | 587 KB |
| `epg_ripper_IE1.xml.gz` | ok | 175 | 44 | 2 | 42 | 2184 | 15606 | 2438 KB |
| `epg_ripper_HR1.xml.gz` | ok | 213 | 39 | 9 | 30 | 2715 | 22863 | 1878 KB |
| `epg_ripper_TR1.xml.gz` | ok | 178 | 39 | 14 | 25 | 2329 | 12893 | 166 KB |
| `epg_ripper_NL1.xml.gz` | ok | 159 | 37 | 14 | 23 | 3469 | 19591 | 1887 KB |
| `epg_ripper_SK1.xml.gz` | ok | 217 | 36 | 1 | 35 | 2218 | 18920 | 1610 KB |
| `epg_ripper_ID1.xml.gz` | ok | 269 | 35 | 13 | 22 | 1152 | 11425 | 125 KB |
| `epg_ripper_PT1.xml.gz` | ok | 178 | 34 | 8 | 26 | 1857 | 19997 | 1597 KB |
| `epg_ripper_PE1.xml.gz` | ok | 164 | 32 | 0 | 32 | 373 | 1960 | 141 KB |
| `epg_ripper_KR1.xml.gz` | ok | 258 | 31 | 12 | 19 | 1466 | 21019 | 606 KB |
| `epg_ripper_AU1.xml.gz` | ok | 354 | 29 | 3 | 26 | 504 | 51169 | 3612 KB |
| `epg_ripper_DUMMY_CHANNELS.xml.gz` | ok | 165 | 29 | 12 | 17 | 1595 | 14245 | 86 KB |
| `epg_ripper_KE1.xml.gz` | ok | 157 | 29 | 0 | 29 | 1349 | 15572 | 174 KB |
| `epg_ripper_PH1.xml.gz` | ok | 134 | 29 | 1 | 28 | 0 | 0 | 1 KB |
| `epg_ripper_AL1.xml.gz` | ok | 178 | 28 | 3 | 25 | 1333 | 8658 | 427 KB |
| `epg_ripper_BA1.xml.gz` | ok | 254 | 28 | 1 | 27 | 2304 | 26017 | 2293 KB |
| `epg_ripper_DK1.xml.gz` | ok | 217 | 28 | 3 | 25 | 1521 | 11691 | 1292 KB |
| `epg_ripper_SG1.xml.gz` | ok | 165 | 27 | 0 | 27 | 1729 | 13815 | 607 KB |
| `epg_ripper_VN1.xml.gz` | ok | 151 | 27 | 13 | 14 | 933 | 11262 | 220 KB |
| `epg_ripper_AT1.xml.gz` | ok | 144 | 26 | 5 | 21 | 2254 | 15695 | 3790 KB |
| `epg_ripper_DISTROTV1.xml.gz` | ok | 90 | 26 | 2 | 24 | 0 | 212 | 19 KB |
| `epg_ripper_FI1.xml.gz` | ok | 110 | 25 | 11 | 14 | 1779 | 8584 | 1068 KB |
| `epg_ripper_MT1.xml.gz` | ok | 192 | 25 | 1 | 24 | 1691 | 16306 | 1271 KB |
| `za.xml` | ok | 161 | 24 | 0 | 24 | 1418 | 13453 | 8754 KB |
| `epg_ripper_NG1.xml.gz` | ok | 130 | 23 | 0 | 23 | 1090 | 12601 | 146 KB |
| `epg_ripper_SE1.xml.gz` | ok | 126 | 23 | 0 | 23 | 1669 | 11772 | 1405 KB |
| `epg_ripper_ZA1.xml.gz` | ok | 145 | 23 | 5 | 18 | 1510 | 15596 | 186 KB |
| `epg_ripper_SA1.xml.gz` | ok | 97 | 22 | 0 | 22 | 0 | 0 | 1 KB |
| `epg_ripper_EG1.xml.gz` | ok | 238 | 20 | 2 | 18 | 0 | 1279 | 195 KB |
| `epg_ripper_HK1.xml.gz` | ok | 143 | 20 | 1 | 19 | 1504 | 11926 | 640 KB |
| `epg_ripper_LT1.xml.gz` | ok | 89 | 20 | 8 | 12 | 1299 | 7092 | 903 KB |
| `epg_ripper_MY1.xml.gz` | ok | 163 | 19 | 0 | 19 | 834 | 10555 | 530 KB |
| `epg_ripper_CY1.xml.gz` | ok | 94 | 17 | 3 | 14 | 1154 | 12351 | 547 KB |
| `epg_ripper_LV1.xml.gz` | ok | 105 | 17 | 1 | 16 | 1128 | 12782 | 788 KB |
| `epg_ripper_PH2.xml.gz` | ok | 130 | 16 | 1 | 15 | 15 | 393 | 19 KB |
| `epg_ripper_BG1.xml.gz` | ok | 86 | 15 | 7 | 8 | 244 | 4013 | 147 KB |
| `epg_ripper_NZ1.xml.gz` | ok | 100 | 15 | 2 | 13 | 827 | 8534 | 451 KB |
| `epg_ripper_IL1.xml.gz` | ok | 119 | 8 | 4 | 4 | 534 | 10296 | 580 KB |
| `epg_ripper_RAKUTEN1.xml.gz` | ok | 1640 | 8 | 8 | 0 | 434 | 182339 | 9449 KB |
| `epg_ripper_NO1.xml.gz` | ok | 161 | 5 | 0 | 5 | 629 | 14342 | 1208 KB |
| `epg_ripper_SV1.xml.gz` | ok | 476 | 5 | 0 | 5 | 265 | 44437 | 1036 KB |
| `epg_ripper_BR1.xml.gz` | ok | 266 | 4 | 2 | 2 | 244 | 15431 | 672 KB |
| `epg_ripper_ASIANTELEVISION1.xml.gz` | ok | 54 | 3 | 0 | 3 | 257 | 6485 | 107 KB |
| `epg_ripper_DIRECTVSPORTS1.xml.gz` | ok | 4 | 3 | 0 | 3 | 128 | 71 | 3 KB |
| `epg_ripper_TBNPLUS1.xml.gz` | ok | 17 | 3 | 0 | 3 | 0 | 289 | 26 KB |
| `epg_ripper_AR1.xml.gz` | ok | 82 | 2 | 0 | 2 | 145 | 10471 | 247 KB |
| `epg_ripper_CL1.xml.gz` | ok | 90 | 2 | 1 | 1 | 97 | 9035 | 251 KB |
| `epg_ripper_CR1.xml.gz` | ok | 117 | 2 | 0 | 2 | 70 | 11526 | 310 KB |
| `epg_ripper_DELUXEMUSIC1.xml.gz` | ok | 5 | 2 | 2 | 0 | 22 | 40 | 3 KB |
| `epg_ripper_FANDUEL1.xml.gz` | ok | 45 | 2 | 2 | 0 | 22 | 4345 | 137 KB |
| `epg_ripper_MX1.xml.gz` | ok | 178 | 2 | 1 | 1 | 42 | 16378 | 420 KB |
| `guide.xml.gz` | ok | 2 | 1 | 1 | 0 | 24 | 81 | 3 KB |
| `epg_ripper_ALJAZEERA1.xml.gz` | ok | 2 | 1 | 0 | 1 | 0 | 148 | 3 KB |
| `epg_ripper_DRAFTKINGS1.xml.gz` | ok | 1 | 1 | 0 | 1 | 0 | 0 | 0 KB |
| `epg_ripper_EC1.xml.gz` | ok | 90 | 1 | 0 | 1 | 45 | 9935 | 240 KB |
| `epg_ripper_JM1.xml.gz` | ok | 25 | 1 | 0 | 1 | 104 | 2449 | 92 KB |
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

- Advertised the merged guide first in **0** playlists.
