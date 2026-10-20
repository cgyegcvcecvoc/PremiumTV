# Deep link check

- **Run:** nightly deep link check (`20261020T100653Z-2944`)
- **Started:** 2026-10-20T10:06:53Z  |  **Finished:** 2026-10-20T10:13:37Z  |  **Duration:** 403.9s
- **Mode:** deep (playlist + segment probe)
- **Unique links checked:** 13830 from 27223 playlist entries in 181 playlists

| Result | Links | Share | Meaning |
|---|---:|---:|---|
| working | 22979 | 84.4% | answered with playable media |
| offline | 515 | 1.9% | confirmed dead - removed when patching |
| unreachable | 2056 | 7.6% | timeout or server error - kept, may recover |
| blocked | 1673 | 6.1% | HTTP 401/403/451 - needs auth or is geo-blocked |

## Per playlist

| Playlist | Entries | Working | Offline | Unreachable | Blocked | Other |
|---|---:|---:|---:|---:|---:|---:|
| `playlists/PremiumTV.m3u` | 13322 | 11450 | 9 | 1027 | 836 | 0 |
| `playlists/AE_Channels.m3u` | 71 | 67 | 3 | 1 | 0 | 0 |
| `playlists/countries/Afghanistan.m3u` | 9 | 8 | 0 | 1 | 0 | 0 |
| `playlists/countries/Albania.m3u` | 27 | 15 | 0 | 8 | 4 | 0 |
| `playlists/countries/Algeria.m3u` | 7 | 5 | 0 | 1 | 1 | 0 |
| `playlists/countries/Andorra.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Angola.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Antigua_and_Barbuda.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Arab_World.m3u` | 15 | 15 | 0 | 0 | 0 | 0 |
| `playlists/countries/Argentina.m3u` | 173 | 156 | 6 | 4 | 7 | 0 |
| `playlists/countries/Armenia.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Aruba.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Australia.m3u` | 45 | 34 | 0 | 4 | 7 | 0 |
| `playlists/countries/Austria.m3u` | 51 | 40 | 1 | 7 | 3 | 0 |
| `playlists/countries/Azerbaijan.m3u` | 17 | 13 | 0 | 2 | 2 | 0 |
| `playlists/countries/Bahamas.m3u` | 3 | 2 | 0 | 1 | 0 | 0 |
| `playlists/countries/Bahrain.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bangladesh.m3u` | 26 | 20 | 0 | 5 | 1 | 0 |
| `playlists/countries/Barbados.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Belarus.m3u` | 36 | 27 | 3 | 6 | 0 | 0 |
| `playlists/countries/Belgium.m3u` | 50 | 28 | 10 | 0 | 12 | 0 |
| `playlists/countries/Belize.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Benin.m3u` | 6 | 3 | 1 | 2 | 0 | 0 |
| `playlists/countries/Bolivia.m3u` | 47 | 43 | 2 | 2 | 0 | 0 |
| `playlists/countries/Bosnia_and_Herzegovina.m3u` | 20 | 8 | 0 | 10 | 2 | 0 |
| `playlists/countries/Brazil.m3u` | 261 | 170 | 20 | 43 | 28 | 0 |
| `playlists/countries/British_Virgin_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Brunei.m3u` | 2 | 0 | 0 | 0 | 2 | 0 |
| `playlists/countries/Bulgaria.m3u` | 43 | 29 | 1 | 11 | 2 | 0 |
| `playlists/countries/Burkina_Faso.m3u` | 5 | 0 | 2 | 0 | 3 | 0 |
| `playlists/countries/Burundi.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cambodia.m3u` | 18 | 14 | 3 | 1 | 0 | 0 |
| `playlists/countries/Cameroon.m3u` | 12 | 9 | 0 | 1 | 2 | 0 |
| `playlists/countries/Canada.m3u` | 194 | 142 | 3 | 19 | 30 | 0 |
| `playlists/countries/Cape_Verde.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Caribbean_Netherlands.m3u` | 6 | 4 | 0 | 2 | 0 | 0 |
| `playlists/countries/Chad.m3u` | 2 | 1 | 0 | 1 | 0 | 0 |
| `playlists/countries/Chile.m3u` | 225 | 200 | 7 | 6 | 12 | 0 |
| `playlists/countries/China.m3u` | 163 | 86 | 6 | 54 | 17 | 0 |
| `playlists/countries/Colombia.m3u` | 114 | 106 | 0 | 5 | 3 | 0 |
| `playlists/countries/Costa_Rica.m3u` | 76 | 61 | 11 | 0 | 4 | 0 |
| `playlists/countries/Croatia.m3u` | 26 | 13 | 11 | 2 | 0 | 0 |
| `playlists/countries/Cuba.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Curacao.m3u` | 4 | 2 | 0 | 2 | 0 | 0 |
| `playlists/countries/Cyprus.m3u` | 20 | 20 | 0 | 0 | 0 | 0 |
| `playlists/countries/Czechia.m3u` | 116 | 96 | 0 | 3 | 17 | 0 |
| `playlists/countries/DR_Congo.m3u` | 13 | 3 | 0 | 10 | 0 | 0 |
| `playlists/countries/Denmark.m3u` | 19 | 8 | 4 | 2 | 5 | 0 |
| `playlists/countries/Dominican_Republic.m3u` | 209 | 191 | 10 | 7 | 1 | 0 |
| `playlists/countries/Ecuador.m3u` | 65 | 52 | 4 | 8 | 1 | 0 |
| `playlists/countries/Egypt.m3u` | 17 | 15 | 0 | 0 | 2 | 0 |
| `playlists/countries/El_Salvador.m3u` | 29 | 14 | 7 | 7 | 1 | 0 |
| `playlists/countries/Equatorial_Guinea.m3u` | 2 | 1 | 0 | 1 | 0 | 0 |
| `playlists/countries/Eritrea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Estonia.m3u` | 26 | 22 | 0 | 3 | 1 | 0 |
| `playlists/countries/Ethiopia.m3u` | 2 | 1 | 0 | 1 | 0 | 0 |
| `playlists/countries/Faroe_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Finland.m3u` | 34 | 19 | 0 | 14 | 1 | 0 |
| `playlists/countries/France.m3u` | 268 | 203 | 6 | 20 | 39 | 0 |
| `playlists/countries/French_Guiana.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/French_Polynesia.m3u` | 1 | 0 | 1 | 0 | 0 | 0 |
| `playlists/countries/Gambia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Georgia.m3u` | 24 | 14 | 4 | 3 | 3 | 0 |
| `playlists/countries/Germany.m3u` | 440 | 385 | 5 | 14 | 36 | 0 |
| `playlists/countries/Ghana.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Greece.m3u` | 92 | 84 | 0 | 4 | 4 | 0 |
| `playlists/countries/Guadeloupe.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guam.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guatemala.m3u` | 51 | 32 | 14 | 5 | 0 | 0 |
| `playlists/countries/Guinea.m3u` | 5 | 3 | 2 | 0 | 0 | 0 |
| `playlists/countries/Guyana.m3u` | 10 | 8 | 0 | 1 | 1 | 0 |
| `playlists/countries/Haiti.m3u` | 11 | 6 | 1 | 3 | 1 | 0 |
| `playlists/countries/Honduras.m3u` | 63 | 43 | 9 | 10 | 1 | 0 |
| `playlists/countries/Hong_Kong.m3u` | 26 | 9 | 2 | 3 | 12 | 0 |
| `playlists/countries/Hungary.m3u` | 147 | 114 | 3 | 23 | 7 | 0 |
| `playlists/countries/Iceland.m3u` | 6 | 4 | 1 | 0 | 1 | 0 |
| `playlists/countries/India.m3u` | 738 | 676 | 8 | 34 | 20 | 0 |
| `playlists/countries/Indonesia.m3u` | 149 | 113 | 22 | 12 | 2 | 0 |
| `playlists/countries/International.m3u` | 1265 | 1152 | 46 | 25 | 42 | 0 |
| `playlists/countries/Iran.m3u` | 96 | 90 | 1 | 3 | 2 | 0 |
| `playlists/countries/Iraq.m3u` | 61 | 56 | 1 | 3 | 1 | 0 |
| `playlists/countries/Ireland.m3u` | 25 | 18 | 0 | 0 | 7 | 0 |
| `playlists/countries/Israel.m3u` | 43 | 30 | 1 | 0 | 12 | 0 |
| `playlists/countries/Italy.m3u` | 620 | 489 | 53 | 47 | 31 | 0 |
| `playlists/countries/Ivory_Coast.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/countries/Jamaica.m3u` | 5 | 4 | 1 | 0 | 0 | 0 |
| `playlists/countries/Japan.m3u` | 22 | 15 | 2 | 0 | 5 | 0 |
| `playlists/countries/Jordan.m3u` | 17 | 17 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kazakhstan.m3u` | 41 | 24 | 0 | 4 | 13 | 0 |
| `playlists/countries/Kenya.m3u` | 7 | 6 | 0 | 1 | 0 | 0 |
| `playlists/countries/Kosovo.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kuwait.m3u` | 13 | 13 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kyrgyzstan.m3u` | 11 | 3 | 5 | 0 | 3 | 0 |
| `playlists/countries/Laos.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Latin_America.m3u` | 34 | 33 | 0 | 0 | 1 | 0 |
| `playlists/countries/Latvia.m3u` | 21 | 17 | 3 | 0 | 1 | 0 |
| `playlists/countries/Lebanon.m3u` | 30 | 27 | 0 | 2 | 1 | 0 |
| `playlists/countries/Libya.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Lithuania.m3u` | 23 | 18 | 0 | 0 | 5 | 0 |
| `playlists/countries/Luxembourg.m3u` | 15 | 12 | 0 | 2 | 1 | 0 |
| `playlists/countries/Macau.m3u` | 7 | 0 | 1 | 6 | 0 | 0 |
| `playlists/countries/Malaysia.m3u` | 7 | 4 | 1 | 0 | 2 | 0 |
| `playlists/countries/Maldives.m3u` | 5 | 4 | 0 | 0 | 1 | 0 |
| `playlists/countries/Mali.m3u` | 4 | 2 | 0 | 1 | 1 | 0 |
| `playlists/countries/Malta.m3u` | 7 | 3 | 0 | 0 | 4 | 0 |
| `playlists/countries/Martinique.m3u` | 6 | 5 | 0 | 1 | 0 | 0 |
| `playlists/countries/Mexico.m3u` | 156 | 117 | 5 | 11 | 23 | 0 |
| `playlists/countries/Moldova.m3u` | 22 | 21 | 1 | 0 | 0 | 0 |
| `playlists/countries/Monaco.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mongolia.m3u` | 75 | 75 | 0 | 0 | 0 | 0 |
| `playlists/countries/Montenegro.m3u` | 6 | 3 | 0 | 0 | 3 | 0 |
| `playlists/countries/Morocco.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mozambique.m3u` | 4 | 2 | 0 | 2 | 0 | 0 |
| `playlists/countries/Myanmar.m3u` | 15 | 8 | 0 | 7 | 0 | 0 |
| `playlists/countries/Namibia.m3u` | 2 | 1 | 1 | 0 | 0 | 0 |
| `playlists/countries/Nepal.m3u` | 10 | 7 | 1 | 0 | 2 | 0 |
| `playlists/countries/Netherlands.m3u` | 176 | 145 | 16 | 8 | 7 | 0 |
| `playlists/countries/New_Zealand.m3u` | 13 | 7 | 4 | 0 | 2 | 0 |
| `playlists/countries/Nicaragua.m3u` | 14 | 5 | 2 | 2 | 5 | 0 |
| `playlists/countries/Niger.m3u` | 4 | 2 | 0 | 0 | 2 | 0 |
| `playlists/countries/Nigeria.m3u` | 43 | 29 | 2 | 7 | 5 | 0 |
| `playlists/countries/North_Korea.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/North_Macedonia.m3u` | 31 | 21 | 8 | 2 | 0 | 0 |
| `playlists/countries/Norway.m3u` | 12 | 7 | 0 | 0 | 5 | 0 |
| `playlists/countries/Oman.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Pakistan.m3u` | 89 | 41 | 3 | 42 | 3 | 0 |
| `playlists/countries/Palestine.m3u` | 19 | 18 | 0 | 0 | 1 | 0 |
| `playlists/countries/Panama.m3u` | 20 | 15 | 2 | 3 | 0 | 0 |
| `playlists/countries/Papua_New_Guinea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Paraguay.m3u` | 62 | 57 | 4 | 0 | 1 | 0 |
| `playlists/countries/Peru.m3u` | 137 | 126 | 2 | 6 | 3 | 0 |
| `playlists/countries/Philippines.m3u` | 11 | 10 | 0 | 1 | 0 | 0 |
| `playlists/countries/Poland.m3u` | 236 | 153 | 0 | 77 | 6 | 0 |
| `playlists/countries/Portugal.m3u` | 62 | 40 | 0 | 16 | 6 | 0 |
| `playlists/countries/Puerto_Rico.m3u` | 28 | 26 | 2 | 0 | 0 | 0 |
| `playlists/countries/Qatar.m3u` | 41 | 34 | 0 | 0 | 7 | 0 |
| `playlists/countries/Republic_of_the_Congo.m3u` | 5 | 2 | 1 | 1 | 1 | 0 |
| `playlists/countries/Romania.m3u` | 140 | 126 | 0 | 11 | 3 | 0 |
| `playlists/countries/Russia.m3u` | 528 | 393 | 28 | 98 | 9 | 0 |
| `playlists/countries/Rwanda.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Kitts_and_Nevis.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Lucia.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saudi_Arabia.m3u` | 58 | 50 | 0 | 0 | 8 | 0 |
| `playlists/countries/Senegal.m3u` | 8 | 5 | 0 | 2 | 1 | 0 |
| `playlists/countries/Serbia.m3u` | 34 | 18 | 3 | 6 | 7 | 0 |
| `playlists/countries/Sierra_Leone.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Singapore.m3u` | 28 | 24 | 1 | 1 | 2 | 0 |
| `playlists/countries/Sint_Maarten.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Slovakia.m3u` | 68 | 58 | 0 | 9 | 1 | 0 |
| `playlists/countries/Slovenia.m3u` | 21 | 7 | 10 | 4 | 0 | 0 |
| `playlists/countries/Somalia.m3u` | 9 | 4 | 0 | 5 | 0 | 0 |
| `playlists/countries/South_Africa.m3u` | 23 | 16 | 4 | 1 | 2 | 0 |
| `playlists/countries/South_Korea.m3u` | 84 | 65 | 2 | 14 | 3 | 0 |
| `playlists/countries/Spain.m3u` | 259 | 196 | 7 | 26 | 30 | 0 |
| `playlists/countries/Sri_Lanka.m3u` | 13 | 7 | 0 | 6 | 0 | 0 |
| `playlists/countries/Sudan.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Suriname.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sweden.m3u` | 390 | 379 | 1 | 2 | 8 | 0 |
| `playlists/countries/Switzerland.m3u` | 37 | 25 | 1 | 5 | 6 | 0 |
| `playlists/countries/Syria.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Taiwan.m3u` | 30 | 15 | 11 | 2 | 2 | 0 |
| `playlists/countries/Tajikistan.m3u` | 14 | 0 | 0 | 14 | 0 | 0 |
| `playlists/countries/Tanzania.m3u` | 5 | 4 | 0 | 1 | 0 | 0 |
| `playlists/countries/Thailand.m3u` | 93 | 63 | 2 | 9 | 19 | 0 |
| `playlists/countries/Togo.m3u` | 9 | 2 | 2 | 1 | 4 | 0 |
| `playlists/countries/Trinidad_and_Tobago.m3u` | 5 | 4 | 0 | 1 | 0 | 0 |
| `playlists/countries/Tunisia.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Turkey.m3u` | 164 | 135 | 12 | 11 | 6 | 0 |
| `playlists/countries/Turkmenistan.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/UK.m3u` | 355 | 225 | 10 | 30 | 90 | 0 |
| `playlists/countries/USA.m3u` | 2899 | 2703 | 29 | 69 | 98 | 0 |
| `playlists/countries/Uganda.m3u` | 15 | 10 | 2 | 2 | 1 | 0 |
| `playlists/countries/Ukraine.m3u` | 192 | 168 | 2 | 19 | 3 | 0 |
| `playlists/countries/United_Arab_Emirates.m3u` | 66 | 42 | 14 | 6 | 4 | 0 |
| `playlists/countries/Uruguay.m3u` | 5 | 4 | 0 | 0 | 1 | 0 |
| `playlists/countries/Uzbekistan.m3u` | 35 | 35 | 0 | 0 | 0 | 0 |
| `playlists/countries/Venezuela.m3u` | 60 | 52 | 2 | 4 | 2 | 0 |
| `playlists/countries/Vietnam.m3u` | 73 | 57 | 1 | 1 | 14 | 0 |
| `playlists/countries/Western_Sahara.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Yemen.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Zimbabwe.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |

## Patches applied

- Removed **472** confirmed-dead links across **72** playlists (working ratio 84.4%).
  - `PremiumTV.m3u`: -9 (13322 -> 13313)
  - `AE_Channels.m3u`: -3 (71 -> 68)
  - `Argentina.m3u`: -6 (173 -> 167)
  - `Austria.m3u`: -1 (51 -> 50)
  - `Belarus.m3u`: -3 (36 -> 33)
  - `Belgium.m3u`: -10 (50 -> 40)
  - `Benin.m3u`: -1 (6 -> 5)
  - `Bolivia.m3u`: -2 (47 -> 45)
  - `Brazil.m3u`: -20 (261 -> 241)
  - `Bulgaria.m3u`: -1 (43 -> 42)
  - `Cambodia.m3u`: -3 (18 -> 15)
  - `Canada.m3u`: -3 (194 -> 191)
  - `Chile.m3u`: -7 (225 -> 218)
  - `China.m3u`: -6 (163 -> 157)
  - `Costa_Rica.m3u`: -11 (76 -> 65)
  - `Denmark.m3u`: -4 (19 -> 15)
  - `Dominican_Republic.m3u`: -10 (209 -> 199)
  - `Ecuador.m3u`: -4 (65 -> 61)
  - `El_Salvador.m3u`: -7 (29 -> 22)
  - `France.m3u`: -6 (268 -> 262)
  - `Georgia.m3u`: -4 (24 -> 20)
  - `Germany.m3u`: -5 (440 -> 435)
  - `Guatemala.m3u`: -14 (51 -> 37)
  - `Haiti.m3u`: -1 (11 -> 10)
  - `Honduras.m3u`: -9 (63 -> 54)
  - `Hong_Kong.m3u`: -2 (26 -> 24)
  - `Hungary.m3u`: -3 (147 -> 144)
  - `Iceland.m3u`: -1 (6 -> 5)
  - `India.m3u`: -8 (738 -> 730)
  - `Indonesia.m3u`: -22 (149 -> 127)
  - `International.m3u`: -46 (1265 -> 1219)
  - `Iran.m3u`: -1 (96 -> 95)
  - `Iraq.m3u`: -1 (61 -> 60)
  - `Israel.m3u`: -1 (43 -> 42)
  - `Italy.m3u`: -53 (620 -> 567)
  - `Jamaica.m3u`: -1 (5 -> 4)
  - `Japan.m3u`: -2 (22 -> 20)
  - `Latvia.m3u`: -3 (21 -> 18)
  - `Macau.m3u`: -1 (7 -> 6)
  - `Malaysia.m3u`: -1 (7 -> 6)
  - `Mexico.m3u`: -5 (156 -> 151)
  - `Moldova.m3u`: -1 (22 -> 21)
  - `Nepal.m3u`: -1 (10 -> 9)
  - `Netherlands.m3u`: -16 (176 -> 160)
  - `New_Zealand.m3u`: -4 (13 -> 9)
  - `Nicaragua.m3u`: -2 (14 -> 12)
  - `Nigeria.m3u`: -2 (43 -> 41)
  - `North_Macedonia.m3u`: -8 (31 -> 23)
  - `Pakistan.m3u`: -3 (89 -> 86)
  - `Panama.m3u`: -2 (20 -> 18)
  - `Paraguay.m3u`: -4 (62 -> 58)
  - `Peru.m3u`: -2 (137 -> 135)
  - `Puerto_Rico.m3u`: -2 (28 -> 26)
  - `Republic_of_the_Congo.m3u`: -1 (5 -> 4)
  - `Russia.m3u`: -28 (528 -> 500)
  - `Serbia.m3u`: -3 (34 -> 31)
  - `Singapore.m3u`: -1 (28 -> 27)
  - `South_Africa.m3u`: -4 (23 -> 19)
  - `South_Korea.m3u`: -2 (84 -> 82)
  - `Spain.m3u`: -7 (259 -> 252)
  - `Sweden.m3u`: -1 (390 -> 389)
  - `Switzerland.m3u`: -1 (37 -> 36)
  - `Thailand.m3u`: -2 (93 -> 91)
  - `Togo.m3u`: -2 (9 -> 7)
  - `Turkey.m3u`: -12 (164 -> 152)
  - `UK.m3u`: -10 (355 -> 345)
  - `USA.m3u`: -29 (2899 -> 2871)
  - `Uganda.m3u`: -2 (15 -> 13)
  - `Ukraine.m3u`: -2 (192 -> 190)
  - `United_Arab_Emirates.m3u`: -14 (66 -> 52)
  - `Venezuela.m3u`: -2 (60 -> 58)
  - `Vietnam.m3u`: -1 (73 -> 72)
  - skipped `Burkina_Faso.m3u`: removing 2/5 entries exceeds --max-remove-ratio 35%
  - skipped `Croatia.m3u`: removing 11/26 entries exceeds --max-remove-ratio 35%
  - skipped `French_Polynesia.m3u`: removing 1/1 entries exceeds --max-remove-ratio 35%
  - skipped `Guinea.m3u`: removing 2/5 entries exceeds --max-remove-ratio 35%
  - skipped `Kyrgyzstan.m3u`: removing 5/11 entries exceeds --max-remove-ratio 35%
  - skipped `Namibia.m3u`: removing 1/2 entries exceeds --max-remove-ratio 35%
  - skipped `Slovenia.m3u`: removing 10/21 entries exceeds --max-remove-ratio 35%
  - skipped `Taiwan.m3u`: removing 11/30 entries exceeds --max-remove-ratio 35%

## Hosts with the most failing links

| Host | Offline | Unreachable |
|---|---:|---:|
| `57.128.231.171:8080` | 0 | 101 |
| `31.148.48.15` | 0 | 96 |
| `hls127.freeott.top:8080` | 0 | 96 |
| `103.250.28.74:8000` | 0 | 60 |
| `57.128.210.196:8080` | 0 | 54 |
| `playlist.xtemus.com` | 15 | 30 |
| `live.teleradiocom.tj` | 0 | 28 |
| `cache0.wonvt.st` | 0 | 26 |
| `live-fi.tvkaista.net` | 0 | 26 |
| `lb.iptvnetwork.net` | 24 | 0 |
| `vgtrkregion-reg.cdnvideo.ru` | 22 | 0 |
| `91.228.35.249:8001` | 0 | 20 |
| `znty.dyndns.org:5010` | 0 | 20 |
| `5f22d76e220e1.streamlock.net` | 0 | 20 |
| `cdn.rostelekom-tv.xyz` | 0 | 18 |
| `151.80.18.177:86` | 0 | 18 |
| `51.254.199.122:8080` | 0 | 18 |
| `64b16f23efbee.streamlock.net` | 0 | 18 |
| `103.72.101.252:8080` | 0 | 18 |
| `mumbai-edge.smartplaytv.in` | 0 | 16 |
| `190.197.41.183` | 0 | 14 |
| `39.134.115.163:8080` | 0 | 14 |
| `183.207.248.71` | 0 | 12 |
| `cdn.tvmatic.net` | 0 | 12 |
| `atlantida1.aquax1.cfd` | 0 | 12 |

## Sample of confirmed-dead links

| Channel | Reason | URL |
|---|---|---|
| Pannon TV (648p) | HTTP 404 | `https://stream.nmih.hu:4102/live.m3u8` |
| Video Mediterraneo | HTTP 404 | `https://bfbe5f347ac4424faf719dda285bc39e.msvdn.net/live/S54897858/4gWO7tTzpK3N/playlist.m3u8` |
| StarPlus (United Kingdom) (576p) | playlist only, HTTP 416 | `https://d1rc86nwwc9fag.cloudfront.net/260723/starplusuk_2500/chunks.m3u8` |
| JTV (720p) | HTTP 404 | `http://122.248.43.242:1935/JTVSURABAYA/_definst_/myStream/playlist.m3u8` |
| Real Television (720p) | HTTP 404 | `https://live-evg10.tv360.bitel.com.pe/bitel/realtv/playlist.m3u8` |
| A&E US Eastern Feed (HD) | dns lookup failed | `https://tvpass.org/live/AEEast/hd` |
| A&E US Eastern Feed (Backup 1) | dns lookup failed | `https://tvpass.org/live/AEEast/sd` |
| ☆ The First 48 🇺🇸 | dns lookup failed | `https://d3ja4g4lkxnrni.cloudfront.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-gxn5naeo1b698/v1/ae_networks_first48_1/samsungheadend_us/latest/main/hls/playlist.m3u8` |
| Bragado TV | connection refused | `https://mp.panelchs.com:1936/8028/ngrp:8028_all/playlist.m3u8` |
| Canal 13 San Luis | connection refused | `https://stream.radiosmundiales.com:19360/sanluismas/sanluismas.m3u8` |
| Telefe Buenos Aires (1080p) | HTTP 404 | `http://45.134.141.161:2200/ARG/TELEFE_HD/index.m3u8` |
| Dance TV [Geo-blocked] | dns lookup failed | `https://op-group1-swiftservehd-1.dens.tv/h/h250/index.m3u8` |
| Tec TV | dns lookup failed | `https://tv.initium.net.ar:3939/live/tectvmainlive.m3u8` |
| Antenne Vorarlberg (720p) [Not 24/7] | connection refused | `https://5857db5306b83.streamlock.net/antennevorarlberg-live/_definst_/mp4:livestream/playlist.m3u8` |
| 8 Kanal Vitebsk Ⓢ | connection refused | `http://95.46.208.8:24433/art` |
| Hawe TV Vitebsk Ⓢ | connection refused | `http://95.46.208.8:26259/nashe` |
| Planeta RTR Ⓢ | dns lookup failed | `https://a3569455801-s26881.cdn.ngenix.net/live/smil:rtrp.smil/chunklist_b1600000.m3u8` |
| VTM 2 (360p) | dns lookup failed | `https://lb.iptvnetwork.net/ls28/10035/playlist.m3u8` |
| VTM 3 (360p) | dns lookup failed | `https://lb.iptvnetwork.net/ls28/10037/playlist.m3u8` |
| VTM (360p) | dns lookup failed | `https://lb.iptvnetwork.net/ls28/10033/playlist.m3u8` |
| VTM 4 (360p) | dns lookup failed | `https://lb.iptvnetwork.net/ls28/10038/playlist.m3u8` |
| EEN | dns lookup failed | `https://live-vrt.rabah.net/groupc/live/8edf3bdf-7db3-41c3-a318-72cb7f82de66/live_aes.isml/playlist.m3u8` |
| KassouaTV (720p) | HTTP 404 | `https://playtv4k.live/live/kassouatv/index.m3u8` |
| Interactivo Television (720p) | dns lookup failed | `https://mist01.homestream.fun/hls/interactivotv2/index.m3u8` |
| PAT (1080p) | HTTP 404 | `http://158.172.155.130:8000/play/a0e6/index.m3u8` |
