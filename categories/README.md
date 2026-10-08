# Category shelf

- **Shelf rebuilt:** 2026-10-08 01:21 UTC (2026-10-07 09:21 PM EDT) — _scheduled guide build_
- **Sources:** [`playlists/PremiumTV.m3u`](../playlists/PremiumTV.m3u) for `All/`, [`playlists/countries/USA.m3u`](../playlists/countries/USA.m3u) for `USA.m3u` and `USA/`
- **Order:** Sports -> Lifestyle -> Fox Channels -> CBS -> NBC -> NBC Sports Channels -> Cartoons -> PBS -> Game Shows (each followed by its own Backups group), then the long tail by size, `Other` last — the published order from `scripts/categorize.py`.
- **One entry per channel:** a channel's spare feeds sit right after it in its `<category> Backups` group, best quality first.

Every file here is a slice of an already published playlist: same channels, same order, same group labels, same guide header. Nothing is re-classified, so loading the shelf can never show a channel the playlist does not have.

## USA

[`USA.m3u`](USA.m3u) — every one of the **2129** working US channels in one file, in category order. The per-category files below are the same list cut up.

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 173 | [`Sports.m3u`](USA/Sports.m3u) |
| 2 | Sports Backups | 38 | [`Sports_Backups.m3u`](USA/Sports_Backups.m3u) |
| 3 | Lifestyle | 116 | [`Lifestyle.m3u`](USA/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 48 | [`Lifestyle_Backups.m3u`](USA/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 29 | [`Fox_Channels.m3u`](USA/Fox_Channels.m3u) |
| 6 | CBS | 29 | [`CBS.m3u`](USA/CBS.m3u) |
| 7 | CBS Backups | 13 | [`CBS_Backups.m3u`](USA/CBS_Backups.m3u) |
| 8 | NBC | 48 | [`NBC.m3u`](USA/NBC.m3u) |
| 9 | NBC Backups | 6 | [`NBC_Backups.m3u`](USA/NBC_Backups.m3u) |
| 10 | NBC Sports Channels | 3 | [`NBC_Sports_Channels.m3u`](USA/NBC_Sports_Channels.m3u) |
| 11 | Cartoons | 32 | [`Cartoons.m3u`](USA/Cartoons.m3u) |
| 12 | Cartoons Backups | 15 | [`Cartoons_Backups.m3u`](USA/Cartoons_Backups.m3u) |
| 13 | PBS | 21 | [`PBS.m3u`](USA/PBS.m3u) |
| 14 | Game Shows | 9 | [`Game_Shows.m3u`](USA/Game_Shows.m3u) |
| 15 | Game Shows Backups | 9 | [`Game_Shows_Backups.m3u`](USA/Game_Shows_Backups.m3u) |
| 16 | United States | 310 | [`United_States.m3u`](USA/United_States.m3u) |
| 17 | United States Backups | 48 | [`United_States_Backups.m3u`](USA/United_States_Backups.m3u) |
| 18 | Movies | 161 | [`Movies.m3u`](USA/Movies.m3u) |
| 19 | Movies Backups | 51 | [`Movies_Backups.m3u`](USA/Movies_Backups.m3u) |
| 20 | Religious | 108 | [`Religious.m3u`](USA/Religious.m3u) |
| 21 | Religious Backups | 14 | [`Religious_Backups.m3u`](USA/Religious_Backups.m3u) |
| 22 | Entertainment | 89 | [`Entertainment.m3u`](USA/Entertainment.m3u) |
| 23 | Entertainment Backups | 18 | [`Entertainment_Backups.m3u`](USA/Entertainment_Backups.m3u) |
| 24 | Documentary | 81 | [`Documentary.m3u`](USA/Documentary.m3u) |
| 25 | Documentary Backups | 23 | [`Documentary_Backups.m3u`](USA/Documentary_Backups.m3u) |
| 26 | Series | 78 | [`Series.m3u`](USA/Series.m3u) |
| 27 | Series Backups | 56 | [`Series_Backups.m3u`](USA/Series_Backups.m3u) |
| 28 | Legislative | 65 | [`Legislative.m3u`](USA/Legislative.m3u) |
| 29 | Music | 63 | [`Music.m3u`](USA/Music.m3u) |
| 30 | Music Backups | 14 | [`Music_Backups.m3u`](USA/Music_Backups.m3u) |
| 31 | Kids | 55 | [`Kids.m3u`](USA/Kids.m3u) |
| 32 | Kids Backups | 21 | [`Kids_Backups.m3u`](USA/Kids_Backups.m3u) |
| 33 | News | 51 | [`News.m3u`](USA/News.m3u) |
| 34 | News Backups | 19 | [`News_Backups.m3u`](USA/News_Backups.m3u) |
| 35 | Education | 28 | [`Education.m3u`](USA/Education.m3u) |
| 36 | Classic TV | 19 | [`Classic_TV.m3u`](USA/Classic_TV.m3u) |
| 37 | Classic TV Backups | 3 | [`Classic_TV_Backups.m3u`](USA/Classic_TV_Backups.m3u) |
| 38 | A&E Networks | 18 | [`A_E_Networks.m3u`](USA/A_E_Networks.m3u) |
| 39 | Comedy | 18 | [`Comedy.m3u`](USA/Comedy.m3u) |
| 40 | Comedy Backups | 16 | [`Comedy_Backups.m3u`](USA/Comedy_Backups.m3u) |
| 41 | Business | 17 | [`Business.m3u`](USA/Business.m3u) |
| 42 | Business Backups | 8 | [`Business_Backups.m3u`](USA/Business_Backups.m3u) |
| 43 | Culture | 17 | [`Culture.m3u`](USA/Culture.m3u) |
| 44 | Family | 14 | [`Family.m3u`](USA/Family.m3u) |
| 45 | Family Backups | 3 | [`Family_Backups.m3u`](USA/Family_Backups.m3u) |
| 46 | International | 8 | [`International.m3u`](USA/International.m3u) |
| 47 | International Backups | 6 | [`International_Backups.m3u`](USA/International_Backups.m3u) |
| 48 | Weather | 3 | [`Weather.m3u`](USA/Weather.m3u) |
| 49 | Other | 21 | [`Other.m3u`](USA/Other.m3u) |

Groups smaller than 3 channels keep no file of their own (they would be a one-link playlist) - they stay in `USA.m3u`, which always holds every US channel.

## All countries

One file per category for the whole library (US channels first inside a category, because that is the published order).

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 469 | [`Sports.m3u`](All/Sports.m3u) |
| 2 | Sports Backups | 70 | [`Sports_Backups.m3u`](All/Sports_Backups.m3u) |
| 3 | Lifestyle | 385 | [`Lifestyle.m3u`](All/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 70 | [`Lifestyle_Backups.m3u`](All/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 32 | [`Fox_Channels.m3u`](All/Fox_Channels.m3u) |
| 6 | CBS | 31 | [`CBS.m3u`](All/CBS.m3u) |
| 7 | CBS Backups | 13 | [`CBS_Backups.m3u`](All/CBS_Backups.m3u) |
| 8 | NBC | 70 | [`NBC.m3u`](All/NBC.m3u) |
| 9 | NBC Backups | 9 | [`NBC_Backups.m3u`](All/NBC_Backups.m3u) |
| 10 | NBC Sports Channels | 5 | [`NBC_Sports_Channels.m3u`](All/NBC_Sports_Channels.m3u) |
| 11 | Cartoons | 89 | [`Cartoons.m3u`](All/Cartoons.m3u) |
| 12 | Cartoons Backups | 19 | [`Cartoons_Backups.m3u`](All/Cartoons_Backups.m3u) |
| 13 | PBS | 34 | [`PBS.m3u`](All/PBS.m3u) |
| 14 | PBS Backups | 7 | [`PBS_Backups.m3u`](All/PBS_Backups.m3u) |
| 15 | Game Shows | 11 | [`Game_Shows.m3u`](All/Game_Shows.m3u) |
| 16 | Game Shows Backups | 11 | [`Game_Shows_Backups.m3u`](All/Game_Shows_Backups.m3u) |
| 17 | Music | 766 | [`Music.m3u`](All/Music.m3u) |
| 18 | Music Backups | 65 | [`Music_Backups.m3u`](All/Music_Backups.m3u) |
| 19 | News | 732 | [`News.m3u`](All/News.m3u) |
| 20 | News Backups | 150 | [`News_Backups.m3u`](All/News_Backups.m3u) |
| 21 | Europe | 696 | [`Europe.m3u`](All/Europe.m3u) |
| 22 | Europe Backups | 69 | [`Europe_Backups.m3u`](All/Europe_Backups.m3u) |
| 23 | Movies | 644 | [`Movies.m3u`](All/Movies.m3u) |
| 24 | Movies Backups | 68 | [`Movies_Backups.m3u`](All/Movies_Backups.m3u) |
| 25 | International | 630 | [`International.m3u`](All/International.m3u) |
| 26 | International Backups | 98 | [`International_Backups.m3u`](All/International_Backups.m3u) |
| 27 | Religious | 572 | [`Religious.m3u`](All/Religious.m3u) |
| 28 | Religious Backups | 40 | [`Religious_Backups.m3u`](All/Religious_Backups.m3u) |
| 29 | Entertainment | 507 | [`Entertainment.m3u`](All/Entertainment.m3u) |
| 30 | Entertainment Backups | 51 | [`Entertainment_Backups.m3u`](All/Entertainment_Backups.m3u) |
| 31 | South America | 459 | [`South_America.m3u`](All/South_America.m3u) |
| 32 | South America Backups | 22 | [`South_America_Backups.m3u`](All/South_America_Backups.m3u) |
| 33 | Asia | 430 | [`Asia.m3u`](All/Asia.m3u) |
| 34 | Asia Backups | 24 | [`Asia_Backups.m3u`](All/Asia_Backups.m3u) |
| 35 | United States | 327 | [`United_States.m3u`](All/United_States.m3u) |
| 36 | United States Backups | 48 | [`United_States_Backups.m3u`](All/United_States_Backups.m3u) |
| 37 | North America | 286 | [`North_America.m3u`](All/North_America.m3u) |
| 38 | North America Backups | 5 | [`North_America_Backups.m3u`](All/North_America_Backups.m3u) |
| 39 | Documentary | 258 | [`Documentary.m3u`](All/Documentary.m3u) |
| 40 | Documentary Backups | 51 | [`Documentary_Backups.m3u`](All/Documentary_Backups.m3u) |
| 41 | Kids | 217 | [`Kids.m3u`](All/Kids.m3u) |
| 42 | Kids Backups | 39 | [`Kids_Backups.m3u`](All/Kids_Backups.m3u) |
| 43 | Series | 143 | [`Series.m3u`](All/Series.m3u) |
| 44 | Series Backups | 69 | [`Series_Backups.m3u`](All/Series_Backups.m3u) |
| 45 | Education | 115 | [`Education.m3u`](All/Education.m3u) |
| 46 | Education Backups | 5 | [`Education_Backups.m3u`](All/Education_Backups.m3u) |
| 47 | Culture | 110 | [`Culture.m3u`](All/Culture.m3u) |
| 48 | Culture Backups | 6 | [`Culture_Backups.m3u`](All/Culture_Backups.m3u) |
| 49 | Legislative | 96 | [`Legislative.m3u`](All/Legislative.m3u) |
| 50 | India | 81 | [`India.m3u`](All/India.m3u) |
| 51 | India Backups | 5 | [`India_Backups.m3u`](All/India_Backups.m3u) |
| 52 | Africa | 66 | [`Africa.m3u`](All/Africa.m3u) |
| 53 | Business | 44 | [`Business.m3u`](All/Business.m3u) |
| 54 | Business Backups | 10 | [`Business_Backups.m3u`](All/Business_Backups.m3u) |
| 55 | Comedy | 39 | [`Comedy.m3u`](All/Comedy.m3u) |
| 56 | Comedy Backups | 23 | [`Comedy_Backups.m3u`](All/Comedy_Backups.m3u) |
| 57 | Classic TV | 31 | [`Classic_TV.m3u`](All/Classic_TV.m3u) |
| 58 | Classic TV Backups | 4 | [`Classic_TV_Backups.m3u`](All/Classic_TV_Backups.m3u) |
| 59 | Family | 25 | [`Family.m3u`](All/Family.m3u) |
| 60 | Family Backups | 3 | [`Family_Backups.m3u`](All/Family_Backups.m3u) |
| 61 | A&E Networks | 23 | [`A_E_Networks.m3u`](All/A_E_Networks.m3u) |
| 62 | UK | 23 | [`UK.m3u`](All/UK.m3u) |
| 63 | UK Backups | 4 | [`UK_Backups.m3u`](All/UK_Backups.m3u) |
| 64 | Canada | 21 | [`Canada.m3u`](All/Canada.m3u) |
| 65 | Weather | 9 | [`Weather.m3u`](All/Weather.m3u) |
| 66 | Animals & Nature | 5 | [`Animals_Nature.m3u`](All/Animals_Nature.m3u) |
| 67 | Aria Web Channels | 5 | [`Aria_Web_Channels.m3u`](All/Aria_Web_Channels.m3u) |
| 68 | Tv Paranormal | 4 | [`Tv_Paranormal.m3u`](All/Tv_Paranormal.m3u) |
| 69 | Australia | 3 | [`Australia.m3u`](All/Australia.m3u) |
| 70 | Global TV | 3 | [`Global_TV.m3u`](All/Global_TV.m3u) |
| 71 | Online TV | 3 | [`Online_TV.m3u`](All/Online_TV.m3u) |
| 72 | Tv Celebrities | 3 | [`Tv_Celebrities.m3u`](All/Tv_Celebrities.m3u) |
| 73 | Other | 262 | [`Other.m3u`](All/Other.m3u) |
| 74 | Other Backups | 134 | [`Other_Backups.m3u`](All/Other_Backups.m3u) |

Groups smaller than 3 channels keep no file of their own; they stay in `playlists/PremiumTV.m3u`.

## Load it

```text
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/USA.m3u          # every US channel, by category
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/USA/Sports.m3u   # just the US sports channels
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/All/Sports.m3u  # every sports channel in the library
```

## Keeping it in order

Rebuilt by `scripts/build_categories.py` after every scrape, deep check and quick update; a file is only rewritten when its channel list actually changed. `scripts/verify_playlists.py --require-shelf` re-plans the shelf from the published playlists and fails the run when a committed file is stale, so this directory can not drift away from the playlists it mirrors.
