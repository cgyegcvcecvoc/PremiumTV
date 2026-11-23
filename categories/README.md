# Category shelf

- **Shelf rebuilt:** 2026-11-23 18:08 UTC (2026-11-23 01:08 PM EST) — _nightly deep link check_
- **Sources:** [`playlists/PremiumTV.m3u`](../playlists/PremiumTV.m3u) for `All/`, [`playlists/live/USA.m3u`](../playlists/live/USA.m3u) for `USA.m3u` and `USA/`
- **Order:** Sports -> Lifestyle -> Fox Channels -> CBS -> NBC -> NBC Sports Channels -> Cartoons -> PBS -> Game Shows (each followed by its own Backups group), then the long tail by size, `Other` last — the published order from `scripts/categorize.py`.
- **One entry per channel:** a channel's spare feeds sit right after it in its `<category> Backups` group, best quality first.

Every file here is a slice of an already published playlist: same channels, same order, same group labels, same guide header. Nothing is re-classified, so loading the shelf can never show a channel the playlist does not have.

## USA

[`USA.m3u`](USA.m3u) — every one of the **3202** working US channels in one file, in category order. The per-category files below are the same list cut up.

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 103 | [`Sports.m3u`](USA/Sports.m3u) |
| 2 | Sports Backups | 80 | [`Sports_Backups.m3u`](USA/Sports_Backups.m3u) |
| 3 | Lifestyle | 150 | [`Lifestyle.m3u`](USA/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 94 | [`Lifestyle_Backups.m3u`](USA/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 40 | [`Fox_Channels.m3u`](USA/Fox_Channels.m3u) |
| 6 | Fox Channels Backups | 3 | [`Fox_Channels_Backups.m3u`](USA/Fox_Channels_Backups.m3u) |
| 7 | CBS | 30 | [`CBS.m3u`](USA/CBS.m3u) |
| 8 | CBS Backups | 42 | [`CBS_Backups.m3u`](USA/CBS_Backups.m3u) |
| 9 | NBC | 48 | [`NBC.m3u`](USA/NBC.m3u) |
| 10 | NBC Backups | 10 | [`NBC_Backups.m3u`](USA/NBC_Backups.m3u) |
| 11 | NBC Sports Channels | 3 | [`NBC_Sports_Channels.m3u`](USA/NBC_Sports_Channels.m3u) |
| 12 | Cartoons | 66 | [`Cartoons.m3u`](USA/Cartoons.m3u) |
| 13 | Cartoons Backups | 37 | [`Cartoons_Backups.m3u`](USA/Cartoons_Backups.m3u) |
| 14 | PBS | 21 | [`PBS.m3u`](USA/PBS.m3u) |
| 15 | PBS Backups | 5 | [`PBS_Backups.m3u`](USA/PBS_Backups.m3u) |
| 16 | Game Shows | 10 | [`Game_Shows.m3u`](USA/Game_Shows.m3u) |
| 17 | Game Shows Backups | 23 | [`Game_Shows_Backups.m3u`](USA/Game_Shows_Backups.m3u) |
| 18 | United States | 366 | [`United_States.m3u`](USA/United_States.m3u) |
| 19 | United States Backups | 52 | [`United_States_Backups.m3u`](USA/United_States_Backups.m3u) |
| 20 | Movies | 224 | [`Movies.m3u`](USA/Movies.m3u) |
| 21 | Movies Backups | 153 | [`Movies_Backups.m3u`](USA/Movies_Backups.m3u) |
| 22 | Series | 154 | [`Series.m3u`](USA/Series.m3u) |
| 23 | Series Backups | 175 | [`Series_Backups.m3u`](USA/Series_Backups.m3u) |
| 24 | Entertainment | 121 | [`Entertainment.m3u`](USA/Entertainment.m3u) |
| 25 | Entertainment Backups | 74 | [`Entertainment_Backups.m3u`](USA/Entertainment_Backups.m3u) |
| 26 | Religious | 119 | [`Religious.m3u`](USA/Religious.m3u) |
| 27 | Religious Backups | 14 | [`Religious_Backups.m3u`](USA/Religious_Backups.m3u) |
| 28 | Music | 95 | [`Music.m3u`](USA/Music.m3u) |
| 29 | Music Backups | 53 | [`Music_Backups.m3u`](USA/Music_Backups.m3u) |
| 30 | Documentary | 93 | [`Documentary.m3u`](USA/Documentary.m3u) |
| 31 | Documentary Backups | 66 | [`Documentary_Backups.m3u`](USA/Documentary_Backups.m3u) |
| 32 | Kids | 82 | [`Kids.m3u`](USA/Kids.m3u) |
| 33 | Kids Backups | 67 | [`Kids_Backups.m3u`](USA/Kids_Backups.m3u) |
| 34 | Legislative | 78 | [`Legislative.m3u`](USA/Legislative.m3u) |
| 35 | News | 69 | [`News.m3u`](USA/News.m3u) |
| 36 | News Backups | 41 | [`News_Backups.m3u`](USA/News_Backups.m3u) |
| 37 | A&E Networks | 61 | [`A_E_Networks.m3u`](USA/A_E_Networks.m3u) |
| 38 | A&E Networks Backups | 15 | [`A_E_Networks_Backups.m3u`](USA/A_E_Networks_Backups.m3u) |
| 39 | Education | 39 | [`Education.m3u`](USA/Education.m3u) |
| 40 | Education Backups | 3 | [`Education_Backups.m3u`](USA/Education_Backups.m3u) |
| 41 | Comedy | 31 | [`Comedy.m3u`](USA/Comedy.m3u) |
| 42 | Comedy Backups | 32 | [`Comedy_Backups.m3u`](USA/Comedy_Backups.m3u) |
| 43 | Classic TV | 23 | [`Classic_TV.m3u`](USA/Classic_TV.m3u) |
| 44 | Classic TV Backups | 16 | [`Classic_TV_Backups.m3u`](USA/Classic_TV_Backups.m3u) |
| 45 | Business | 17 | [`Business.m3u`](USA/Business.m3u) |
| 46 | Business Backups | 12 | [`Business_Backups.m3u`](USA/Business_Backups.m3u) |
| 47 | Culture | 17 | [`Culture.m3u`](USA/Culture.m3u) |
| 48 | Family | 14 | [`Family.m3u`](USA/Family.m3u) |
| 49 | Family Backups | 6 | [`Family_Backups.m3u`](USA/Family_Backups.m3u) |
| 50 | International | 7 | [`International.m3u`](USA/International.m3u) |
| 51 | Weather | 5 | [`Weather.m3u`](USA/Weather.m3u) |
| 52 | Weather Backups | 4 | [`Weather_Backups.m3u`](USA/Weather_Backups.m3u) |
| 53 | En Español | 3 | [`En_Espa_ol.m3u`](USA/En_Espa_ol.m3u) |
| 54 | En Español Backups | 10 | [`En_Espa_ol_Backups.m3u`](USA/En_Espa_ol_Backups.m3u) |
| 55 | Other | 8 | [`Other.m3u`](USA/Other.m3u) |

Groups smaller than 3 channels keep no file of their own (they would be a one-link playlist) - they stay in `USA.m3u`, which always holds every US channel.

## All countries

One file per category for the whole library (US channels first inside a category, because that is the published order).

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 516 | [`Sports.m3u`](All/Sports.m3u) |
| 2 | Sports Backups | 146 | [`Sports_Backups.m3u`](All/Sports_Backups.m3u) |
| 3 | Lifestyle | 510 | [`Lifestyle.m3u`](All/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 162 | [`Lifestyle_Backups.m3u`](All/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 45 | [`Fox_Channels.m3u`](All/Fox_Channels.m3u) |
| 6 | Fox Channels Backups | 3 | [`Fox_Channels_Backups.m3u`](All/Fox_Channels_Backups.m3u) |
| 7 | CBS | 45 | [`CBS.m3u`](All/CBS.m3u) |
| 8 | CBS Backups | 33 | [`CBS_Backups.m3u`](All/CBS_Backups.m3u) |
| 9 | NBC | 77 | [`NBC.m3u`](All/NBC.m3u) |
| 10 | NBC Backups | 17 | [`NBC_Backups.m3u`](All/NBC_Backups.m3u) |
| 11 | NBC Sports Channels | 6 | [`NBC_Sports_Channels.m3u`](All/NBC_Sports_Channels.m3u) |
| 12 | NBC Sports Channels Backups | 3 | [`NBC_Sports_Channels_Backups.m3u`](All/NBC_Sports_Channels_Backups.m3u) |
| 13 | Cartoons | 186 | [`Cartoons.m3u`](All/Cartoons.m3u) |
| 14 | Cartoons Backups | 56 | [`Cartoons_Backups.m3u`](All/Cartoons_Backups.m3u) |
| 15 | PBS | 41 | [`PBS.m3u`](All/PBS.m3u) |
| 16 | PBS Backups | 11 | [`PBS_Backups.m3u`](All/PBS_Backups.m3u) |
| 17 | Game Shows | 21 | [`Game_Shows.m3u`](All/Game_Shows.m3u) |
| 18 | Game Shows Backups | 31 | [`Game_Shows_Backups.m3u`](All/Game_Shows_Backups.m3u) |
| 19 | International | 876 | [`International.m3u`](All/International.m3u) |
| 20 | International Backups | 138 | [`International_Backups.m3u`](All/International_Backups.m3u) |
| 21 | News | 850 | [`News.m3u`](All/News.m3u) |
| 22 | News Backups | 228 | [`News_Backups.m3u`](All/News_Backups.m3u) |
| 23 | Music | 847 | [`Music.m3u`](All/Music.m3u) |
| 24 | Music Backups | 139 | [`Music_Backups.m3u`](All/Music_Backups.m3u) |
| 25 | Movies | 829 | [`Movies.m3u`](All/Movies.m3u) |
| 26 | Movies Backups | 188 | [`Movies_Backups.m3u`](All/Movies_Backups.m3u) |
| 27 | Europe | 707 | [`Europe.m3u`](All/Europe.m3u) |
| 28 | Europe Backups | 35 | [`Europe_Backups.m3u`](All/Europe_Backups.m3u) |
| 29 | Entertainment | 703 | [`Entertainment.m3u`](All/Entertainment.m3u) |
| 30 | Entertainment Backups | 147 | [`Entertainment_Backups.m3u`](All/Entertainment_Backups.m3u) |
| 31 | Religious | 617 | [`Religious.m3u`](All/Religious.m3u) |
| 32 | Religious Backups | 45 | [`Religious_Backups.m3u`](All/Religious_Backups.m3u) |
| 33 | South America | 481 | [`South_America.m3u`](All/South_America.m3u) |
| 34 | South America Backups | 22 | [`South_America_Backups.m3u`](All/South_America_Backups.m3u) |
| 35 | Asia | 475 | [`Asia.m3u`](All/Asia.m3u) |
| 36 | Asia Backups | 22 | [`Asia_Backups.m3u`](All/Asia_Backups.m3u) |
| 37 | United States | 366 | [`United_States.m3u`](All/United_States.m3u) |
| 38 | United States Backups | 56 | [`United_States_Backups.m3u`](All/United_States_Backups.m3u) |
| 39 | Documentary | 329 | [`Documentary.m3u`](All/Documentary.m3u) |
| 40 | Documentary Backups | 106 | [`Documentary_Backups.m3u`](All/Documentary_Backups.m3u) |
| 41 | Kids | 305 | [`Kids.m3u`](All/Kids.m3u) |
| 42 | Kids Backups | 103 | [`Kids_Backups.m3u`](All/Kids_Backups.m3u) |
| 43 | Series | 293 | [`Series.m3u`](All/Series.m3u) |
| 44 | Series Backups | 197 | [`Series_Backups.m3u`](All/Series_Backups.m3u) |
| 45 | North America | 292 | [`North_America.m3u`](All/North_America.m3u) |
| 46 | North America Backups | 4 | [`North_America_Backups.m3u`](All/North_America_Backups.m3u) |
| 47 | Education | 130 | [`Education.m3u`](All/Education.m3u) |
| 48 | Education Backups | 15 | [`Education_Backups.m3u`](All/Education_Backups.m3u) |
| 49 | Culture | 122 | [`Culture.m3u`](All/Culture.m3u) |
| 50 | Culture Backups | 8 | [`Culture_Backups.m3u`](All/Culture_Backups.m3u) |
| 51 | Comedy | 112 | [`Comedy.m3u`](All/Comedy.m3u) |
| 52 | Comedy Backups | 43 | [`Comedy_Backups.m3u`](All/Comedy_Backups.m3u) |
| 53 | Legislative | 112 | [`Legislative.m3u`](All/Legislative.m3u) |
| 54 | Legislative Backups | 3 | [`Legislative_Backups.m3u`](All/Legislative_Backups.m3u) |
| 55 | A&E Networks | 110 | [`A_E_Networks.m3u`](All/A_E_Networks.m3u) |
| 56 | A&E Networks Backups | 24 | [`A_E_Networks_Backups.m3u`](All/A_E_Networks_Backups.m3u) |
| 57 | India | 69 | [`India.m3u`](All/India.m3u) |
| 58 | India Backups | 9 | [`India_Backups.m3u`](All/India_Backups.m3u) |
| 59 | Africa | 68 | [`Africa.m3u`](All/Africa.m3u) |
| 60 | Canada | 58 | [`Canada.m3u`](All/Canada.m3u) |
| 61 | Business | 51 | [`Business.m3u`](All/Business.m3u) |
| 62 | Business Backups | 16 | [`Business_Backups.m3u`](All/Business_Backups.m3u) |
| 63 | Classic TV | 49 | [`Classic_TV.m3u`](All/Classic_TV.m3u) |
| 64 | Classic TV Backups | 22 | [`Classic_TV_Backups.m3u`](All/Classic_TV_Backups.m3u) |
| 65 | Family | 29 | [`Family.m3u`](All/Family.m3u) |
| 66 | Family Backups | 6 | [`Family_Backups.m3u`](All/Family_Backups.m3u) |
| 67 | En Español | 19 | [`En_Espa_ol.m3u`](All/En_Espa_ol.m3u) |
| 68 | En Español Backups | 10 | [`En_Espa_ol_Backups.m3u`](All/En_Espa_ol_Backups.m3u) |
| 69 | UK | 19 | [`UK.m3u`](All/UK.m3u) |
| 70 | Australia | 15 | [`Australia.m3u`](All/Australia.m3u) |
| 71 | Aria Web Channels | 13 | [`Aria_Web_Channels.m3u`](All/Aria_Web_Channels.m3u) |
| 72 | Weather | 12 | [`Weather.m3u`](All/Weather.m3u) |
| 73 | Weather Backups | 5 | [`Weather_Backups.m3u`](All/Weather_Backups.m3u) |
| 74 | Sci-Fi | 10 | [`Sci_Fi.m3u`](All/Sci_Fi.m3u) |
| 75 | Sci-Fi Backups | 8 | [`Sci_Fi_Backups.m3u`](All/Sci_Fi_Backups.m3u) |
| 76 | Animals & Nature | 9 | [`Animals_Nature.m3u`](All/Animals_Nature.m3u) |
| 77 | Animals & Nature Backups | 3 | [`Animals_Nature_Backups.m3u`](All/Animals_Nature_Backups.m3u) |
| 78 | DLTV | 9 | [`DLTV.m3u`](All/DLTV.m3u) |
| 79 | Drama | 8 | [`Drama.m3u`](All/Drama.m3u) |
| 80 | Drama Backups | 4 | [`Drama_Backups.m3u`](All/Drama_Backups.m3u) |
| 81 | Tv Celebrities | 8 | [`Tv_Celebrities.m3u`](All/Tv_Celebrities.m3u) |
| 82 | United Kingdom | 6 | [`United_Kingdom.m3u`](All/United_Kingdom.m3u) |
| 83 | Online TV | 5 | [`Online_TV.m3u`](All/Online_TV.m3u) |
| 84 | Online TV Backups | 8 | [`Online_TV_Backups.m3u`](All/Online_TV_Backups.m3u) |
| 85 | Tv Paranormal | 5 | [`Tv_Paranormal.m3u`](All/Tv_Paranormal.m3u) |
| 86 | Season's Greetings | 4 | [`Season_s_Greetings.m3u`](All/Season_s_Greetings.m3u) |
| 87 | Tv Shows | 4 | [`Tv_Shows.m3u`](All/Tv_Shows.m3u) |
| 88 | Westerns | 4 | [`Westerns.m3u`](All/Westerns.m3u) |
| 89 | Westerns Backups | 6 | [`Westerns_Backups.m3u`](All/Westerns_Backups.m3u) |
| 90 | Animals + Nature | 3 | [`Animals_Nature.m3u`](All/Animals_Nature.m3u) |
| 91 | Animals + Nature Backups | 3 | [`Animals_Nature_Backups.m3u`](All/Animals_Nature_Backups.m3u) |
| 92 | Relax | 3 | [`Relax.m3u`](All/Relax.m3u) |
| 93 | True Crime | 3 | [`True_Crime.m3u`](All/True_Crime.m3u) |
| 94 | Other | 201 | [`Other.m3u`](All/Other.m3u) |
| 95 | Other Backups | 114 | [`Other_Backups.m3u`](All/Other_Backups.m3u) |

Groups smaller than 3 channels keep no file of their own; they stay in `playlists/PremiumTV.m3u`.

## Load it

```text
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV/main/categories/USA.m3u          # every US channel, by category
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV/main/categories/USA/Sports.m3u   # just the US sports channels
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV/main/categories/All/Sports.m3u  # every sports channel in the library
```

## Keeping it in order

Rebuilt by `scripts/build_categories.py` after every scrape, deep check and quick update; a file is only rewritten when its channel list actually changed. `scripts/verify_playlists.py --require-shelf` re-plans the shelf from the published playlists and fails the run when a committed file is stale, so this directory can not drift away from the playlists it mirrors.
