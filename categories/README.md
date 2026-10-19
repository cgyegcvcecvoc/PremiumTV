# Category shelf

- **Shelf rebuilt:** 2026-10-19 21:12 UTC (2026-10-19 05:12 PM EDT) — _manual re-scrape (run-scrape.txt)_
- **Sources:** [`playlists/PremiumTV.m3u`](../playlists/PremiumTV.m3u) for `All/`, [`playlists/live/USA.m3u`](../playlists/live/USA.m3u) for `USA.m3u` and `USA/`
- **Order:** Sports -> Lifestyle -> Fox Channels -> CBS -> NBC -> NBC Sports Channels -> Cartoons -> PBS -> Game Shows (each followed by its own Backups group), then the long tail by size, `Other` last — the published order from `scripts/categorize.py`.
- **One entry per channel:** a channel's spare feeds sit right after it in its `<category> Backups` group, best quality first.

Every file here is a slice of an already published playlist: same channels, same order, same group labels, same guide header. Nothing is re-classified, so loading the shelf can never show a channel the playlist does not have.

## USA

[`USA.m3u`](USA.m3u) — every one of the **2736** working US channels in one file, in category order. The per-category files below are the same list cut up.

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 157 | [`Sports.m3u`](USA/Sports.m3u) |
| 2 | Sports Backups | 49 | [`Sports_Backups.m3u`](USA/Sports_Backups.m3u) |
| 3 | Lifestyle | 154 | [`Lifestyle.m3u`](USA/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 55 | [`Lifestyle_Backups.m3u`](USA/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 25 | [`Fox_Channels.m3u`](USA/Fox_Channels.m3u) |
| 6 | CBS | 30 | [`CBS.m3u`](USA/CBS.m3u) |
| 7 | CBS Backups | 14 | [`CBS_Backups.m3u`](USA/CBS_Backups.m3u) |
| 8 | NBC | 44 | [`NBC.m3u`](USA/NBC.m3u) |
| 9 | NBC Backups | 6 | [`NBC_Backups.m3u`](USA/NBC_Backups.m3u) |
| 10 | NBC Sports Channels | 7 | [`NBC_Sports_Channels.m3u`](USA/NBC_Sports_Channels.m3u) |
| 11 | Cartoons | 69 | [`Cartoons.m3u`](USA/Cartoons.m3u) |
| 12 | Cartoons Backups | 14 | [`Cartoons_Backups.m3u`](USA/Cartoons_Backups.m3u) |
| 13 | PBS | 21 | [`PBS.m3u`](USA/PBS.m3u) |
| 14 | PBS Backups | 3 | [`PBS_Backups.m3u`](USA/PBS_Backups.m3u) |
| 15 | Game Shows | 10 | [`Game_Shows.m3u`](USA/Game_Shows.m3u) |
| 16 | Game Shows Backups | 14 | [`Game_Shows_Backups.m3u`](USA/Game_Shows_Backups.m3u) |
| 17 | United States | 315 | [`United_States.m3u`](USA/United_States.m3u) |
| 18 | United States Backups | 56 | [`United_States_Backups.m3u`](USA/United_States_Backups.m3u) |
| 19 | Movies | 237 | [`Movies.m3u`](USA/Movies.m3u) |
| 20 | Movies Backups | 80 | [`Movies_Backups.m3u`](USA/Movies_Backups.m3u) |
| 21 | Series | 165 | [`Series.m3u`](USA/Series.m3u) |
| 22 | Series Backups | 91 | [`Series_Backups.m3u`](USA/Series_Backups.m3u) |
| 23 | Entertainment | 145 | [`Entertainment.m3u`](USA/Entertainment.m3u) |
| 24 | Entertainment Backups | 40 | [`Entertainment_Backups.m3u`](USA/Entertainment_Backups.m3u) |
| 25 | Religious | 118 | [`Religious.m3u`](USA/Religious.m3u) |
| 26 | Religious Backups | 15 | [`Religious_Backups.m3u`](USA/Religious_Backups.m3u) |
| 27 | Documentary | 115 | [`Documentary.m3u`](USA/Documentary.m3u) |
| 28 | Documentary Backups | 37 | [`Documentary_Backups.m3u`](USA/Documentary_Backups.m3u) |
| 29 | Music | 97 | [`Music.m3u`](USA/Music.m3u) |
| 30 | Music Backups | 25 | [`Music_Backups.m3u`](USA/Music_Backups.m3u) |
| 31 | Kids | 90 | [`Kids.m3u`](USA/Kids.m3u) |
| 32 | Kids Backups | 35 | [`Kids_Backups.m3u`](USA/Kids_Backups.m3u) |
| 33 | Legislative | 63 | [`Legislative.m3u`](USA/Legislative.m3u) |
| 34 | News | 60 | [`News.m3u`](USA/News.m3u) |
| 35 | News Backups | 27 | [`News_Backups.m3u`](USA/News_Backups.m3u) |
| 36 | Comedy | 33 | [`Comedy.m3u`](USA/Comedy.m3u) |
| 37 | Comedy Backups | 19 | [`Comedy_Backups.m3u`](USA/Comedy_Backups.m3u) |
| 38 | Education | 30 | [`Education.m3u`](USA/Education.m3u) |
| 39 | Education Backups | 3 | [`Education_Backups.m3u`](USA/Education_Backups.m3u) |
| 40 | Classic TV | 28 | [`Classic_TV.m3u`](USA/Classic_TV.m3u) |
| 41 | Classic TV Backups | 7 | [`Classic_TV_Backups.m3u`](USA/Classic_TV_Backups.m3u) |
| 42 | A&E Networks | 24 | [`A_E_Networks.m3u`](USA/A_E_Networks.m3u) |
| 43 | Business | 17 | [`Business.m3u`](USA/Business.m3u) |
| 44 | Business Backups | 10 | [`Business_Backups.m3u`](USA/Business_Backups.m3u) |
| 45 | Culture | 15 | [`Culture.m3u`](USA/Culture.m3u) |
| 46 | Family | 15 | [`Family.m3u`](USA/Family.m3u) |
| 47 | Family Backups | 3 | [`Family_Backups.m3u`](USA/Family_Backups.m3u) |
| 48 | International | 6 | [`International.m3u`](USA/International.m3u) |
| 49 | Weather | 5 | [`Weather.m3u`](USA/Weather.m3u) |
| 50 | Weather Backups | 3 | [`Weather_Backups.m3u`](USA/Weather_Backups.m3u) |
| 51 | Other | 18 | [`Other.m3u`](USA/Other.m3u) |

Groups smaller than 3 channels keep no file of their own (they would be a one-link playlist) - they stay in `USA.m3u`, which always holds every US channel.

## All countries

One file per category for the whole library (US channels first inside a category, because that is the published order).

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 538 | [`Sports.m3u`](All/Sports.m3u) |
| 2 | Sports Backups | 89 | [`Sports_Backups.m3u`](All/Sports_Backups.m3u) |
| 3 | Lifestyle | 493 | [`Lifestyle.m3u`](All/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 90 | [`Lifestyle_Backups.m3u`](All/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 28 | [`Fox_Channels.m3u`](All/Fox_Channels.m3u) |
| 6 | CBS | 34 | [`CBS.m3u`](All/CBS.m3u) |
| 7 | CBS Backups | 14 | [`CBS_Backups.m3u`](All/CBS_Backups.m3u) |
| 8 | NBC | 70 | [`NBC.m3u`](All/NBC.m3u) |
| 9 | NBC Backups | 11 | [`NBC_Backups.m3u`](All/NBC_Backups.m3u) |
| 10 | NBC Sports Channels | 10 | [`NBC_Sports_Channels.m3u`](All/NBC_Sports_Channels.m3u) |
| 11 | Cartoons | 189 | [`Cartoons.m3u`](All/Cartoons.m3u) |
| 12 | Cartoons Backups | 18 | [`Cartoons_Backups.m3u`](All/Cartoons_Backups.m3u) |
| 13 | PBS | 35 | [`PBS.m3u`](All/PBS.m3u) |
| 14 | PBS Backups | 8 | [`PBS_Backups.m3u`](All/PBS_Backups.m3u) |
| 15 | Game Shows | 12 | [`Game_Shows.m3u`](All/Game_Shows.m3u) |
| 16 | Game Shows Backups | 15 | [`Game_Shows_Backups.m3u`](All/Game_Shows_Backups.m3u) |
| 17 | Music | 856 | [`Music.m3u`](All/Music.m3u) |
| 18 | Music Backups | 88 | [`Music_Backups.m3u`](All/Music_Backups.m3u) |
| 19 | Movies | 852 | [`Movies.m3u`](All/Movies.m3u) |
| 20 | Movies Backups | 97 | [`Movies_Backups.m3u`](All/Movies_Backups.m3u) |
| 21 | News | 753 | [`News.m3u`](All/News.m3u) |
| 22 | News Backups | 161 | [`News_Backups.m3u`](All/News_Backups.m3u) |
| 23 | Europe | 730 | [`Europe.m3u`](All/Europe.m3u) |
| 24 | Europe Backups | 67 | [`Europe_Backups.m3u`](All/Europe_Backups.m3u) |
| 25 | Entertainment | 658 | [`Entertainment.m3u`](All/Entertainment.m3u) |
| 26 | Entertainment Backups | 69 | [`Entertainment_Backups.m3u`](All/Entertainment_Backups.m3u) |
| 27 | International | 626 | [`International.m3u`](All/International.m3u) |
| 28 | International Backups | 100 | [`International_Backups.m3u`](All/International_Backups.m3u) |
| 29 | Religious | 571 | [`Religious.m3u`](All/Religious.m3u) |
| 30 | Religious Backups | 36 | [`Religious_Backups.m3u`](All/Religious_Backups.m3u) |
| 31 | South America | 474 | [`South_America.m3u`](All/South_America.m3u) |
| 32 | South America Backups | 22 | [`South_America_Backups.m3u`](All/South_America_Backups.m3u) |
| 33 | Asia | 459 | [`Asia.m3u`](All/Asia.m3u) |
| 34 | Asia Backups | 23 | [`Asia_Backups.m3u`](All/Asia_Backups.m3u) |
| 35 | Documentary | 394 | [`Documentary.m3u`](All/Documentary.m3u) |
| 36 | Documentary Backups | 73 | [`Documentary_Backups.m3u`](All/Documentary_Backups.m3u) |
| 37 | Series | 333 | [`Series.m3u`](All/Series.m3u) |
| 38 | Series Backups | 108 | [`Series_Backups.m3u`](All/Series_Backups.m3u) |
| 39 | United States | 331 | [`United_States.m3u`](All/United_States.m3u) |
| 40 | United States Backups | 56 | [`United_States_Backups.m3u`](All/United_States_Backups.m3u) |
| 41 | Kids | 297 | [`Kids.m3u`](All/Kids.m3u) |
| 42 | Kids Backups | 56 | [`Kids_Backups.m3u`](All/Kids_Backups.m3u) |
| 43 | North America | 288 | [`North_America.m3u`](All/North_America.m3u) |
| 44 | North America Backups | 5 | [`North_America_Backups.m3u`](All/North_America_Backups.m3u) |
| 45 | Comedy | 119 | [`Comedy.m3u`](All/Comedy.m3u) |
| 46 | Comedy Backups | 26 | [`Comedy_Backups.m3u`](All/Comedy_Backups.m3u) |
| 47 | Education | 119 | [`Education.m3u`](All/Education.m3u) |
| 48 | Education Backups | 13 | [`Education_Backups.m3u`](All/Education_Backups.m3u) |
| 49 | Culture | 116 | [`Culture.m3u`](All/Culture.m3u) |
| 50 | Culture Backups | 8 | [`Culture_Backups.m3u`](All/Culture_Backups.m3u) |
| 51 | Legislative | 98 | [`Legislative.m3u`](All/Legislative.m3u) |
| 52 | Legislative Backups | 3 | [`Legislative_Backups.m3u`](All/Legislative_Backups.m3u) |
| 53 | India | 84 | [`India.m3u`](All/India.m3u) |
| 54 | India Backups | 5 | [`India_Backups.m3u`](All/India_Backups.m3u) |
| 55 | Classic TV | 68 | [`Classic_TV.m3u`](All/Classic_TV.m3u) |
| 56 | Classic TV Backups | 8 | [`Classic_TV_Backups.m3u`](All/Classic_TV_Backups.m3u) |
| 57 | Africa | 62 | [`Africa.m3u`](All/Africa.m3u) |
| 58 | Business | 45 | [`Business.m3u`](All/Business.m3u) |
| 59 | Business Backups | 12 | [`Business_Backups.m3u`](All/Business_Backups.m3u) |
| 60 | Family | 31 | [`Family.m3u`](All/Family.m3u) |
| 61 | Family Backups | 3 | [`Family_Backups.m3u`](All/Family_Backups.m3u) |
| 62 | A&E Networks | 29 | [`A_E_Networks.m3u`](All/A_E_Networks.m3u) |
| 63 | UK | 25 | [`UK.m3u`](All/UK.m3u) |
| 64 | UK Backups | 4 | [`UK_Backups.m3u`](All/UK_Backups.m3u) |
| 65 | Canada | 23 | [`Canada.m3u`](All/Canada.m3u) |
| 66 | Australia | 15 | [`Australia.m3u`](All/Australia.m3u) |
| 67 | Weather | 11 | [`Weather.m3u`](All/Weather.m3u) |
| 68 | Weather Backups | 4 | [`Weather_Backups.m3u`](All/Weather_Backups.m3u) |
| 69 | Animals & Nature | 9 | [`Animals_Nature.m3u`](All/Animals_Nature.m3u) |
| 70 | Animals & Nature Backups | 3 | [`Animals_Nature_Backups.m3u`](All/Animals_Nature_Backups.m3u) |
| 71 | DLTV | 9 | [`DLTV.m3u`](All/DLTV.m3u) |
| 72 | Tv Celebrities | 9 | [`Tv_Celebrities.m3u`](All/Tv_Celebrities.m3u) |
| 73 | Global TV | 8 | [`Global_TV.m3u`](All/Global_TV.m3u) |
| 74 | Tv Paranormal | 8 | [`Tv_Paranormal.m3u`](All/Tv_Paranormal.m3u) |
| 75 | Tv Paranormal Backups | 3 | [`Tv_Paranormal_Backups.m3u`](All/Tv_Paranormal_Backups.m3u) |
| 76 | Aria Web Channels | 5 | [`Aria_Web_Channels.m3u`](All/Aria_Web_Channels.m3u) |
| 77 | Online TV | 5 | [`Online_TV.m3u`](All/Online_TV.m3u) |
| 78 | Tv Shows | 5 | [`Tv_Shows.m3u`](All/Tv_Shows.m3u) |
| 79 | Oceania | 4 | [`Oceania.m3u`](All/Oceania.m3u) |
| 80 | Relax | 3 | [`Relax.m3u`](All/Relax.m3u) |
| 81 | Other | 252 | [`Other.m3u`](All/Other.m3u) |
| 82 | Other Backups | 140 | [`Other_Backups.m3u`](All/Other_Backups.m3u) |

Groups smaller than 3 channels keep no file of their own; they stay in `playlists/PremiumTV.m3u`.

## Load it

```text
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/USA.m3u          # every US channel, by category
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/USA/Sports.m3u   # just the US sports channels
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/All/Sports.m3u  # every sports channel in the library
```

## Keeping it in order

Rebuilt by `scripts/build_categories.py` after every scrape, deep check and quick update; a file is only rewritten when its channel list actually changed. `scripts/verify_playlists.py --require-shelf` re-plans the shelf from the published playlists and fails the run when a committed file is stale, so this directory can not drift away from the playlists it mirrors.
