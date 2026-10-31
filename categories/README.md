# Category shelf

- **Shelf rebuilt:** 2026-10-30 22:14 UTC (2026-10-30 06:14 PM EDT) — _manual re-scrape (run-scrape.txt)_
- **Sources:** [`playlists/PremiumTV.m3u`](../playlists/PremiumTV.m3u) for `All/`, [`playlists/live/USA.m3u`](../playlists/live/USA.m3u) for `USA.m3u` and `USA/`
- **Order:** Sports -> Lifestyle -> Fox Channels -> CBS -> NBC -> NBC Sports Channels -> Cartoons -> PBS -> Game Shows (each followed by its own Backups group), then the long tail by size, `Other` last — the published order from `scripts/categorize.py`.
- **One entry per channel:** a channel's spare feeds sit right after it in its `<category> Backups` group, best quality first.

Every file here is a slice of an already published playlist: same channels, same order, same group labels, same guide header. Nothing is re-classified, so loading the shelf can never show a channel the playlist does not have.

## USA

[`USA.m3u`](USA.m3u) — every one of the **2833** working US channels in one file, in category order. The per-category files below are the same list cut up.

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 152 | [`Sports.m3u`](USA/Sports.m3u) |
| 2 | Sports Backups | 52 | [`Sports_Backups.m3u`](USA/Sports_Backups.m3u) |
| 3 | Lifestyle | 161 | [`Lifestyle.m3u`](USA/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 59 | [`Lifestyle_Backups.m3u`](USA/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 25 | [`Fox_Channels.m3u`](USA/Fox_Channels.m3u) |
| 6 | CBS | 27 | [`CBS.m3u`](USA/CBS.m3u) |
| 7 | CBS Backups | 15 | [`CBS_Backups.m3u`](USA/CBS_Backups.m3u) |
| 8 | NBC | 42 | [`NBC.m3u`](USA/NBC.m3u) |
| 9 | NBC Backups | 6 | [`NBC_Backups.m3u`](USA/NBC_Backups.m3u) |
| 10 | NBC Sports Channels | 4 | [`NBC_Sports_Channels.m3u`](USA/NBC_Sports_Channels.m3u) |
| 11 | Cartoons | 73 | [`Cartoons.m3u`](USA/Cartoons.m3u) |
| 12 | Cartoons Backups | 14 | [`Cartoons_Backups.m3u`](USA/Cartoons_Backups.m3u) |
| 13 | PBS | 21 | [`PBS.m3u`](USA/PBS.m3u) |
| 14 | Game Shows | 10 | [`Game_Shows.m3u`](USA/Game_Shows.m3u) |
| 15 | Game Shows Backups | 15 | [`Game_Shows_Backups.m3u`](USA/Game_Shows_Backups.m3u) |
| 16 | United States | 351 | [`United_States.m3u`](USA/United_States.m3u) |
| 17 | United States Backups | 61 | [`United_States_Backups.m3u`](USA/United_States_Backups.m3u) |
| 18 | Movies | 233 | [`Movies.m3u`](USA/Movies.m3u) |
| 19 | Movies Backups | 83 | [`Movies_Backups.m3u`](USA/Movies_Backups.m3u) |
| 20 | Series | 166 | [`Series.m3u`](USA/Series.m3u) |
| 21 | Series Backups | 95 | [`Series_Backups.m3u`](USA/Series_Backups.m3u) |
| 22 | Entertainment | 146 | [`Entertainment.m3u`](USA/Entertainment.m3u) |
| 23 | Entertainment Backups | 47 | [`Entertainment_Backups.m3u`](USA/Entertainment_Backups.m3u) |
| 24 | Documentary | 122 | [`Documentary.m3u`](USA/Documentary.m3u) |
| 25 | Documentary Backups | 37 | [`Documentary_Backups.m3u`](USA/Documentary_Backups.m3u) |
| 26 | Religious | 118 | [`Religious.m3u`](USA/Religious.m3u) |
| 27 | Religious Backups | 16 | [`Religious_Backups.m3u`](USA/Religious_Backups.m3u) |
| 28 | Music | 102 | [`Music.m3u`](USA/Music.m3u) |
| 29 | Music Backups | 25 | [`Music_Backups.m3u`](USA/Music_Backups.m3u) |
| 30 | Kids | 86 | [`Kids.m3u`](USA/Kids.m3u) |
| 31 | Kids Backups | 37 | [`Kids_Backups.m3u`](USA/Kids_Backups.m3u) |
| 32 | Legislative | 80 | [`Legislative.m3u`](USA/Legislative.m3u) |
| 33 | News | 64 | [`News.m3u`](USA/News.m3u) |
| 34 | News Backups | 29 | [`News_Backups.m3u`](USA/News_Backups.m3u) |
| 35 | Education | 42 | [`Education.m3u`](USA/Education.m3u) |
| 36 | Education Backups | 3 | [`Education_Backups.m3u`](USA/Education_Backups.m3u) |
| 37 | Comedy | 34 | [`Comedy.m3u`](USA/Comedy.m3u) |
| 38 | Comedy Backups | 19 | [`Comedy_Backups.m3u`](USA/Comedy_Backups.m3u) |
| 39 | Classic TV | 28 | [`Classic_TV.m3u`](USA/Classic_TV.m3u) |
| 40 | Classic TV Backups | 7 | [`Classic_TV_Backups.m3u`](USA/Classic_TV_Backups.m3u) |
| 41 | A&E Networks | 24 | [`A_E_Networks.m3u`](USA/A_E_Networks.m3u) |
| 42 | Culture | 19 | [`Culture.m3u`](USA/Culture.m3u) |
| 43 | Business | 17 | [`Business.m3u`](USA/Business.m3u) |
| 44 | Business Backups | 10 | [`Business_Backups.m3u`](USA/Business_Backups.m3u) |
| 45 | Family | 15 | [`Family.m3u`](USA/Family.m3u) |
| 46 | Family Backups | 3 | [`Family_Backups.m3u`](USA/Family_Backups.m3u) |
| 47 | Weather | 5 | [`Weather.m3u`](USA/Weather.m3u) |
| 48 | Weather Backups | 3 | [`Weather_Backups.m3u`](USA/Weather_Backups.m3u) |
| 49 | International | 4 | [`International.m3u`](USA/International.m3u) |
| 50 | Other | 10 | [`Other.m3u`](USA/Other.m3u) |

Groups smaller than 3 channels keep no file of their own (they would be a one-link playlist) - they stay in `USA.m3u`, which always holds every US channel.

## All countries

One file per category for the whole library (US channels first inside a category, because that is the published order).

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 539 | [`Sports.m3u`](All/Sports.m3u) |
| 2 | Sports Backups | 95 | [`Sports_Backups.m3u`](All/Sports_Backups.m3u) |
| 3 | Lifestyle | 518 | [`Lifestyle.m3u`](All/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 94 | [`Lifestyle_Backups.m3u`](All/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 28 | [`Fox_Channels.m3u`](All/Fox_Channels.m3u) |
| 6 | CBS | 30 | [`CBS.m3u`](All/CBS.m3u) |
| 7 | CBS Backups | 15 | [`CBS_Backups.m3u`](All/CBS_Backups.m3u) |
| 8 | NBC | 69 | [`NBC.m3u`](All/NBC.m3u) |
| 9 | NBC Backups | 11 | [`NBC_Backups.m3u`](All/NBC_Backups.m3u) |
| 10 | NBC Sports Channels | 7 | [`NBC_Sports_Channels.m3u`](All/NBC_Sports_Channels.m3u) |
| 11 | Cartoons | 192 | [`Cartoons.m3u`](All/Cartoons.m3u) |
| 12 | Cartoons Backups | 18 | [`Cartoons_Backups.m3u`](All/Cartoons_Backups.m3u) |
| 13 | PBS | 45 | [`PBS.m3u`](All/PBS.m3u) |
| 14 | PBS Backups | 12 | [`PBS_Backups.m3u`](All/PBS_Backups.m3u) |
| 15 | Game Shows | 12 | [`Game_Shows.m3u`](All/Game_Shows.m3u) |
| 16 | Game Shows Backups | 16 | [`Game_Shows_Backups.m3u`](All/Game_Shows_Backups.m3u) |
| 17 | Music | 921 | [`Music.m3u`](All/Music.m3u) |
| 18 | Music Backups | 88 | [`Music_Backups.m3u`](All/Music_Backups.m3u) |
| 19 | News | 867 | [`News.m3u`](All/News.m3u) |
| 20 | News Backups | 184 | [`News_Backups.m3u`](All/News_Backups.m3u) |
| 21 | Movies | 862 | [`Movies.m3u`](All/Movies.m3u) |
| 22 | Movies Backups | 101 | [`Movies_Backups.m3u`](All/Movies_Backups.m3u) |
| 23 | Europe | 773 | [`Europe.m3u`](All/Europe.m3u) |
| 24 | Europe Backups | 70 | [`Europe_Backups.m3u`](All/Europe_Backups.m3u) |
| 25 | Entertainment | 711 | [`Entertainment.m3u`](All/Entertainment.m3u) |
| 26 | Entertainment Backups | 83 | [`Entertainment_Backups.m3u`](All/Entertainment_Backups.m3u) |
| 27 | International | 691 | [`International.m3u`](All/International.m3u) |
| 28 | International Backups | 110 | [`International_Backups.m3u`](All/International_Backups.m3u) |
| 29 | Religious | 616 | [`Religious.m3u`](All/Religious.m3u) |
| 30 | Religious Backups | 43 | [`Religious_Backups.m3u`](All/Religious_Backups.m3u) |
| 31 | Asia | 499 | [`Asia.m3u`](All/Asia.m3u) |
| 32 | Asia Backups | 23 | [`Asia_Backups.m3u`](All/Asia_Backups.m3u) |
| 33 | South America | 496 | [`South_America.m3u`](All/South_America.m3u) |
| 34 | South America Backups | 23 | [`South_America_Backups.m3u`](All/South_America_Backups.m3u) |
| 35 | Documentary | 397 | [`Documentary.m3u`](All/Documentary.m3u) |
| 36 | Documentary Backups | 75 | [`Documentary_Backups.m3u`](All/Documentary_Backups.m3u) |
| 37 | United States | 367 | [`United_States.m3u`](All/United_States.m3u) |
| 38 | United States Backups | 61 | [`United_States_Backups.m3u`](All/United_States_Backups.m3u) |
| 39 | Series | 340 | [`Series.m3u`](All/Series.m3u) |
| 40 | Series Backups | 112 | [`Series_Backups.m3u`](All/Series_Backups.m3u) |
| 41 | Kids | 310 | [`Kids.m3u`](All/Kids.m3u) |
| 42 | Kids Backups | 61 | [`Kids_Backups.m3u`](All/Kids_Backups.m3u) |
| 43 | North America | 303 | [`North_America.m3u`](All/North_America.m3u) |
| 44 | North America Backups | 7 | [`North_America_Backups.m3u`](All/North_America_Backups.m3u) |
| 45 | Education | 136 | [`Education.m3u`](All/Education.m3u) |
| 46 | Education Backups | 14 | [`Education_Backups.m3u`](All/Education_Backups.m3u) |
| 47 | Culture | 131 | [`Culture.m3u`](All/Culture.m3u) |
| 48 | Culture Backups | 7 | [`Culture_Backups.m3u`](All/Culture_Backups.m3u) |
| 49 | Legislative | 128 | [`Legislative.m3u`](All/Legislative.m3u) |
| 50 | Legislative Backups | 3 | [`Legislative_Backups.m3u`](All/Legislative_Backups.m3u) |
| 51 | Comedy | 122 | [`Comedy.m3u`](All/Comedy.m3u) |
| 52 | Comedy Backups | 26 | [`Comedy_Backups.m3u`](All/Comedy_Backups.m3u) |
| 53 | India | 89 | [`India.m3u`](All/India.m3u) |
| 54 | India Backups | 10 | [`India_Backups.m3u`](All/India_Backups.m3u) |
| 55 | Africa | 76 | [`Africa.m3u`](All/Africa.m3u) |
| 56 | Classic TV | 72 | [`Classic_TV.m3u`](All/Classic_TV.m3u) |
| 57 | Classic TV Backups | 8 | [`Classic_TV_Backups.m3u`](All/Classic_TV_Backups.m3u) |
| 58 | Business | 50 | [`Business.m3u`](All/Business.m3u) |
| 59 | Business Backups | 13 | [`Business_Backups.m3u`](All/Business_Backups.m3u) |
| 60 | Family | 33 | [`Family.m3u`](All/Family.m3u) |
| 61 | Family Backups | 3 | [`Family_Backups.m3u`](All/Family_Backups.m3u) |
| 62 | A&E Networks | 29 | [`A_E_Networks.m3u`](All/A_E_Networks.m3u) |
| 63 | UK | 25 | [`UK.m3u`](All/UK.m3u) |
| 64 | UK Backups | 5 | [`UK_Backups.m3u`](All/UK_Backups.m3u) |
| 65 | Australia | 22 | [`Australia.m3u`](All/Australia.m3u) |
| 66 | Canada | 22 | [`Canada.m3u`](All/Canada.m3u) |
| 67 | Weather | 12 | [`Weather.m3u`](All/Weather.m3u) |
| 68 | Weather Backups | 4 | [`Weather_Backups.m3u`](All/Weather_Backups.m3u) |
| 69 | Animals & Nature | 9 | [`Animals_Nature.m3u`](All/Animals_Nature.m3u) |
| 70 | Animals & Nature Backups | 3 | [`Animals_Nature_Backups.m3u`](All/Animals_Nature_Backups.m3u) |
| 71 | DLTV | 9 | [`DLTV.m3u`](All/DLTV.m3u) |
| 72 | Tv Celebrities | 9 | [`Tv_Celebrities.m3u`](All/Tv_Celebrities.m3u) |
| 73 | Tv Paranormal | 8 | [`Tv_Paranormal.m3u`](All/Tv_Paranormal.m3u) |
| 74 | Tv Paranormal Backups | 3 | [`Tv_Paranormal_Backups.m3u`](All/Tv_Paranormal_Backups.m3u) |
| 75 | Global TV | 7 | [`Global_TV.m3u`](All/Global_TV.m3u) |
| 76 | Online TV | 7 | [`Online_TV.m3u`](All/Online_TV.m3u) |
| 77 | Aria Web Channels | 6 | [`Aria_Web_Channels.m3u`](All/Aria_Web_Channels.m3u) |
| 78 | Tv Shows | 5 | [`Tv_Shows.m3u`](All/Tv_Shows.m3u) |
| 79 | Oceania | 4 | [`Oceania.m3u`](All/Oceania.m3u) |
| 80 | Other | 249 | [`Other.m3u`](All/Other.m3u) |
| 81 | Other Backups | 140 | [`Other_Backups.m3u`](All/Other_Backups.m3u) |

Groups smaller than 3 channels keep no file of their own; they stay in `playlists/PremiumTV.m3u`.

## Load it

```text
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/USA.m3u          # every US channel, by category
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/USA/Sports.m3u   # just the US sports channels
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/All/Sports.m3u  # every sports channel in the library
```

## Keeping it in order

Rebuilt by `scripts/build_categories.py` after every scrape, deep check and quick update; a file is only rewritten when its channel list actually changed. `scripts/verify_playlists.py --require-shelf` re-plans the shelf from the published playlists and fails the run when a committed file is stale, so this directory can not drift away from the playlists it mirrors.
