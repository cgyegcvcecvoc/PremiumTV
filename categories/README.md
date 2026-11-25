# Category shelf

- **Shelf rebuilt:** 2026-11-25 13:18 UTC (2026-11-25 08:18 AM EST) — _manual re-scrape (run-scrape.txt)_
- **Sources:** [`playlists/PremiumTV.m3u`](../playlists/PremiumTV.m3u) for `All/`, [`playlists/live/USA.m3u`](../playlists/live/USA.m3u) for `USA.m3u` and `USA/`
- **Order:** Sports -> Lifestyle -> Fox Channels -> CBS -> NBC -> NBC Sports Channels -> Cartoons -> PBS -> Game Shows (each followed by its own Backups group), then the long tail by size, `Other` last — the published order from `scripts/categorize.py`.
- **One entry per channel:** a channel's spare feeds sit right after it in its `<category> Backups` group, best quality first.

Every file here is a slice of an already published playlist: same channels, same order, same group labels, same guide header. Nothing is re-classified, so loading the shelf can never show a channel the playlist does not have.

## USA

[`USA.m3u`](USA.m3u) — every one of the **3279** working US channels in one file, in category order. The per-category files below are the same list cut up.

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 111 | [`Sports.m3u`](USA/Sports.m3u) |
| 2 | Sports Backups | 85 | [`Sports_Backups.m3u`](USA/Sports_Backups.m3u) |
| 3 | Lifestyle | 150 | [`Lifestyle.m3u`](USA/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 97 | [`Lifestyle_Backups.m3u`](USA/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 41 | [`Fox_Channels.m3u`](USA/Fox_Channels.m3u) |
| 6 | Fox Channels Backups | 3 | [`Fox_Channels_Backups.m3u`](USA/Fox_Channels_Backups.m3u) |
| 7 | CBS | 40 | [`CBS.m3u`](USA/CBS.m3u) |
| 8 | CBS Backups | 32 | [`CBS_Backups.m3u`](USA/CBS_Backups.m3u) |
| 9 | NBC | 45 | [`NBC.m3u`](USA/NBC.m3u) |
| 10 | NBC Backups | 12 | [`NBC_Backups.m3u`](USA/NBC_Backups.m3u) |
| 11 | NBC Sports Channels | 3 | [`NBC_Sports_Channels.m3u`](USA/NBC_Sports_Channels.m3u) |
| 12 | Cartoons | 67 | [`Cartoons.m3u`](USA/Cartoons.m3u) |
| 13 | Cartoons Backups | 39 | [`Cartoons_Backups.m3u`](USA/Cartoons_Backups.m3u) |
| 14 | PBS | 21 | [`PBS.m3u`](USA/PBS.m3u) |
| 15 | PBS Backups | 5 | [`PBS_Backups.m3u`](USA/PBS_Backups.m3u) |
| 16 | Game Shows | 11 | [`Game_Shows.m3u`](USA/Game_Shows.m3u) |
| 17 | Game Shows Backups | 24 | [`Game_Shows_Backups.m3u`](USA/Game_Shows_Backups.m3u) |
| 18 | United States | 367 | [`United_States.m3u`](USA/United_States.m3u) |
| 19 | United States Backups | 64 | [`United_States_Backups.m3u`](USA/United_States_Backups.m3u) |
| 20 | Movies | 223 | [`Movies.m3u`](USA/Movies.m3u) |
| 21 | Movies Backups | 153 | [`Movies_Backups.m3u`](USA/Movies_Backups.m3u) |
| 22 | Series | 155 | [`Series.m3u`](USA/Series.m3u) |
| 23 | Series Backups | 178 | [`Series_Backups.m3u`](USA/Series_Backups.m3u) |
| 24 | Entertainment | 119 | [`Entertainment.m3u`](USA/Entertainment.m3u) |
| 25 | Entertainment Backups | 77 | [`Entertainment_Backups.m3u`](USA/Entertainment_Backups.m3u) |
| 26 | Religious | 117 | [`Religious.m3u`](USA/Religious.m3u) |
| 27 | Religious Backups | 12 | [`Religious_Backups.m3u`](USA/Religious_Backups.m3u) |
| 28 | Music | 96 | [`Music.m3u`](USA/Music.m3u) |
| 29 | Music Backups | 54 | [`Music_Backups.m3u`](USA/Music_Backups.m3u) |
| 30 | Documentary | 95 | [`Documentary.m3u`](USA/Documentary.m3u) |
| 31 | Documentary Backups | 70 | [`Documentary_Backups.m3u`](USA/Documentary_Backups.m3u) |
| 32 | Kids | 82 | [`Kids.m3u`](USA/Kids.m3u) |
| 33 | Kids Backups | 69 | [`Kids_Backups.m3u`](USA/Kids_Backups.m3u) |
| 34 | Legislative | 80 | [`Legislative.m3u`](USA/Legislative.m3u) |
| 35 | News | 71 | [`News.m3u`](USA/News.m3u) |
| 36 | News Backups | 43 | [`News_Backups.m3u`](USA/News_Backups.m3u) |
| 37 | A&E Networks | 63 | [`A_E_Networks.m3u`](USA/A_E_Networks.m3u) |
| 38 | A&E Networks Backups | 17 | [`A_E_Networks_Backups.m3u`](USA/A_E_Networks_Backups.m3u) |
| 39 | Education | 41 | [`Education.m3u`](USA/Education.m3u) |
| 40 | Education Backups | 3 | [`Education_Backups.m3u`](USA/Education_Backups.m3u) |
| 41 | Comedy | 30 | [`Comedy.m3u`](USA/Comedy.m3u) |
| 42 | Comedy Backups | 32 | [`Comedy_Backups.m3u`](USA/Comedy_Backups.m3u) |
| 43 | Classic TV | 23 | [`Classic_TV.m3u`](USA/Classic_TV.m3u) |
| 44 | Classic TV Backups | 16 | [`Classic_TV_Backups.m3u`](USA/Classic_TV_Backups.m3u) |
| 45 | Business | 18 | [`Business.m3u`](USA/Business.m3u) |
| 46 | Business Backups | 13 | [`Business_Backups.m3u`](USA/Business_Backups.m3u) |
| 47 | Culture | 18 | [`Culture.m3u`](USA/Culture.m3u) |
| 48 | Family | 15 | [`Family.m3u`](USA/Family.m3u) |
| 49 | Family Backups | 6 | [`Family_Backups.m3u`](USA/Family_Backups.m3u) |
| 50 | International | 10 | [`International.m3u`](USA/International.m3u) |
| 51 | Aria Web Channels | 5 | [`Aria_Web_Channels.m3u`](USA/Aria_Web_Channels.m3u) |
| 52 | Weather | 5 | [`Weather.m3u`](USA/Weather.m3u) |
| 53 | Weather Backups | 5 | [`Weather_Backups.m3u`](USA/Weather_Backups.m3u) |
| 54 | En Español | 3 | [`En_Espa_ol.m3u`](USA/En_Espa_ol.m3u) |
| 55 | En Español Backups | 10 | [`En_Espa_ol_Backups.m3u`](USA/En_Espa_ol_Backups.m3u) |
| 56 | Other | 10 | [`Other.m3u`](USA/Other.m3u) |

Groups smaller than 3 channels keep no file of their own (they would be a one-link playlist) - they stay in `USA.m3u`, which always holds every US channel.

## All countries

One file per category for the whole library (US channels first inside a category, because that is the published order).

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 532 | [`Sports.m3u`](All/Sports.m3u) |
| 2 | Sports Backups | 162 | [`Sports_Backups.m3u`](All/Sports_Backups.m3u) |
| 3 | Lifestyle | 514 | [`Lifestyle.m3u`](All/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 177 | [`Lifestyle_Backups.m3u`](All/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 48 | [`Fox_Channels.m3u`](All/Fox_Channels.m3u) |
| 6 | Fox Channels Backups | 3 | [`Fox_Channels_Backups.m3u`](All/Fox_Channels_Backups.m3u) |
| 7 | CBS | 45 | [`CBS.m3u`](All/CBS.m3u) |
| 8 | CBS Backups | 33 | [`CBS_Backups.m3u`](All/CBS_Backups.m3u) |
| 9 | NBC | 77 | [`NBC.m3u`](All/NBC.m3u) |
| 10 | NBC Backups | 19 | [`NBC_Backups.m3u`](All/NBC_Backups.m3u) |
| 11 | NBC Sports Channels | 6 | [`NBC_Sports_Channels.m3u`](All/NBC_Sports_Channels.m3u) |
| 12 | NBC Sports Channels Backups | 3 | [`NBC_Sports_Channels_Backups.m3u`](All/NBC_Sports_Channels_Backups.m3u) |
| 13 | Cartoons | 186 | [`Cartoons.m3u`](All/Cartoons.m3u) |
| 14 | Cartoons Backups | 60 | [`Cartoons_Backups.m3u`](All/Cartoons_Backups.m3u) |
| 15 | PBS | 41 | [`PBS.m3u`](All/PBS.m3u) |
| 16 | PBS Backups | 17 | [`PBS_Backups.m3u`](All/PBS_Backups.m3u) |
| 17 | Game Shows | 22 | [`Game_Shows.m3u`](All/Game_Shows.m3u) |
| 18 | Game Shows Backups | 32 | [`Game_Shows_Backups.m3u`](All/Game_Shows_Backups.m3u) |
| 19 | International | 1797 | [`International.m3u`](All/International.m3u) |
| 20 | International Backups | 262 | [`International_Backups.m3u`](All/International_Backups.m3u) |
| 21 | News | 876 | [`News.m3u`](All/News.m3u) |
| 22 | News Backups | 338 | [`News_Backups.m3u`](All/News_Backups.m3u) |
| 23 | Music | 862 | [`Music.m3u`](All/Music.m3u) |
| 24 | Music Backups | 170 | [`Music_Backups.m3u`](All/Music_Backups.m3u) |
| 25 | Movies | 828 | [`Movies.m3u`](All/Movies.m3u) |
| 26 | Movies Backups | 201 | [`Movies_Backups.m3u`](All/Movies_Backups.m3u) |
| 27 | Entertainment | 698 | [`Entertainment.m3u`](All/Entertainment.m3u) |
| 28 | Entertainment Backups | 181 | [`Entertainment_Backups.m3u`](All/Entertainment_Backups.m3u) |
| 29 | Religious | 616 | [`Religious.m3u`](All/Religious.m3u) |
| 30 | Religious Backups | 72 | [`Religious_Backups.m3u`](All/Religious_Backups.m3u) |
| 31 | Europe | 410 | [`Europe.m3u`](All/Europe.m3u) |
| 32 | Europe Backups | 39 | [`Europe_Backups.m3u`](All/Europe_Backups.m3u) |
| 33 | United States | 369 | [`United_States.m3u`](All/United_States.m3u) |
| 34 | United States Backups | 67 | [`United_States_Backups.m3u`](All/United_States_Backups.m3u) |
| 35 | Documentary | 333 | [`Documentary.m3u`](All/Documentary.m3u) |
| 36 | Documentary Backups | 113 | [`Documentary_Backups.m3u`](All/Documentary_Backups.m3u) |
| 37 | Kids | 308 | [`Kids.m3u`](All/Kids.m3u) |
| 38 | Kids Backups | 109 | [`Kids_Backups.m3u`](All/Kids_Backups.m3u) |
| 39 | Asia | 304 | [`Asia.m3u`](All/Asia.m3u) |
| 40 | Asia Backups | 7 | [`Asia_Backups.m3u`](All/Asia_Backups.m3u) |
| 41 | Series | 293 | [`Series.m3u`](All/Series.m3u) |
| 42 | Series Backups | 203 | [`Series_Backups.m3u`](All/Series_Backups.m3u) |
| 43 | South America | 235 | [`South_America.m3u`](All/South_America.m3u) |
| 44 | South America Backups | 5 | [`South_America_Backups.m3u`](All/South_America_Backups.m3u) |
| 45 | North America | 164 | [`North_America.m3u`](All/North_America.m3u) |
| 46 | North America Backups | 3 | [`North_America_Backups.m3u`](All/North_America_Backups.m3u) |
| 47 | Education | 126 | [`Education.m3u`](All/Education.m3u) |
| 48 | Education Backups | 14 | [`Education_Backups.m3u`](All/Education_Backups.m3u) |
| 49 | Culture | 124 | [`Culture.m3u`](All/Culture.m3u) |
| 50 | Culture Backups | 8 | [`Culture_Backups.m3u`](All/Culture_Backups.m3u) |
| 51 | Legislative | 113 | [`Legislative.m3u`](All/Legislative.m3u) |
| 52 | Legislative Backups | 5 | [`Legislative_Backups.m3u`](All/Legislative_Backups.m3u) |
| 53 | A&E Networks | 112 | [`A_E_Networks.m3u`](All/A_E_Networks.m3u) |
| 54 | A&E Networks Backups | 27 | [`A_E_Networks_Backups.m3u`](All/A_E_Networks_Backups.m3u) |
| 55 | Comedy | 108 | [`Comedy.m3u`](All/Comedy.m3u) |
| 56 | Comedy Backups | 44 | [`Comedy_Backups.m3u`](All/Comedy_Backups.m3u) |
| 57 | India | 91 | [`India.m3u`](All/India.m3u) |
| 58 | India Backups | 26 | [`India_Backups.m3u`](All/India_Backups.m3u) |
| 59 | Business | 54 | [`Business.m3u`](All/Business.m3u) |
| 60 | Business Backups | 20 | [`Business_Backups.m3u`](All/Business_Backups.m3u) |
| 61 | Canada | 52 | [`Canada.m3u`](All/Canada.m3u) |
| 62 | Classic TV | 49 | [`Classic_TV.m3u`](All/Classic_TV.m3u) |
| 63 | Classic TV Backups | 23 | [`Classic_TV_Backups.m3u`](All/Classic_TV_Backups.m3u) |
| 64 | Andalucía | 47 | [`Andaluc_a.m3u`](All/Andaluc_a.m3u) |
| 65 | Andalucía Backups | 4 | [`Andaluc_a_Backups.m3u`](All/Andaluc_a_Backups.m3u) |
| 66 | Family | 29 | [`Family.m3u`](All/Family.m3u) |
| 67 | Family Backups | 7 | [`Family_Backups.m3u`](All/Family_Backups.m3u) |
| 68 | Africa | 27 | [`Africa.m3u`](All/Africa.m3u) |
| 69 | En Español | 19 | [`En_Espa_ol.m3u`](All/En_Espa_ol.m3u) |
| 70 | En Español Backups | 11 | [`En_Espa_ol_Backups.m3u`](All/En_Espa_ol_Backups.m3u) |
| 71 | Australia | 16 | [`Australia.m3u`](All/Australia.m3u) |
| 72 | C. Valenciana | 15 | [`C_Valenciana.m3u`](All/C_Valenciana.m3u) |
| 73 | Cataluña | 15 | [`Catalu_a.m3u`](All/Catalu_a.m3u) |
| 74 | Musicales | 15 | [`Musicales.m3u`](All/Musicales.m3u) |
| 75 | Musicales Backups | 8 | [`Musicales_Backups.m3u`](All/Musicales_Backups.m3u) |
| 76 | UK | 15 | [`UK.m3u`](All/UK.m3u) |
| 77 | United Kingdom | 15 | [`United_Kingdom.m3u`](All/United_Kingdom.m3u) |
| 78 | Aria Web Channels | 13 | [`Aria_Web_Channels.m3u`](All/Aria_Web_Channels.m3u) |
| 79 | Canarias | 12 | [`Canarias.m3u`](All/Canarias.m3u) |
| 80 | Canarias Backups | 4 | [`Canarias_Backups.m3u`](All/Canarias_Backups.m3u) |
| 81 | Int. América | 12 | [`Int_Am_rica.m3u`](All/Int_Am_rica.m3u) |
| 82 | Int. América Backups | 4 | [`Int_Am_rica_Backups.m3u`](All/Int_Am_rica_Backups.m3u) |
| 83 | Weather | 12 | [`Weather.m3u`](All/Weather.m3u) |
| 84 | Weather Backups | 6 | [`Weather_Backups.m3u`](All/Weather_Backups.m3u) |
| 85 | Eventuales | 11 | [`Eventuales.m3u`](All/Eventuales.m3u) |
| 86 | Eventuales Backups | 17 | [`Eventuales_Backups.m3u`](All/Eventuales_Backups.m3u) |
| 87 | Int. Europa | 11 | [`Int_Europa.m3u`](All/Int_Europa.m3u) |
| 88 | Int. Europa Backups | 4 | [`Int_Europa_Backups.m3u`](All/Int_Europa_Backups.m3u) |
| 89 | Galicia | 10 | [`Galicia.m3u`](All/Galicia.m3u) |
| 90 | Galicia Backups | 5 | [`Galicia_Backups.m3u`](All/Galicia_Backups.m3u) |
| 91 | Sci-Fi | 10 | [`Sci_Fi.m3u`](All/Sci_Fi.m3u) |
| 92 | Sci-Fi Backups | 8 | [`Sci_Fi_Backups.m3u`](All/Sci_Fi_Backups.m3u) |
| 93 | Animals & Nature | 12 | [`Animals_Nature.m3u`](All/Animals_Nature.m3u) |
| 94 | Animals & Nature Backups | 6 | [`Animals_Nature_Backups.m3u`](All/Animals_Nature_Backups.m3u) |
| 95 | DLTV | 9 | [`DLTV.m3u`](All/DLTV.m3u) |
| 96 | País Vasco | 9 | [`Pa_s_Vasco.m3u`](All/Pa_s_Vasco.m3u) |
| 97 | Drama | 8 | [`Drama.m3u`](All/Drama.m3u) |
| 98 | Drama Backups | 4 | [`Drama_Backups.m3u`](All/Drama_Backups.m3u) |
| 99 | Int. Otros | 7 | [`Int_Otros.m3u`](All/Int_Otros.m3u) |
| 100 | Religiosos | 7 | [`Religiosos.m3u`](All/Religiosos.m3u) |
| 101 | Tv Celebrities | 7 | [`Tv_Celebrities.m3u`](All/Tv_Celebrities.m3u) |
| 102 | C. de Madrid | 6 | [`C_de_Madrid.m3u`](All/C_de_Madrid.m3u) |
| 103 | C. de Madrid Backups | 3 | [`C_de_Madrid_Backups.m3u`](All/C_de_Madrid_Backups.m3u) |
| 104 | Castilla-La Mancha | 6 | [`Castilla_La_Mancha.m3u`](All/Castilla_La_Mancha.m3u) |
| 105 | Infantiles | 6 | [`Infantiles.m3u`](All/Infantiles.m3u) |
| 106 | Int. Asia | 5 | [`Int_Asia.m3u`](All/Int_Asia.m3u) |
| 107 | Online TV | 5 | [`Online_TV.m3u`](All/Online_TV.m3u) |
| 108 | Online TV Backups | 22 | [`Online_TV_Backups.m3u`](All/Online_TV_Backups.m3u) |
| 109 | Tv Paranormal | 5 | [`Tv_Paranormal.m3u`](All/Tv_Paranormal.m3u) |
| 110 | Cantabria | 4 | [`Cantabria.m3u`](All/Cantabria.m3u) |
| 111 | Season's Greetings | 4 | [`Season_s_Greetings.m3u`](All/Season_s_Greetings.m3u) |
| 112 | Tv Shows | 4 | [`Tv_Shows.m3u`](All/Tv_Shows.m3u) |
| 113 | Westerns | 4 | [`Westerns.m3u`](All/Westerns.m3u) |
| 114 | Westerns Backups | 6 | [`Westerns_Backups.m3u`](All/Westerns_Backups.m3u) |
| 115 | Extremadura | 3 | [`Extremadura.m3u`](All/Extremadura.m3u) |
| 116 | Generalistas | 3 | [`Generalistas.m3u`](All/Generalistas.m3u) |
| 117 | Global TV | 3 | [`Global_TV.m3u`](All/Global_TV.m3u) |
| 118 | Int. África | 3 | [`Int_frica.m3u`](All/Int_frica.m3u) |
| 119 | Int. África Backups | 4 | [`Int_frica_Backups.m3u`](All/Int_frica_Backups.m3u) |
| 120 | R. de Murcia | 3 | [`R_de_Murcia.m3u`](All/R_de_Murcia.m3u) |
| 121 | Relax | 3 | [`Relax.m3u`](All/Relax.m3u) |
| 122 | True Crime | 3 | [`True_Crime.m3u`](All/True_Crime.m3u) |
| 123 | Castilla y León Backups | 3 | [`Castilla_y_Le_n_Backups.m3u`](All/Castilla_y_Le_n_Backups.m3u) |
| 124 | Other | 252 | [`Other.m3u`](All/Other.m3u) |
| 125 | Other Backups | 372 | [`Other_Backups.m3u`](All/Other_Backups.m3u) |

Groups smaller than 3 channels keep no file of their own; they stay in `playlists/PremiumTV.m3u`.

## Load it

```text
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV/main/categories/USA.m3u          # every US channel, by category
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV/main/categories/USA/Sports.m3u   # just the US sports channels
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV/main/categories/All/Sports.m3u  # every sports channel in the library
```

## Keeping it in order

Rebuilt by `scripts/build_categories.py` after every scrape, deep check and quick update; a file is only rewritten when its channel list actually changed. `scripts/verify_playlists.py --require-shelf` re-plans the shelf from the published playlists and fails the run when a committed file is stale, so this directory can not drift away from the playlists it mirrors.
