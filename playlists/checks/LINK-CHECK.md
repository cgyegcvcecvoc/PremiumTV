# Deep link check

- **Run:** nightly deep link check (`20261124T174046Z-3252`)
- **Started:** 2026-11-24T17:40:46Z  |  **Finished:** 2026-11-24T17:46:53Z  |  **Duration:** 366.6s
- **Mode:** deep (playlist + segment probe)
- **Unique links checked:** 13269 from 26576 playlist entries in 177 playlists

| Result | Links | Share | Meaning |
|---|---:|---:|---|
| working | 24654 | 92.8% | answered with playable media |
| offline | 99 | 0.4% | confirmed dead - removed when patching |
| unreachable | 359 | 1.4% | timeout or server error - kept, may recover |
| blocked | 1464 | 5.5% | HTTP 401/403/451 - needs auth or is geo-blocked |

## Per playlist

| Playlist | Entries | Working | Offline | Unreachable | Blocked | Other |
|---|---:|---:|---:|---:|---:|---:|
| `playlists/PremiumTV.m3u` | 13173 | 12255 | 18 | 177 | 723 | 0 |
| `playlists/AE_Channels.m3u` | 134 | 115 | 0 | 1 | 18 | 0 |
| `playlists/countries/Afghanistan.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Albania.m3u` | 21 | 20 | 0 | 1 | 0 | 0 |
| `playlists/countries/Algeria.m3u` | 5 | 4 | 0 | 0 | 1 | 0 |
| `playlists/countries/Andorra.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Angola.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Arab_World.m3u` | 14 | 14 | 0 | 0 | 0 | 0 |
| `playlists/countries/Argentina.m3u` | 170 | 162 | 3 | 2 | 3 | 0 |
| `playlists/countries/Armenia.m3u` | 10 | 5 | 0 | 0 | 5 | 0 |
| `playlists/countries/Aruba.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Australia.m3u` | 32 | 31 | 0 | 1 | 0 | 0 |
| `playlists/countries/Austria.m3u` | 38 | 37 | 0 | 1 | 0 | 0 |
| `playlists/countries/Azerbaijan.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bahamas.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bahrain.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bangladesh.m3u` | 18 | 18 | 0 | 0 | 0 | 0 |
| `playlists/countries/Barbados.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Belarus.m3u` | 31 | 26 | 0 | 5 | 0 | 0 |
| `playlists/countries/Belgium.m3u` | 37 | 37 | 0 | 0 | 0 | 0 |
| `playlists/countries/Belize.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Benin.m3u` | 7 | 4 | 1 | 2 | 0 | 0 |
| `playlists/countries/Bolivia.m3u` | 64 | 62 | 1 | 1 | 0 | 0 |
| `playlists/countries/Bosnia_and_Herzegovina.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Brazil.m3u` | 182 | 178 | 1 | 2 | 1 | 0 |
| `playlists/countries/British_Virgin_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bulgaria.m3u` | 63 | 61 | 0 | 1 | 1 | 0 |
| `playlists/countries/Burkina_Faso.m3u` | 3 | 2 | 0 | 1 | 0 | 0 |
| `playlists/countries/Burundi.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cambodia.m3u` | 17 | 17 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cameroon.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/countries/Canada.m3u` | 189 | 180 | 0 | 3 | 6 | 0 |
| `playlists/countries/Cape_Verde.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Caribbean_Netherlands.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Chad.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Chile.m3u` | 186 | 184 | 1 | 1 | 0 | 0 |
| `playlists/countries/China.m3u` | 104 | 101 | 1 | 2 | 0 | 0 |
| `playlists/countries/Colombia.m3u` | 116 | 115 | 0 | 0 | 1 | 0 |
| `playlists/countries/Costa_Rica.m3u` | 60 | 58 | 0 | 1 | 1 | 0 |
| `playlists/countries/Croatia.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cuba.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Curacao.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cyprus.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Czechia.m3u` | 107 | 106 | 1 | 0 | 0 | 0 |
| `playlists/countries/DR_Congo.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Denmark.m3u` | 8 | 7 | 1 | 0 | 0 | 0 |
| `playlists/countries/Dominican_Republic.m3u` | 219 | 205 | 6 | 8 | 0 | 0 |
| `playlists/countries/Ecuador.m3u` | 51 | 45 | 1 | 1 | 4 | 0 |
| `playlists/countries/Egypt.m3u` | 17 | 17 | 0 | 0 | 0 | 0 |
| `playlists/countries/El_Salvador.m3u` | 20 | 20 | 0 | 0 | 0 | 0 |
| `playlists/countries/Equatorial_Guinea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Eritrea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Estonia.m3u` | 24 | 22 | 0 | 1 | 1 | 0 |
| `playlists/countries/Ethiopia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Faroe_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Finland.m3u` | 33 | 33 | 0 | 0 | 0 | 0 |
| `playlists/countries/France.m3u` | 274 | 265 | 0 | 6 | 3 | 0 |
| `playlists/countries/French_Guiana.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Gambia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Georgia.m3u` | 17 | 17 | 0 | 0 | 0 | 0 |
| `playlists/countries/Germany.m3u` | 369 | 367 | 0 | 0 | 2 | 0 |
| `playlists/countries/Ghana.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Greece.m3u` | 86 | 83 | 0 | 2 | 1 | 0 |
| `playlists/countries/Guadeloupe.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guam.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guatemala.m3u` | 34 | 34 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guinea.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guyana.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Haiti.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Honduras.m3u` | 46 | 45 | 1 | 0 | 0 | 0 |
| `playlists/countries/Hong_Kong.m3u` | 6 | 5 | 0 | 0 | 1 | 0 |
| `playlists/countries/Hungary.m3u` | 152 | 150 | 0 | 2 | 0 | 0 |
| `playlists/countries/Iceland.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/India.m3u` | 832 | 822 | 4 | 4 | 2 | 0 |
| `playlists/countries/Indonesia.m3u` | 110 | 107 | 1 | 2 | 0 | 0 |
| `playlists/countries/International.m3u` | 1528 | 1291 | 5 | 5 | 227 | 0 |
| `playlists/countries/Iran.m3u` | 92 | 92 | 0 | 0 | 0 | 0 |
| `playlists/countries/Iraq.m3u` | 61 | 61 | 0 | 0 | 0 | 0 |
| `playlists/countries/Ireland.m3u` | 25 | 23 | 0 | 0 | 2 | 0 |
| `playlists/countries/Israel.m3u` | 56 | 43 | 0 | 0 | 13 | 0 |
| `playlists/countries/Italy.m3u` | 538 | 518 | 2 | 18 | 0 | 0 |
| `playlists/countries/Ivory_Coast.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Jamaica.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Japan.m3u` | 24 | 23 | 1 | 0 | 0 | 0 |
| `playlists/countries/Jordan.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kazakhstan.m3u` | 37 | 18 | 0 | 1 | 18 | 0 |
| `playlists/countries/Kenya.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kosovo.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kuwait.m3u` | 14 | 13 | 1 | 0 | 0 | 0 |
| `playlists/countries/Kyrgyzstan.m3u` | 3 | 1 | 0 | 2 | 0 | 0 |
| `playlists/countries/Laos.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Latin_America.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Latvia.m3u` | 7 | 5 | 0 | 0 | 2 | 0 |
| `playlists/countries/Lebanon.m3u` | 26 | 26 | 0 | 0 | 0 | 0 |
| `playlists/countries/Libya.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Lithuania.m3u` | 19 | 12 | 0 | 0 | 7 | 0 |
| `playlists/countries/Luxembourg.m3u` | 13 | 13 | 0 | 0 | 0 | 0 |
| `playlists/countries/Malaysia.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Maldives.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Malta.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Martinique.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mexico.m3u` | 127 | 126 | 1 | 0 | 0 | 0 |
| `playlists/countries/Moldova.m3u` | 18 | 18 | 0 | 0 | 0 | 0 |
| `playlists/countries/Monaco.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mongolia.m3u` | 78 | 78 | 0 | 0 | 0 | 0 |
| `playlists/countries/Montenegro.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Morocco.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mozambique.m3u` | 3 | 2 | 1 | 0 | 0 | 0 |
| `playlists/countries/Myanmar.m3u` | 14 | 6 | 0 | 8 | 0 | 0 |
| `playlists/countries/Namibia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nepal.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Netherlands.m3u` | 161 | 152 | 1 | 6 | 2 | 0 |
| `playlists/countries/New_Zealand.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nicaragua.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Niger.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nigeria.m3u` | 33 | 32 | 1 | 0 | 0 | 0 |
| `playlists/countries/North_Korea.m3u` | 5 | 1 | 0 | 0 | 4 | 0 |
| `playlists/countries/North_Macedonia.m3u` | 20 | 20 | 0 | 0 | 0 | 0 |
| `playlists/countries/Norway.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/countries/Oman.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Pakistan.m3u` | 50 | 36 | 1 | 12 | 1 | 0 |
| `playlists/countries/Palestine.m3u` | 22 | 22 | 0 | 0 | 0 | 0 |
| `playlists/countries/Panama.m3u` | 15 | 14 | 0 | 1 | 0 | 0 |
| `playlists/countries/Papua_New_Guinea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Paraguay.m3u` | 53 | 41 | 4 | 2 | 6 | 0 |
| `playlists/countries/Peru.m3u` | 148 | 147 | 1 | 0 | 0 | 0 |
| `playlists/countries/Philippines.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Poland.m3u` | 198 | 190 | 0 | 6 | 2 | 0 |
| `playlists/countries/Portugal.m3u` | 44 | 43 | 0 | 1 | 0 | 0 |
| `playlists/countries/Puerto_Rico.m3u` | 28 | 26 | 1 | 0 | 1 | 0 |
| `playlists/countries/Qatar.m3u` | 37 | 36 | 0 | 0 | 1 | 0 |
| `playlists/countries/Republic_of_the_Congo.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Romania.m3u` | 172 | 170 | 1 | 1 | 0 | 0 |
| `playlists/countries/Russia.m3u` | 468 | 371 | 3 | 17 | 77 | 0 |
| `playlists/countries/Rwanda.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Kitts_and_Nevis.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Lucia.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saudi_Arabia.m3u` | 55 | 55 | 0 | 0 | 0 | 0 |
| `playlists/countries/Senegal.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Serbia.m3u` | 28 | 28 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sierra_Leone.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Singapore.m3u` | 34 | 29 | 0 | 0 | 5 | 0 |
| `playlists/countries/Sint_Maarten.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Slovakia.m3u` | 64 | 64 | 0 | 0 | 0 | 0 |
| `playlists/countries/Slovenia.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Somalia.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/South_Africa.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/South_Korea.m3u` | 99 | 91 | 0 | 8 | 0 | 0 |
| `playlists/countries/Spain.m3u` | 207 | 185 | 6 | 6 | 10 | 0 |
| `playlists/countries/Sri_Lanka.m3u` | 8 | 7 | 0 | 1 | 0 | 0 |
| `playlists/countries/Sudan.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Suriname.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sweden.m3u` | 274 | 272 | 2 | 0 | 0 | 0 |
| `playlists/countries/Switzerland.m3u` | 47 | 45 | 1 | 0 | 1 | 0 |
| `playlists/countries/Syria.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Taiwan.m3u` | 17 | 12 | 0 | 5 | 0 | 0 |
| `playlists/countries/Tajikistan.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Tanzania.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Thailand.m3u` | 80 | 80 | 0 | 0 | 0 | 0 |
| `playlists/countries/Togo.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Trinidad_and_Tobago.m3u` | 7 | 6 | 1 | 0 | 0 | 0 |
| `playlists/countries/Tunisia.m3u` | 4 | 3 | 0 | 1 | 0 | 0 |
| `playlists/countries/Turkey.m3u` | 160 | 152 | 5 | 3 | 0 | 0 |
| `playlists/countries/Turkmenistan.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/UK.m3u` | 269 | 261 | 2 | 2 | 4 | 0 |
| `playlists/countries/USA.m3u` | 3218 | 2947 | 12 | 25 | 234 | 0 |
| `playlists/countries/Uganda.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/countries/Ukraine.m3u` | 171 | 98 | 0 | 0 | 73 | 0 |
| `playlists/countries/United_Arab_Emirates.m3u` | 44 | 44 | 0 | 0 | 0 | 0 |
| `playlists/countries/Uruguay.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Uzbekistan.m3u` | 30 | 30 | 0 | 0 | 0 | 0 |
| `playlists/countries/Vatican_City.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Venezuela.m3u` | 55 | 53 | 2 | 0 | 0 | 0 |
| `playlists/countries/Vietnam.m3u` | 84 | 81 | 3 | 0 | 0 | 0 |
| `playlists/countries/Western_Sahara.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Yemen.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Zimbabwe.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |

## Patches applied

- Removed **99** confirmed-dead links across **37** playlists (working ratio 92.8%).
  - `PremiumTV.m3u`: -18 (13173 -> 13155)
  - `Argentina.m3u`: -3 (170 -> 167)
  - `Benin.m3u`: -1 (7 -> 6)
  - `Bolivia.m3u`: -1 (64 -> 63)
  - `Brazil.m3u`: -1 (182 -> 181)
  - `Chile.m3u`: -1 (186 -> 185)
  - `China.m3u`: -1 (104 -> 103)
  - `Czechia.m3u`: -1 (107 -> 106)
  - `Denmark.m3u`: -1 (8 -> 7)
  - `Dominican_Republic.m3u`: -6 (219 -> 213)
  - `Ecuador.m3u`: -1 (51 -> 50)
  - `Honduras.m3u`: -1 (46 -> 45)
  - `India.m3u`: -4 (832 -> 828)
  - `Indonesia.m3u`: -1 (110 -> 109)
  - `International.m3u`: -5 (1528 -> 1523)
  - `Italy.m3u`: -2 (538 -> 536)
  - `Japan.m3u`: -1 (24 -> 23)
  - `Kuwait.m3u`: -1 (14 -> 13)
  - `Mexico.m3u`: -1 (127 -> 126)
  - `Mozambique.m3u`: -1 (3 -> 2)
  - `Netherlands.m3u`: -1 (161 -> 160)
  - `Nigeria.m3u`: -1 (33 -> 32)
  - `Pakistan.m3u`: -1 (50 -> 49)
  - `Paraguay.m3u`: -4 (53 -> 49)
  - `Peru.m3u`: -1 (148 -> 147)
  - `Puerto_Rico.m3u`: -1 (28 -> 27)
  - `Romania.m3u`: -1 (172 -> 171)
  - `Russia.m3u`: -3 (468 -> 465)
  - `Spain.m3u`: -6 (207 -> 201)
  - `Sweden.m3u`: -2 (274 -> 272)
  - `Switzerland.m3u`: -1 (47 -> 46)
  - `Trinidad_and_Tobago.m3u`: -1 (7 -> 6)
  - `Turkey.m3u`: -5 (160 -> 155)
  - `UK.m3u`: -2 (269 -> 267)
  - `USA.m3u`: -12 (3218 -> 3207)
  - `Venezuela.m3u`: -2 (55 -> 53)
  - `Vietnam.m3u`: -3 (84 -> 81)

## Hosts with the most failing links

| Host | Offline | Unreachable |
|---|---:|---:|
| `vuvuu-geil-m3u8.yaskar661.workers.dev` | 0 | 38 |
| `online.godstands.tv:5443` | 0 | 24 |
| `jmp2.uk` | 12 | 10 |
| `mrtvott.com` | 0 | 16 |
| `121.149.218.55:9981` | 0 | 14 |
| `64b16f23efbee.streamlock.net` | 0 | 14 |
| `5f22d76e220e1.streamlock.net` | 0 | 12 |
| `raw.githubusercontent.com` | 0 | 10 |
| `edge.essastream.com` | 0 | 10 |
| `securestream11.champds.com` | 0 | 10 |
| `edge55.dc.beltelecom.by` | 0 | 8 |
| `cache0.wonvt.st` | 0 | 7 |
| `line.iptvhunt.com:80` | 0 | 6 |
| `dethich.pw` | 6 | 0 |
| `158.172.155.130:8000` | 0 | 6 |
| `193.47.62.41` | 6 | 0 |
| `90.163.85.113:8093` | 0 | 4 |
| `cdnlivetv.tv` | 0 | 4 |
| `streamer-cache.grnet.gr` | 0 | 4 |
| `d39g1vxj2ef6in.cloudfront.net` | 0 | 4 |
| `176.126.166.43:1935` | 0 | 4 |
| `212.70.131.37:8000` | 0 | 4 |
| `live-3.otcnet.ru` | 0 | 4 |
| `streaming.jarabacoatv.com` | 0 | 4 |
| `reflect-batv.cablecast.tv` | 0 | 4 |

## Sample of confirmed-dead links

| Channel | Reason | URL |
|---|---|---|
| ☆ Darcizzle Offshore 🇺🇸 | variant HTTP 422 | `https://ssai.aniview.com/api/v1/hls/stream.m3u8?AVS_SSAIID=69099f3b30a6ba46360d7c72&AV_CHANNEL_NAME=Fishing-Offshore&AV_CONTENT_LANGUAGE=en&AV_CONTENT_RATING=TV-14&cb=MX_CACHEBUSTER&AV_APPPKGNAME=MX_APP_BUNDLE&AV_APPNAME=MX_APP_NAME&AV_APPSTOREURL=MX_APP_STORE_URL&AV_WIDTH=MX_WIDTH&AV_HEIGHT=MX_HEIGHT&AV_LANGUAGE=MX_DEVICE_LANGUAGE&AV_IFA_TYPE=MX_IFA_TYPE&AV_CATEGORY=IAB17-32&AV_TITLE=Fishing-Offshore&AV_EPISODE=MX_CONTENT_EPISODE&AV_CONTENT_GENRE=Fishing&AV_GDPR=MX_GDPR&AV_CONSENT=MX_CONSENT&AV_COPPA=MX_COPPA&AV_IDFA=MX_IFA&AV_CCPA=MX_US_PRIVACY&AV_CONTENT_CHANNEL=Fishing-Offshore&AV_CUSTOM17=Google--520678__193__13827__0__0__0____MP&AV_CUSTOM18=MX_GIVN&AV_CUSTOM19=pn%3D2v2lTwj4%26context%3Dmid-13827` |
| Vinh Long TV 4 (720p) | HTTP 404 | `https://dethich.pw/thvl4/index.m3u8` |
| VTV6 (720p) | HTTP 404 | `https://dethich.pw/vtv6/index.m3u8` |
| AWSN (Backup 1) | playlist only, HTTP 403 | `https://jmp2.uk/plu-660e7404e8fba8000853abc0.m3u8` |
| PGA Tour (Backup 3) | playlist only, HTTP 403 | `https://jmp2.uk/plu-5de94dacb394a300099fa22a.m3u8` |
| Bayres TV (720p) | HTTP 404 | `https://streaming01.mikrolive.tv/bayrestv/live/playlist.m3u8` |
| Corrientes TV (352p) | HTTP 404 | `https://617c5175c970b.streamlock.net:4444/13max2/live13maxtv2026/playlist.m3u8` |
| Neo TV (Argentina) | HTTP 404 | `https://videostream.shockmedia.com.ar:19360/neotvdigital/neotvdigital.m3u8` |
| Speedline TV | HTTP 404 | `https://cdn-us-east-prod-ingest-infra-dacast-com.akamaized.net/dbe59037-07a0-4f1c-82a2-7de94b4b62d2/index.m3u8` |
| TV OFF (1080p) | HTTP 404 | `https://edge.enhdtv.com/tvoff/index.m3u8` |
| Rede Minas (720p) | HTTP 404 | `https://8hzcavccys.zoeweb.tv/redeminas/ngrp:redeminas_all/playlist.m3u8` |
| Turno (720p) | playlist only, HTTP 404 | `https://redirector.dps.live/hls/turno/playlist.m3u8` |
| Hebi News Channel (480p) [Not 24/7] | variant HTTP 404 | `http://pili-live-hls.hebitv.com/hebi/hebi.m3u8` |
| CNN Prima News (Backup 2) | HTTP 404 | `https://sktv.mxnticek.eu/new/stream.php?ch=PrimaNews` |
| TVMarineret (1080p) | connection refused | `http://sdream.info:8080/hls/livestream/index.m3u8` |
| Alcarrizos TV (720p) [Not 24/7] | HTTP 404 | `https://5790d294af2dc.streamlock.net/alcarrizostv/alcarrizostv/playlist.m3u8` |
| Canalda 26 HD [Not 24/7] | HTTP 404 | `https://canalda.rgradio.net:3084/live/canaldalive.m3u8` |
| Del Pueblo TV [Not 24/7] | HTTP 404 | `https://vdopanel.jlahozconsulting.com:3869/hybrid/play.m3u8` |
| JPD TV [Not 24/7] | HTTP 404 | `https://imagenuniversaltv.net:3026/live/juanpabloduartetvlive.m3u8` |
| Telecontacto | HTTP 404 | `https://streaming.grupomediosdelnorte.com:19360/telecontacto/telecontacto.m3u8` |
| Vos y TV (720p) [Not 24/7] | HTTP 404 | `https://cloud37.ecuatel.com/vostv/live/manifest.m3u8` |
| Maya TV | HTTP 404 | `https://media.streambrothers.com:19360/8036/8036.m3u8` |
| KCL TV (720p) | HTTP 404 | `https://kcltv.livebox.co.in/kclhls/live.m3u8` |
| Rupasi Bangla (720p) | playlist only, HTTP 404 | `https://cdn.pishow.tv/ott/live/1039/master.m3u8` |
| DD Chandana (576p) | playlist only, HTTP 404 | `https://cdn.pishow.tv/ott/live/28/master.m3u8` |
