# Deep link check - archives and category shelf

- **Run:** biweekly deep cleanup: archives, shelf and source copies (`20261115T190956Z-3188`)
- **Started:** 2026-11-15T19:09:56Z  |  **Finished:** 2026-11-15T19:20:25Z  |  **Duration:** 629.1s
- **Mode:** deep (playlist + segment probe)
- **Unique links checked:** 17200 from 68546 playlist entries in 234 playlists

| Result | Links | Share | Meaning |
|---|---:|---:|---|
| working | 57243 | 83.5% | answered with playable media |
| offline | 5810 | 8.5% | confirmed dead - removed when patching |
| unreachable | 2658 | 3.9% | timeout or server error - kept, may recover |
| blocked | 2785 | 4.1% | HTTP 401/403/451 - needs auth or is geo-blocked |
| unsupported | 37 | 0.1% | non-HTTP scheme, cannot be probed |
| invalid | 13 | 0.0% | malformed or non-http URL |

## Per playlist

| Playlist | Entries | Working | Offline | Unreachable | Blocked | Other |
|---|---:|---:|---:|---:|---:|---:|
| `playlists/Priority_Channels.m3u` | 14 | 13 | 1 | 0 | 0 | 0 |
| `playlists/PremiumTV_all.m3u` | 17200 | 12120 | 2661 | 1158 | 1239 | 22 |
| `playlists/categories/A_E_Networks.m3u` | 99 | 98 | 0 | 0 | 1 | 0 |
| `playlists/categories/A_E_Networks_Backups.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/categories/Africa.m3u` | 69 | 68 | 0 | 1 | 0 | 0 |
| `playlists/categories/Animals_Nature.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/categories/Animals_Nature_Backups.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/categories/Aria_Web_Channels.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/categories/Asia.m3u` | 452 | 442 | 3 | 7 | 0 | 0 |
| `playlists/categories/Asia_Backups.m3u` | 24 | 23 | 0 | 1 | 0 | 0 |
| `playlists/categories/Australia.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/categories/Business.m3u` | 45 | 42 | 0 | 2 | 1 | 0 |
| `playlists/categories/Business_Backups.m3u` | 14 | 14 | 0 | 0 | 0 | 0 |
| `playlists/categories/CBS.m3u` | 31 | 31 | 0 | 0 | 0 | 0 |
| `playlists/categories/CBS_Backups.m3u` | 14 | 14 | 0 | 0 | 0 | 0 |
| `playlists/categories/Canada.m3u` | 21 | 21 | 0 | 0 | 0 | 0 |
| `playlists/categories/Cartoons.m3u` | 198 | 193 | 0 | 1 | 4 | 0 |
| `playlists/categories/Cartoons_Backups.m3u` | 29 | 29 | 0 | 0 | 0 | 0 |
| `playlists/categories/Classic_TV.m3u` | 60 | 60 | 0 | 0 | 0 | 0 |
| `playlists/categories/Classic_TV_Backups.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/categories/Comedy.m3u` | 112 | 111 | 0 | 1 | 0 | 0 |
| `playlists/categories/Comedy_Backups.m3u` | 32 | 32 | 0 | 0 | 0 | 0 |
| `playlists/categories/Culture.m3u` | 117 | 115 | 1 | 1 | 0 | 0 |
| `playlists/categories/Culture_Backups.m3u` | 6 | 5 | 1 | 0 | 0 | 0 |
| `playlists/categories/DLTV.m3u` | 9 | 8 | 0 | 1 | 0 | 0 |
| `playlists/categories/Documentary.m3u` | 324 | 317 | 2 | 2 | 3 | 0 |
| `playlists/categories/Documentary_Backups.m3u` | 85 | 84 | 0 | 1 | 0 | 0 |
| `playlists/categories/Education.m3u` | 128 | 126 | 0 | 2 | 0 | 0 |
| `playlists/categories/Education_Backups.m3u` | 14 | 13 | 0 | 1 | 0 | 0 |
| `playlists/categories/Entertainment.m3u` | 677 | 671 | 2 | 4 | 0 | 0 |
| `playlists/categories/Entertainment_Backups.m3u` | 110 | 109 | 0 | 1 | 0 | 0 |
| `playlists/categories/Europe.m3u` | 719 | 696 | 1 | 10 | 12 | 0 |
| `playlists/categories/Europe_Backups.m3u` | 59 | 54 | 0 | 5 | 0 | 0 |
| `playlists/categories/Eurovision_Song_Contest_Asia_On_Aria_November_14Th.m3u` | 7 | 6 | 1 | 0 | 0 | 0 |
| `playlists/categories/Family.m3u` | 29 | 28 | 1 | 0 | 0 | 0 |
| `playlists/categories/Family_Backups.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/categories/Fox_Channels.m3u` | 29 | 29 | 0 | 0 | 0 | 0 |
| `playlists/categories/Game_Shows.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/categories/Game_Shows_Backups.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/categories/Global_TV.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/categories/Global_TV_Backups.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/categories/India.m3u` | 70 | 70 | 0 | 0 | 0 | 0 |
| `playlists/categories/India_Backups.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/categories/International.m3u` | 670 | 637 | 9 | 19 | 5 | 0 |
| `playlists/categories/International_Backups.m3u` | 97 | 94 | 1 | 2 | 0 | 0 |
| `playlists/categories/Kids.m3u` | 302 | 293 | 0 | 4 | 5 | 0 |
| `playlists/categories/Kids_Backups.m3u` | 76 | 76 | 0 | 0 | 0 | 0 |
| `playlists/categories/Legislative.m3u` | 114 | 110 | 1 | 3 | 0 | 0 |
| `playlists/categories/Lifestyle.m3u` | 460 | 457 | 0 | 3 | 0 | 0 |
| `playlists/categories/Lifestyle_Backups.m3u` | 121 | 121 | 0 | 0 | 0 | 0 |
| `playlists/categories/Movies.m3u` | 827 | 813 | 0 | 10 | 4 | 0 |
| `playlists/categories/Movies_Backups.m3u` | 133 | 132 | 0 | 0 | 1 | 0 |
| `playlists/categories/Music.m3u` | 831 | 824 | 5 | 2 | 0 | 0 |
| `playlists/categories/Music_Backups.m3u` | 114 | 114 | 0 | 0 | 0 | 0 |
| `playlists/categories/NBC.m3u` | 67 | 67 | 0 | 0 | 0 | 0 |
| `playlists/categories/NBC_Backups.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/categories/NBC_Sports_Channels.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/categories/News.m3u` | 845 | 819 | 3 | 7 | 16 | 0 |
| `playlists/categories/News_Backups.m3u` | 204 | 203 | 0 | 0 | 1 | 0 |
| `playlists/categories/North_America.m3u` | 279 | 270 | 3 | 5 | 1 | 0 |
| `playlists/categories/North_America_Backups.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/categories/Oceania.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/categories/Online_TV.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/categories/Online_TV_Backups.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/categories/Other.m3u` | 252 | 251 | 0 | 1 | 0 | 0 |
| `playlists/categories/Other_Backups.m3u` | 138 | 138 | 0 | 0 | 0 | 0 |
| `playlists/categories/PBS.m3u` | 40 | 39 | 1 | 0 | 0 | 0 |
| `playlists/categories/PBS_Backups.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/categories/Religious.m3u` | 573 | 568 | 0 | 2 | 3 | 0 |
| `playlists/categories/Religious_Backups.m3u` | 36 | 36 | 0 | 0 | 0 | 0 |
| `playlists/categories/Series.m3u` | 320 | 319 | 0 | 0 | 1 | 0 |
| `playlists/categories/Series_Backups.m3u` | 129 | 129 | 0 | 0 | 0 | 0 |
| `playlists/categories/South_America.m3u` | 452 | 441 | 3 | 3 | 5 | 0 |
| `playlists/categories/South_America_Backups.m3u` | 18 | 18 | 0 | 0 | 0 | 0 |
| `playlists/categories/Sports.m3u` | 559 | 511 | 15 | 12 | 21 | 0 |
| `playlists/categories/Sports_Backups.m3u` | 125 | 125 | 0 | 0 | 0 | 0 |
| `playlists/categories/Tv_Celebrities.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/categories/Tv_Paranormal.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/categories/Tv_Paranormal_Backups.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/categories/Tv_Shows.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/categories/UK.m3u` | 26 | 26 | 0 | 0 | 0 | 0 |
| `playlists/categories/UK_Backups.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/categories/United_States.m3u` | 342 | 335 | 2 | 3 | 2 | 0 |
| `playlists/categories/United_States_Backups.m3u` | 73 | 73 | 0 | 0 | 0 | 0 |
| `playlists/categories/Weather.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/categories/Weather_Backups.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/sources/VIP-m3u-playlist.m3u` | 202 | 190 | 10 | 0 | 2 | 0 |
| `playlists/sources/ae-networks.m3u` | 53 | 47 | 3 | 3 | 0 | 0 |
| `playlists/sources/aria.m3u` | 249 | 177 | 21 | 1 | 50 | 0 |
| `playlists/sources/doms9.m3u` | 587 | 209 | 122 | 19 | 237 | 0 |
| `playlists/sources/free-tv.m3u` | 2203 | 1298 | 540 | 152 | 203 | 10 |
| `playlists/sources/iptv-org.m3u` | 11502 | 8344 | 1591 | 853 | 699 | 15 |
| `playlists/sources/israel-tv-plus.m3u` | 307 | 119 | 95 | 0 | 93 | 0 |
| `playlists/sources/local-channels.m3u` | 4 | 2 | 2 | 0 | 0 | 0 |
| `playlists/sources/m3u.m3u` | 842 | 674 | 127 | 18 | 21 | 2 |
| `playlists/sources/openstream.m3u` | 5428 | 5002 | 369 | 44 | 13 | 0 |
| `playlists/sources/priority-channels.m3u` | 14 | 13 | 1 | 0 | 0 | 0 |
| `playlists/sources/xtemus.m3u` | 317 | 29 | 127 | 142 | 18 | 1 |
| `categories/USA.m3u` | 2827 | 2776 | 15 | 17 | 19 | 0 |
| `categories/All/A_E_Networks.m3u` | 99 | 98 | 0 | 0 | 1 | 0 |
| `categories/All/A_E_Networks_Backups.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `categories/All/Africa.m3u` | 69 | 68 | 0 | 1 | 0 | 0 |
| `categories/All/Animals_Nature.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `categories/All/Animals_Nature_Backups.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `categories/All/Aria_Web_Channels.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `categories/All/Asia.m3u` | 452 | 442 | 3 | 7 | 0 | 0 |
| `categories/All/Asia_Backups.m3u` | 24 | 23 | 0 | 1 | 0 | 0 |
| `categories/All/Australia.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `categories/All/Business.m3u` | 45 | 42 | 0 | 2 | 1 | 0 |
| `categories/All/Business_Backups.m3u` | 14 | 14 | 0 | 0 | 0 | 0 |
| `categories/All/CBS.m3u` | 31 | 31 | 0 | 0 | 0 | 0 |
| `categories/All/CBS_Backups.m3u` | 14 | 14 | 0 | 0 | 0 | 0 |
| `categories/All/Canada.m3u` | 21 | 21 | 0 | 0 | 0 | 0 |
| `categories/All/Cartoons.m3u` | 198 | 193 | 0 | 1 | 4 | 0 |
| `categories/All/Cartoons_Backups.m3u` | 29 | 29 | 0 | 0 | 0 | 0 |
| `categories/All/Classic_TV.m3u` | 60 | 60 | 0 | 0 | 0 | 0 |
| `categories/All/Classic_TV_Backups.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `categories/All/Comedy.m3u` | 112 | 111 | 0 | 1 | 0 | 0 |
| `categories/All/Comedy_Backups.m3u` | 32 | 32 | 0 | 0 | 0 | 0 |
| `categories/All/Culture.m3u` | 117 | 115 | 1 | 1 | 0 | 0 |
| `categories/All/Culture_Backups.m3u` | 6 | 5 | 1 | 0 | 0 | 0 |
| `categories/All/DLTV.m3u` | 9 | 8 | 0 | 1 | 0 | 0 |
| `categories/All/Documentary.m3u` | 324 | 317 | 2 | 2 | 3 | 0 |
| `categories/All/Documentary_Backups.m3u` | 85 | 84 | 0 | 1 | 0 | 0 |
| `categories/All/Education.m3u` | 128 | 126 | 0 | 2 | 0 | 0 |
| `categories/All/Education_Backups.m3u` | 14 | 13 | 0 | 1 | 0 | 0 |
| `categories/All/Entertainment.m3u` | 677 | 671 | 2 | 4 | 0 | 0 |
| `categories/All/Entertainment_Backups.m3u` | 110 | 109 | 0 | 1 | 0 | 0 |
| `categories/All/Europe.m3u` | 719 | 696 | 1 | 10 | 12 | 0 |
| `categories/All/Europe_Backups.m3u` | 59 | 54 | 0 | 5 | 0 | 0 |
| `categories/All/Eurovision_Song_Contest_Asia_On_Aria_November_14Th.m3u` | 7 | 6 | 1 | 0 | 0 | 0 |
| `categories/All/Family.m3u` | 29 | 28 | 1 | 0 | 0 | 0 |
| `categories/All/Family_Backups.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `categories/All/Fox_Channels.m3u` | 29 | 29 | 0 | 0 | 0 | 0 |
| `categories/All/Game_Shows.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `categories/All/Game_Shows_Backups.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `categories/All/Global_TV.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `categories/All/Global_TV_Backups.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `categories/All/India.m3u` | 70 | 70 | 0 | 0 | 0 | 0 |
| `categories/All/India_Backups.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `categories/All/International.m3u` | 670 | 637 | 9 | 19 | 5 | 0 |
| `categories/All/International_Backups.m3u` | 97 | 94 | 1 | 2 | 0 | 0 |
| `categories/All/Kids.m3u` | 302 | 293 | 0 | 4 | 5 | 0 |
| `categories/All/Kids_Backups.m3u` | 76 | 76 | 0 | 0 | 0 | 0 |
| `categories/All/Legislative.m3u` | 114 | 110 | 1 | 3 | 0 | 0 |
| `categories/All/Lifestyle.m3u` | 460 | 457 | 0 | 3 | 0 | 0 |
| `categories/All/Lifestyle_Backups.m3u` | 121 | 121 | 0 | 0 | 0 | 0 |
| `categories/All/Movies.m3u` | 827 | 813 | 0 | 10 | 4 | 0 |
| `categories/All/Movies_Backups.m3u` | 133 | 132 | 0 | 0 | 1 | 0 |
| `categories/All/Music.m3u` | 831 | 824 | 5 | 2 | 0 | 0 |
| `categories/All/Music_Backups.m3u` | 114 | 114 | 0 | 0 | 0 | 0 |
| `categories/All/NBC.m3u` | 67 | 67 | 0 | 0 | 0 | 0 |
| `categories/All/NBC_Backups.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `categories/All/NBC_Sports_Channels.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `categories/All/News.m3u` | 845 | 819 | 3 | 7 | 16 | 0 |
| `categories/All/News_Backups.m3u` | 204 | 203 | 0 | 0 | 1 | 0 |
| `categories/All/North_America.m3u` | 279 | 270 | 3 | 5 | 1 | 0 |
| `categories/All/North_America_Backups.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `categories/All/Oceania.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `categories/All/Online_TV.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `categories/All/Online_TV_Backups.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `categories/All/Other.m3u` | 252 | 251 | 0 | 1 | 0 | 0 |
| `categories/All/Other_Backups.m3u` | 138 | 138 | 0 | 0 | 0 | 0 |
| `categories/All/PBS.m3u` | 40 | 39 | 1 | 0 | 0 | 0 |
| `categories/All/PBS_Backups.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `categories/All/Religious.m3u` | 573 | 568 | 0 | 2 | 3 | 0 |
| `categories/All/Religious_Backups.m3u` | 36 | 36 | 0 | 0 | 0 | 0 |
| `categories/All/Series.m3u` | 320 | 319 | 0 | 0 | 1 | 0 |
| `categories/All/Series_Backups.m3u` | 129 | 129 | 0 | 0 | 0 | 0 |
| `categories/All/South_America.m3u` | 452 | 441 | 3 | 3 | 5 | 0 |
| `categories/All/South_America_Backups.m3u` | 18 | 18 | 0 | 0 | 0 | 0 |
| `categories/All/Sports.m3u` | 559 | 511 | 15 | 12 | 21 | 0 |
| `categories/All/Sports_Backups.m3u` | 125 | 125 | 0 | 0 | 0 | 0 |
| `categories/All/Tv_Celebrities.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `categories/All/Tv_Paranormal.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `categories/All/Tv_Paranormal_Backups.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `categories/All/Tv_Shows.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `categories/All/UK.m3u` | 26 | 26 | 0 | 0 | 0 | 0 |
| `categories/All/UK_Backups.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `categories/All/United_States.m3u` | 342 | 335 | 2 | 3 | 2 | 0 |
| `categories/All/United_States_Backups.m3u` | 73 | 73 | 0 | 0 | 0 | 0 |
| `categories/All/Weather.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `categories/All/Weather_Backups.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `categories/USA/A_E_Networks.m3u` | 59 | 58 | 0 | 0 | 1 | 0 |
| `categories/USA/A_E_Networks_Backups.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `categories/USA/Business.m3u` | 17 | 16 | 0 | 1 | 0 | 0 |
| `categories/USA/Business_Backups.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `categories/USA/CBS.m3u` | 27 | 27 | 0 | 0 | 0 | 0 |
| `categories/USA/CBS_Backups.m3u` | 14 | 14 | 0 | 0 | 0 | 0 |
| `categories/USA/Cartoons.m3u` | 71 | 69 | 0 | 0 | 2 | 0 |
| `categories/USA/Cartoons_Backups.m3u` | 24 | 24 | 0 | 0 | 0 | 0 |
| `categories/USA/Classic_TV.m3u` | 17 | 17 | 0 | 0 | 0 | 0 |
| `categories/USA/Classic_TV_Backups.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `categories/USA/Comedy.m3u` | 32 | 31 | 0 | 1 | 0 | 0 |
| `categories/USA/Comedy_Backups.m3u` | 21 | 21 | 0 | 0 | 0 | 0 |
| `categories/USA/Culture.m3u` | 18 | 18 | 0 | 0 | 0 | 0 |
| `categories/USA/Documentary.m3u` | 92 | 87 | 0 | 2 | 3 | 0 |
| `categories/USA/Documentary_Backups.m3u` | 45 | 45 | 0 | 0 | 0 | 0 |
| `categories/USA/Education.m3u` | 40 | 39 | 0 | 1 | 0 | 0 |
| `categories/USA/Education_Backups.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `categories/USA/Entertainment.m3u` | 120 | 120 | 0 | 0 | 0 | 0 |
| `categories/USA/Entertainment_Backups.m3u` | 54 | 54 | 0 | 0 | 0 | 0 |
| `categories/USA/Family.m3u` | 13 | 13 | 0 | 0 | 0 | 0 |
| `categories/USA/Family_Backups.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `categories/USA/Fox_Channels.m3u` | 25 | 25 | 0 | 0 | 0 | 0 |
| `categories/USA/Game_Shows.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `categories/USA/Game_Shows_Backups.m3u` | 15 | 15 | 0 | 0 | 0 | 0 |
| `categories/USA/International.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `categories/USA/Kids.m3u` | 82 | 79 | 0 | 1 | 2 | 0 |
| `categories/USA/Kids_Backups.m3u` | 44 | 44 | 0 | 0 | 0 | 0 |
| `categories/USA/Legislative.m3u` | 79 | 76 | 0 | 3 | 0 | 0 |
| `categories/USA/Lifestyle.m3u` | 140 | 139 | 0 | 1 | 0 | 0 |
| `categories/USA/Lifestyle_Backups.m3u` | 75 | 75 | 0 | 0 | 0 | 0 |
| `categories/USA/Movies.m3u` | 218 | 217 | 0 | 1 | 0 | 0 |
| `categories/USA/Movies_Backups.m3u` | 105 | 105 | 0 | 0 | 0 | 0 |
| `categories/USA/Music.m3u` | 94 | 94 | 0 | 0 | 0 | 0 |
| `categories/USA/Music_Backups.m3u` | 35 | 35 | 0 | 0 | 0 | 0 |
| `categories/USA/NBC.m3u` | 40 | 40 | 0 | 0 | 0 | 0 |
| `categories/USA/NBC_Backups.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `categories/USA/NBC_Sports_Channels.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `categories/USA/News.m3u` | 60 | 59 | 0 | 0 | 1 | 0 |
| `categories/USA/News_Backups.m3u` | 25 | 25 | 0 | 0 | 0 | 0 |
| `categories/USA/Other.m3u` | 17 | 17 | 0 | 0 | 0 | 0 |
| `categories/USA/PBS.m3u` | 21 | 21 | 0 | 0 | 0 | 0 |
| `categories/USA/Religious.m3u` | 102 | 101 | 0 | 1 | 0 | 0 |
| `categories/USA/Religious_Backups.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `categories/USA/Series.m3u` | 161 | 161 | 0 | 0 | 0 | 0 |
| `categories/USA/Series_Backups.m3u` | 107 | 107 | 0 | 0 | 0 | 0 |
| `categories/USA/Sports.m3u` | 140 | 117 | 13 | 2 | 8 | 0 |
| `categories/USA/Sports_Backups.m3u` | 69 | 69 | 0 | 0 | 0 | 0 |
| `categories/USA/United_States.m3u` | 342 | 335 | 2 | 3 | 2 | 0 |
| `categories/USA/United_States_Backups.m3u` | 73 | 73 | 0 | 0 | 0 | 0 |
| `categories/USA/Weather.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `categories/USA/Weather_Backups.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |

## Patches applied

- Removed **3158** confirmed-dead links across **52** playlists (working ratio 83.6%).
  - `Priority_Channels.m3u`: -1 (14 -> 13)
  - `Asia.m3u`: -3 (452 -> 449)
  - `Culture.m3u`: -1 (117 -> 116)
  - `Culture_Backups.m3u`: -1 (6 -> 5)
  - `Documentary.m3u`: -2 (324 -> 322)
  - `Entertainment.m3u`: -2 (677 -> 675)
  - `Europe.m3u`: -1 (719 -> 718)
  - `Eurovision_Song_Contest_Asia_On_Aria_November_14Th.m3u`: -1 (7 -> 6)
  - `Family.m3u`: -1 (29 -> 28)
  - `International.m3u`: -9 (670 -> 661)
  - `International_Backups.m3u`: -1 (97 -> 96)
  - `Legislative.m3u`: -1 (114 -> 113)
  - `Music.m3u`: -5 (831 -> 826)
  - `News.m3u`: -3 (845 -> 842)
  - `North_America.m3u`: -3 (279 -> 276)
  - `PBS.m3u`: -1 (40 -> 39)
  - `South_America.m3u`: -3 (452 -> 449)
  - `Sports.m3u`: -15 (559 -> 544)
  - `United_States.m3u`: -2 (342 -> 340)
  - `VIP-m3u-playlist.m3u`: -10 (202 -> 192)
  - `ae-networks.m3u`: -3 (53 -> 50)
  - `aria.m3u`: -21 (249 -> 228)
  - `doms9.m3u`: -122 (587 -> 465)
  - `free-tv.m3u`: -546 (2203 -> 1657)
  - `iptv-org.m3u`: -1591 (11502 -> 9911)
  - `israel-tv-plus.m3u`: -95 (307 -> 212)
  - `local-channels.m3u`: -2 (4 -> 2)
  - `m3u.m3u`: -129 (842 -> 713)
  - `openstream.m3u`: -369 (5428 -> 5059)
  - `priority-channels.m3u`: -1 (14 -> 13)
  - `xtemus.m3u`: -128 (317 -> 189)
  - `USA.m3u`: -15 (2827 -> 2812)
  - `Asia.m3u`: -3 (452 -> 449)
  - `Culture.m3u`: -1 (117 -> 116)
  - `Culture_Backups.m3u`: -1 (6 -> 5)
  - `Documentary.m3u`: -2 (324 -> 322)
  - `Entertainment.m3u`: -2 (677 -> 675)
  - `Europe.m3u`: -1 (719 -> 718)
  - `Eurovision_Song_Contest_Asia_On_Aria_November_14Th.m3u`: -1 (7 -> 6)
  - `Family.m3u`: -1 (29 -> 28)
  - `International.m3u`: -9 (670 -> 661)
  - `International_Backups.m3u`: -1 (97 -> 96)
  - `Legislative.m3u`: -1 (114 -> 113)
  - `Music.m3u`: -5 (831 -> 826)
  - `News.m3u`: -3 (845 -> 842)
  - `North_America.m3u`: -3 (279 -> 276)
  - `PBS.m3u`: -1 (40 -> 39)
  - `South_America.m3u`: -3 (452 -> 449)
  - `Sports.m3u`: -15 (559 -> 544)
  - `United_States.m3u`: -2 (342 -> 340)
  - `Sports.m3u`: -13 (140 -> 127)
  - `United_States.m3u`: -2 (342 -> 340)
  - reported only `PremiumTV_all.m3u`: 2665 of 17200 links are dead; the file keeps every one of them by design

## Hosts with the most failing links

| Host | Offline | Unreachable |
|---|---:|---:|
| `playlist.xtemus.com` | 250 | 42 |
| `www.youtube.com` | 231 | 26 |
| `youtu.be` | 0 | 246 |
| `b84203c4.ottrast.com` | 175 | 0 |
| `jmp2.uk` | 135 | 0 |
| `live20.bozztv.com` | 99 | 0 |
| `31.148.48.15` | 0 | 96 |
| `ncdn.telewebion.ir` | 64 | 0 |
| `103.250.28.74:8000` | 0 | 62 |
| `goliveafrica.media:9998` | 61 | 0 |
| `168.196.127.137:6001` | 0 | 56 |
| `candyshop.st` | 56 | 0 |
| `vgtrkregion-reg.cdnvideo.ru` | 56 | 0 |
| `live.streamingfast.net` | 54 | 0 |
| `lb.iptvnetwork.net` | 48 | 0 |
| `193.47.62.41` | 44 | 0 |
| `edge2.candyshop.st` | 42 | 0 |
| `stream.oursnetworktv.com` | 42 | 0 |
| `edge.candyshop.st` | 38 | 0 |
| `64b16f23efbee.streamlock.net` | 2 | 35 |
| `mixedshop.pw` | 0 | 36 |
| `lbgo.bozztv.com` | 0 | 36 |
| `37.49.224.5` | 36 | 0 |
| `mumbai-edge.smartplaytv.in` | 36 | 0 |
| `dtv.vol.net.ua` | 34 | 0 |

## Sample of confirmed-dead links

| Channel | Reason | URL |
|---|---|---|
| [NFL] NFL Network (iSTRMEAST) | HTTP 404 | `https://chatgpt.hereisman.net/playlist/54923/load-playlist` |
| ספורט 1 HD (Sport 1) | HTTP 404 | `http://b84203c4.ottrast.com/iptv/QAP2YS2594ZQS3/12249/index.m3u8` |
| ספורט 2 HD (Sport 2) | HTTP 404 | `http://b84203c4.ottrast.com/iptv/QAP2YS2594ZQS3/12250/index.m3u8` |
| ספורט 3 HD (Sport 3) | HTTP 404 | `http://b84203c4.ottrast.com/iptv/QAP2YS2594ZQS3/12251/index.m3u8` |
| ספורט 4 FHD (Sport 4) | HTTP 404 | `http://b84203c4.ottrast.com/iptv/QAP2YS2594ZQS3/12252/index.m3u8` |
| ספורט 6 HD (Sport 6) | HTTP 404 | `http://b84203c4.ottrast.com/iptv/QAP2YS2594ZQS3/32003/index.m3u8` |
| Garuda TV (1080p) | playlist only, HTTP 404 | `https://hgmtv.com:19360/garudatvlivestreaming/garudatvlivestreaming.m3u8` |
| VTV5 Tay Nam Bo HD (1080p) | HTTP 404 | `https://dethich.pw/vtv5tnb/index.m3u8` |
| VTV8 HD (720p) | HTTP 404 | `https://dethich.pw/vtv8/index.m3u8` |
| El 33 Originals (1080p) [Not 24/7] | playlist only, HTTP 403 | `https://directes-tv-int.3catdirectes.cat/live-content/c33-super3-hls/master.m3u8` |
| El 33 Originals (1080p) [Not 24/7] | playlist only, HTTP 403 | `https://directes-tv-int.3catdirectes.cat/live-origin/c33-super3-hls/master.m3u8` |
| Asharq Documentary (1080p) | playlist only, HTTP 404 | `https://svs.itworkscdn.net/asharqdocumentarylive/asharqdocumentary.smil/playlist_dvr.m3u8` |
| ☆ Discovery 🇮🇹 | playlist only, HTTP 403 | `https://jmp2.uk/stvp-IT31000026G` |
| Fortune TV (720p) | variant HTTP 404 | `http://103.215.194.93:8282/hls/fortunetv/vmix.m3u8` |
| Nexus TV (576p) | HTTP 404 | `https://tvsen6.aynaott.com/Epm7WrFa/index.m3u8` |
| BTB 3 (1080p) | playlist lists no segments | `https://emisja3.btb.j00r.us/iptv/session/3/live.m3u8` |
| VTV3 (Vietnam) | HTTP 404 | `https://dethich.pw/vtv3/index.m3u8` |
| HTVC Family (720p) | HTTP 404 | `https://dethich.pw/htvcgiadinh/index.m3u8` |
| M2 / Petőfi TV Ⓖ | HTTP 404 | `http://141.94.193.53:80/M2_HD/index.m3u8` |
| Nuova Tv 2 | HTTP 404 | `https://nuovatv.net:8443/tv2/stream.m3u8` |
| RTP Africa (504p) [Not 24/7] | empty response | `https://streaming-live.rtp.pt/liverepeater/smil:rtpafrica.smil/playlist.m3u8` |
| Tele Acras | variant HTTP 404 | `https://5db313b643fd8.streamlock.net/teleacras/teleacras/playlist.m3u8` |
| TOKYO MX チャンネル | variant HTTP 400 | `https://cdn-uw2-prod.tsv2.amagi.tv/linear/amg01287-rakutentvjapan-tokyomx-cmaf-rakutenjp/playlist.m3u8` |
| Prima MAX | HTTP 404 | `https://sktv.mxnticek.eu/new/stream.php?ch=PrimaMax` |
| Hellenic Parliament TV (1080p) | HTTP 404 | `https://ert-ucdn.broadpeak-aas.com/bpk-tv/VOULITV/default/index.m3u8` |
