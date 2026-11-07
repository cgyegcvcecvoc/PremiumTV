# Category shelf

- **Shelf rebuilt:** 2026-11-07 13:04 UTC (2026-11-07 08:04 AM EST) — _nightly deep link check_
- **Sources:** [`playlists/PremiumTV.m3u`](../playlists/PremiumTV.m3u) for `All/`, [`playlists/live/USA.m3u`](../playlists/live/USA.m3u) for `USA.m3u` and `USA/`
- **Order:** Sports -> Lifestyle -> Fox Channels -> CBS -> NBC -> NBC Sports Channels -> Cartoons -> PBS -> Game Shows (each followed by its own Backups group), then the long tail by size, `Other` last — the published order from `scripts/categorize.py`.
- **One entry per channel:** a channel's spare feeds sit right after it in its `<category> Backups` group, best quality first.

Every file here is a slice of an already published playlist: same channels, same order, same group labels, same guide header. Nothing is re-classified, so loading the shelf can never show a channel the playlist does not have.

## USA

[`USA.m3u`](USA.m3u) — every one of the **2916** working US channels in one file, in category order. The per-category files below are the same list cut up.

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 125 | [`Sports.m3u`](USA/Sports.m3u) |
| 2 | Sports Backups | 72 | [`Sports_Backups.m3u`](USA/Sports_Backups.m3u) |
| 3 | Lifestyle | 156 | [`Lifestyle.m3u`](USA/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 77 | [`Lifestyle_Backups.m3u`](USA/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 23 | [`Fox_Channels.m3u`](USA/Fox_Channels.m3u) |
| 6 | CBS | 27 | [`CBS.m3u`](USA/CBS.m3u) |
| 7 | CBS Backups | 14 | [`CBS_Backups.m3u`](USA/CBS_Backups.m3u) |
| 8 | NBC | 41 | [`NBC.m3u`](USA/NBC.m3u) |
| 9 | NBC Backups | 7 | [`NBC_Backups.m3u`](USA/NBC_Backups.m3u) |
| 10 | NBC Sports Channels | 6 | [`NBC_Sports_Channels.m3u`](USA/NBC_Sports_Channels.m3u) |
| 11 | Cartoons | 74 | [`Cartoons.m3u`](USA/Cartoons.m3u) |
| 12 | Cartoons Backups | 25 | [`Cartoons_Backups.m3u`](USA/Cartoons_Backups.m3u) |
| 13 | PBS | 21 | [`PBS.m3u`](USA/PBS.m3u) |
| 14 | Game Shows | 10 | [`Game_Shows.m3u`](USA/Game_Shows.m3u) |
| 15 | Game Shows Backups | 15 | [`Game_Shows_Backups.m3u`](USA/Game_Shows_Backups.m3u) |
| 16 | United States | 345 | [`United_States.m3u`](USA/United_States.m3u) |
| 17 | United States Backups | 75 | [`United_States_Backups.m3u`](USA/United_States_Backups.m3u) |
| 18 | Movies | 238 | [`Movies.m3u`](USA/Movies.m3u) |
| 19 | Movies Backups | 104 | [`Movies_Backups.m3u`](USA/Movies_Backups.m3u) |
| 20 | Series | 164 | [`Series.m3u`](USA/Series.m3u) |
| 21 | Series Backups | 109 | [`Series_Backups.m3u`](USA/Series_Backups.m3u) |
| 22 | Entertainment | 135 | [`Entertainment.m3u`](USA/Entertainment.m3u) |
| 23 | Entertainment Backups | 56 | [`Entertainment_Backups.m3u`](USA/Entertainment_Backups.m3u) |
| 24 | Documentary | 117 | [`Documentary.m3u`](USA/Documentary.m3u) |
| 25 | Documentary Backups | 50 | [`Documentary_Backups.m3u`](USA/Documentary_Backups.m3u) |
| 26 | Religious | 115 | [`Religious.m3u`](USA/Religious.m3u) |
| 27 | Religious Backups | 14 | [`Religious_Backups.m3u`](USA/Religious_Backups.m3u) |
| 28 | Music | 99 | [`Music.m3u`](USA/Music.m3u) |
| 29 | Music Backups | 36 | [`Music_Backups.m3u`](USA/Music_Backups.m3u) |
| 30 | Kids | 85 | [`Kids.m3u`](USA/Kids.m3u) |
| 31 | Kids Backups | 44 | [`Kids_Backups.m3u`](USA/Kids_Backups.m3u) |
| 32 | Legislative | 78 | [`Legislative.m3u`](USA/Legislative.m3u) |
| 33 | News | 59 | [`News.m3u`](USA/News.m3u) |
| 34 | News Backups | 26 | [`News_Backups.m3u`](USA/News_Backups.m3u) |
| 35 | Education | 41 | [`Education.m3u`](USA/Education.m3u) |
| 36 | Education Backups | 3 | [`Education_Backups.m3u`](USA/Education_Backups.m3u) |
| 37 | Comedy | 36 | [`Comedy.m3u`](USA/Comedy.m3u) |
| 38 | Comedy Backups | 21 | [`Comedy_Backups.m3u`](USA/Comedy_Backups.m3u) |
| 39 | Classic TV | 25 | [`Classic_TV.m3u`](USA/Classic_TV.m3u) |
| 40 | Classic TV Backups | 10 | [`Classic_TV_Backups.m3u`](USA/Classic_TV_Backups.m3u) |
| 41 | A&E Networks | 24 | [`A_E_Networks.m3u`](USA/A_E_Networks.m3u) |
| 42 | Culture | 19 | [`Culture.m3u`](USA/Culture.m3u) |
| 43 | Business | 16 | [`Business.m3u`](USA/Business.m3u) |
| 44 | Business Backups | 11 | [`Business_Backups.m3u`](USA/Business_Backups.m3u) |
| 45 | Family | 15 | [`Family.m3u`](USA/Family.m3u) |
| 46 | Family Backups | 5 | [`Family_Backups.m3u`](USA/Family_Backups.m3u) |
| 47 | Weather | 5 | [`Weather.m3u`](USA/Weather.m3u) |
| 48 | Weather Backups | 3 | [`Weather_Backups.m3u`](USA/Weather_Backups.m3u) |
| 49 | International | 4 | [`International.m3u`](USA/International.m3u) |
| 50 | Other | 19 | [`Other.m3u`](USA/Other.m3u) |

Groups smaller than 3 channels keep no file of their own (they would be a one-link playlist) - they stay in `USA.m3u`, which always holds every US channel.

## All countries

One file per category for the whole library (US channels first inside a category, because that is the published order).

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 500 | [`Sports.m3u`](All/Sports.m3u) |
| 2 | Sports Backups | 120 | [`Sports_Backups.m3u`](All/Sports_Backups.m3u) |
| 3 | Lifestyle | 479 | [`Lifestyle.m3u`](All/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 125 | [`Lifestyle_Backups.m3u`](All/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 26 | [`Fox_Channels.m3u`](All/Fox_Channels.m3u) |
| 6 | CBS | 30 | [`CBS.m3u`](All/CBS.m3u) |
| 7 | CBS Backups | 14 | [`CBS_Backups.m3u`](All/CBS_Backups.m3u) |
| 8 | NBC | 68 | [`NBC.m3u`](All/NBC.m3u) |
| 9 | NBC Backups | 11 | [`NBC_Backups.m3u`](All/NBC_Backups.m3u) |
| 10 | NBC Sports Channels | 8 | [`NBC_Sports_Channels.m3u`](All/NBC_Sports_Channels.m3u) |
| 11 | Cartoons | 194 | [`Cartoons.m3u`](All/Cartoons.m3u) |
| 12 | Cartoons Backups | 30 | [`Cartoons_Backups.m3u`](All/Cartoons_Backups.m3u) |
| 13 | PBS | 39 | [`PBS.m3u`](All/PBS.m3u) |
| 14 | PBS Backups | 6 | [`PBS_Backups.m3u`](All/PBS_Backups.m3u) |
| 15 | Game Shows | 12 | [`Game_Shows.m3u`](All/Game_Shows.m3u) |
| 16 | Game Shows Backups | 16 | [`Game_Shows_Backups.m3u`](All/Game_Shows_Backups.m3u) |
| 17 | Movies | 861 | [`Movies.m3u`](All/Movies.m3u) |
| 18 | Movies Backups | 132 | [`Movies_Backups.m3u`](All/Movies_Backups.m3u) |
| 19 | Music | 835 | [`Music.m3u`](All/Music.m3u) |
| 20 | Music Backups | 115 | [`Music_Backups.m3u`](All/Music_Backups.m3u) |
| 21 | News | 820 | [`News.m3u`](All/News.m3u) |
| 22 | News Backups | 202 | [`News_Backups.m3u`](All/News_Backups.m3u) |
| 23 | Europe | 744 | [`Europe.m3u`](All/Europe.m3u) |
| 24 | Europe Backups | 65 | [`Europe_Backups.m3u`](All/Europe_Backups.m3u) |
| 25 | Entertainment | 696 | [`Entertainment.m3u`](All/Entertainment.m3u) |
| 26 | Entertainment Backups | 113 | [`Entertainment_Backups.m3u`](All/Entertainment_Backups.m3u) |
| 27 | International | 639 | [`International.m3u`](All/International.m3u) |
| 28 | International Backups | 97 | [`International_Backups.m3u`](All/International_Backups.m3u) |
| 29 | Religious | 591 | [`Religious.m3u`](All/Religious.m3u) |
| 30 | Religious Backups | 43 | [`Religious_Backups.m3u`](All/Religious_Backups.m3u) |
| 31 | Asia | 467 | [`Asia.m3u`](All/Asia.m3u) |
| 32 | Asia Backups | 25 | [`Asia_Backups.m3u`](All/Asia_Backups.m3u) |
| 33 | South America | 448 | [`South_America.m3u`](All/South_America.m3u) |
| 34 | South America Backups | 22 | [`South_America_Backups.m3u`](All/South_America_Backups.m3u) |
| 35 | Documentary | 379 | [`Documentary.m3u`](All/Documentary.m3u) |
| 36 | Documentary Backups | 91 | [`Documentary_Backups.m3u`](All/Documentary_Backups.m3u) |
| 37 | United States | 345 | [`United_States.m3u`](All/United_States.m3u) |
| 38 | United States Backups | 75 | [`United_States_Backups.m3u`](All/United_States_Backups.m3u) |
| 39 | Series | 321 | [`Series.m3u`](All/Series.m3u) |
| 40 | Series Backups | 129 | [`Series_Backups.m3u`](All/Series_Backups.m3u) |
| 41 | Kids | 306 | [`Kids.m3u`](All/Kids.m3u) |
| 42 | Kids Backups | 74 | [`Kids_Backups.m3u`](All/Kids_Backups.m3u) |
| 43 | North America | 261 | [`North_America.m3u`](All/North_America.m3u) |
| 44 | North America Backups | 6 | [`North_America_Backups.m3u`](All/North_America_Backups.m3u) |
| 45 | Education | 124 | [`Education.m3u`](All/Education.m3u) |
| 46 | Education Backups | 15 | [`Education_Backups.m3u`](All/Education_Backups.m3u) |
| 47 | Culture | 119 | [`Culture.m3u`](All/Culture.m3u) |
| 48 | Culture Backups | 6 | [`Culture_Backups.m3u`](All/Culture_Backups.m3u) |
| 49 | Comedy | 114 | [`Comedy.m3u`](All/Comedy.m3u) |
| 50 | Comedy Backups | 32 | [`Comedy_Backups.m3u`](All/Comedy_Backups.m3u) |
| 51 | Legislative | 112 | [`Legislative.m3u`](All/Legislative.m3u) |
| 52 | Classic TV | 68 | [`Classic_TV.m3u`](All/Classic_TV.m3u) |
| 53 | Classic TV Backups | 12 | [`Classic_TV_Backups.m3u`](All/Classic_TV_Backups.m3u) |
| 54 | India | 67 | [`India.m3u`](All/India.m3u) |
| 55 | India Backups | 6 | [`India_Backups.m3u`](All/India_Backups.m3u) |
| 56 | Africa | 64 | [`Africa.m3u`](All/Africa.m3u) |
| 57 | Business | 47 | [`Business.m3u`](All/Business.m3u) |
| 58 | Business Backups | 13 | [`Business_Backups.m3u`](All/Business_Backups.m3u) |
| 59 | Family | 30 | [`Family.m3u`](All/Family.m3u) |
| 60 | Family Backups | 6 | [`Family_Backups.m3u`](All/Family_Backups.m3u) |
| 61 | A&E Networks | 28 | [`A_E_Networks.m3u`](All/A_E_Networks.m3u) |
| 62 | UK | 26 | [`UK.m3u`](All/UK.m3u) |
| 63 | UK Backups | 6 | [`UK_Backups.m3u`](All/UK_Backups.m3u) |
| 64 | Canada | 20 | [`Canada.m3u`](All/Canada.m3u) |
| 65 | Weather | 12 | [`Weather.m3u`](All/Weather.m3u) |
| 66 | Weather Backups | 4 | [`Weather_Backups.m3u`](All/Weather_Backups.m3u) |
| 67 | Australia | 11 | [`Australia.m3u`](All/Australia.m3u) |
| 68 | Animals & Nature | 9 | [`Animals_Nature.m3u`](All/Animals_Nature.m3u) |
| 69 | Animals & Nature Backups | 3 | [`Animals_Nature_Backups.m3u`](All/Animals_Nature_Backups.m3u) |
| 70 | DLTV | 9 | [`DLTV.m3u`](All/DLTV.m3u) |
| 71 | Tv Celebrities | 7 | [`Tv_Celebrities.m3u`](All/Tv_Celebrities.m3u) |
| 72 | Aria Web Channels | 6 | [`Aria_Web_Channels.m3u`](All/Aria_Web_Channels.m3u) |
| 73 | Tv Paranormal | 6 | [`Tv_Paranormal.m3u`](All/Tv_Paranormal.m3u) |
| 74 | Tv Paranormal Backups | 3 | [`Tv_Paranormal_Backups.m3u`](All/Tv_Paranormal_Backups.m3u) |
| 75 | Global TV | 5 | [`Global_TV.m3u`](All/Global_TV.m3u) |
| 76 | Global TV Backups | 3 | [`Global_TV_Backups.m3u`](All/Global_TV_Backups.m3u) |
| 77 | Oceania | 4 | [`Oceania.m3u`](All/Oceania.m3u) |
| 78 | Online TV | 4 | [`Online_TV.m3u`](All/Online_TV.m3u) |
| 79 | Online TV Backups | 7 | [`Online_TV_Backups.m3u`](All/Online_TV_Backups.m3u) |
| 80 | Tv Shows | 4 | [`Tv_Shows.m3u`](All/Tv_Shows.m3u) |
| 81 | Other | 261 | [`Other.m3u`](All/Other.m3u) |
| 82 | Other Backups | 140 | [`Other_Backups.m3u`](All/Other_Backups.m3u) |

Groups smaller than 3 channels keep no file of their own; they stay in `playlists/PremiumTV.m3u`.

## Load it

```text
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV/main/categories/USA.m3u          # every US channel, by category
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV/main/categories/USA/Sports.m3u   # just the US sports channels
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV/main/categories/All/Sports.m3u  # every sports channel in the library
```

## Keeping it in order

Rebuilt by `scripts/build_categories.py` after every scrape, deep check and quick update; a file is only rewritten when its channel list actually changed. `scripts/verify_playlists.py --require-shelf` re-plans the shelf from the published playlists and fails the run when a committed file is stale, so this directory can not drift away from the playlists it mirrors.
