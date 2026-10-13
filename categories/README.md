# Category shelf

- **Shelf rebuilt:** 2026-10-13 10:56 UTC (2026-10-13 06:56 AM EDT) — _11:29 PM overnight recheck_
- **Sources:** [`playlists/PremiumTV.m3u`](../playlists/PremiumTV.m3u) for `All/`, [`playlists/countries/USA.m3u`](../playlists/countries/USA.m3u) for `USA.m3u` and `USA/`
- **Order:** Sports -> Lifestyle -> Fox Channels -> CBS -> NBC -> NBC Sports Channels -> Cartoons -> PBS -> Game Shows (each followed by its own Backups group), then the long tail by size, `Other` last — the published order from `scripts/categorize.py`.
- **One entry per channel:** a channel's spare feeds sit right after it in its `<category> Backups` group, best quality first.

Every file here is a slice of an already published playlist: same channels, same order, same group labels, same guide header. Nothing is re-classified, so loading the shelf can never show a channel the playlist does not have.

## USA

[`USA.m3u`](USA.m3u) — every one of the **2579** working US channels in one file, in category order. The per-category files below are the same list cut up.

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 140 | [`Sports.m3u`](USA/Sports.m3u) |
| 2 | Sports Backups | 47 | [`Sports_Backups.m3u`](USA/Sports_Backups.m3u) |
| 3 | Lifestyle | 141 | [`Lifestyle.m3u`](USA/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 51 | [`Lifestyle_Backups.m3u`](USA/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 27 | [`Fox_Channels.m3u`](USA/Fox_Channels.m3u) |
| 6 | CBS | 30 | [`CBS.m3u`](USA/CBS.m3u) |
| 7 | CBS Backups | 14 | [`CBS_Backups.m3u`](USA/CBS_Backups.m3u) |
| 8 | NBC | 45 | [`NBC.m3u`](USA/NBC.m3u) |
| 9 | NBC Backups | 7 | [`NBC_Backups.m3u`](USA/NBC_Backups.m3u) |
| 10 | NBC Sports Channels | 3 | [`NBC_Sports_Channels.m3u`](USA/NBC_Sports_Channels.m3u) |
| 11 | Cartoons | 61 | [`Cartoons.m3u`](USA/Cartoons.m3u) |
| 12 | Cartoons Backups | 19 | [`Cartoons_Backups.m3u`](USA/Cartoons_Backups.m3u) |
| 13 | PBS | 21 | [`PBS.m3u`](USA/PBS.m3u) |
| 14 | Game Shows | 10 | [`Game_Shows.m3u`](USA/Game_Shows.m3u) |
| 15 | Game Shows Backups | 13 | [`Game_Shows_Backups.m3u`](USA/Game_Shows_Backups.m3u) |
| 16 | United States | 313 | [`United_States.m3u`](USA/United_States.m3u) |
| 17 | United States Backups | 55 | [`United_States_Backups.m3u`](USA/United_States_Backups.m3u) |
| 18 | Movies | 231 | [`Movies.m3u`](USA/Movies.m3u) |
| 19 | Movies Backups | 80 | [`Movies_Backups.m3u`](USA/Movies_Backups.m3u) |
| 20 | Series | 148 | [`Series.m3u`](USA/Series.m3u) |
| 21 | Series Backups | 84 | [`Series_Backups.m3u`](USA/Series_Backups.m3u) |
| 22 | Entertainment | 135 | [`Entertainment.m3u`](USA/Entertainment.m3u) |
| 23 | Entertainment Backups | 36 | [`Entertainment_Backups.m3u`](USA/Entertainment_Backups.m3u) |
| 24 | Documentary | 113 | [`Documentary.m3u`](USA/Documentary.m3u) |
| 25 | Documentary Backups | 33 | [`Documentary_Backups.m3u`](USA/Documentary_Backups.m3u) |
| 26 | Religious | 107 | [`Religious.m3u`](USA/Religious.m3u) |
| 27 | Religious Backups | 14 | [`Religious_Backups.m3u`](USA/Religious_Backups.m3u) |
| 28 | Music | 85 | [`Music.m3u`](USA/Music.m3u) |
| 29 | Music Backups | 20 | [`Music_Backups.m3u`](USA/Music_Backups.m3u) |
| 30 | Kids | 80 | [`Kids.m3u`](USA/Kids.m3u) |
| 31 | Kids Backups | 30 | [`Kids_Backups.m3u`](USA/Kids_Backups.m3u) |
| 32 | Legislative | 65 | [`Legislative.m3u`](USA/Legislative.m3u) |
| 33 | News | 57 | [`News.m3u`](USA/News.m3u) |
| 34 | News Backups | 24 | [`News_Backups.m3u`](USA/News_Backups.m3u) |
| 35 | Education | 32 | [`Education.m3u`](USA/Education.m3u) |
| 36 | Education Backups | 3 | [`Education_Backups.m3u`](USA/Education_Backups.m3u) |
| 37 | Classic TV | 26 | [`Classic_TV.m3u`](USA/Classic_TV.m3u) |
| 38 | Classic TV Backups | 7 | [`Classic_TV_Backups.m3u`](USA/Classic_TV_Backups.m3u) |
| 39 | Comedy | 26 | [`Comedy.m3u`](USA/Comedy.m3u) |
| 40 | Comedy Backups | 19 | [`Comedy_Backups.m3u`](USA/Comedy_Backups.m3u) |
| 41 | A&E Networks | 21 | [`A_E_Networks.m3u`](USA/A_E_Networks.m3u) |
| 42 | Business | 17 | [`Business.m3u`](USA/Business.m3u) |
| 43 | Business Backups | 8 | [`Business_Backups.m3u`](USA/Business_Backups.m3u) |
| 44 | Culture | 17 | [`Culture.m3u`](USA/Culture.m3u) |
| 45 | Family | 15 | [`Family.m3u`](USA/Family.m3u) |
| 46 | Family Backups | 3 | [`Family_Backups.m3u`](USA/Family_Backups.m3u) |
| 47 | International | 7 | [`International.m3u`](USA/International.m3u) |
| 48 | International Backups | 6 | [`International_Backups.m3u`](USA/International_Backups.m3u) |
| 49 | Weather | 4 | [`Weather.m3u`](USA/Weather.m3u) |
| 50 | Weather Backups | 3 | [`Weather_Backups.m3u`](USA/Weather_Backups.m3u) |
| 51 | Other | 14 | [`Other.m3u`](USA/Other.m3u) |

Groups smaller than 3 channels keep no file of their own (they would be a one-link playlist) - they stay in `USA.m3u`, which always holds every US channel.

## All countries

One file per category for the whole library (US channels first inside a category, because that is the published order).

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 495 | [`Sports.m3u`](All/Sports.m3u) |
| 2 | Sports Backups | 86 | [`Sports_Backups.m3u`](All/Sports_Backups.m3u) |
| 3 | Lifestyle | 455 | [`Lifestyle.m3u`](All/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 86 | [`Lifestyle_Backups.m3u`](All/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 29 | [`Fox_Channels.m3u`](All/Fox_Channels.m3u) |
| 6 | CBS | 33 | [`CBS.m3u`](All/CBS.m3u) |
| 7 | CBS Backups | 14 | [`CBS_Backups.m3u`](All/CBS_Backups.m3u) |
| 8 | NBC | 70 | [`NBC.m3u`](All/NBC.m3u) |
| 9 | NBC Backups | 11 | [`NBC_Backups.m3u`](All/NBC_Backups.m3u) |
| 10 | NBC Sports Channels | 6 | [`NBC_Sports_Channels.m3u`](All/NBC_Sports_Channels.m3u) |
| 11 | Cartoons | 169 | [`Cartoons.m3u`](All/Cartoons.m3u) |
| 12 | Cartoons Backups | 23 | [`Cartoons_Backups.m3u`](All/Cartoons_Backups.m3u) |
| 13 | PBS | 34 | [`PBS.m3u`](All/PBS.m3u) |
| 14 | PBS Backups | 7 | [`PBS_Backups.m3u`](All/PBS_Backups.m3u) |
| 15 | Game Shows | 12 | [`Game_Shows.m3u`](All/Game_Shows.m3u) |
| 16 | Game Shows Backups | 14 | [`Game_Shows_Backups.m3u`](All/Game_Shows_Backups.m3u) |
| 17 | Music | 798 | [`Music.m3u`](All/Music.m3u) |
| 18 | Music Backups | 75 | [`Music_Backups.m3u`](All/Music_Backups.m3u) |
| 19 | Movies | 789 | [`Movies.m3u`](All/Movies.m3u) |
| 20 | Movies Backups | 97 | [`Movies_Backups.m3u`](All/Movies_Backups.m3u) |
| 21 | News | 757 | [`News.m3u`](All/News.m3u) |
| 22 | News Backups | 162 | [`News_Backups.m3u`](All/News_Backups.m3u) |
| 23 | Europe | 663 | [`Europe.m3u`](All/Europe.m3u) |
| 24 | Europe Backups | 60 | [`Europe_Backups.m3u`](All/Europe_Backups.m3u) |
| 25 | Entertainment | 612 | [`Entertainment.m3u`](All/Entertainment.m3u) |
| 26 | Entertainment Backups | 68 | [`Entertainment_Backups.m3u`](All/Entertainment_Backups.m3u) |
| 27 | International | 594 | [`International.m3u`](All/International.m3u) |
| 28 | International Backups | 98 | [`International_Backups.m3u`](All/International_Backups.m3u) |
| 29 | Religious | 555 | [`Religious.m3u`](All/Religious.m3u) |
| 30 | Religious Backups | 41 | [`Religious_Backups.m3u`](All/Religious_Backups.m3u) |
| 31 | South America | 452 | [`South_America.m3u`](All/South_America.m3u) |
| 32 | South America Backups | 22 | [`South_America_Backups.m3u`](All/South_America_Backups.m3u) |
| 33 | Asia | 437 | [`Asia.m3u`](All/Asia.m3u) |
| 34 | Asia Backups | 22 | [`Asia_Backups.m3u`](All/Asia_Backups.m3u) |
| 35 | Documentary | 355 | [`Documentary.m3u`](All/Documentary.m3u) |
| 36 | Documentary Backups | 67 | [`Documentary_Backups.m3u`](All/Documentary_Backups.m3u) |
| 37 | United States | 330 | [`United_States.m3u`](All/United_States.m3u) |
| 38 | United States Backups | 55 | [`United_States_Backups.m3u`](All/United_States_Backups.m3u) |
| 39 | Series | 290 | [`Series.m3u`](All/Series.m3u) |
| 40 | Series Backups | 100 | [`Series_Backups.m3u`](All/Series_Backups.m3u) |
| 41 | North America | 271 | [`North_America.m3u`](All/North_America.m3u) |
| 42 | North America Backups | 5 | [`North_America_Backups.m3u`](All/North_America_Backups.m3u) |
| 43 | Kids | 246 | [`Kids.m3u`](All/Kids.m3u) |
| 44 | Kids Backups | 49 | [`Kids_Backups.m3u`](All/Kids_Backups.m3u) |
| 45 | Education | 117 | [`Education.m3u`](All/Education.m3u) |
| 46 | Education Backups | 8 | [`Education_Backups.m3u`](All/Education_Backups.m3u) |
| 47 | Comedy | 105 | [`Comedy.m3u`](All/Comedy.m3u) |
| 48 | Comedy Backups | 26 | [`Comedy_Backups.m3u`](All/Comedy_Backups.m3u) |
| 49 | Culture | 102 | [`Culture.m3u`](All/Culture.m3u) |
| 50 | Culture Backups | 7 | [`Culture_Backups.m3u`](All/Culture_Backups.m3u) |
| 51 | Legislative | 98 | [`Legislative.m3u`](All/Legislative.m3u) |
| 52 | Legislative Backups | 3 | [`Legislative_Backups.m3u`](All/Legislative_Backups.m3u) |
| 53 | India | 78 | [`India.m3u`](All/India.m3u) |
| 54 | India Backups | 5 | [`India_Backups.m3u`](All/India_Backups.m3u) |
| 55 | Africa | 65 | [`Africa.m3u`](All/Africa.m3u) |
| 56 | Classic TV | 63 | [`Classic_TV.m3u`](All/Classic_TV.m3u) |
| 57 | Classic TV Backups | 8 | [`Classic_TV_Backups.m3u`](All/Classic_TV_Backups.m3u) |
| 58 | Business | 45 | [`Business.m3u`](All/Business.m3u) |
| 59 | Business Backups | 10 | [`Business_Backups.m3u`](All/Business_Backups.m3u) |
| 60 | Family | 27 | [`Family.m3u`](All/Family.m3u) |
| 61 | Family Backups | 3 | [`Family_Backups.m3u`](All/Family_Backups.m3u) |
| 62 | A&E Networks | 26 | [`A_E_Networks.m3u`](All/A_E_Networks.m3u) |
| 63 | UK | 25 | [`UK.m3u`](All/UK.m3u) |
| 64 | UK Backups | 4 | [`UK_Backups.m3u`](All/UK_Backups.m3u) |
| 65 | Canada | 21 | [`Canada.m3u`](All/Canada.m3u) |
| 66 | Weather | 10 | [`Weather.m3u`](All/Weather.m3u) |
| 67 | Weather Backups | 4 | [`Weather_Backups.m3u`](All/Weather_Backups.m3u) |
| 68 | Tv Paranormal | 7 | [`Tv_Paranormal.m3u`](All/Tv_Paranormal.m3u) |
| 69 | Animals & Nature | 6 | [`Animals_Nature.m3u`](All/Animals_Nature.m3u) |
| 70 | Tv Celebrities | 6 | [`Tv_Celebrities.m3u`](All/Tv_Celebrities.m3u) |
| 71 | Aria Web Channels | 5 | [`Aria_Web_Channels.m3u`](All/Aria_Web_Channels.m3u) |
| 72 | Australia | 4 | [`Australia.m3u`](All/Australia.m3u) |
| 73 | Online TV | 3 | [`Online_TV.m3u`](All/Online_TV.m3u) |
| 74 | Relax | 3 | [`Relax.m3u`](All/Relax.m3u) |
| 75 | Tv Shows | 3 | [`Tv_Shows.m3u`](All/Tv_Shows.m3u) |
| 76 | Other | 258 | [`Other.m3u`](All/Other.m3u) |
| 77 | Other Backups | 132 | [`Other_Backups.m3u`](All/Other_Backups.m3u) |

Groups smaller than 3 channels keep no file of their own; they stay in `playlists/PremiumTV.m3u`.

## Load it

```text
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/USA.m3u          # every US channel, by category
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/USA/Sports.m3u   # just the US sports channels
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/All/Sports.m3u  # every sports channel in the library
```

## Keeping it in order

Rebuilt by `scripts/build_categories.py` after every scrape, deep check and quick update; a file is only rewritten when its channel list actually changed. `scripts/verify_playlists.py --require-shelf` re-plans the shelf from the published playlists and fails the run when a committed file is stale, so this directory can not drift away from the playlists it mirrors.
