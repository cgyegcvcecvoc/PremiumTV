# Category shelf

- **Shelf rebuilt:** 2026-11-28 03:38 UTC (2026-11-27 10:38 PM EST) — _4:41 PM final check_
- **Sources:** [`playlists/PremiumTV.m3u`](../playlists/PremiumTV.m3u) for `All/`, [`playlists/live/USA.m3u`](../playlists/live/USA.m3u) for `USA.m3u` and `USA/`
- **Order:** Sports -> Lifestyle -> Fox Channels -> CBS -> NBC -> NBC Sports Channels -> Cartoons -> PBS -> Game Shows (each followed by its own Backups group), then the long tail by size, `Other` last — the published order from `scripts/categorize.py`.
- **One entry per channel:** a channel's spare feeds sit right after it in its `<category> Backups` group, best quality first.

Every file here is a slice of an already published playlist: same channels, same order, same group labels, same guide header. Nothing is re-classified, so loading the shelf can never show a channel the playlist does not have.

## USA

[`USA.m3u`](USA.m3u) — every one of the **3905** working US channels in one file, in category order. The per-category files below are the same list cut up.

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 200 | [`Sports.m3u`](USA/Sports.m3u) |
| 2 | Sports Backups | 102 | [`Sports_Backups.m3u`](USA/Sports_Backups.m3u) |
| 3 | Lifestyle | 162 | [`Lifestyle.m3u`](USA/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 118 | [`Lifestyle_Backups.m3u`](USA/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 44 | [`Fox_Channels.m3u`](USA/Fox_Channels.m3u) |
| 6 | Fox Channels Backups | 11 | [`Fox_Channels_Backups.m3u`](USA/Fox_Channels_Backups.m3u) |
| 7 | CBS | 40 | [`CBS.m3u`](USA/CBS.m3u) |
| 8 | CBS Backups | 33 | [`CBS_Backups.m3u`](USA/CBS_Backups.m3u) |
| 9 | NBC | 49 | [`NBC.m3u`](USA/NBC.m3u) |
| 10 | NBC Backups | 16 | [`NBC_Backups.m3u`](USA/NBC_Backups.m3u) |
| 11 | NBC Sports Channels | 4 | [`NBC_Sports_Channels.m3u`](USA/NBC_Sports_Channels.m3u) |
| 12 | NBC Sports Channels Backups | 3 | [`NBC_Sports_Channels_Backups.m3u`](USA/NBC_Sports_Channels_Backups.m3u) |
| 13 | Cartoons | 68 | [`Cartoons.m3u`](USA/Cartoons.m3u) |
| 14 | Cartoons Backups | 39 | [`Cartoons_Backups.m3u`](USA/Cartoons_Backups.m3u) |
| 15 | PBS | 25 | [`PBS.m3u`](USA/PBS.m3u) |
| 16 | PBS Backups | 7 | [`PBS_Backups.m3u`](USA/PBS_Backups.m3u) |
| 17 | Game Shows | 13 | [`Game_Shows.m3u`](USA/Game_Shows.m3u) |
| 18 | Game Shows Backups | 31 | [`Game_Shows_Backups.m3u`](USA/Game_Shows_Backups.m3u) |
| 19 | United States | 559 | [`United_States.m3u`](USA/United_States.m3u) |
| 20 | United States Backups | 90 | [`United_States_Backups.m3u`](USA/United_States_Backups.m3u) |
| 21 | Movies | 239 | [`Movies.m3u`](USA/Movies.m3u) |
| 22 | Movies Backups | 166 | [`Movies_Backups.m3u`](USA/Movies_Backups.m3u) |
| 23 | Series | 142 | [`Series.m3u`](USA/Series.m3u) |
| 24 | Series Backups | 165 | [`Series_Backups.m3u`](USA/Series_Backups.m3u) |
| 25 | Entertainment | 129 | [`Entertainment.m3u`](USA/Entertainment.m3u) |
| 26 | Entertainment Backups | 112 | [`Entertainment_Backups.m3u`](USA/Entertainment_Backups.m3u) |
| 27 | Music | 120 | [`Music.m3u`](USA/Music.m3u) |
| 28 | Music Backups | 59 | [`Music_Backups.m3u`](USA/Music_Backups.m3u) |
| 29 | Religious | 117 | [`Religious.m3u`](USA/Religious.m3u) |
| 30 | Religious Backups | 12 | [`Religious_Backups.m3u`](USA/Religious_Backups.m3u) |
| 31 | Documentary | 99 | [`Documentary.m3u`](USA/Documentary.m3u) |
| 32 | Documentary Backups | 69 | [`Documentary_Backups.m3u`](USA/Documentary_Backups.m3u) |
| 33 | News | 82 | [`News.m3u`](USA/News.m3u) |
| 34 | News Backups | 60 | [`News_Backups.m3u`](USA/News_Backups.m3u) |
| 35 | Kids | 80 | [`Kids.m3u`](USA/Kids.m3u) |
| 36 | Kids Backups | 71 | [`Kids_Backups.m3u`](USA/Kids_Backups.m3u) |
| 37 | Legislative | 80 | [`Legislative.m3u`](USA/Legislative.m3u) |
| 38 | A&E Networks | 57 | [`A_E_Networks.m3u`](USA/A_E_Networks.m3u) |
| 39 | A&E Networks Backups | 61 | [`A_E_Networks_Backups.m3u`](USA/A_E_Networks_Backups.m3u) |
| 40 | Education | 41 | [`Education.m3u`](USA/Education.m3u) |
| 41 | Education Backups | 3 | [`Education_Backups.m3u`](USA/Education_Backups.m3u) |
| 42 | Comedy | 30 | [`Comedy.m3u`](USA/Comedy.m3u) |
| 43 | Comedy Backups | 41 | [`Comedy_Backups.m3u`](USA/Comedy_Backups.m3u) |
| 44 | International | 27 | [`International.m3u`](USA/International.m3u) |
| 45 | International Backups | 29 | [`International_Backups.m3u`](USA/International_Backups.m3u) |
| 46 | Classic TV | 23 | [`Classic_TV.m3u`](USA/Classic_TV.m3u) |
| 47 | Classic TV Backups | 17 | [`Classic_TV_Backups.m3u`](USA/Classic_TV_Backups.m3u) |
| 48 | Business | 20 | [`Business.m3u`](USA/Business.m3u) |
| 49 | Business Backups | 14 | [`Business_Backups.m3u`](USA/Business_Backups.m3u) |
| 50 | Culture | 18 | [`Culture.m3u`](USA/Culture.m3u) |
| 51 | Family | 15 | [`Family.m3u`](USA/Family.m3u) |
| 52 | Family Backups | 6 | [`Family_Backups.m3u`](USA/Family_Backups.m3u) |
| 53 | Canada | 7 | [`Canada.m3u`](USA/Canada.m3u) |
| 54 | Canada Backups | 12 | [`Canada_Backups.m3u`](USA/Canada_Backups.m3u) |
| 55 | Aria Web Channels | 5 | [`Aria_Web_Channels.m3u`](USA/Aria_Web_Channels.m3u) |
| 56 | Weather | 5 | [`Weather.m3u`](USA/Weather.m3u) |
| 57 | Weather Backups | 7 | [`Weather_Backups.m3u`](USA/Weather_Backups.m3u) |
| 58 | United Kingdom | 4 | [`United_Kingdom.m3u`](USA/United_Kingdom.m3u) |
| 59 | United Kingdom Backups | 7 | [`United_Kingdom_Backups.m3u`](USA/United_Kingdom_Backups.m3u) |
| 60 | En Español | 3 | [`En_Espa_ol.m3u`](USA/En_Espa_ol.m3u) |
| 61 | En Español Backups | 10 | [`En_Espa_ol_Backups.m3u`](USA/En_Espa_ol_Backups.m3u) |
| 62 | Other | 9 | [`Other.m3u`](USA/Other.m3u) |

Groups smaller than 3 channels keep no file of their own (they would be a one-link playlist) - they stay in `USA.m3u`, which always holds every US channel.

## All countries

One file per category for the whole library (US channels first inside a category, because that is the published order).

| # | Category | Channels | Playlist |
|---|---|---:|---|
| 1 | Sports | 785 | [`Sports.m3u`](All/Sports.m3u) |
| 2 | Sports Backups | 218 | [`Sports_Backups.m3u`](All/Sports_Backups.m3u) |
| 3 | Lifestyle | 621 | [`Lifestyle.m3u`](All/Lifestyle.m3u) |
| 4 | Lifestyle Backups | 210 | [`Lifestyle_Backups.m3u`](All/Lifestyle_Backups.m3u) |
| 5 | Fox Channels | 52 | [`Fox_Channels.m3u`](All/Fox_Channels.m3u) |
| 6 | Fox Channels Backups | 12 | [`Fox_Channels_Backups.m3u`](All/Fox_Channels_Backups.m3u) |
| 7 | CBS | 46 | [`CBS.m3u`](All/CBS.m3u) |
| 8 | CBS Backups | 34 | [`CBS_Backups.m3u`](All/CBS_Backups.m3u) |
| 9 | NBC | 88 | [`NBC.m3u`](All/NBC.m3u) |
| 10 | NBC Backups | 30 | [`NBC_Backups.m3u`](All/NBC_Backups.m3u) |
| 11 | NBC Sports Channels | 7 | [`NBC_Sports_Channels.m3u`](All/NBC_Sports_Channels.m3u) |
| 12 | NBC Sports Channels Backups | 4 | [`NBC_Sports_Channels_Backups.m3u`](All/NBC_Sports_Channels_Backups.m3u) |
| 13 | Cartoons | 224 | [`Cartoons.m3u`](All/Cartoons.m3u) |
| 14 | Cartoons Backups | 66 | [`Cartoons_Backups.m3u`](All/Cartoons_Backups.m3u) |
| 15 | PBS | 49 | [`PBS.m3u`](All/PBS.m3u) |
| 16 | PBS Backups | 23 | [`PBS_Backups.m3u`](All/PBS_Backups.m3u) |
| 17 | Game Shows | 38 | [`Game_Shows.m3u`](All/Game_Shows.m3u) |
| 18 | Game Shows Backups | 47 | [`Game_Shows_Backups.m3u`](All/Game_Shows_Backups.m3u) |
| 19 | International | 3004 | [`International.m3u`](All/International.m3u) |
| 20 | International Backups | 465 | [`International_Backups.m3u`](All/International_Backups.m3u) |
| 21 | News | 1008 | [`News.m3u`](All/News.m3u) |
| 22 | News Backups | 409 | [`News_Backups.m3u`](All/News_Backups.m3u) |
| 23 | Music | 1005 | [`Music.m3u`](All/Music.m3u) |
| 24 | Music Backups | 201 | [`Music_Backups.m3u`](All/Music_Backups.m3u) |
| 25 | Movies | 976 | [`Movies.m3u`](All/Movies.m3u) |
| 26 | Movies Backups | 254 | [`Movies_Backups.m3u`](All/Movies_Backups.m3u) |
| 27 | Entertainment | 810 | [`Entertainment.m3u`](All/Entertainment.m3u) |
| 28 | Entertainment Backups | 241 | [`Entertainment_Backups.m3u`](All/Entertainment_Backups.m3u) |
| 29 | Religious | 628 | [`Religious.m3u`](All/Religious.m3u) |
| 30 | Religious Backups | 74 | [`Religious_Backups.m3u`](All/Religious_Backups.m3u) |
| 31 | United States | 561 | [`United_States.m3u`](All/United_States.m3u) |
| 32 | United States Backups | 91 | [`United_States_Backups.m3u`](All/United_States_Backups.m3u) |
| 33 | Europe | 403 | [`Europe.m3u`](All/Europe.m3u) |
| 34 | Europe Backups | 7 | [`Europe_Backups.m3u`](All/Europe_Backups.m3u) |
| 35 | Documentary | 401 | [`Documentary.m3u`](All/Documentary.m3u) |
| 36 | Documentary Backups | 133 | [`Documentary_Backups.m3u`](All/Documentary_Backups.m3u) |
| 37 | Kids | 328 | [`Kids.m3u`](All/Kids.m3u) |
| 38 | Kids Backups | 117 | [`Kids_Backups.m3u`](All/Kids_Backups.m3u) |
| 39 | Canada | 312 | [`Canada.m3u`](All/Canada.m3u) |
| 40 | Canada Backups | 56 | [`Canada_Backups.m3u`](All/Canada_Backups.m3u) |
| 41 | Asia | 295 | [`Asia.m3u`](All/Asia.m3u) |
| 42 | Asia Backups | 5 | [`Asia_Backups.m3u`](All/Asia_Backups.m3u) |
| 43 | Series | 265 | [`Series.m3u`](All/Series.m3u) |
| 44 | Series Backups | 195 | [`Series_Backups.m3u`](All/Series_Backups.m3u) |
| 45 | South America | 250 | [`South_America.m3u`](All/South_America.m3u) |
| 46 | South America Backups | 7 | [`South_America_Backups.m3u`](All/South_America_Backups.m3u) |
| 47 | United Kingdom | 245 | [`United_Kingdom.m3u`](All/United_Kingdom.m3u) |
| 48 | United Kingdom Backups | 38 | [`United_Kingdom_Backups.m3u`](All/United_Kingdom_Backups.m3u) |
| 49 | North America | 159 | [`North_America.m3u`](All/North_America.m3u) |
| 50 | North America Backups | 3 | [`North_America_Backups.m3u`](All/North_America_Backups.m3u) |
| 51 | Australia | 156 | [`Australia.m3u`](All/Australia.m3u) |
| 52 | India | 155 | [`India.m3u`](All/India.m3u) |
| 53 | India Backups | 31 | [`India_Backups.m3u`](All/India_Backups.m3u) |
| 54 | A&E Networks | 130 | [`A_E_Networks.m3u`](All/A_E_Networks.m3u) |
| 55 | A&E Networks Backups | 82 | [`A_E_Networks_Backups.m3u`](All/A_E_Networks_Backups.m3u) |
| 56 | Education | 125 | [`Education.m3u`](All/Education.m3u) |
| 57 | Education Backups | 15 | [`Education_Backups.m3u`](All/Education_Backups.m3u) |
| 58 | Culture | 120 | [`Culture.m3u`](All/Culture.m3u) |
| 59 | Culture Backups | 7 | [`Culture_Backups.m3u`](All/Culture_Backups.m3u) |
| 60 | Comedy | 117 | [`Comedy.m3u`](All/Comedy.m3u) |
| 61 | Comedy Backups | 59 | [`Comedy_Backups.m3u`](All/Comedy_Backups.m3u) |
| 62 | Legislative | 111 | [`Legislative.m3u`](All/Legislative.m3u) |
| 63 | Legislative Backups | 5 | [`Legislative_Backups.m3u`](All/Legislative_Backups.m3u) |
| 64 | Business | 74 | [`Business.m3u`](All/Business.m3u) |
| 65 | Business Backups | 24 | [`Business_Backups.m3u`](All/Business_Backups.m3u) |
| 66 | Andalucía | 52 | [`Andaluc_a.m3u`](All/Andaluc_a.m3u) |
| 67 | Andalucía Backups | 4 | [`Andaluc_a_Backups.m3u`](All/Andaluc_a_Backups.m3u) |
| 68 | Classic TV | 50 | [`Classic_TV.m3u`](All/Classic_TV.m3u) |
| 69 | Classic TV Backups | 26 | [`Classic_TV_Backups.m3u`](All/Classic_TV_Backups.m3u) |
| 70 | Fast Tubi | 35 | [`Fast_Tubi.m3u`](All/Fast_Tubi.m3u) |
| 71 | Africa | 29 | [`Africa.m3u`](All/Africa.m3u) |
| 72 | Family | 29 | [`Family.m3u`](All/Family.m3u) |
| 73 | Family Backups | 7 | [`Family_Backups.m3u`](All/Family_Backups.m3u) |
| 74 | NZ | 26 | [`NZ.m3u`](All/NZ.m3u) |
| 75 | NZ Backups | 6 | [`NZ_Backups.m3u`](All/NZ_Backups.m3u) |
| 76 | Cataluña | 25 | [`Catalu_a.m3u`](All/Catalu_a.m3u) |
| 77 | En Español | 20 | [`En_Espa_ol.m3u`](All/En_Espa_ol.m3u) |
| 78 | En Español Backups | 14 | [`En_Espa_ol_Backups.m3u`](All/En_Espa_ol_Backups.m3u) |
| 79 | Musicales | 16 | [`Musicales.m3u`](All/Musicales.m3u) |
| 80 | Musicales Backups | 8 | [`Musicales_Backups.m3u`](All/Musicales_Backups.m3u) |
| 81 | C. Valenciana | 15 | [`C_Valenciana.m3u`](All/C_Valenciana.m3u) |
| 82 | Int. América | 15 | [`Int_Am_rica.m3u`](All/Int_Am_rica.m3u) |
| 83 | Int. América Backups | 5 | [`Int_Am_rica_Backups.m3u`](All/Int_Am_rica_Backups.m3u) |
| 84 | UK | 15 | [`UK.m3u`](All/UK.m3u) |
| 85 | Aria Web Channels | 13 | [`Aria_Web_Channels.m3u`](All/Aria_Web_Channels.m3u) |
| 86 | Drama | 12 | [`Drama.m3u`](All/Drama.m3u) |
| 87 | Drama Backups | 13 | [`Drama_Backups.m3u`](All/Drama_Backups.m3u) |
| 88 | Weather | 12 | [`Weather.m3u`](All/Weather.m3u) |
| 89 | Weather Backups | 9 | [`Weather_Backups.m3u`](All/Weather_Backups.m3u) |
| 90 | Eventuales | 11 | [`Eventuales.m3u`](All/Eventuales.m3u) |
| 91 | Eventuales Backups | 20 | [`Eventuales_Backups.m3u`](All/Eventuales_Backups.m3u) |
| 92 | Int. Europa | 11 | [`Int_Europa.m3u`](All/Int_Europa.m3u) |
| 93 | Int. Europa Backups | 4 | [`Int_Europa_Backups.m3u`](All/Int_Europa_Backups.m3u) |
| 94 | Galicia | 10 | [`Galicia.m3u`](All/Galicia.m3u) |
| 95 | Galicia Backups | 5 | [`Galicia_Backups.m3u`](All/Galicia_Backups.m3u) |
| 96 | Sci-Fi | 10 | [`Sci_Fi.m3u`](All/Sci_Fi.m3u) |
| 97 | Sci-Fi Backups | 10 | [`Sci_Fi_Backups.m3u`](All/Sci_Fi_Backups.m3u) |
| 98 | DLTV | 9 | [`DLTV.m3u`](All/DLTV.m3u) |
| 99 | País Vasco | 9 | [`Pa_s_Vasco.m3u`](All/Pa_s_Vasco.m3u) |
| 100 | Canarias | 7 | [`Canarias.m3u`](All/Canarias.m3u) |
| 101 | Canarias Backups | 4 | [`Canarias_Backups.m3u`](All/Canarias_Backups.m3u) |
| 102 | Infantiles | 7 | [`Infantiles.m3u`](All/Infantiles.m3u) |
| 103 | Int. Otros | 7 | [`Int_Otros.m3u`](All/Int_Otros.m3u) |
| 104 | Religiosos | 7 | [`Religiosos.m3u`](All/Religiosos.m3u) |
| 105 | Tv Celebrities | 7 | [`Tv_Celebrities.m3u`](All/Tv_Celebrities.m3u) |
| 106 | C. de Madrid | 6 | [`C_de_Madrid.m3u`](All/C_de_Madrid.m3u) |
| 107 | C. de Madrid Backups | 3 | [`C_de_Madrid_Backups.m3u`](All/C_de_Madrid_Backups.m3u) |
| 108 | Generalistas | 6 | [`Generalistas.m3u`](All/Generalistas.m3u) |
| 109 | True Crime | 6 | [`True_Crime.m3u`](All/True_Crime.m3u) |
| 110 | True Crime Backups | 6 | [`True_Crime_Backups.m3u`](All/True_Crime_Backups.m3u) |
| 111 | Castilla-La Mancha | 5 | [`Castilla_La_Mancha.m3u`](All/Castilla_La_Mancha.m3u) |
| 112 | Crime | 5 | [`Crime.m3u`](All/Crime.m3u) |
| 113 | Int. Asia | 5 | [`Int_Asia.m3u`](All/Int_Asia.m3u) |
| 114 | Online TV | 5 | [`Online_TV.m3u`](All/Online_TV.m3u) |
| 115 | Online TV Backups | 7 | [`Online_TV_Backups.m3u`](All/Online_TV_Backups.m3u) |
| 116 | Westerns | 5 | [`Westerns.m3u`](All/Westerns.m3u) |
| 117 | Westerns Backups | 8 | [`Westerns_Backups.m3u`](All/Westerns_Backups.m3u) |
| 118 | Animals + Nature | 7 | [`Animals_Nature.m3u`](All/Animals_Nature.m3u) |
| 119 | Animals + Nature Backups | 7 | [`Animals_Nature_Backups.m3u`](All/Animals_Nature_Backups.m3u) |
| 120 | Cantabria | 4 | [`Cantabria.m3u`](All/Cantabria.m3u) |
| 121 | Season's Greetings | 4 | [`Season_s_Greetings.m3u`](All/Season_s_Greetings.m3u) |
| 122 | Tv Paranormal | 4 | [`Tv_Paranormal.m3u`](All/Tv_Paranormal.m3u) |
| 123 | Animals | 3 | [`Animals.m3u`](All/Animals.m3u) |
| 124 | Extremadura | 3 | [`Extremadura.m3u`](All/Extremadura.m3u) |
| 125 | Int. África | 3 | [`Int_frica.m3u`](All/Int_frica.m3u) |
| 126 | Int. África Backups | 5 | [`Int_frica_Backups.m3u`](All/Int_frica_Backups.m3u) |
| 127 | R. de Murcia | 3 | [`R_de_Murcia.m3u`](All/R_de_Murcia.m3u) |
| 128 | Relax | 3 | [`Relax.m3u`](All/Relax.m3u) |
| 129 | Romance | 3 | [`Romance.m3u`](All/Romance.m3u) |
| 130 | Castilla y León Backups | 3 | [`Castilla_y_Le_n_Backups.m3u`](All/Castilla_y_Le_n_Backups.m3u) |
| 131 | Other | 460 | [`Other.m3u`](All/Other.m3u) |
| 132 | Other Backups | 73 | [`Other_Backups.m3u`](All/Other_Backups.m3u) |

Groups smaller than 3 channels keep no file of their own; they stay in `playlists/PremiumTV.m3u`.

## Load it

```text
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV/main/categories/USA.m3u          # every US channel, by category
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV/main/categories/USA/Sports.m3u   # just the US sports channels
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV/main/categories/All/Sports.m3u  # every sports channel in the library
```

## Keeping it in order

Rebuilt by `scripts/build_categories.py` after every scrape, deep check and quick update; a file is only rewritten when its channel list actually changed. `scripts/verify_playlists.py --require-shelf` re-plans the shelf from the published playlists and fails the run when a committed file is stale, so this directory can not drift away from the playlists it mirrors.
