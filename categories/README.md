# Category shelf

- **Shelf rebuilt:** 2026-10-24 00:05 UTC (2026-10-23 08:05 PM EDT) — _scheduled guide build_
- **Sources:** [`playlists/PremiumTV.m3u`](../playlists/PremiumTV.m3u) for `All/`, [`playlists/live/USA.m3u`](../playlists/live/USA.m3u) for `USA.m3u` and `USA/`
- **Order:** Sports -> Lifestyle -> Fox Channels -> CBS -> NBC -> NBC Sports Channels -> Cartoons -> PBS -> Game Shows (each followed by its own Backups group), then the long tail by size, `Other` last — the published order from `scripts/categorize.py`.
- **One entry per channel:** a channel's spare feeds sit right after it in its `<category> Backups` group, best quality first.

Every file here is a slice of an already published playlist: same channels, same order, same group labels, same guide header. Nothing is re-classified, so loading the shelf can never show a channel the playlist does not have.

## USA

[`USA.m3u`](USA.m3u) — every one of the **2998** working US channels in one file, in category order. The per-category files below are the same list cut up.

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 212 | [`Sports.m3u`](USA/Sports.m3u) |
| 2 | Sports Backups | 54 | [`Sports_Backups.m3u`](USA/Sports_Backups.m3u) |
| 3 | Lifestyle | 161 | [`Lifestyle.m3u`](USA/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 57 | [`Lifestyle_Backups.m3u`](USA/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 28 | [`Fox_Channels.m3u`](USA/Fox_Channels.m3u) |
| 6 | CBS | 30 | [`CBS.m3u`](USA/CBS.m3u) |
| 7 | CBS Backups | 23 | [`CBS_Backups.m3u`](USA/CBS_Backups.m3u) |
| 8 | NBC | 46 | [`NBC.m3u`](USA/NBC.m3u) |
| 9 | NBC Backups | 6 | [`NBC_Backups.m3u`](USA/NBC_Backups.m3u) |
| 10 | NBC Sports Channels | 5 | [`NBC_Sports_Channels.m3u`](USA/NBC_Sports_Channels.m3u) |
| 11 | Cartoons | 79 | [`Cartoons.m3u`](USA/Cartoons.m3u) |
| 12 | Cartoons Backups | 15 | [`Cartoons_Backups.m3u`](USA/Cartoons_Backups.m3u) |
| 13 | PBS | 21 | [`PBS.m3u`](USA/PBS.m3u) |
| 14 | Game Shows | 10 | [`Game_Shows.m3u`](USA/Game_Shows.m3u) |
| 15 | Game Shows Backups | 14 | [`Game_Shows_Backups.m3u`](USA/Game_Shows_Backups.m3u) |
| 16 | United States | 370 | [`United_States.m3u`](USA/United_States.m3u) |
| 17 | United States Backups | 61 | [`United_States_Backups.m3u`](USA/United_States_Backups.m3u) |
| 18 | Movies | 254 | [`Movies.m3u`](USA/Movies.m3u) |
| 19 | Movies Backups | 85 | [`Movies_Backups.m3u`](USA/Movies_Backups.m3u) |
| 20 | Series | 164 | [`Series.m3u`](USA/Series.m3u) |
| 21 | Series Backups | 87 | [`Series_Backups.m3u`](USA/Series_Backups.m3u) |
| 22 | Entertainment | 145 | [`Entertainment.m3u`](USA/Entertainment.m3u) |
| 23 | Entertainment Backups | 43 | [`Entertainment_Backups.m3u`](USA/Entertainment_Backups.m3u) |
| 24 | Religious | 124 | [`Religious.m3u`](USA/Religious.m3u) |
| 25 | Religious Backups | 13 | [`Religious_Backups.m3u`](USA/Religious_Backups.m3u) |
| 26 | Documentary | 121 | [`Documentary.m3u`](USA/Documentary.m3u) |
| 27 | Documentary Backups | 39 | [`Documentary_Backups.m3u`](USA/Documentary_Backups.m3u) |
| 28 | Music | 103 | [`Music.m3u`](USA/Music.m3u) |
| 29 | Music Backups | 25 | [`Music_Backups.m3u`](USA/Music_Backups.m3u) |
| 30 | Kids | 92 | [`Kids.m3u`](USA/Kids.m3u) |
| 31 | Kids Backups | 36 | [`Kids_Backups.m3u`](USA/Kids_Backups.m3u) |
| 32 | Legislative | 83 | [`Legislative.m3u`](USA/Legislative.m3u) |
| 33 | News | 80 | [`News.m3u`](USA/News.m3u) |
| 34 | News Backups | 32 | [`News_Backups.m3u`](USA/News_Backups.m3u) |
| 35 | Education | 45 | [`Education.m3u`](USA/Education.m3u) |
| 36 | Education Backups | 3 | [`Education_Backups.m3u`](USA/Education_Backups.m3u) |
| 37 | Comedy | 37 | [`Comedy.m3u`](USA/Comedy.m3u) |
| 38 | Comedy Backups | 20 | [`Comedy_Backups.m3u`](USA/Comedy_Backups.m3u) |
| 39 | Classic TV | 25 | [`Classic_TV.m3u`](USA/Classic_TV.m3u) |
| 40 | Classic TV Backups | 5 | [`Classic_TV_Backups.m3u`](USA/Classic_TV_Backups.m3u) |
| 41 | A&E Networks | 24 | [`A_E_Networks.m3u`](USA/A_E_Networks.m3u) |
| 42 | Culture | 23 | [`Culture.m3u`](USA/Culture.m3u) |
| 43 | Business | 17 | [`Business.m3u`](USA/Business.m3u) |
| 44 | Business Backups | 10 | [`Business_Backups.m3u`](USA/Business_Backups.m3u) |
| 45 | Family | 15 | [`Family.m3u`](USA/Family.m3u) |
| 46 | Weather | 6 | [`Weather.m3u`](USA/Weather.m3u) |
| 47 | Weather Backups | 3 | [`Weather_Backups.m3u`](USA/Weather_Backups.m3u) |
| 48 | International | 5 | [`International.m3u`](USA/International.m3u) |
| 49 | Animals & Nature | 4 | [`Animals_Nature.m3u`](USA/Animals_Nature.m3u) |
| 50 | Other | 19 | [`Other.m3u`](USA/Other.m3u) |

Groups smaller than 3 channels keep no file of their own (they would be a one-link playlist) - they stay in `USA.m3u`, which always holds every US channel.

## All countries

One file per category for the whole library (US channels first inside a category, because that is the published order).

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 656 | [`Sports.m3u`](All/Sports.m3u) |
| 2 | Sports Backups | 98 | [`Sports_Backups.m3u`](All/Sports_Backups.m3u) |
| 3 | Lifestyle | 534 | [`Lifestyle.m3u`](All/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 94 | [`Lifestyle_Backups.m3u`](All/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 31 | [`Fox_Channels.m3u`](All/Fox_Channels.m3u) |
| 6 | CBS | 33 | [`CBS.m3u`](All/CBS.m3u) |
| 7 | CBS Backups | 24 | [`CBS_Backups.m3u`](All/CBS_Backups.m3u) |
| 8 | NBC | 75 | [`NBC.m3u`](All/NBC.m3u) |
| 9 | NBC Backups | 10 | [`NBC_Backups.m3u`](All/NBC_Backups.m3u) |
| 10 | NBC Sports Channels | 9 | [`NBC_Sports_Channels.m3u`](All/NBC_Sports_Channels.m3u) |
| 11 | Cartoons | 210 | [`Cartoons.m3u`](All/Cartoons.m3u) |
| 12 | Cartoons Backups | 20 | [`Cartoons_Backups.m3u`](All/Cartoons_Backups.m3u) |
| 13 | PBS | 36 | [`PBS.m3u`](All/PBS.m3u) |
| 14 | PBS Backups | 7 | [`PBS_Backups.m3u`](All/PBS_Backups.m3u) |
| 15 | Game Shows | 12 | [`Game_Shows.m3u`](All/Game_Shows.m3u) |
| 16 | Game Shows Backups | 15 | [`Game_Shows_Backups.m3u`](All/Game_Shows_Backups.m3u) |
| 17 | News | 967 | [`News.m3u`](All/News.m3u) |
| 18 | News Backups | 190 | [`News_Backups.m3u`](All/News_Backups.m3u) |
| 19 | Music | 962 | [`Music.m3u`](All/Music.m3u) |
| 20 | Music Backups | 88 | [`Music_Backups.m3u`](All/Music_Backups.m3u) |
| 21 | Movies | 932 | [`Movies.m3u`](All/Movies.m3u) |
| 22 | Movies Backups | 102 | [`Movies_Backups.m3u`](All/Movies_Backups.m3u) |
| 23 | Europe | 882 | [`Europe.m3u`](All/Europe.m3u) |
| 24 | Europe Backups | 69 | [`Europe_Backups.m3u`](All/Europe_Backups.m3u) |
| 25 | International | 819 | [`International.m3u`](All/International.m3u) |
| 26 | International Backups | 118 | [`International_Backups.m3u`](All/International_Backups.m3u) |
| 27 | Entertainment | 745 | [`Entertainment.m3u`](All/Entertainment.m3u) |
| 28 | Entertainment Backups | 81 | [`Entertainment_Backups.m3u`](All/Entertainment_Backups.m3u) |
| 29 | Religious | 633 | [`Religious.m3u`](All/Religious.m3u) |
| 30 | Religious Backups | 39 | [`Religious_Backups.m3u`](All/Religious_Backups.m3u) |
| 31 | Asia | 624 | [`Asia.m3u`](All/Asia.m3u) |
| 32 | Asia Backups | 31 | [`Asia_Backups.m3u`](All/Asia_Backups.m3u) |
| 33 | South America | 552 | [`South_America.m3u`](All/South_America.m3u) |
| 34 | South America Backups | 23 | [`South_America_Backups.m3u`](All/South_America_Backups.m3u) |
| 35 | Documentary | 393 | [`Documentary.m3u`](All/Documentary.m3u) |
| 36 | Documentary Backups | 74 | [`Documentary_Backups.m3u`](All/Documentary_Backups.m3u) |
| 37 | United States | 387 | [`United_States.m3u`](All/United_States.m3u) |
| 38 | United States Backups | 61 | [`United_States_Backups.m3u`](All/United_States_Backups.m3u) |
| 39 | Series | 343 | [`Series.m3u`](All/Series.m3u) |
| 40 | Series Backups | 104 | [`Series_Backups.m3u`](All/Series_Backups.m3u) |
| 41 | Kids | 342 | [`Kids.m3u`](All/Kids.m3u) |
| 42 | Kids Backups | 59 | [`Kids_Backups.m3u`](All/Kids_Backups.m3u) |
| 43 | North America | 334 | [`North_America.m3u`](All/North_America.m3u) |
| 44 | North America Backups | 5 | [`North_America_Backups.m3u`](All/North_America_Backups.m3u) |
| 45 | Education | 160 | [`Education.m3u`](All/Education.m3u) |
| 46 | Education Backups | 13 | [`Education_Backups.m3u`](All/Education_Backups.m3u) |
| 47 | Legislative | 147 | [`Legislative.m3u`](All/Legislative.m3u) |
| 48 | Legislative Backups | 3 | [`Legislative_Backups.m3u`](All/Legislative_Backups.m3u) |
| 49 | Culture | 144 | [`Culture.m3u`](All/Culture.m3u) |
| 50 | Culture Backups | 11 | [`Culture_Backups.m3u`](All/Culture_Backups.m3u) |
| 51 | Comedy | 126 | [`Comedy.m3u`](All/Comedy.m3u) |
| 52 | Comedy Backups | 27 | [`Comedy_Backups.m3u`](All/Comedy_Backups.m3u) |
| 53 | Africa | 99 | [`Africa.m3u`](All/Africa.m3u) |
| 54 | India | 82 | [`India.m3u`](All/India.m3u) |
| 55 | India Backups | 5 | [`India_Backups.m3u`](All/India_Backups.m3u) |
| 56 | Classic TV | 70 | [`Classic_TV.m3u`](All/Classic_TV.m3u) |
| 57 | Classic TV Backups | 6 | [`Classic_TV_Backups.m3u`](All/Classic_TV_Backups.m3u) |
| 58 | Business | 57 | [`Business.m3u`](All/Business.m3u) |
| 59 | Business Backups | 12 | [`Business_Backups.m3u`](All/Business_Backups.m3u) |
| 60 | Canada | 46 | [`Canada.m3u`](All/Canada.m3u) |
| 61 | UK | 36 | [`UK.m3u`](All/UK.m3u) |
| 62 | UK Backups | 5 | [`UK_Backups.m3u`](All/UK_Backups.m3u) |
| 63 | Family | 33 | [`Family.m3u`](All/Family.m3u) |
| 64 | A&E Networks | 29 | [`A_E_Networks.m3u`](All/A_E_Networks.m3u) |
| 65 | Australia | 24 | [`Australia.m3u`](All/Australia.m3u) |
| 66 | Global TV | 16 | [`Global_TV.m3u`](All/Global_TV.m3u) |
| 67 | Digital TV | 15 | [`Digital_TV.m3u`](All/Digital_TV.m3u) |
| 68 | Animals & Nature | 14 | [`Animals_Nature.m3u`](All/Animals_Nature.m3u) |
| 69 | Animals & Nature Backups | 7 | [`Animals_Nature_Backups.m3u`](All/Animals_Nature_Backups.m3u) |
| 70 | Weather | 14 | [`Weather.m3u`](All/Weather.m3u) |
| 71 | Weather Backups | 4 | [`Weather_Backups.m3u`](All/Weather_Backups.m3u) |
| 72 | DLTV | 10 | [`DLTV.m3u`](All/DLTV.m3u) |
| 73 | Tv Paranormal | 10 | [`Tv_Paranormal.m3u`](All/Tv_Paranormal.m3u) |
| 74 | Tv Paranormal Backups | 5 | [`Tv_Paranormal_Backups.m3u`](All/Tv_Paranormal_Backups.m3u) |
| 75 | Online TV | 9 | [`Online_TV.m3u`](All/Online_TV.m3u) |
| 76 | Online TV Backups | 5 | [`Online_TV_Backups.m3u`](All/Online_TV_Backups.m3u) |
| 77 | Tv Celebrities | 9 | [`Tv_Celebrities.m3u`](All/Tv_Celebrities.m3u) |
| 78 | Tv Shows | 6 | [`Tv_Shows.m3u`](All/Tv_Shows.m3u) |
| 79 | Aria Web Channels | 5 | [`Aria_Web_Channels.m3u`](All/Aria_Web_Channels.m3u) |
| 80 | Oceania | 4 | [`Oceania.m3u`](All/Oceania.m3u) |
| 81 | Other | 284 | [`Other.m3u`](All/Other.m3u) |
| 82 | Other Backups | 141 | [`Other_Backups.m3u`](All/Other_Backups.m3u) |

Groups smaller than 3 channels keep no file of their own; they stay in `playlists/PremiumTV.m3u`.

## Load it

```text
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/USA.m3u          # every US channel, by category
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/USA/Sports.m3u   # just the US sports channels
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/All/Sports.m3u  # every sports channel in the library
```

## Keeping it in order

Rebuilt by `scripts/build_categories.py` after every scrape, deep check and quick update; a file is only rewritten when its channel list actually changed. `scripts/verify_playlists.py --require-shelf` re-plans the shelf from the published playlists and fails the run when a committed file is stale, so this directory can not drift away from the playlists it mirrors.
