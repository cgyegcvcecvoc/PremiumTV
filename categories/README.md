# Category shelf

- **Shelf rebuilt:** 2026-11-03 14:15 UTC (2026-11-03 09:15 AM EST) — _nightly deep link check_
- **Sources:** [`playlists/PremiumTV.m3u`](../playlists/PremiumTV.m3u) for `All/`, [`playlists/live/USA.m3u`](../playlists/live/USA.m3u) for `USA.m3u` and `USA/`
- **Order:** Sports -> Lifestyle -> Fox Channels -> CBS -> NBC -> NBC Sports Channels -> Cartoons -> PBS -> Game Shows (each followed by its own Backups group), then the long tail by size, `Other` last — the published order from `scripts/categorize.py`.
- **One entry per channel:** a channel's spare feeds sit right after it in its `<category> Backups` group, best quality first.

Every file here is a slice of an already published playlist: same channels, same order, same group labels, same guide header. Nothing is re-classified, so loading the shelf can never show a channel the playlist does not have.

## USA

[`USA.m3u`](USA.m3u) — every one of the **2757** working US channels in one file, in category order. The per-category files below are the same list cut up.

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 137 | [`Sports.m3u`](USA/Sports.m3u) |
| 2 | Sports Backups | 51 | [`Sports_Backups.m3u`](USA/Sports_Backups.m3u) |
| 3 | Lifestyle | 160 | [`Lifestyle.m3u`](USA/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 61 | [`Lifestyle_Backups.m3u`](USA/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 23 | [`Fox_Channels.m3u`](USA/Fox_Channels.m3u) |
| 6 | CBS | 27 | [`CBS.m3u`](USA/CBS.m3u) |
| 7 | CBS Backups | 14 | [`CBS_Backups.m3u`](USA/CBS_Backups.m3u) |
| 8 | NBC | 41 | [`NBC.m3u`](USA/NBC.m3u) |
| 9 | NBC Backups | 6 | [`NBC_Backups.m3u`](USA/NBC_Backups.m3u) |
| 10 | NBC Sports Channels | 6 | [`NBC_Sports_Channels.m3u`](USA/NBC_Sports_Channels.m3u) |
| 11 | Cartoons | 74 | [`Cartoons.m3u`](USA/Cartoons.m3u) |
| 12 | Cartoons Backups | 15 | [`Cartoons_Backups.m3u`](USA/Cartoons_Backups.m3u) |
| 13 | PBS | 21 | [`PBS.m3u`](USA/PBS.m3u) |
| 14 | Game Shows | 10 | [`Game_Shows.m3u`](USA/Game_Shows.m3u) |
| 15 | Game Shows Backups | 15 | [`Game_Shows_Backups.m3u`](USA/Game_Shows_Backups.m3u) |
| 16 | United States | 314 | [`United_States.m3u`](USA/United_States.m3u) |
| 17 | United States Backups | 58 | [`United_States_Backups.m3u`](USA/United_States_Backups.m3u) |
| 18 | Movies | 248 | [`Movies.m3u`](USA/Movies.m3u) |
| 19 | Movies Backups | 82 | [`Movies_Backups.m3u`](USA/Movies_Backups.m3u) |
| 20 | Series | 168 | [`Series.m3u`](USA/Series.m3u) |
| 21 | Series Backups | 94 | [`Series_Backups.m3u`](USA/Series_Backups.m3u) |
| 22 | Entertainment | 146 | [`Entertainment.m3u`](USA/Entertainment.m3u) |
| 23 | Entertainment Backups | 46 | [`Entertainment_Backups.m3u`](USA/Entertainment_Backups.m3u) |
| 24 | Documentary | 123 | [`Documentary.m3u`](USA/Documentary.m3u) |
| 25 | Documentary Backups | 37 | [`Documentary_Backups.m3u`](USA/Documentary_Backups.m3u) |
| 26 | Religious | 117 | [`Religious.m3u`](USA/Religious.m3u) |
| 27 | Religious Backups | 15 | [`Religious_Backups.m3u`](USA/Religious_Backups.m3u) |
| 28 | Music | 102 | [`Music.m3u`](USA/Music.m3u) |
| 29 | Music Backups | 24 | [`Music_Backups.m3u`](USA/Music_Backups.m3u) |
| 30 | Kids | 86 | [`Kids.m3u`](USA/Kids.m3u) |
| 31 | Kids Backups | 36 | [`Kids_Backups.m3u`](USA/Kids_Backups.m3u) |
| 32 | Legislative | 62 | [`Legislative.m3u`](USA/Legislative.m3u) |
| 33 | News | 57 | [`News.m3u`](USA/News.m3u) |
| 34 | News Backups | 26 | [`News_Backups.m3u`](USA/News_Backups.m3u) |
| 35 | Comedy | 36 | [`Comedy.m3u`](USA/Comedy.m3u) |
| 36 | Comedy Backups | 19 | [`Comedy_Backups.m3u`](USA/Comedy_Backups.m3u) |
| 37 | Education | 33 | [`Education.m3u`](USA/Education.m3u) |
| 38 | Education Backups | 3 | [`Education_Backups.m3u`](USA/Education_Backups.m3u) |
| 39 | Classic TV | 27 | [`Classic_TV.m3u`](USA/Classic_TV.m3u) |
| 40 | Classic TV Backups | 7 | [`Classic_TV_Backups.m3u`](USA/Classic_TV_Backups.m3u) |
| 41 | A&E Networks | 24 | [`A_E_Networks.m3u`](USA/A_E_Networks.m3u) |
| 42 | Business | 17 | [`Business.m3u`](USA/Business.m3u) |
| 43 | Business Backups | 10 | [`Business_Backups.m3u`](USA/Business_Backups.m3u) |
| 44 | Culture | 17 | [`Culture.m3u`](USA/Culture.m3u) |
| 45 | Family | 15 | [`Family.m3u`](USA/Family.m3u) |
| 46 | Family Backups | 3 | [`Family_Backups.m3u`](USA/Family_Backups.m3u) |
| 47 | Weather | 5 | [`Weather.m3u`](USA/Weather.m3u) |
| 48 | Weather Backups | 3 | [`Weather_Backups.m3u`](USA/Weather_Backups.m3u) |
| 49 | International | 4 | [`International.m3u`](USA/International.m3u) |
| 50 | Other | 19 | [`Other.m3u`](USA/Other.m3u) |

Groups smaller than 3 channels keep no file of their own (they would be a one-link playlist) - they stay in `USA.m3u`, which always holds every US channel.

## All countries

One file per category for the whole library (US channels first inside a category, because that is the published order).

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 543 | [`Sports.m3u`](All/Sports.m3u) |
| 2 | Sports Backups | 93 | [`Sports_Backups.m3u`](All/Sports_Backups.m3u) |
| 3 | Lifestyle | 516 | [`Lifestyle.m3u`](All/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 96 | [`Lifestyle_Backups.m3u`](All/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 26 | [`Fox_Channels.m3u`](All/Fox_Channels.m3u) |
| 6 | CBS | 30 | [`CBS.m3u`](All/CBS.m3u) |
| 7 | CBS Backups | 14 | [`CBS_Backups.m3u`](All/CBS_Backups.m3u) |
| 8 | NBC | 68 | [`NBC.m3u`](All/NBC.m3u) |
| 9 | NBC Backups | 10 | [`NBC_Backups.m3u`](All/NBC_Backups.m3u) |
| 10 | NBC Sports Channels | 9 | [`NBC_Sports_Channels.m3u`](All/NBC_Sports_Channels.m3u) |
| 11 | Cartoons | 196 | [`Cartoons.m3u`](All/Cartoons.m3u) |
| 12 | Cartoons Backups | 19 | [`Cartoons_Backups.m3u`](All/Cartoons_Backups.m3u) |
| 13 | PBS | 40 | [`PBS.m3u`](All/PBS.m3u) |
| 14 | PBS Backups | 7 | [`PBS_Backups.m3u`](All/PBS_Backups.m3u) |
| 15 | Game Shows | 12 | [`Game_Shows.m3u`](All/Game_Shows.m3u) |
| 16 | Game Shows Backups | 16 | [`Game_Shows_Backups.m3u`](All/Game_Shows_Backups.m3u) |
| 17 | Movies | 895 | [`Movies.m3u`](All/Movies.m3u) |
| 18 | Movies Backups | 102 | [`Movies_Backups.m3u`](All/Movies_Backups.m3u) |
| 19 | Music | 892 | [`Music.m3u`](All/Music.m3u) |
| 20 | Music Backups | 86 | [`Music_Backups.m3u`](All/Music_Backups.m3u) |
| 21 | News | 867 | [`News.m3u`](All/News.m3u) |
| 22 | News Backups | 168 | [`News_Backups.m3u`](All/News_Backups.m3u) |
| 23 | Europe | 761 | [`Europe.m3u`](All/Europe.m3u) |
| 24 | Europe Backups | 65 | [`Europe_Backups.m3u`](All/Europe_Backups.m3u) |
| 25 | Entertainment | 754 | [`Entertainment.m3u`](All/Entertainment.m3u) |
| 26 | Entertainment Backups | 82 | [`Entertainment_Backups.m3u`](All/Entertainment_Backups.m3u) |
| 27 | International | 659 | [`International.m3u`](All/International.m3u) |
| 28 | International Backups | 105 | [`International_Backups.m3u`](All/International_Backups.m3u) |
| 29 | Religious | 610 | [`Religious.m3u`](All/Religious.m3u) |
| 30 | Religious Backups | 41 | [`Religious_Backups.m3u`](All/Religious_Backups.m3u) |
| 31 | Asia | 470 | [`Asia.m3u`](All/Asia.m3u) |
| 32 | Asia Backups | 23 | [`Asia_Backups.m3u`](All/Asia_Backups.m3u) |
| 33 | South America | 467 | [`South_America.m3u`](All/South_America.m3u) |
| 34 | South America Backups | 23 | [`South_America_Backups.m3u`](All/South_America_Backups.m3u) |
| 35 | Documentary | 402 | [`Documentary.m3u`](All/Documentary.m3u) |
| 36 | Documentary Backups | 75 | [`Documentary_Backups.m3u`](All/Documentary_Backups.m3u) |
| 37 | Series | 339 | [`Series.m3u`](All/Series.m3u) |
| 38 | Series Backups | 110 | [`Series_Backups.m3u`](All/Series_Backups.m3u) |
| 39 | United States | 330 | [`United_States.m3u`](All/United_States.m3u) |
| 40 | United States Backups | 58 | [`United_States_Backups.m3u`](All/United_States_Backups.m3u) |
| 41 | Kids | 324 | [`Kids.m3u`](All/Kids.m3u) |
| 42 | Kids Backups | 58 | [`Kids_Backups.m3u`](All/Kids_Backups.m3u) |
| 43 | North America | 291 | [`North_America.m3u`](All/North_America.m3u) |
| 44 | North America Backups | 5 | [`North_America_Backups.m3u`](All/North_America_Backups.m3u) |
| 45 | Comedy | 122 | [`Comedy.m3u`](All/Comedy.m3u) |
| 46 | Comedy Backups | 26 | [`Comedy_Backups.m3u`](All/Comedy_Backups.m3u) |
| 47 | Culture | 120 | [`Culture.m3u`](All/Culture.m3u) |
| 48 | Culture Backups | 7 | [`Culture_Backups.m3u`](All/Culture_Backups.m3u) |
| 49 | Education | 119 | [`Education.m3u`](All/Education.m3u) |
| 50 | Education Backups | 13 | [`Education_Backups.m3u`](All/Education_Backups.m3u) |
| 51 | Legislative | 96 | [`Legislative.m3u`](All/Legislative.m3u) |
| 52 | Legislative Backups | 3 | [`Legislative_Backups.m3u`](All/Legislative_Backups.m3u) |
| 53 | Classic TV | 71 | [`Classic_TV.m3u`](All/Classic_TV.m3u) |
| 54 | Classic TV Backups | 8 | [`Classic_TV_Backups.m3u`](All/Classic_TV_Backups.m3u) |
| 55 | India | 71 | [`India.m3u`](All/India.m3u) |
| 56 | India Backups | 10 | [`India_Backups.m3u`](All/India_Backups.m3u) |
| 57 | Africa | 64 | [`Africa.m3u`](All/Africa.m3u) |
| 58 | Business | 48 | [`Business.m3u`](All/Business.m3u) |
| 59 | Business Backups | 12 | [`Business_Backups.m3u`](All/Business_Backups.m3u) |
| 60 | Family | 31 | [`Family.m3u`](All/Family.m3u) |
| 61 | Family Backups | 3 | [`Family_Backups.m3u`](All/Family_Backups.m3u) |
| 62 | A&E Networks | 28 | [`A_E_Networks.m3u`](All/A_E_Networks.m3u) |
| 63 | Canada | 22 | [`Canada.m3u`](All/Canada.m3u) |
| 64 | UK | 22 | [`UK.m3u`](All/UK.m3u) |
| 65 | UK Backups | 4 | [`UK_Backups.m3u`](All/UK_Backups.m3u) |
| 66 | Australia | 12 | [`Australia.m3u`](All/Australia.m3u) |
| 67 | Weather | 12 | [`Weather.m3u`](All/Weather.m3u) |
| 68 | Weather Backups | 4 | [`Weather_Backups.m3u`](All/Weather_Backups.m3u) |
| 69 | Animals & Nature | 9 | [`Animals_Nature.m3u`](All/Animals_Nature.m3u) |
| 70 | Animals & Nature Backups | 3 | [`Animals_Nature_Backups.m3u`](All/Animals_Nature_Backups.m3u) |
| 71 | DLTV | 9 | [`DLTV.m3u`](All/DLTV.m3u) |
| 72 | Tv Celebrities | 9 | [`Tv_Celebrities.m3u`](All/Tv_Celebrities.m3u) |
| 73 | Online TV | 8 | [`Online_TV.m3u`](All/Online_TV.m3u) |
| 74 | Online TV Backups | 6 | [`Online_TV_Backups.m3u`](All/Online_TV_Backups.m3u) |
| 75 | Tv Paranormal | 8 | [`Tv_Paranormal.m3u`](All/Tv_Paranormal.m3u) |
| 76 | Tv Paranormal Backups | 3 | [`Tv_Paranormal_Backups.m3u`](All/Tv_Paranormal_Backups.m3u) |
| 77 | Global TV | 7 | [`Global_TV.m3u`](All/Global_TV.m3u) |
| 78 | Aria Web Channels | 6 | [`Aria_Web_Channels.m3u`](All/Aria_Web_Channels.m3u) |
| 79 | Tv Shows | 5 | [`Tv_Shows.m3u`](All/Tv_Shows.m3u) |
| 80 | Oceania | 4 | [`Oceania.m3u`](All/Oceania.m3u) |
| 81 | Other | 261 | [`Other.m3u`](All/Other.m3u) |
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
