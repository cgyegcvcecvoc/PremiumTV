# Category shelf

- **Shelf rebuilt:** 2026-11-25 20:30 UTC (2026-11-25 03:30 PM EST) — _source audit 2026-11-25_
- **Sources:** [`playlists/PremiumTV.m3u`](../playlists/PremiumTV.m3u) for `All/`, [`playlists/live/USA.m3u`](../playlists/live/USA.m3u) for `USA.m3u` and `USA/`
- **Order:** Sports -> Lifestyle -> Fox Channels -> CBS -> NBC -> NBC Sports Channels -> Cartoons -> PBS -> Game Shows (each followed by its own Backups group), then the long tail by size, `Other` last — the published order from `scripts/categorize.py`.
- **One entry per channel:** a channel's spare feeds sit right after it in its `<category> Backups` group, best quality first.

Every file here is a slice of an already published playlist: same channels, same order, same group labels, same guide header. Nothing is re-classified, so loading the shelf can never show a channel the playlist does not have.

## USA

[`USA.m3u`](USA.m3u) — every one of the **4437** working US channels in one file, in category order. The per-category files below are the same list cut up.

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 156 | [`Sports.m3u`](USA/Sports.m3u) |
| 2 | Sports Backups | 129 | [`Sports_Backups.m3u`](USA/Sports_Backups.m3u) |
| 3 | Lifestyle | 176 | [`Lifestyle.m3u`](USA/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 140 | [`Lifestyle_Backups.m3u`](USA/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 42 | [`Fox_Channels.m3u`](USA/Fox_Channels.m3u) |
| 6 | Fox Channels Backups | 12 | [`Fox_Channels_Backups.m3u`](USA/Fox_Channels_Backups.m3u) |
| 7 | CBS | 41 | [`CBS.m3u`](USA/CBS.m3u) |
| 8 | CBS Backups | 34 | [`CBS_Backups.m3u`](USA/CBS_Backups.m3u) |
| 9 | NBC | 50 | [`NBC.m3u`](USA/NBC.m3u) |
| 10 | NBC Backups | 20 | [`NBC_Backups.m3u`](USA/NBC_Backups.m3u) |
| 11 | NBC Sports Channels | 4 | [`NBC_Sports_Channels.m3u`](USA/NBC_Sports_Channels.m3u) |
| 12 | NBC Sports Channels Backups | 4 | [`NBC_Sports_Channels_Backups.m3u`](USA/NBC_Sports_Channels_Backups.m3u) |
| 13 | Cartoons | 70 | [`Cartoons.m3u`](USA/Cartoons.m3u) |
| 14 | Cartoons Backups | 45 | [`Cartoons_Backups.m3u`](USA/Cartoons_Backups.m3u) |
| 15 | PBS | 25 | [`PBS.m3u`](USA/PBS.m3u) |
| 16 | PBS Backups | 8 | [`PBS_Backups.m3u`](USA/PBS_Backups.m3u) |
| 17 | Game Shows | 15 | [`Game_Shows.m3u`](USA/Game_Shows.m3u) |
| 18 | Game Shows Backups | 37 | [`Game_Shows_Backups.m3u`](USA/Game_Shows_Backups.m3u) |
| 19 | United States | 758 | [`United_States.m3u`](USA/United_States.m3u) |
| 20 | United States Backups | 218 | [`United_States_Backups.m3u`](USA/United_States_Backups.m3u) |
| 21 | Movies | 251 | [`Movies.m3u`](USA/Movies.m3u) |
| 22 | Movies Backups | 196 | [`Movies_Backups.m3u`](USA/Movies_Backups.m3u) |
| 23 | Series | 137 | [`Series.m3u`](USA/Series.m3u) |
| 24 | Series Backups | 179 | [`Series_Backups.m3u`](USA/Series_Backups.m3u) |
| 25 | Entertainment | 133 | [`Entertainment.m3u`](USA/Entertainment.m3u) |
| 26 | Entertainment Backups | 116 | [`Entertainment_Backups.m3u`](USA/Entertainment_Backups.m3u) |
| 27 | Music | 129 | [`Music.m3u`](USA/Music.m3u) |
| 28 | Music Backups | 72 | [`Music_Backups.m3u`](USA/Music_Backups.m3u) |
| 29 | Religious | 118 | [`Religious.m3u`](USA/Religious.m3u) |
| 30 | Religious Backups | 14 | [`Religious_Backups.m3u`](USA/Religious_Backups.m3u) |
| 31 | Documentary | 103 | [`Documentary.m3u`](USA/Documentary.m3u) |
| 32 | Documentary Backups | 83 | [`Documentary_Backups.m3u`](USA/Documentary_Backups.m3u) |
| 33 | Kids | 82 | [`Kids.m3u`](USA/Kids.m3u) |
| 34 | Kids Backups | 78 | [`Kids_Backups.m3u`](USA/Kids_Backups.m3u) |
| 35 | News | 81 | [`News.m3u`](USA/News.m3u) |
| 36 | News Backups | 69 | [`News_Backups.m3u`](USA/News_Backups.m3u) |
| 37 | Legislative | 80 | [`Legislative.m3u`](USA/Legislative.m3u) |
| 38 | A&E Networks | 59 | [`A_E_Networks.m3u`](USA/A_E_Networks.m3u) |
| 39 | A&E Networks Backups | 85 | [`A_E_Networks_Backups.m3u`](USA/A_E_Networks_Backups.m3u) |
| 40 | Education | 41 | [`Education.m3u`](USA/Education.m3u) |
| 41 | Education Backups | 3 | [`Education_Backups.m3u`](USA/Education_Backups.m3u) |
| 42 | Comedy | 28 | [`Comedy.m3u`](USA/Comedy.m3u) |
| 43 | Comedy Backups | 42 | [`Comedy_Backups.m3u`](USA/Comedy_Backups.m3u) |
| 44 | International | 26 | [`International.m3u`](USA/International.m3u) |
| 45 | International Backups | 33 | [`International_Backups.m3u`](USA/International_Backups.m3u) |
| 46 | Classic TV | 23 | [`Classic_TV.m3u`](USA/Classic_TV.m3u) |
| 47 | Classic TV Backups | 17 | [`Classic_TV_Backups.m3u`](USA/Classic_TV_Backups.m3u) |
| 48 | Business | 19 | [`Business.m3u`](USA/Business.m3u) |
| 49 | Business Backups | 19 | [`Business_Backups.m3u`](USA/Business_Backups.m3u) |
| 50 | Culture | 18 | [`Culture.m3u`](USA/Culture.m3u) |
| 51 | Family | 15 | [`Family.m3u`](USA/Family.m3u) |
| 52 | Family Backups | 6 | [`Family_Backups.m3u`](USA/Family_Backups.m3u) |
| 53 | Canada | 6 | [`Canada.m3u`](USA/Canada.m3u) |
| 54 | Canada Backups | 16 | [`Canada_Backups.m3u`](USA/Canada_Backups.m3u) |
| 55 | Aria Web Channels | 5 | [`Aria_Web_Channels.m3u`](USA/Aria_Web_Channels.m3u) |
| 56 | Weather | 5 | [`Weather.m3u`](USA/Weather.m3u) |
| 57 | Weather Backups | 8 | [`Weather_Backups.m3u`](USA/Weather_Backups.m3u) |
| 58 | En Español | 3 | [`En_Espa_ol.m3u`](USA/En_Espa_ol.m3u) |
| 59 | En Español Backups | 10 | [`En_Espa_ol_Backups.m3u`](USA/En_Espa_ol_Backups.m3u) |
| 60 | United Kingdom | 3 | [`United_Kingdom.m3u`](USA/United_Kingdom.m3u) |
| 61 | United Kingdom Backups | 7 | [`United_Kingdom_Backups.m3u`](USA/United_Kingdom_Backups.m3u) |
| 62 | Other | 9 | [`Other.m3u`](USA/Other.m3u) |

Groups smaller than 3 channels keep no file of their own (they would be a one-link playlist) - they stay in `USA.m3u`, which always holds every US channel.

## All countries

One file per category for the whole library (US channels first inside a category, because that is the published order).

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 764 | [`Sports.m3u`](All/Sports.m3u) |
| 2 | Sports Backups | 254 | [`Sports_Backups.m3u`](All/Sports_Backups.m3u) |
| 3 | Lifestyle | 641 | [`Lifestyle.m3u`](All/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 229 | [`Lifestyle_Backups.m3u`](All/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 52 | [`Fox_Channels.m3u`](All/Fox_Channels.m3u) |
| 6 | Fox Channels Backups | 13 | [`Fox_Channels_Backups.m3u`](All/Fox_Channels_Backups.m3u) |
| 7 | CBS | 46 | [`CBS.m3u`](All/CBS.m3u) |
| 8 | CBS Backups | 35 | [`CBS_Backups.m3u`](All/CBS_Backups.m3u) |
| 9 | NBC | 90 | [`NBC.m3u`](All/NBC.m3u) |
| 10 | NBC Backups | 34 | [`NBC_Backups.m3u`](All/NBC_Backups.m3u) |
| 11 | NBC Sports Channels | 7 | [`NBC_Sports_Channels.m3u`](All/NBC_Sports_Channels.m3u) |
| 12 | NBC Sports Channels Backups | 5 | [`NBC_Sports_Channels_Backups.m3u`](All/NBC_Sports_Channels_Backups.m3u) |
| 13 | Cartoons | 220 | [`Cartoons.m3u`](All/Cartoons.m3u) |
| 14 | Cartoons Backups | 71 | [`Cartoons_Backups.m3u`](All/Cartoons_Backups.m3u) |
| 15 | PBS | 46 | [`PBS.m3u`](All/PBS.m3u) |
| 16 | PBS Backups | 22 | [`PBS_Backups.m3u`](All/PBS_Backups.m3u) |
| 17 | Game Shows | 42 | [`Game_Shows.m3u`](All/Game_Shows.m3u) |
| 18 | Game Shows Backups | 52 | [`Game_Shows_Backups.m3u`](All/Game_Shows_Backups.m3u) |
| 19 | International | 3006 | [`International.m3u`](All/International.m3u) |
| 20 | International Backups | 490 | [`International_Backups.m3u`](All/International_Backups.m3u) |
| 21 | Music | 1030 | [`Music.m3u`](All/Music.m3u) |
| 22 | Music Backups | 221 | [`Music_Backups.m3u`](All/Music_Backups.m3u) |
| 23 | News | 998 | [`News.m3u`](All/News.m3u) |
| 24 | News Backups | 418 | [`News_Backups.m3u`](All/News_Backups.m3u) |
| 25 | Movies | 996 | [`Movies.m3u`](All/Movies.m3u) |
| 26 | Movies Backups | 287 | [`Movies_Backups.m3u`](All/Movies_Backups.m3u) |
| 27 | Entertainment | 811 | [`Entertainment.m3u`](All/Entertainment.m3u) |
| 28 | Entertainment Backups | 245 | [`Entertainment_Backups.m3u`](All/Entertainment_Backups.m3u) |
| 29 | United States | 761 | [`United_States.m3u`](All/United_States.m3u) |
| 30 | United States Backups | 222 | [`United_States_Backups.m3u`](All/United_States_Backups.m3u) |
| 31 | Religious | 632 | [`Religious.m3u`](All/Religious.m3u) |
| 32 | Religious Backups | 76 | [`Religious_Backups.m3u`](All/Religious_Backups.m3u) |
| 33 | Europe | 411 | [`Europe.m3u`](All/Europe.m3u) |
| 34 | Europe Backups | 37 | [`Europe_Backups.m3u`](All/Europe_Backups.m3u) |
| 35 | Documentary | 409 | [`Documentary.m3u`](All/Documentary.m3u) |
| 36 | Documentary Backups | 142 | [`Documentary_Backups.m3u`](All/Documentary_Backups.m3u) |
| 37 | Canada | 367 | [`Canada.m3u`](All/Canada.m3u) |
| 38 | Canada Backups | 66 | [`Canada_Backups.m3u`](All/Canada_Backups.m3u) |
| 39 | Kids | 331 | [`Kids.m3u`](All/Kids.m3u) |
| 40 | Kids Backups | 125 | [`Kids_Backups.m3u`](All/Kids_Backups.m3u) |
| 41 | Asia | 296 | [`Asia.m3u`](All/Asia.m3u) |
| 42 | Asia Backups | 5 | [`Asia_Backups.m3u`](All/Asia_Backups.m3u) |
| 43 | United Kingdom | 296 | [`United_Kingdom.m3u`](All/United_Kingdom.m3u) |
| 44 | United Kingdom Backups | 43 | [`United_Kingdom_Backups.m3u`](All/United_Kingdom_Backups.m3u) |
| 45 | Series | 262 | [`Series.m3u`](All/Series.m3u) |
| 46 | Series Backups | 209 | [`Series_Backups.m3u`](All/Series_Backups.m3u) |
| 47 | South America | 249 | [`South_America.m3u`](All/South_America.m3u) |
| 48 | South America Backups | 6 | [`South_America_Backups.m3u`](All/South_America_Backups.m3u) |
| 49 | North America | 162 | [`North_America.m3u`](All/North_America.m3u) |
| 50 | North America Backups | 5 | [`North_America_Backups.m3u`](All/North_America_Backups.m3u) |
| 51 | Australia | 157 | [`Australia.m3u`](All/Australia.m3u) |
| 52 | Australia Backups | 3 | [`Australia_Backups.m3u`](All/Australia_Backups.m3u) |
| 53 | India | 157 | [`India.m3u`](All/India.m3u) |
| 54 | India Backups | 30 | [`India_Backups.m3u`](All/India_Backups.m3u) |
| 55 | Education | 129 | [`Education.m3u`](All/Education.m3u) |
| 56 | Education Backups | 15 | [`Education_Backups.m3u`](All/Education_Backups.m3u) |
| 57 | A&E Networks | 127 | [`A_E_Networks.m3u`](All/A_E_Networks.m3u) |
| 58 | A&E Networks Backups | 113 | [`A_E_Networks_Backups.m3u`](All/A_E_Networks_Backups.m3u) |
| 59 | Culture | 123 | [`Culture.m3u`](All/Culture.m3u) |
| 60 | Culture Backups | 7 | [`Culture_Backups.m3u`](All/Culture_Backups.m3u) |
| 61 | Comedy | 112 | [`Comedy.m3u`](All/Comedy.m3u) |
| 62 | Comedy Backups | 58 | [`Comedy_Backups.m3u`](All/Comedy_Backups.m3u) |
| 63 | Legislative | 112 | [`Legislative.m3u`](All/Legislative.m3u) |
| 64 | Legislative Backups | 4 | [`Legislative_Backups.m3u`](All/Legislative_Backups.m3u) |
| 65 | NZ | 92 | [`NZ.m3u`](All/NZ.m3u) |
| 66 | NZ Backups | 24 | [`NZ_Backups.m3u`](All/NZ_Backups.m3u) |
| 67 | Business | 75 | [`Business.m3u`](All/Business.m3u) |
| 68 | Business Backups | 29 | [`Business_Backups.m3u`](All/Business_Backups.m3u) |
| 69 | Andalucía | 55 | [`Andaluc_a.m3u`](All/Andaluc_a.m3u) |
| 70 | Andalucía Backups | 4 | [`Andaluc_a_Backups.m3u`](All/Andaluc_a_Backups.m3u) |
| 71 | Classic TV | 50 | [`Classic_TV.m3u`](All/Classic_TV.m3u) |
| 72 | Classic TV Backups | 27 | [`Classic_TV_Backups.m3u`](All/Classic_TV_Backups.m3u) |
| 73 | Family | 31 | [`Family.m3u`](All/Family.m3u) |
| 74 | Family Backups | 7 | [`Family_Backups.m3u`](All/Family_Backups.m3u) |
| 75 | Africa | 28 | [`Africa.m3u`](All/Africa.m3u) |
| 76 | Cataluña | 23 | [`Catalu_a.m3u`](All/Catalu_a.m3u) |
| 77 | Fast Tubi | 21 | [`Fast_Tubi.m3u`](All/Fast_Tubi.m3u) |
| 78 | En Español | 20 | [`En_Espa_ol.m3u`](All/En_Espa_ol.m3u) |
| 79 | En Español Backups | 13 | [`En_Espa_ol_Backups.m3u`](All/En_Espa_ol_Backups.m3u) |
| 80 | Musicales | 16 | [`Musicales.m3u`](All/Musicales.m3u) |
| 81 | Musicales Backups | 8 | [`Musicales_Backups.m3u`](All/Musicales_Backups.m3u) |
| 82 | C. Valenciana | 15 | [`C_Valenciana.m3u`](All/C_Valenciana.m3u) |
| 83 | Int. América | 15 | [`Int_Am_rica.m3u`](All/Int_Am_rica.m3u) |
| 84 | Int. América Backups | 5 | [`Int_Am_rica_Backups.m3u`](All/Int_Am_rica_Backups.m3u) |
| 85 | UK | 15 | [`UK.m3u`](All/UK.m3u) |
| 86 | Aria Web Channels | 13 | [`Aria_Web_Channels.m3u`](All/Aria_Web_Channels.m3u) |
| 87 | Canarias | 12 | [`Canarias.m3u`](All/Canarias.m3u) |
| 88 | Canarias Backups | 4 | [`Canarias_Backups.m3u`](All/Canarias_Backups.m3u) |
| 89 | Drama | 12 | [`Drama.m3u`](All/Drama.m3u) |
| 90 | Drama Backups | 14 | [`Drama_Backups.m3u`](All/Drama_Backups.m3u) |
| 91 | Weather | 12 | [`Weather.m3u`](All/Weather.m3u) |
| 92 | Weather Backups | 10 | [`Weather_Backups.m3u`](All/Weather_Backups.m3u) |
| 93 | Eventuales | 11 | [`Eventuales.m3u`](All/Eventuales.m3u) |
| 94 | Eventuales Backups | 22 | [`Eventuales_Backups.m3u`](All/Eventuales_Backups.m3u) |
| 95 | Int. Europa | 11 | [`Int_Europa.m3u`](All/Int_Europa.m3u) |
| 96 | Int. Europa Backups | 4 | [`Int_Europa_Backups.m3u`](All/Int_Europa_Backups.m3u) |
| 97 | Galicia | 10 | [`Galicia.m3u`](All/Galicia.m3u) |
| 98 | Galicia Backups | 5 | [`Galicia_Backups.m3u`](All/Galicia_Backups.m3u) |
| 99 | Sci-Fi | 10 | [`Sci_Fi.m3u`](All/Sci_Fi.m3u) |
| 100 | Sci-Fi Backups | 9 | [`Sci_Fi_Backups.m3u`](All/Sci_Fi_Backups.m3u) |
| 101 | DLTV | 9 | [`DLTV.m3u`](All/DLTV.m3u) |
| 102 | País Vasco | 9 | [`Pa_s_Vasco.m3u`](All/Pa_s_Vasco.m3u) |
| 103 | Infantiles | 7 | [`Infantiles.m3u`](All/Infantiles.m3u) |
| 104 | Int. Otros | 7 | [`Int_Otros.m3u`](All/Int_Otros.m3u) |
| 105 | Religiosos | 7 | [`Religiosos.m3u`](All/Religiosos.m3u) |
| 106 | True Crime | 7 | [`True_Crime.m3u`](All/True_Crime.m3u) |
| 107 | True Crime Backups | 7 | [`True_Crime_Backups.m3u`](All/True_Crime_Backups.m3u) |
| 108 | C. de Madrid | 6 | [`C_de_Madrid.m3u`](All/C_de_Madrid.m3u) |
| 109 | C. de Madrid Backups | 3 | [`C_de_Madrid_Backups.m3u`](All/C_de_Madrid_Backups.m3u) |
| 110 | Castilla-La Mancha | 6 | [`Castilla_La_Mancha.m3u`](All/Castilla_La_Mancha.m3u) |
| 111 | Tv Celebrities | 6 | [`Tv_Celebrities.m3u`](All/Tv_Celebrities.m3u) |
| 112 | Int. Asia | 5 | [`Int_Asia.m3u`](All/Int_Asia.m3u) |
| 113 | Online TV | 5 | [`Online_TV.m3u`](All/Online_TV.m3u) |
| 114 | Online TV Backups | 7 | [`Online_TV_Backups.m3u`](All/Online_TV_Backups.m3u) |
| 115 | Westerns | 5 | [`Westerns.m3u`](All/Westerns.m3u) |
| 116 | Westerns Backups | 8 | [`Westerns_Backups.m3u`](All/Westerns_Backups.m3u) |
| 117 | Animals + Nature | 7 | [`Animals_Nature.m3u`](All/Animals_Nature.m3u) |
| 118 | Animals + Nature Backups | 8 | [`Animals_Nature_Backups.m3u`](All/Animals_Nature_Backups.m3u) |
| 119 | Cantabria | 4 | [`Cantabria.m3u`](All/Cantabria.m3u) |
| 120 | Romance | 4 | [`Romance.m3u`](All/Romance.m3u) |
| 121 | Season's Greetings | 4 | [`Season_s_Greetings.m3u`](All/Season_s_Greetings.m3u) |
| 122 | Tv Paranormal | 4 | [`Tv_Paranormal.m3u`](All/Tv_Paranormal.m3u) |
| 123 | Crime | 3 | [`Crime.m3u`](All/Crime.m3u) |
| 124 | Extremadura | 3 | [`Extremadura.m3u`](All/Extremadura.m3u) |
| 125 | Generalistas | 3 | [`Generalistas.m3u`](All/Generalistas.m3u) |
| 126 | Int. África | 3 | [`Int_frica.m3u`](All/Int_frica.m3u) |
| 127 | Int. África Backups | 5 | [`Int_frica_Backups.m3u`](All/Int_frica_Backups.m3u) |
| 128 | R. de Murcia | 3 | [`R_de_Murcia.m3u`](All/R_de_Murcia.m3u) |
| 129 | Relax | 3 | [`Relax.m3u`](All/Relax.m3u) |
| 130 | Castilla y León Backups | 3 | [`Castilla_y_Le_n_Backups.m3u`](All/Castilla_y_Le_n_Backups.m3u) |
| 131 | Other | 175 | [`Other.m3u`](All/Other.m3u) |
| 132 | Other Backups | 332 | [`Other_Backups.m3u`](All/Other_Backups.m3u) |

Groups smaller than 3 channels keep no file of their own; they stay in `playlists/PremiumTV.m3u`.

## Load it

```text
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV/main/categories/USA.m3u          # every US channel, by category
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV/main/categories/USA/Sports.m3u   # just the US sports channels
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV/main/categories/All/Sports.m3u  # every sports channel in the library
```

## Keeping it in order

Rebuilt by `scripts/build_categories.py` after every scrape, deep check and quick update; a file is only rewritten when its channel list actually changed. `scripts/verify_playlists.py --require-shelf` re-plans the shelf from the published playlists and fails the run when a committed file is stale, so this directory can not drift away from the playlists it mirrors.
