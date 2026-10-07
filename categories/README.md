# Category shelf

- **Shelf rebuilt:** 2026-10-07 11:47 UTC (2026-10-07 07:47 AM EDT) — _nightly deep link check_
- **Sources:** [`playlists/PremiumTV.m3u`](../playlists/PremiumTV.m3u) for `All/`, [`playlists/countries/USA.m3u`](../playlists/countries/USA.m3u) for `USA.m3u` and `USA/`
- **Order:** Sports -> Lifestyle -> Fox Channels -> CBS -> NBC -> NBC Sports Channels -> Cartoons -> PBS -> Game Shows (each followed by its own Backups group), then the long tail by size, `Other` last — the published order from `scripts/categorize.py`.
- **One entry per channel:** a channel's spare feeds sit right after it in its `<category> Backups` group, best quality first.

Every file here is a slice of an already published playlist: same channels, same order, same group labels, same guide header. Nothing is re-classified, so loading the shelf can never show a channel the playlist does not have.

## USA

[`USA.m3u`](USA.m3u) — every one of the **2044** working US channels in one file, in category order. The per-category files below are the same list cut up.

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 133 | [`Sports.m3u`](USA/Sports.m3u) |
| 2 | Sports Backups | 39 | [`Sports_Backups.m3u`](USA/Sports_Backups.m3u) |
| 3 | Lifestyle | 115 | [`Lifestyle.m3u`](USA/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 46 | [`Lifestyle_Backups.m3u`](USA/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 28 | [`Fox_Channels.m3u`](USA/Fox_Channels.m3u) |
| 6 | CBS | 29 | [`CBS.m3u`](USA/CBS.m3u) |
| 7 | CBS Backups | 13 | [`CBS_Backups.m3u`](USA/CBS_Backups.m3u) |
| 8 | NBC | 49 | [`NBC.m3u`](USA/NBC.m3u) |
| 9 | NBC Backups | 6 | [`NBC_Backups.m3u`](USA/NBC_Backups.m3u) |
| 10 | Cartoons | 27 | [`Cartoons.m3u`](USA/Cartoons.m3u) |
| 11 | Cartoons Backups | 14 | [`Cartoons_Backups.m3u`](USA/Cartoons_Backups.m3u) |
| 12 | PBS | 21 | [`PBS.m3u`](USA/PBS.m3u) |
| 13 | Game Shows | 9 | [`Game_Shows.m3u`](USA/Game_Shows.m3u) |
| 14 | Game Shows Backups | 9 | [`Game_Shows_Backups.m3u`](USA/Game_Shows_Backups.m3u) |
| 15 | United States | 305 | [`United_States.m3u`](USA/United_States.m3u) |
| 16 | United States Backups | 48 | [`United_States_Backups.m3u`](USA/United_States_Backups.m3u) |
| 17 | Movies | 153 | [`Movies.m3u`](USA/Movies.m3u) |
| 18 | Movies Backups | 52 | [`Movies_Backups.m3u`](USA/Movies_Backups.m3u) |
| 19 | Religious | 109 | [`Religious.m3u`](USA/Religious.m3u) |
| 20 | Religious Backups | 11 | [`Religious_Backups.m3u`](USA/Religious_Backups.m3u) |
| 21 | Entertainment | 87 | [`Entertainment.m3u`](USA/Entertainment.m3u) |
| 22 | Entertainment Backups | 18 | [`Entertainment_Backups.m3u`](USA/Entertainment_Backups.m3u) |
| 23 | Series | 79 | [`Series.m3u`](USA/Series.m3u) |
| 24 | Series Backups | 56 | [`Series_Backups.m3u`](USA/Series_Backups.m3u) |
| 25 | Documentary | 74 | [`Documentary.m3u`](USA/Documentary.m3u) |
| 26 | Documentary Backups | 22 | [`Documentary_Backups.m3u`](USA/Documentary_Backups.m3u) |
| 27 | Legislative | 65 | [`Legislative.m3u`](USA/Legislative.m3u) |
| 28 | Music | 63 | [`Music.m3u`](USA/Music.m3u) |
| 29 | Music Backups | 14 | [`Music_Backups.m3u`](USA/Music_Backups.m3u) |
| 30 | Kids | 51 | [`Kids.m3u`](USA/Kids.m3u) |
| 31 | Kids Backups | 20 | [`Kids_Backups.m3u`](USA/Kids_Backups.m3u) |
| 32 | News | 51 | [`News.m3u`](USA/News.m3u) |
| 33 | News Backups | 20 | [`News_Backups.m3u`](USA/News_Backups.m3u) |
| 34 | Education | 28 | [`Education.m3u`](USA/Education.m3u) |
| 35 | Classic TV | 19 | [`Classic_TV.m3u`](USA/Classic_TV.m3u) |
| 36 | Classic TV Backups | 3 | [`Classic_TV_Backups.m3u`](USA/Classic_TV_Backups.m3u) |
| 37 | A&E Networks | 18 | [`A_E_Networks.m3u`](USA/A_E_Networks.m3u) |
| 38 | Business | 17 | [`Business.m3u`](USA/Business.m3u) |
| 39 | Business Backups | 8 | [`Business_Backups.m3u`](USA/Business_Backups.m3u) |
| 40 | Comedy | 17 | [`Comedy.m3u`](USA/Comedy.m3u) |
| 41 | Comedy Backups | 16 | [`Comedy_Backups.m3u`](USA/Comedy_Backups.m3u) |
| 42 | Culture | 17 | [`Culture.m3u`](USA/Culture.m3u) |
| 43 | Family | 14 | [`Family.m3u`](USA/Family.m3u) |
| 44 | International | 7 | [`International.m3u`](USA/International.m3u) |
| 45 | International Backups | 5 | [`International_Backups.m3u`](USA/International_Backups.m3u) |
| 46 | Weather | 3 | [`Weather.m3u`](USA/Weather.m3u) |
| 47 | Other | 17 | [`Other.m3u`](USA/Other.m3u) |

Groups smaller than 3 channels keep no file of their own (they would be a one-link playlist) - they stay in `USA.m3u`, which always holds every US channel.

## All countries

One file per category for the whole library (US channels first inside a category, because that is the published order).

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 431 | [`Sports.m3u`](All/Sports.m3u) |
| 2 | Sports Backups | 71 | [`Sports_Backups.m3u`](All/Sports_Backups.m3u) |
| 3 | Lifestyle | 380 | [`Lifestyle.m3u`](All/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 68 | [`Lifestyle_Backups.m3u`](All/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 31 | [`Fox_Channels.m3u`](All/Fox_Channels.m3u) |
| 6 | CBS | 31 | [`CBS.m3u`](All/CBS.m3u) |
| 7 | CBS Backups | 13 | [`CBS_Backups.m3u`](All/CBS_Backups.m3u) |
| 8 | NBC | 71 | [`NBC.m3u`](All/NBC.m3u) |
| 9 | NBC Backups | 9 | [`NBC_Backups.m3u`](All/NBC_Backups.m3u) |
| 10 | NBC Sports Channels | 4 | [`NBC_Sports_Channels.m3u`](All/NBC_Sports_Channels.m3u) |
| 11 | Cartoons | 85 | [`Cartoons.m3u`](All/Cartoons.m3u) |
| 12 | Cartoons Backups | 18 | [`Cartoons_Backups.m3u`](All/Cartoons_Backups.m3u) |
| 13 | PBS | 34 | [`PBS.m3u`](All/PBS.m3u) |
| 14 | PBS Backups | 7 | [`PBS_Backups.m3u`](All/PBS_Backups.m3u) |
| 15 | Game Shows | 11 | [`Game_Shows.m3u`](All/Game_Shows.m3u) |
| 16 | Game Shows Backups | 11 | [`Game_Shows_Backups.m3u`](All/Game_Shows_Backups.m3u) |
| 17 | Music | 765 | [`Music.m3u`](All/Music.m3u) |
| 18 | Music Backups | 67 | [`Music_Backups.m3u`](All/Music_Backups.m3u) |
| 19 | News | 737 | [`News.m3u`](All/News.m3u) |
| 20 | News Backups | 150 | [`News_Backups.m3u`](All/News_Backups.m3u) |
| 21 | Europe | 692 | [`Europe.m3u`](All/Europe.m3u) |
| 22 | Europe Backups | 69 | [`Europe_Backups.m3u`](All/Europe_Backups.m3u) |
| 23 | Movies | 637 | [`Movies.m3u`](All/Movies.m3u) |
| 24 | Movies Backups | 69 | [`Movies_Backups.m3u`](All/Movies_Backups.m3u) |
| 25 | International | 628 | [`International.m3u`](All/International.m3u) |
| 26 | International Backups | 98 | [`International_Backups.m3u`](All/International_Backups.m3u) |
| 27 | Religious | 565 | [`Religious.m3u`](All/Religious.m3u) |
| 28 | Religious Backups | 37 | [`Religious_Backups.m3u`](All/Religious_Backups.m3u) |
| 29 | Entertainment | 498 | [`Entertainment.m3u`](All/Entertainment.m3u) |
| 30 | Entertainment Backups | 52 | [`Entertainment_Backups.m3u`](All/Entertainment_Backups.m3u) |
| 31 | South America | 438 | [`South_America.m3u`](All/South_America.m3u) |
| 32 | South America Backups | 22 | [`South_America_Backups.m3u`](All/South_America_Backups.m3u) |
| 33 | Asia | 431 | [`Asia.m3u`](All/Asia.m3u) |
| 34 | Asia Backups | 25 | [`Asia_Backups.m3u`](All/Asia_Backups.m3u) |
| 35 | United States | 322 | [`United_States.m3u`](All/United_States.m3u) |
| 36 | United States Backups | 48 | [`United_States_Backups.m3u`](All/United_States_Backups.m3u) |
| 37 | North America | 270 | [`North_America.m3u`](All/North_America.m3u) |
| 38 | North America Backups | 5 | [`North_America_Backups.m3u`](All/North_America_Backups.m3u) |
| 39 | Documentary | 249 | [`Documentary.m3u`](All/Documentary.m3u) |
| 40 | Documentary Backups | 50 | [`Documentary_Backups.m3u`](All/Documentary_Backups.m3u) |
| 41 | Kids | 202 | [`Kids.m3u`](All/Kids.m3u) |
| 42 | Kids Backups | 38 | [`Kids_Backups.m3u`](All/Kids_Backups.m3u) |
| 43 | Series | 143 | [`Series.m3u`](All/Series.m3u) |
| 44 | Series Backups | 69 | [`Series_Backups.m3u`](All/Series_Backups.m3u) |
| 45 | Education | 113 | [`Education.m3u`](All/Education.m3u) |
| 46 | Education Backups | 5 | [`Education_Backups.m3u`](All/Education_Backups.m3u) |
| 47 | Culture | 104 | [`Culture.m3u`](All/Culture.m3u) |
| 48 | Culture Backups | 7 | [`Culture_Backups.m3u`](All/Culture_Backups.m3u) |
| 49 | Legislative | 97 | [`Legislative.m3u`](All/Legislative.m3u) |
| 50 | India | 82 | [`India.m3u`](All/India.m3u) |
| 51 | India Backups | 5 | [`India_Backups.m3u`](All/India_Backups.m3u) |
| 52 | Africa | 66 | [`Africa.m3u`](All/Africa.m3u) |
| 53 | Business | 45 | [`Business.m3u`](All/Business.m3u) |
| 54 | Business Backups | 10 | [`Business_Backups.m3u`](All/Business_Backups.m3u) |
| 55 | Comedy | 38 | [`Comedy.m3u`](All/Comedy.m3u) |
| 56 | Comedy Backups | 23 | [`Comedy_Backups.m3u`](All/Comedy_Backups.m3u) |
| 57 | Classic TV | 31 | [`Classic_TV.m3u`](All/Classic_TV.m3u) |
| 58 | Classic TV Backups | 4 | [`Classic_TV_Backups.m3u`](All/Classic_TV_Backups.m3u) |
| 59 | Family | 25 | [`Family.m3u`](All/Family.m3u) |
| 60 | UK | 24 | [`UK.m3u`](All/UK.m3u) |
| 61 | UK Backups | 4 | [`UK_Backups.m3u`](All/UK_Backups.m3u) |
| 62 | A&E Networks | 23 | [`A_E_Networks.m3u`](All/A_E_Networks.m3u) |
| 63 | Canada | 21 | [`Canada.m3u`](All/Canada.m3u) |
| 64 | Weather | 9 | [`Weather.m3u`](All/Weather.m3u) |
| 65 | Animals & Nature | 5 | [`Animals_Nature.m3u`](All/Animals_Nature.m3u) |
| 66 | Aria Web Channels | 5 | [`Aria_Web_Channels.m3u`](All/Aria_Web_Channels.m3u) |
| 67 | Online TV | 4 | [`Online_TV.m3u`](All/Online_TV.m3u) |
| 68 | Tv Paranormal | 4 | [`Tv_Paranormal.m3u`](All/Tv_Paranormal.m3u) |
| 69 | Global TV | 3 | [`Global_TV.m3u`](All/Global_TV.m3u) |
| 70 | Tv Celebrities | 3 | [`Tv_Celebrities.m3u`](All/Tv_Celebrities.m3u) |
| 71 | Other | 259 | [`Other.m3u`](All/Other.m3u) |
| 72 | Other Backups | 135 | [`Other_Backups.m3u`](All/Other_Backups.m3u) |

Groups smaller than 3 channels keep no file of their own; they stay in `playlists/PremiumTV.m3u`.

## Load it

```text
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/USA.m3u          # every US channel, by category
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/USA/Sports.m3u   # just the US sports channels
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/All/Sports.m3u  # every sports channel in the library
```

## Keeping it in order

Rebuilt by `scripts/build_categories.py` after every scrape, deep check and quick update; a file is only rewritten when its channel list actually changed. `scripts/verify_playlists.py --require-shelf` re-plans the shelf from the published playlists and fails the run when a committed file is stale, so this directory can not drift away from the playlists it mirrors.
