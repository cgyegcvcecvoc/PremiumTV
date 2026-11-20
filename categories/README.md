# Category shelf

- **Shelf rebuilt:** 2026-11-20 13:24 UTC (2026-11-20 08:24 AM EST) — _11:29 PM overnight recheck_
- **Sources:** [`playlists/PremiumTV.m3u`](../playlists/PremiumTV.m3u) for `All/`, [`playlists/live/USA.m3u`](../playlists/live/USA.m3u) for `USA.m3u` and `USA/`
- **Order:** Sports -> Lifestyle -> Fox Channels -> CBS -> NBC -> NBC Sports Channels -> Cartoons -> PBS -> Game Shows (each followed by its own Backups group), then the long tail by size, `Other` last — the published order from `scripts/categorize.py`.
- **One entry per channel:** a channel's spare feeds sit right after it in its `<category> Backups` group, best quality first.

Every file here is a slice of an already published playlist: same channels, same order, same group labels, same guide header. Nothing is re-classified, so loading the shelf can never show a channel the playlist does not have.

## USA

[`USA.m3u`](USA.m3u) — every one of the **2967** working US channels in one file, in category order. The per-category files below are the same list cut up.

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 123 | [`Sports.m3u`](USA/Sports.m3u) |
| 2 | Sports Backups | 66 | [`Sports_Backups.m3u`](USA/Sports_Backups.m3u) |
| 3 | Lifestyle | 152 | [`Lifestyle.m3u`](USA/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 76 | [`Lifestyle_Backups.m3u`](USA/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 41 | [`Fox_Channels.m3u`](USA/Fox_Channels.m3u) |
| 6 | CBS | 40 | [`CBS.m3u`](USA/CBS.m3u) |
| 7 | CBS Backups | 14 | [`CBS_Backups.m3u`](USA/CBS_Backups.m3u) |
| 8 | NBC | 44 | [`NBC.m3u`](USA/NBC.m3u) |
| 9 | NBC Backups | 6 | [`NBC_Backups.m3u`](USA/NBC_Backups.m3u) |
| 10 | NBC Sports Channels | 4 | [`NBC_Sports_Channels.m3u`](USA/NBC_Sports_Channels.m3u) |
| 11 | Cartoons | 75 | [`Cartoons.m3u`](USA/Cartoons.m3u) |
| 12 | Cartoons Backups | 24 | [`Cartoons_Backups.m3u`](USA/Cartoons_Backups.m3u) |
| 13 | PBS | 21 | [`PBS.m3u`](USA/PBS.m3u) |
| 14 | PBS Backups | 3 | [`PBS_Backups.m3u`](USA/PBS_Backups.m3u) |
| 15 | Game Shows | 10 | [`Game_Shows.m3u`](USA/Game_Shows.m3u) |
| 16 | Game Shows Backups | 15 | [`Game_Shows_Backups.m3u`](USA/Game_Shows_Backups.m3u) |
| 17 | United States | 364 | [`United_States.m3u`](USA/United_States.m3u) |
| 18 | United States Backups | 77 | [`United_States_Backups.m3u`](USA/United_States_Backups.m3u) |
| 19 | Movies | 226 | [`Movies.m3u`](USA/Movies.m3u) |
| 20 | Movies Backups | 107 | [`Movies_Backups.m3u`](USA/Movies_Backups.m3u) |
| 21 | Series | 163 | [`Series.m3u`](USA/Series.m3u) |
| 22 | Series Backups | 107 | [`Series_Backups.m3u`](USA/Series_Backups.m3u) |
| 23 | Entertainment | 129 | [`Entertainment.m3u`](USA/Entertainment.m3u) |
| 24 | Entertainment Backups | 56 | [`Entertainment_Backups.m3u`](USA/Entertainment_Backups.m3u) |
| 25 | Religious | 118 | [`Religious.m3u`](USA/Religious.m3u) |
| 26 | Religious Backups | 14 | [`Religious_Backups.m3u`](USA/Religious_Backups.m3u) |
| 27 | Music | 101 | [`Music.m3u`](USA/Music.m3u) |
| 28 | Music Backups | 36 | [`Music_Backups.m3u`](USA/Music_Backups.m3u) |
| 29 | Documentary | 94 | [`Documentary.m3u`](USA/Documentary.m3u) |
| 30 | Documentary Backups | 45 | [`Documentary_Backups.m3u`](USA/Documentary_Backups.m3u) |
| 31 | Kids | 86 | [`Kids.m3u`](USA/Kids.m3u) |
| 32 | Kids Backups | 44 | [`Kids_Backups.m3u`](USA/Kids_Backups.m3u) |
| 33 | Legislative | 78 | [`Legislative.m3u`](USA/Legislative.m3u) |
| 34 | News | 67 | [`News.m3u`](USA/News.m3u) |
| 35 | News Backups | 27 | [`News_Backups.m3u`](USA/News_Backups.m3u) |
| 36 | A&E Networks | 61 | [`A_E_Networks.m3u`](USA/A_E_Networks.m3u) |
| 37 | A&E Networks Backups | 10 | [`A_E_Networks_Backups.m3u`](USA/A_E_Networks_Backups.m3u) |
| 38 | Education | 39 | [`Education.m3u`](USA/Education.m3u) |
| 39 | Education Backups | 3 | [`Education_Backups.m3u`](USA/Education_Backups.m3u) |
| 40 | Comedy | 35 | [`Comedy.m3u`](USA/Comedy.m3u) |
| 41 | Comedy Backups | 22 | [`Comedy_Backups.m3u`](USA/Comedy_Backups.m3u) |
| 42 | Classic TV | 25 | [`Classic_TV.m3u`](USA/Classic_TV.m3u) |
| 43 | Classic TV Backups | 10 | [`Classic_TV_Backups.m3u`](USA/Classic_TV_Backups.m3u) |
| 44 | Culture | 18 | [`Culture.m3u`](USA/Culture.m3u) |
| 45 | Business | 17 | [`Business.m3u`](USA/Business.m3u) |
| 46 | Business Backups | 11 | [`Business_Backups.m3u`](USA/Business_Backups.m3u) |
| 47 | Family | 14 | [`Family.m3u`](USA/Family.m3u) |
| 48 | Family Backups | 5 | [`Family_Backups.m3u`](USA/Family_Backups.m3u) |
| 49 | Weather | 5 | [`Weather.m3u`](USA/Weather.m3u) |
| 50 | Weather Backups | 4 | [`Weather_Backups.m3u`](USA/Weather_Backups.m3u) |
| 51 | International | 4 | [`International.m3u`](USA/International.m3u) |
| 52 | Tv Shows | 3 | [`Tv_Shows.m3u`](USA/Tv_Shows.m3u) |
| 53 | Other | 14 | [`Other.m3u`](USA/Other.m3u) |

Groups smaller than 3 channels keep no file of their own (they would be a one-link playlist) - they stay in `USA.m3u`, which always holds every US channel.

## All countries

One file per category for the whole library (US channels first inside a category, because that is the published order).

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 519 | [`Sports.m3u`](All/Sports.m3u) |
| 2 | Sports Backups | 118 | [`Sports_Backups.m3u`](All/Sports_Backups.m3u) |
| 3 | Lifestyle | 480 | [`Lifestyle.m3u`](All/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 123 | [`Lifestyle_Backups.m3u`](All/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 45 | [`Fox_Channels.m3u`](All/Fox_Channels.m3u) |
| 6 | CBS | 43 | [`CBS.m3u`](All/CBS.m3u) |
| 7 | CBS Backups | 14 | [`CBS_Backups.m3u`](All/CBS_Backups.m3u) |
| 8 | NBC | 71 | [`NBC.m3u`](All/NBC.m3u) |
| 9 | NBC Backups | 11 | [`NBC_Backups.m3u`](All/NBC_Backups.m3u) |
| 10 | NBC Sports Channels | 6 | [`NBC_Sports_Channels.m3u`](All/NBC_Sports_Channels.m3u) |
| 11 | Cartoons | 201 | [`Cartoons.m3u`](All/Cartoons.m3u) |
| 12 | Cartoons Backups | 29 | [`Cartoons_Backups.m3u`](All/Cartoons_Backups.m3u) |
| 13 | PBS | 39 | [`PBS.m3u`](All/PBS.m3u) |
| 14 | PBS Backups | 7 | [`PBS_Backups.m3u`](All/PBS_Backups.m3u) |
| 15 | Game Shows | 12 | [`Game_Shows.m3u`](All/Game_Shows.m3u) |
| 16 | Game Shows Backups | 16 | [`Game_Shows_Backups.m3u`](All/Game_Shows_Backups.m3u) |
| 17 | Music | 858 | [`Music.m3u`](All/Music.m3u) |
| 18 | Music Backups | 117 | [`Music_Backups.m3u`](All/Music_Backups.m3u) |
| 19 | News | 857 | [`News.m3u`](All/News.m3u) |
| 20 | News Backups | 207 | [`News_Backups.m3u`](All/News_Backups.m3u) |
| 21 | Movies | 850 | [`Movies.m3u`](All/Movies.m3u) |
| 22 | Movies Backups | 138 | [`Movies_Backups.m3u`](All/Movies_Backups.m3u) |
| 23 | Europe | 756 | [`Europe.m3u`](All/Europe.m3u) |
| 24 | Europe Backups | 59 | [`Europe_Backups.m3u`](All/Europe_Backups.m3u) |
| 25 | Entertainment | 701 | [`Entertainment.m3u`](All/Entertainment.m3u) |
| 26 | Entertainment Backups | 120 | [`Entertainment_Backups.m3u`](All/Entertainment_Backups.m3u) |
| 27 | International | 668 | [`International.m3u`](All/International.m3u) |
| 28 | International Backups | 100 | [`International_Backups.m3u`](All/International_Backups.m3u) |
| 29 | Religious | 598 | [`Religious.m3u`](All/Religious.m3u) |
| 30 | Religious Backups | 42 | [`Religious_Backups.m3u`](All/Religious_Backups.m3u) |
| 31 | Asia | 474 | [`Asia.m3u`](All/Asia.m3u) |
| 32 | Asia Backups | 23 | [`Asia_Backups.m3u`](All/Asia_Backups.m3u) |
| 33 | South America | 470 | [`South_America.m3u`](All/South_America.m3u) |
| 34 | South America Backups | 21 | [`South_America_Backups.m3u`](All/South_America_Backups.m3u) |
| 35 | United States | 364 | [`United_States.m3u`](All/United_States.m3u) |
| 36 | United States Backups | 77 | [`United_States_Backups.m3u`](All/United_States_Backups.m3u) |
| 37 | Documentary | 335 | [`Documentary.m3u`](All/Documentary.m3u) |
| 38 | Documentary Backups | 85 | [`Documentary_Backups.m3u`](All/Documentary_Backups.m3u) |
| 39 | Series | 321 | [`Series.m3u`](All/Series.m3u) |
| 40 | Series Backups | 129 | [`Series_Backups.m3u`](All/Series_Backups.m3u) |
| 41 | Kids | 311 | [`Kids.m3u`](All/Kids.m3u) |
| 42 | Kids Backups | 77 | [`Kids_Backups.m3u`](All/Kids_Backups.m3u) |
| 43 | North America | 285 | [`North_America.m3u`](All/North_America.m3u) |
| 44 | North America Backups | 5 | [`North_America_Backups.m3u`](All/North_America_Backups.m3u) |
| 45 | Education | 134 | [`Education.m3u`](All/Education.m3u) |
| 46 | Education Backups | 14 | [`Education_Backups.m3u`](All/Education_Backups.m3u) |
| 47 | Culture | 124 | [`Culture.m3u`](All/Culture.m3u) |
| 48 | Culture Backups | 7 | [`Culture_Backups.m3u`](All/Culture_Backups.m3u) |
| 49 | Comedy | 114 | [`Comedy.m3u`](All/Comedy.m3u) |
| 50 | Comedy Backups | 33 | [`Comedy_Backups.m3u`](All/Comedy_Backups.m3u) |
| 51 | Legislative | 113 | [`Legislative.m3u`](All/Legislative.m3u) |
| 52 | A&E Networks | 102 | [`A_E_Networks.m3u`](All/A_E_Networks.m3u) |
| 53 | A&E Networks Backups | 13 | [`A_E_Networks_Backups.m3u`](All/A_E_Networks_Backups.m3u) |
| 54 | India | 76 | [`India.m3u`](All/India.m3u) |
| 55 | India Backups | 9 | [`India_Backups.m3u`](All/India_Backups.m3u) |
| 56 | Africa | 68 | [`Africa.m3u`](All/Africa.m3u) |
| 57 | Classic TV | 68 | [`Classic_TV.m3u`](All/Classic_TV.m3u) |
| 58 | Classic TV Backups | 12 | [`Classic_TV_Backups.m3u`](All/Classic_TV_Backups.m3u) |
| 59 | Business | 49 | [`Business.m3u`](All/Business.m3u) |
| 60 | Business Backups | 15 | [`Business_Backups.m3u`](All/Business_Backups.m3u) |
| 61 | Family | 28 | [`Family.m3u`](All/Family.m3u) |
| 62 | Family Backups | 5 | [`Family_Backups.m3u`](All/Family_Backups.m3u) |
| 63 | UK | 26 | [`UK.m3u`](All/UK.m3u) |
| 64 | UK Backups | 4 | [`UK_Backups.m3u`](All/UK_Backups.m3u) |
| 65 | Canada | 20 | [`Canada.m3u`](All/Canada.m3u) |
| 66 | Weather | 12 | [`Weather.m3u`](All/Weather.m3u) |
| 67 | Weather Backups | 5 | [`Weather_Backups.m3u`](All/Weather_Backups.m3u) |
| 68 | Australia | 11 | [`Australia.m3u`](All/Australia.m3u) |
| 69 | Animals & Nature | 9 | [`Animals_Nature.m3u`](All/Animals_Nature.m3u) |
| 70 | Animals & Nature Backups | 3 | [`Animals_Nature_Backups.m3u`](All/Animals_Nature_Backups.m3u) |
| 71 | DLTV | 9 | [`DLTV.m3u`](All/DLTV.m3u) |
| 72 | Tv Celebrities | 7 | [`Tv_Celebrities.m3u`](All/Tv_Celebrities.m3u) |
| 73 | Aria Web Channels | 6 | [`Aria_Web_Channels.m3u`](All/Aria_Web_Channels.m3u) |
| 74 | Global TV | 5 | [`Global_TV.m3u`](All/Global_TV.m3u) |
| 75 | Global TV Backups | 3 | [`Global_TV_Backups.m3u`](All/Global_TV_Backups.m3u) |
| 76 | Online TV | 5 | [`Online_TV.m3u`](All/Online_TV.m3u) |
| 77 | Online TV Backups | 8 | [`Online_TV_Backups.m3u`](All/Online_TV_Backups.m3u) |
| 78 | Tv Paranormal | 5 | [`Tv_Paranormal.m3u`](All/Tv_Paranormal.m3u) |
| 79 | Tv Paranormal Backups | 3 | [`Tv_Paranormal_Backups.m3u`](All/Tv_Paranormal_Backups.m3u) |
| 80 | Tv Shows | 5 | [`Tv_Shows.m3u`](All/Tv_Shows.m3u) |
| 81 | Oceania | 4 | [`Oceania.m3u`](All/Oceania.m3u) |
| 82 | Other | 251 | [`Other.m3u`](All/Other.m3u) |
| 83 | Other Backups | 138 | [`Other_Backups.m3u`](All/Other_Backups.m3u) |

Groups smaller than 3 channels keep no file of their own; they stay in `playlists/PremiumTV.m3u`.

## Load it

```text
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV/main/categories/USA.m3u          # every US channel, by category
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV/main/categories/USA/Sports.m3u   # just the US sports channels
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV/main/categories/All/Sports.m3u  # every sports channel in the library
```

## Keeping it in order

Rebuilt by `scripts/build_categories.py` after every scrape, deep check and quick update; a file is only rewritten when its channel list actually changed. `scripts/verify_playlists.py --require-shelf` re-plans the shelf from the published playlists and fails the run when a committed file is stale, so this directory can not drift away from the playlists it mirrors.
