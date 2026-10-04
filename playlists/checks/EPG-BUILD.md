# Merged TV guide build

- **Run:** scheduled guide build (`20261004T000706Z-2146`)
- **Started:** 2026-10-04T00:07:06Z | **Finished:** 2026-10-04T00:10:14Z | **Duration:** 188.3s
- **Guide link (`.xml`):** `https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml`
- **Gzipped:** `https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml.gz`
- **Window:** 20261003180706 +0000 to 20261005083806 +0000 UTC (32.52h ahead, 6h back; trimmed from 48h to fit the size budget)

| Result | Value |
|---|---:|
| Guides merged | 82 of 94 |
| Playlist channels | 7978 |
| Channels with a guide | 2224 (27.9%) |
| Programmes in the guide | 93936 |
| Duplicate events merged | 246945 |
| Overlapping events dropped | 65545 |
| Events dropped (out of window / placeholder) | 4301746 |
| XML size | 61052 KB |
| Gzipped size | 7173 KB |

Published [`playlists/epg/PremiumTV.xml`](../epg/PremiumTV.xml) and [`playlists/epg/PremiumTV.xml.gz`](../epg/PremiumTV.xml.gz).

## Size trimming

- 80.8 MB over the 60 MB budget: window cut from 48h to 34.9h ahead
- 63.1 MB over the 60 MB budget: window cut from 35h to 32.5h ahead

## Upstream guides

| Guide | Status | Channels seen | Matched | By id | By name | Programmes kept | Dropped | Read |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `epg_ripper_ALL_SOURCES1.xml.gz` | ok | 27386 | 3759 | 1470 | 2289 | 211629 | 2494010 | 198549 KB |
| `all.xml.gz` | ok | 2959 | 628 | 16 | 612 | 15076 | 55965 | 7133 KB |
| `all.xml.gz` | ok | 2637 | 611 | 91 | 520 | 5353 | 18307 | 2722 KB |
| `epg_ripper_IN1.xml.gz` | ok | 1166 | 391 | 327 | 64 | 23802 | 88873 | 4072 KB |
| `epg_ripper_IN4.xml.gz` | ok | 557 | 267 | 211 | 56 | 8308 | 12339 | 985 KB |
| `epg_ripper_PLEX1.xml.gz` | ok | 693 | 215 | 74 | 141 | 13251 | 63592 | 4644 KB |
| `TV.xml` | ok | 241 | 189 | 186 | 3 | 10721 | 13529 | 24173 KB |
| `epg_ripper_CZ1.xml.gz` | ok | 1087 | 179 | 37 | 142 | 9148 | 49094 | 6204 KB |
| `epg_ripper_PL1.xml.gz` | ok | 636 | 119 | 27 | 92 | 10535 | 96256 | 8650 KB |
| `epg_ripper_RO1.xml.gz` | ok | 370 | 116 | 50 | 66 | 7082 | 38332 | 1802 KB |
| `epg_ripper_UY1.xml.gz` | ok | 521 | 111 | 0 | 111 | 3963 | 26488 | 2509 KB |
| `epg_ripper_CH1.xml.gz` | ok | 751 | 101 | 4 | 97 | 7101 | 79989 | 6124 KB |
| `epg_ripper_BE2.xml.gz` | ok | 571 | 93 | 4 | 89 | 6259 | 56159 | 5680 KB |
| `epg_ripper_FR1.xml.gz` | ok | 574 | 92 | 35 | 57 | 6790 | 62303 | 5507 KB |
| `epg_ripper_HU1.xml.gz` | ok | 193 | 73 | 47 | 26 | 5067 | 18337 | 1846 KB |
| `epg_ripper_TR3.xml.gz` | ok | 287 | 72 | 39 | 33 | 5673 | 26977 | 1685 KB |
| `epg_ripper_UK1.xml.gz` | ok | 486 | 70 | 43 | 27 | 3204 | 38589 | 2844 KB |
| `guide.xml.gz` | ok | 343 | 68 | 5 | 63 | 4299 | 28354 | 2517 KB |
| `epg_ripper_RS1.xml.gz` | ok | 721 | 62 | 10 | 52 | 4826 | 78352 | 7620 KB |
| `epg_ripper_GR1.xml.gz` | ok | 318 | 61 | 21 | 40 | 2918 | 20924 | 1687 KB |
| `epg_ripper_DE1.xml.gz` | ok | 266 | 58 | 34 | 24 | 4150 | 22543 | 4324 KB |
| `epg_ripper_ES1.xml.gz` | ok | 373 | 54 | 29 | 25 | 2815 | 31193 | 3233 KB |
| `epg_ripper_RO2.xml.gz` | ok | 148 | 49 | 19 | 30 | 20 | 158 | 13 KB |
| `epg_ripper_CO1.xml.gz` | ok | 138 | 46 | 14 | 32 | 2249 | 7645 | 582 KB |
| `epg_ripper_IT1.xml.gz` | ok | 193 | 41 | 26 | 15 | 3505 | 16373 | 1620 KB |
| `epg_ripper_TR1.xml.gz` | ok | 178 | 38 | 14 | 24 | 2254 | 12849 | 166 KB |
| `epg_ripper_HR1.xml.gz` | ok | 213 | 37 | 8 | 29 | 2636 | 24083 | 1941 KB |
| `epg_ripper_NL1.xml.gz` | ok | 159 | 36 | 14 | 22 | 3520 | 19540 | 1887 KB |
| `epg_ripper_PT1.xml.gz` | ok | 178 | 35 | 8 | 27 | 1941 | 19697 | 1575 KB |
| `epg_ripper_IE1.xml.gz` | ok | 175 | 34 | 0 | 34 | 1721 | 16069 | 2438 KB |
| `epg_ripper_ID1.xml.gz` | ok | 269 | 33 | 12 | 21 | 1113 | 11464 | 125 KB |
| `epg_ripper_PE1.xml.gz` | ok | 164 | 32 | 0 | 32 | 378 | 1955 | 141 KB |
| `epg_ripper_SK1.xml.gz` | ok | 217 | 32 | 1 | 31 | 1988 | 19150 | 1610 KB |
| `epg_ripper_KR1.xml.gz` | ok | 258 | 31 | 12 | 19 | 1480 | 21005 | 606 KB |
| `epg_ripper_KE1.xml.gz` | ok | 157 | 30 | 0 | 30 | 1427 | 15568 | 175 KB |
| `epg_ripper_AL1.xml.gz` | ok | 178 | 28 | 3 | 25 | 1266 | 8725 | 427 KB |
| `epg_ripper_AU1.xml.gz` | ok | 354 | 28 | 3 | 25 | 392 | 51281 | 3612 KB |
| `epg_ripper_DUMMY_CHANNELS.xml.gz` | ok | 165 | 28 | 11 | 17 | 1512 | 14328 | 86 KB |
| `epg_ripper_PH1.xml.gz` | ok | 134 | 28 | 1 | 27 | 0 | 0 | 1 KB |
| `epg_ripper_BA1.xml.gz` | ok | 254 | 27 | 1 | 26 | 2273 | 25922 | 2267 KB |
| `epg_ripper_DK1.xml.gz` | ok | 217 | 27 | 3 | 24 | 1509 | 11707 | 1293 KB |
| `epg_ripper_SG1.xml.gz` | ok | 165 | 27 | 0 | 27 | 1739 | 13805 | 607 KB |
| `epg_ripper_VN1.xml.gz` | ok | 151 | 27 | 13 | 14 | 1595 | 10886 | 221 KB |
| `epg_ripper_AT1.xml.gz` | ok | 144 | 26 | 5 | 21 | 2269 | 15626 | 3698 KB |
| `epg_ripper_DISTROTV1.xml.gz` | ok | 90 | 26 | 2 | 24 | 0 | 212 | 19 KB |
| `epg_ripper_NG1.xml.gz` | ok | 130 | 24 | 0 | 24 | 1155 | 12292 | 143 KB |
| `za.xml` | ok | 161 | 24 | 0 | 24 | 1332 | 13539 | 8754 KB |
| `epg_ripper_FI1.xml.gz` | ok | 110 | 23 | 11 | 12 | 1583 | 8780 | 1068 KB |
| `epg_ripper_SA1.xml.gz` | ok | 97 | 23 | 0 | 23 | 0 | 0 | 1 KB |
| `epg_ripper_ZA1.xml.gz` | ok | 145 | 23 | 5 | 18 | 1461 | 15719 | 185 KB |
| `epg_ripper_MT1.xml.gz` | ok | 192 | 22 | 1 | 21 | 1478 | 16519 | 1271 KB |
| `epg_ripper_MY1.xml.gz` | ok | 163 | 20 | 0 | 20 | 821 | 10568 | 530 KB |
| `epg_ripper_SE1.xml.gz` | ok | 126 | 20 | 0 | 20 | 1434 | 12007 | 1405 KB |
| `epg_ripper_EG1.xml.gz` | ok | 238 | 19 | 2 | 17 | 0 | 1279 | 195 KB |
| `epg_ripper_HK1.xml.gz` | ok | 143 | 19 | 1 | 18 | 1427 | 12003 | 640 KB |
| `epg_ripper_LT1.xml.gz` | ok | 89 | 19 | 8 | 11 | 1213 | 7178 | 903 KB |
| `epg_ripper_LV1.xml.gz` | ok | 105 | 18 | 1 | 17 | 1187 | 12669 | 768 KB |
| `epg_ripper_CY1.xml.gz` | ok | 94 | 17 | 3 | 14 | 1207 | 12194 | 538 KB |
| `epg_ripper_NZ1.xml.gz` | ok | 100 | 16 | 2 | 14 | 928 | 8433 | 451 KB |
| `epg_ripper_BG1.xml.gz` | ok | 86 | 14 | 7 | 7 | 692 | 6501 | 217 KB |
| `epg_ripper_PH2.xml.gz` | ok | 130 | 14 | 1 | 13 | 3 | 391 | 18 KB |
| `epg_ripper_IL1.xml.gz` | ok | 119 | 8 | 4 | 4 | 511 | 10319 | 580 KB |
| `epg_ripper_RAKUTEN1.xml.gz` | ok | 1640 | 8 | 8 | 0 | 431 | 182342 | 9449 KB |
| `epg_ripper_SV1.xml.gz` | ok | 476 | 5 | 0 | 5 | 244 | 44458 | 1036 KB |
| `epg_ripper_BR1.xml.gz` | ok | 266 | 4 | 2 | 2 | 245 | 15430 | 672 KB |
| `epg_ripper_NO1.xml.gz` | ok | 161 | 4 | 0 | 4 | 396 | 14519 | 1230 KB |
| `epg_ripper_ASIANTELEVISION1.xml.gz` | ok | 54 | 3 | 0 | 3 | 251 | 6491 | 107 KB |
| `epg_ripper_DIRECTVSPORTS1.xml.gz` | ok | 4 | 3 | 0 | 3 | 125 | 74 | 3 KB |
| `epg_ripper_TBNPLUS1.xml.gz` | ok | 17 | 3 | 0 | 3 | 0 | 289 | 26 KB |
| `epg_ripper_AR1.xml.gz` | ok | 82 | 2 | 0 | 2 | 148 | 10498 | 250 KB |
| `epg_ripper_CL1.xml.gz` | ok | 90 | 2 | 1 | 1 | 107 | 9439 | 255 KB |
| `epg_ripper_CR1.xml.gz` | ok | 117 | 2 | 0 | 2 | 60 | 11536 | 310 KB |
| `epg_ripper_DELUXEMUSIC1.xml.gz` | ok | 5 | 2 | 2 | 0 | 20 | 42 | 3 KB |
| `epg_ripper_FANDUEL1.xml.gz` | ok | 45 | 2 | 2 | 0 | 26 | 4341 | 137 KB |
| `epg_ripper_MX1.xml.gz` | ok | 178 | 2 | 1 | 1 | 54 | 16083 | 405 KB |
| `guide.xml.gz` | ok | 2 | 1 | 1 | 0 | 46 | 66 | 3 KB |
| `epg_ripper_ALJAZEERA1.xml.gz` | ok | 2 | 1 | 0 | 1 | 0 | 148 | 3 KB |
| `epg_ripper_DRAFTKINGS1.xml.gz` | ok | 1 | 1 | 0 | 1 | 0 | 0 | 0 KB |
| `epg_ripper_EC1.xml.gz` | ok | 90 | 1 | 0 | 1 | 32 | 9948 | 240 KB |
| `epg_ripper_JM1.xml.gz` | ok | 25 | 1 | 0 | 1 | 90 | 2463 | 92 KB |
| `epg_ripper_JP1.xml.gz` | ok | 133 | 1 | 0 | 1 | 43 | 9916 | 1171 KB |
| `epg_ripper_RALLY_TV1.xml.gz` | ok | 1 | 1 | 0 | 1 | 0 | 0 | 0 KB |
| `epg_ripper_BEIN1.xml.gz` | nomatch | 80 | 0 | 0 | 0 | 0 | 3268 | 35 KB |
| `epg_ripper_DO1.xml.gz` | nomatch | 56 | 0 | 0 | 0 | 0 | 4973 | 167 KB |
| `epg_ripper_JP2.xml.gz` | nomatch | 244 | 0 | 0 | 0 | 0 | 0 | 4 KB |
| `epg_ripper_PA1.xml.gz` | nomatch | 106 | 0 | 0 | 0 | 0 | 10726 | 271 KB |
| `epg_ripper_PK1.xml.gz` | nomatch | 8 | 0 | 0 | 0 | 0 | 0 | 0 KB |
| `epg_ripper_SA2.xml.gz` | nomatch | 41 | 0 | 0 | 0 | 0 | 4628 | 103 KB |
| `epg_ripper_SPORTKLUB1.xml.gz` | nomatch | 16 | 0 | 0 | 0 | 0 | 973 | 36 KB |
| `epg_ripper_SSPORTPLUS1.xml.gz` | nomatch | 1 | 0 | 0 | 0 | 0 | 71 | 1 KB |
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
