# Category shelf

- **Shelf rebuilt:** 2026-10-10 23:52 UTC (2026-10-10 07:52 PM EDT) — _4:41 PM final check_
- **Sources:** [`playlists/PremiumTV.m3u`](../playlists/PremiumTV.m3u) for `All/`, [`playlists/countries/USA.m3u`](../playlists/countries/USA.m3u) for `USA.m3u` and `USA/`
- **Order:** Sports -> Lifestyle -> Fox Channels -> CBS -> NBC -> NBC Sports Channels -> Cartoons -> PBS -> Game Shows (each followed by its own Backups group), then the long tail by size, `Other` last — the published order from `scripts/categorize.py`.
- **One entry per channel:** a channel's spare feeds sit right after it in its `<category> Backups` group, best quality first.

Every file here is a slice of an already published playlist: same channels, same order, same group labels, same guide header. Nothing is re-classified, so loading the shelf can never show a channel the playlist does not have.

## USA

[`USA.m3u`](USA.m3u) — every one of the **2194** working US channels in one file, in category order. The per-category files below are the same list cut up.

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 316 | [`Sports.m3u`](USA/Sports.m3u) |
| 2 | Sports Backups | 34 | [`Sports_Backups.m3u`](USA/Sports_Backups.m3u) |
| 3 | Lifestyle | 118 | [`Lifestyle.m3u`](USA/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 44 | [`Lifestyle_Backups.m3u`](USA/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 27 | [`Fox_Channels.m3u`](USA/Fox_Channels.m3u) |
| 6 | CBS | 25 | [`CBS.m3u`](USA/CBS.m3u) |
| 7 | CBS Backups | 14 | [`CBS_Backups.m3u`](USA/CBS_Backups.m3u) |
| 8 | NBC | 46 | [`NBC.m3u`](USA/NBC.m3u) |
| 9 | NBC Backups | 5 | [`NBC_Backups.m3u`](USA/NBC_Backups.m3u) |
| 10 | NBC Sports Channels | 5 | [`NBC_Sports_Channels.m3u`](USA/NBC_Sports_Channels.m3u) |
| 11 | Cartoons | 28 | [`Cartoons.m3u`](USA/Cartoons.m3u) |
| 12 | Cartoons Backups | 14 | [`Cartoons_Backups.m3u`](USA/Cartoons_Backups.m3u) |
| 13 | PBS | 16 | [`PBS.m3u`](USA/PBS.m3u) |
| 14 | Game Shows | 9 | [`Game_Shows.m3u`](USA/Game_Shows.m3u) |
| 15 | Game Shows Backups | 8 | [`Game_Shows_Backups.m3u`](USA/Game_Shows_Backups.m3u) |
| 16 | United States | 280 | [`United_States.m3u`](USA/United_States.m3u) |
| 17 | United States Backups | 47 | [`United_States_Backups.m3u`](USA/United_States_Backups.m3u) |
| 18 | Movies | 164 | [`Movies.m3u`](USA/Movies.m3u) |
| 19 | Movies Backups | 53 | [`Movies_Backups.m3u`](USA/Movies_Backups.m3u) |
| 20 | Religious | 105 | [`Religious.m3u`](USA/Religious.m3u) |
| 21 | Religious Backups | 14 | [`Religious_Backups.m3u`](USA/Religious_Backups.m3u) |
| 22 | Entertainment | 87 | [`Entertainment.m3u`](USA/Entertainment.m3u) |
| 23 | Entertainment Backups | 22 | [`Entertainment_Backups.m3u`](USA/Entertainment_Backups.m3u) |
| 24 | Documentary | 82 | [`Documentary.m3u`](USA/Documentary.m3u) |
| 25 | Documentary Backups | 25 | [`Documentary_Backups.m3u`](USA/Documentary_Backups.m3u) |
| 26 | Series | 74 | [`Series.m3u`](USA/Series.m3u) |
| 27 | Series Backups | 43 | [`Series_Backups.m3u`](USA/Series_Backups.m3u) |
| 28 | Music | 65 | [`Music.m3u`](USA/Music.m3u) |
| 29 | Music Backups | 13 | [`Music_Backups.m3u`](USA/Music_Backups.m3u) |
| 30 | Legislative | 62 | [`Legislative.m3u`](USA/Legislative.m3u) |
| 31 | Kids | 56 | [`Kids.m3u`](USA/Kids.m3u) |
| 32 | Kids Backups | 22 | [`Kids_Backups.m3u`](USA/Kids_Backups.m3u) |
| 33 | News | 52 | [`News.m3u`](USA/News.m3u) |
| 34 | News Backups | 22 | [`News_Backups.m3u`](USA/News_Backups.m3u) |
| 35 | Education | 27 | [`Education.m3u`](USA/Education.m3u) |
| 36 | Classic TV | 18 | [`Classic_TV.m3u`](USA/Classic_TV.m3u) |
| 37 | Comedy | 18 | [`Comedy.m3u`](USA/Comedy.m3u) |
| 38 | Comedy Backups | 16 | [`Comedy_Backups.m3u`](USA/Comedy_Backups.m3u) |
| 39 | Business | 17 | [`Business.m3u`](USA/Business.m3u) |
| 40 | Business Backups | 8 | [`Business_Backups.m3u`](USA/Business_Backups.m3u) |
| 41 | A&E Networks | 16 | [`A_E_Networks.m3u`](USA/A_E_Networks.m3u) |
| 42 | Culture | 15 | [`Culture.m3u`](USA/Culture.m3u) |
| 43 | Family | 14 | [`Family.m3u`](USA/Family.m3u) |
| 44 | Family Backups | 3 | [`Family_Backups.m3u`](USA/Family_Backups.m3u) |
| 45 | International | 4 | [`International.m3u`](USA/International.m3u) |
| 46 | International Backups | 4 | [`International_Backups.m3u`](USA/International_Backups.m3u) |
| 47 | Weather | 3 | [`Weather.m3u`](USA/Weather.m3u) |
| 48 | Other | 21 | [`Other.m3u`](USA/Other.m3u) |

Groups smaller than 3 channels keep no file of their own (they would be a one-link playlist) - they stay in `USA.m3u`, which always holds every US channel.

## All countries

One file per category for the whole library (US channels first inside a category, because that is the published order).

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 609 | [`Sports.m3u`](All/Sports.m3u) |
| 2 | Sports Backups | 65 | [`Sports_Backups.m3u`](All/Sports_Backups.m3u) |
| 3 | Lifestyle | 363 | [`Lifestyle.m3u`](All/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 67 | [`Lifestyle_Backups.m3u`](All/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 29 | [`Fox_Channels.m3u`](All/Fox_Channels.m3u) |
| 6 | CBS | 27 | [`CBS.m3u`](All/CBS.m3u) |
| 7 | CBS Backups | 14 | [`CBS_Backups.m3u`](All/CBS_Backups.m3u) |
| 8 | NBC | 66 | [`NBC.m3u`](All/NBC.m3u) |
| 9 | NBC Backups | 7 | [`NBC_Backups.m3u`](All/NBC_Backups.m3u) |
| 10 | NBC Sports Channels | 7 | [`NBC_Sports_Channels.m3u`](All/NBC_Sports_Channels.m3u) |
| 11 | Cartoons | 79 | [`Cartoons.m3u`](All/Cartoons.m3u) |
| 12 | Cartoons Backups | 18 | [`Cartoons_Backups.m3u`](All/Cartoons_Backups.m3u) |
| 13 | PBS | 29 | [`PBS.m3u`](All/PBS.m3u) |
| 14 | PBS Backups | 8 | [`PBS_Backups.m3u`](All/PBS_Backups.m3u) |
| 15 | Game Shows | 11 | [`Game_Shows.m3u`](All/Game_Shows.m3u) |
| 16 | Game Shows Backups | 9 | [`Game_Shows_Backups.m3u`](All/Game_Shows_Backups.m3u) |
| 17 | Music | 755 | [`Music.m3u`](All/Music.m3u) |
| 18 | Music Backups | 60 | [`Music_Backups.m3u`](All/Music_Backups.m3u) |
| 19 | News | 731 | [`News.m3u`](All/News.m3u) |
| 20 | News Backups | 152 | [`News_Backups.m3u`](All/News_Backups.m3u) |
| 21 | Europe | 675 | [`Europe.m3u`](All/Europe.m3u) |
| 22 | Europe Backups | 54 | [`Europe_Backups.m3u`](All/Europe_Backups.m3u) |
| 23 | International | 625 | [`International.m3u`](All/International.m3u) |
| 24 | International Backups | 105 | [`International_Backups.m3u`](All/International_Backups.m3u) |
| 25 | Movies | 618 | [`Movies.m3u`](All/Movies.m3u) |
| 26 | Movies Backups | 69 | [`Movies_Backups.m3u`](All/Movies_Backups.m3u) |
| 27 | Religious | 564 | [`Religious.m3u`](All/Religious.m3u) |
| 28 | Religious Backups | 40 | [`Religious_Backups.m3u`](All/Religious_Backups.m3u) |
| 29 | Entertainment | 493 | [`Entertainment.m3u`](All/Entertainment.m3u) |
| 30 | Entertainment Backups | 56 | [`Entertainment_Backups.m3u`](All/Entertainment_Backups.m3u) |
| 31 | South America | 455 | [`South_America.m3u`](All/South_America.m3u) |
| 32 | South America Backups | 21 | [`South_America_Backups.m3u`](All/South_America_Backups.m3u) |
| 33 | Asia | 424 | [`Asia.m3u`](All/Asia.m3u) |
| 34 | Asia Backups | 24 | [`Asia_Backups.m3u`](All/Asia_Backups.m3u) |
| 35 | United States | 297 | [`United_States.m3u`](All/United_States.m3u) |
| 36 | United States Backups | 47 | [`United_States_Backups.m3u`](All/United_States_Backups.m3u) |
| 37 | North America | 295 | [`North_America.m3u`](All/North_America.m3u) |
| 38 | North America Backups | 5 | [`North_America_Backups.m3u`](All/North_America_Backups.m3u) |
| 39 | Documentary | 234 | [`Documentary.m3u`](All/Documentary.m3u) |
| 40 | Documentary Backups | 48 | [`Documentary_Backups.m3u`](All/Documentary_Backups.m3u) |
| 41 | Kids | 215 | [`Kids.m3u`](All/Kids.m3u) |
| 42 | Kids Backups | 40 | [`Kids_Backups.m3u`](All/Kids_Backups.m3u) |
| 43 | Series | 136 | [`Series.m3u`](All/Series.m3u) |
| 44 | Series Backups | 56 | [`Series_Backups.m3u`](All/Series_Backups.m3u) |
| 45 | Education | 112 | [`Education.m3u`](All/Education.m3u) |
| 46 | Education Backups | 5 | [`Education_Backups.m3u`](All/Education_Backups.m3u) |
| 47 | Culture | 109 | [`Culture.m3u`](All/Culture.m3u) |
| 48 | Culture Backups | 8 | [`Culture_Backups.m3u`](All/Culture_Backups.m3u) |
| 49 | Legislative | 94 | [`Legislative.m3u`](All/Legislative.m3u) |
| 50 | Legislative Backups | 3 | [`Legislative_Backups.m3u`](All/Legislative_Backups.m3u) |
| 51 | India | 77 | [`India.m3u`](All/India.m3u) |
| 52 | India Backups | 4 | [`India_Backups.m3u`](All/India_Backups.m3u) |
| 53 | Africa | 63 | [`Africa.m3u`](All/Africa.m3u) |
| 54 | Business | 46 | [`Business.m3u`](All/Business.m3u) |
| 55 | Business Backups | 10 | [`Business_Backups.m3u`](All/Business_Backups.m3u) |
| 56 | Comedy | 40 | [`Comedy.m3u`](All/Comedy.m3u) |
| 57 | Comedy Backups | 23 | [`Comedy_Backups.m3u`](All/Comedy_Backups.m3u) |
| 58 | Classic TV | 30 | [`Classic_TV.m3u`](All/Classic_TV.m3u) |
| 59 | Classic TV Backups | 3 | [`Classic_TV_Backups.m3u`](All/Classic_TV_Backups.m3u) |
| 60 | Family | 24 | [`Family.m3u`](All/Family.m3u) |
| 61 | Family Backups | 3 | [`Family_Backups.m3u`](All/Family_Backups.m3u) |
| 62 | UK | 24 | [`UK.m3u`](All/UK.m3u) |
| 63 | UK Backups | 4 | [`UK_Backups.m3u`](All/UK_Backups.m3u) |
| 64 | A&E Networks | 21 | [`A_E_Networks.m3u`](All/A_E_Networks.m3u) |
| 65 | Canada | 19 | [`Canada.m3u`](All/Canada.m3u) |
| 66 | Weather | 9 | [`Weather.m3u`](All/Weather.m3u) |
| 67 | Aria Web Channels | 5 | [`Aria_Web_Channels.m3u`](All/Aria_Web_Channels.m3u) |
| 68 | Animals & Nature | 4 | [`Animals_Nature.m3u`](All/Animals_Nature.m3u) |
| 69 | Online TV | 4 | [`Online_TV.m3u`](All/Online_TV.m3u) |
| 70 | Tv Paranormal | 4 | [`Tv_Paranormal.m3u`](All/Tv_Paranormal.m3u) |
| 71 | Australia | 3 | [`Australia.m3u`](All/Australia.m3u) |
| 72 | Tv Celebrities | 3 | [`Tv_Celebrities.m3u`](All/Tv_Celebrities.m3u) |
| 73 | Other | 249 | [`Other.m3u`](All/Other.m3u) |
| 74 | Other Backups | 132 | [`Other_Backups.m3u`](All/Other_Backups.m3u) |

Groups smaller than 3 channels keep no file of their own; they stay in `playlists/PremiumTV.m3u`.

## Load it

```text
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/USA.m3u          # every US channel, by category
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/USA/Sports.m3u   # just the US sports channels
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/categories/All/Sports.m3u  # every sports channel in the library
```

## Keeping it in order

Rebuilt by `scripts/build_categories.py` after every scrape, deep check and quick update; a file is only rewritten when its channel list actually changed. `scripts/verify_playlists.py --require-shelf` re-plans the shelf from the published playlists and fails the run when a committed file is stale, so this directory can not drift away from the playlists it mirrors.
