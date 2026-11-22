# Deep link check

- **Run:** nightly deep link check (`20261122T143436Z-3203`)
- **Started:** 2026-11-22T14:34:36Z  |  **Finished:** 2026-11-22T14:39:03Z  |  **Duration:** 267.3s
- **Mode:** deep (playlist + segment probe)
- **Unique links checked:** 12434 from 24865 playlist entries in 177 playlists

| Result | Links | Share | Meaning |
|---|---:|---:|---|
| working | 23553 | 94.7% | answered with playable media |
| offline | 142 | 0.6% | confirmed dead - removed when patching |
| unreachable | 542 | 2.2% | timeout or server error - kept, may recover |
| blocked | 628 | 2.5% | HTTP 401/403/451 - needs auth or is geo-blocked |

## Per playlist

| Playlist | Entries | Working | Offline | Unreachable | Blocked | Other |
|---|---:|---:|---:|---:|---:|---:|
| `playlists/PremiumTV.m3u` | 12317 | 11716 | 19 | 268 | 314 | 0 |
| `playlists/AE_Channels.m3u` | 114 | 109 | 0 | 5 | 0 | 0 |
| `playlists/countries/Afghanistan.m3u` | 11 | 10 | 1 | 0 | 0 | 0 |
| `playlists/countries/Albania.m3u` | 21 | 21 | 0 | 0 | 0 | 0 |
| `playlists/countries/Algeria.m3u` | 3 | 2 | 0 | 0 | 1 | 0 |
| `playlists/countries/Andorra.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Angola.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Arab_World.m3u` | 14 | 14 | 0 | 0 | 0 | 0 |
| `playlists/countries/Argentina.m3u` | 171 | 163 | 3 | 1 | 4 | 0 |
| `playlists/countries/Armenia.m3u` | 10 | 5 | 0 | 0 | 5 | 0 |
| `playlists/countries/Aruba.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Australia.m3u` | 32 | 32 | 0 | 0 | 0 | 0 |
| `playlists/countries/Austria.m3u` | 40 | 37 | 2 | 1 | 0 | 0 |
| `playlists/countries/Azerbaijan.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bahamas.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bahrain.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bangladesh.m3u` | 19 | 18 | 0 | 1 | 0 | 0 |
| `playlists/countries/Barbados.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Belarus.m3u` | 31 | 27 | 0 | 4 | 0 | 0 |
| `playlists/countries/Belgium.m3u` | 37 | 37 | 0 | 0 | 0 | 0 |
| `playlists/countries/Belize.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Benin.m3u` | 5 | 4 | 1 | 0 | 0 | 0 |
| `playlists/countries/Bolivia.m3u` | 53 | 52 | 1 | 0 | 0 | 0 |
| `playlists/countries/Bosnia_and_Herzegovina.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Brazil.m3u` | 170 | 167 | 0 | 3 | 0 | 0 |
| `playlists/countries/British_Virgin_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bulgaria.m3u` | 62 | 61 | 0 | 0 | 1 | 0 |
| `playlists/countries/Burkina_Faso.m3u` | 3 | 1 | 0 | 0 | 2 | 0 |
| `playlists/countries/Burundi.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cambodia.m3u` | 16 | 15 | 1 | 0 | 0 | 0 |
| `playlists/countries/Cameroon.m3u` | 12 | 10 | 1 | 1 | 0 | 0 |
| `playlists/countries/Canada.m3u` | 189 | 178 | 1 | 10 | 0 | 0 |
| `playlists/countries/Cape_Verde.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Caribbean_Netherlands.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Chad.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Chile.m3u` | 181 | 171 | 6 | 4 | 0 | 0 |
| `playlists/countries/China.m3u` | 93 | 90 | 0 | 3 | 0 | 0 |
| `playlists/countries/Colombia.m3u` | 112 | 108 | 2 | 1 | 1 | 0 |
| `playlists/countries/Costa_Rica.m3u` | 60 | 58 | 0 | 1 | 1 | 0 |
| `playlists/countries/Croatia.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cuba.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Curacao.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cyprus.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Czechia.m3u` | 110 | 104 | 0 | 6 | 0 | 0 |
| `playlists/countries/DR_Congo.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Denmark.m3u` | 8 | 7 | 0 | 0 | 1 | 0 |
| `playlists/countries/Dominican_Republic.m3u` | 202 | 198 | 4 | 0 | 0 | 0 |
| `playlists/countries/Ecuador.m3u` | 52 | 44 | 2 | 0 | 6 | 0 |
| `playlists/countries/Egypt.m3u` | 17 | 15 | 0 | 1 | 1 | 0 |
| `playlists/countries/El_Salvador.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/Equatorial_Guinea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Eritrea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Estonia.m3u` | 21 | 20 | 0 | 0 | 1 | 0 |
| `playlists/countries/Ethiopia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Faroe_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Finland.m3u` | 26 | 23 | 3 | 0 | 0 | 0 |
| `playlists/countries/France.m3u` | 274 | 262 | 1 | 7 | 4 | 0 |
| `playlists/countries/French_Guiana.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Georgia.m3u` | 17 | 17 | 0 | 0 | 0 | 0 |
| `playlists/countries/Germany.m3u` | 363 | 359 | 1 | 1 | 2 | 0 |
| `playlists/countries/Ghana.m3u` | 5 | 4 | 1 | 0 | 0 | 0 |
| `playlists/countries/Greece.m3u` | 78 | 75 | 0 | 2 | 1 | 0 |
| `playlists/countries/Guadeloupe.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guam.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guatemala.m3u` | 33 | 31 | 2 | 0 | 0 | 0 |
| `playlists/countries/Guinea.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guyana.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Haiti.m3u` | 3 | 1 | 1 | 1 | 0 | 0 |
| `playlists/countries/Honduras.m3u` | 44 | 44 | 0 | 0 | 0 | 0 |
| `playlists/countries/Hong_Kong.m3u` | 6 | 4 | 0 | 1 | 1 | 0 |
| `playlists/countries/Hungary.m3u` | 161 | 160 | 0 | 1 | 0 | 0 |
| `playlists/countries/Iceland.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/India.m3u` | 862 | 807 | 7 | 45 | 3 | 0 |
| `playlists/countries/Indonesia.m3u` | 105 | 98 | 2 | 5 | 0 | 0 |
| `playlists/countries/International.m3u` | 1040 | 1026 | 3 | 9 | 2 | 0 |
| `playlists/countries/Iran.m3u` | 92 | 92 | 0 | 0 | 0 | 0 |
| `playlists/countries/Iraq.m3u` | 61 | 59 | 2 | 0 | 0 | 0 |
| `playlists/countries/Ireland.m3u` | 27 | 22 | 0 | 3 | 2 | 0 |
| `playlists/countries/Israel.m3u` | 61 | 43 | 5 | 0 | 13 | 0 |
| `playlists/countries/Italy.m3u` | 544 | 509 | 6 | 19 | 10 | 0 |
| `playlists/countries/Ivory_Coast.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Jamaica.m3u` | 6 | 5 | 1 | 0 | 0 | 0 |
| `playlists/countries/Japan.m3u` | 23 | 23 | 0 | 0 | 0 | 0 |
| `playlists/countries/Jordan.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kazakhstan.m3u` | 36 | 28 | 0 | 1 | 7 | 0 |
| `playlists/countries/Kenya.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kosovo.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kuwait.m3u` | 14 | 14 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kyrgyzstan.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Laos.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Latin_America.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Latvia.m3u` | 7 | 4 | 0 | 0 | 3 | 0 |
| `playlists/countries/Lebanon.m3u` | 26 | 26 | 0 | 0 | 0 | 0 |
| `playlists/countries/Libya.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Lithuania.m3u` | 19 | 12 | 0 | 0 | 7 | 0 |
| `playlists/countries/Luxembourg.m3u` | 13 | 13 | 0 | 0 | 0 | 0 |
| `playlists/countries/Malaysia.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Maldives.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Malta.m3u` | 9 | 3 | 0 | 6 | 0 | 0 |
| `playlists/countries/Martinique.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mauritania.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mexico.m3u` | 129 | 128 | 1 | 0 | 0 | 0 |
| `playlists/countries/Moldova.m3u` | 18 | 18 | 0 | 0 | 0 | 0 |
| `playlists/countries/Monaco.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mongolia.m3u` | 77 | 77 | 0 | 0 | 0 | 0 |
| `playlists/countries/Montenegro.m3u` | 10 | 4 | 0 | 6 | 0 | 0 |
| `playlists/countries/Morocco.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mozambique.m3u` | 2 | 1 | 1 | 0 | 0 | 0 |
| `playlists/countries/Myanmar.m3u` | 13 | 13 | 0 | 0 | 0 | 0 |
| `playlists/countries/Namibia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nepal.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Netherlands.m3u` | 155 | 152 | 1 | 1 | 1 | 0 |
| `playlists/countries/New_Zealand.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nicaragua.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Niger.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nigeria.m3u` | 29 | 29 | 0 | 0 | 0 | 0 |
| `playlists/countries/North_Korea.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/North_Macedonia.m3u` | 19 | 19 | 0 | 0 | 0 | 0 |
| `playlists/countries/Norway.m3u` | 15 | 9 | 0 | 6 | 0 | 0 |
| `playlists/countries/Oman.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Pakistan.m3u` | 49 | 46 | 0 | 3 | 0 | 0 |
| `playlists/countries/Palestine.m3u` | 21 | 21 | 0 | 0 | 0 | 0 |
| `playlists/countries/Panama.m3u` | 14 | 13 | 0 | 1 | 0 | 0 |
| `playlists/countries/Papua_New_Guinea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Paraguay.m3u` | 51 | 38 | 7 | 0 | 6 | 0 |
| `playlists/countries/Peru.m3u` | 138 | 133 | 1 | 4 | 0 | 0 |
| `playlists/countries/Philippines.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Poland.m3u` | 195 | 187 | 0 | 7 | 1 | 0 |
| `playlists/countries/Portugal.m3u` | 50 | 47 | 2 | 1 | 0 | 0 |
| `playlists/countries/Puerto_Rico.m3u` | 24 | 23 | 1 | 0 | 0 | 0 |
| `playlists/countries/Qatar.m3u` | 37 | 36 | 0 | 0 | 1 | 0 |
| `playlists/countries/Republic_of_the_Congo.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Romania.m3u` | 172 | 171 | 1 | 0 | 0 | 0 |
| `playlists/countries/Russia.m3u` | 450 | 370 | 1 | 14 | 65 | 0 |
| `playlists/countries/Rwanda.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Kitts_and_Nevis.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Lucia.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saudi_Arabia.m3u` | 51 | 51 | 0 | 0 | 0 | 0 |
| `playlists/countries/Senegal.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Serbia.m3u` | 27 | 27 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sierra_Leone.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Singapore.m3u` | 34 | 29 | 0 | 0 | 5 | 0 |
| `playlists/countries/Sint_Maarten.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Slovakia.m3u` | 65 | 60 | 0 | 5 | 0 | 0 |
| `playlists/countries/Slovenia.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Somalia.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/South_Africa.m3u` | 15 | 15 | 0 | 0 | 0 | 0 |
| `playlists/countries/South_Korea.m3u` | 84 | 81 | 0 | 3 | 0 | 0 |
| `playlists/countries/Spain.m3u` | 197 | 181 | 3 | 3 | 10 | 0 |
| `playlists/countries/Sri_Lanka.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sudan.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Suriname.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sweden.m3u` | 277 | 277 | 0 | 0 | 0 | 0 |
| `playlists/countries/Switzerland.m3u` | 47 | 46 | 0 | 0 | 1 | 0 |
| `playlists/countries/Syria.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Taiwan.m3u` | 17 | 17 | 0 | 0 | 0 | 0 |
| `playlists/countries/Tajikistan.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Tanzania.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Thailand.m3u` | 76 | 76 | 0 | 0 | 0 | 0 |
| `playlists/countries/Togo.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Trinidad_and_Tobago.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Tunisia.m3u` | 5 | 4 | 0 | 1 | 0 | 0 |
| `playlists/countries/Turkey.m3u` | 155 | 149 | 3 | 3 | 0 | 0 |
| `playlists/countries/Turkmenistan.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/UK.m3u` | 268 | 262 | 0 | 5 | 1 | 0 |
| `playlists/countries/USA.m3u` | 3009 | 2850 | 37 | 53 | 69 | 0 |
| `playlists/countries/Uganda.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Ukraine.m3u` | 171 | 95 | 3 | 0 | 73 | 0 |
| `playlists/countries/United_Arab_Emirates.m3u` | 44 | 44 | 0 | 0 | 0 | 0 |
| `playlists/countries/Uruguay.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Uzbekistan.m3u` | 30 | 28 | 0 | 0 | 2 | 0 |
| `playlists/countries/Vatican_City.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Venezuela.m3u` | 47 | 46 | 0 | 1 | 0 | 0 |
| `playlists/countries/Vietnam.m3u` | 76 | 61 | 1 | 14 | 0 | 0 |
| `playlists/countries/Western_Sahara.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Yemen.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Zimbabwe.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |

## Patches applied

- Removed **142** confirmed-dead links across **40** playlists (working ratio 94.7%).
  - `PremiumTV.m3u`: -19 (12317 -> 12298)
  - `Afghanistan.m3u`: -1 (11 -> 10)
  - `Argentina.m3u`: -3 (171 -> 168)
  - `Austria.m3u`: -2 (40 -> 38)
  - `Benin.m3u`: -1 (5 -> 4)
  - `Bolivia.m3u`: -1 (53 -> 52)
  - `Cambodia.m3u`: -1 (16 -> 15)
  - `Cameroon.m3u`: -1 (12 -> 11)
  - `Canada.m3u`: -1 (189 -> 188)
  - `Chile.m3u`: -6 (181 -> 175)
  - `Colombia.m3u`: -2 (112 -> 110)
  - `Dominican_Republic.m3u`: -4 (202 -> 198)
  - `Ecuador.m3u`: -2 (52 -> 50)
  - `Finland.m3u`: -3 (26 -> 23)
  - `France.m3u`: -1 (274 -> 273)
  - `Germany.m3u`: -1 (363 -> 362)
  - `Ghana.m3u`: -1 (5 -> 4)
  - `Guatemala.m3u`: -2 (33 -> 31)
  - `Haiti.m3u`: -1 (3 -> 2)
  - `India.m3u`: -7 (862 -> 855)
  - `Indonesia.m3u`: -2 (105 -> 103)
  - `International.m3u`: -3 (1040 -> 1037)
  - `Iraq.m3u`: -2 (61 -> 59)
  - `Israel.m3u`: -5 (61 -> 56)
  - `Italy.m3u`: -6 (544 -> 538)
  - `Jamaica.m3u`: -1 (6 -> 5)
  - `Mexico.m3u`: -1 (129 -> 128)
  - `Mozambique.m3u`: -1 (2 -> 1)
  - `Netherlands.m3u`: -1 (155 -> 154)
  - `Paraguay.m3u`: -7 (51 -> 44)
  - `Peru.m3u`: -1 (138 -> 137)
  - `Portugal.m3u`: -2 (50 -> 48)
  - `Puerto_Rico.m3u`: -1 (24 -> 23)
  - `Romania.m3u`: -1 (172 -> 171)
  - `Russia.m3u`: -1 (450 -> 449)
  - `Spain.m3u`: -3 (197 -> 194)
  - `Turkey.m3u`: -3 (155 -> 152)
  - `USA.m3u`: -37 (3009 -> 2973)
  - `Ukraine.m3u`: -3 (171 -> 168)
  - `Vietnam.m3u`: -1 (76 -> 75)

## Hosts with the most failing links

| Host | Offline | Unreachable |
|---|---:|---:|
| `116.90.120.149:8000` | 0 | 105 |
| `23.237.104.106:8080` | 0 | 82 |
| `line.iptvhunt.com:80` | 0 | 60 |
| `freem3u.xyz` | 0 | 35 |
| `vuvuu-geil-m3u8.yaskar661.workers.dev` | 0 | 22 |
| `sktv.mxnticek.eu` | 0 | 21 |
| `193.47.62.41` | 18 | 0 |
| `64b16f23efbee.streamlock.net` | 0 | 14 |
| `5f22d76e220e1.streamlock.net` | 0 | 12 |
| `tvsen6.aynaott.com` | 10 | 0 |
| `185.228.163.146:8000` | 0 | 8 |
| `l.cztvcloud.com` | 0 | 8 |
| `cache0.wonvt.st` | 0 | 7 |
| `cdnlivetv.tv` | 0 | 6 |
| `121.149.218.55:9981` | 0 | 6 |
| `edge55.dc.beltelecom.by` | 0 | 6 |
| `cfd-v4-service-channel-stitcher-use1-1.prd.pluto.tv` | 0 | 6 |
| `202.150.172.59` | 0 | 6 |
| `181.224.200.5:2277` | 0 | 6 |
| `5c2974786200d.streamlock.net` | 6 | 0 |
| `45.170.130.224:8000` | 6 | 0 |
| `tvsen3.aynaott.com` | 4 | 0 |
| `5f11919dca3bd.streamlock.net` | 0 | 4 |
| `d39g1vxj2ef6in.cloudfront.net` | 0 | 4 |
| `streaming.softwarecreation.it` | 0 | 4 |

## Sample of confirmed-dead links

| Channel | Reason | URL |
|---|---|---|
| Canal Guapa (1080p) | HTTP 404 | `https://guapa-live.argosworkspace.com/guapa/index.m3u8` |
| Food Network (Backup 1) | HTTP 404 | `https://tvsen3.aynaott.com/7hm4TfVp/index.m3u8` |
| Fox Business | HTTP 404 | `https://tvsen6.aynaott.com/foxbusiness/index.m3u8` |
| Fox News Channel (1080p) | HTTP 404 | `https://tvsen6.aynaott.com/foxnews/index.m3u8` |
| Disney Junior | HTTP 404 | `https://tvsen5.aynaott.com/disney/index.m3u8` |
| Shams TV (Afghanistan) (1080p) | playlist only, HTTP 404 | `https://fflive-darya-educationtv.b-cdn.net/master.m3u8` |
| TyC Sports USA | HTTP 404 | `http://45.170.130.224:8000/play/a020/index.m3u8` |
| Eco TV (1080p) | HTTP 404 | `https://stream.arcast.com.ar/ecotv/ngrp:ecotv_all/playlist.m3u8` |
| TV Mana Argentina (576p) [Not 24/7] | variant HTTP 404 | `https://w2.manasat.com/tvmana-ar/smil:tvmana-ar.smil/playlist.m3u8` |
| ORF Sport+ | dns lookup failed | `https://test02.mdn.ors.at/orf/orfs/qxa/manifest.m3u8` |
| ORF 1 | dns lookup failed | `https://test02.mdn.ors.at/orf/orf1/qxa/manifest.m3u8` |
| Benin TV Junior (720p) | playlist only, HTTP 404 | `https://srtblive.streamakaci.tv/ortb/ortb2-multi/playlist_dvr.m3u8` |
| TELE 6 (1080p) | HTTP 404 | `https://183.giatvcdn.com/ssh101/ssh101/tele6/playlist.m3u8` |
| EAC News TV | HTTP 404 | `https://live.eac-news.com/LiveApp/streams/eacnews.m3u8` |
| Play TV (Cameroon) (720p) [Not 24/7] | HTTP 404 | `http://connectiktv.ddns.net:5000/playtv/@playtv/playlist.m3u8` |
| Total Crime (Backup 1) | playlist only, HTTP 403 | `https://bamca-crimetime-lg.amagi.tv/playlist.m3u8` |
| Agricultura TV (1080p) | playlist only, HTTP 404 | `https://redirector.rudo.video/hls-video/ey6283je82983je9823je8jowowiekldk9838274/921tv/921tv.smil/playlist.m3u8` |
| Oli TV (Chile) (1080p) | HTTP 404 | `https://v4.tustreaming.cl/retroplaytv/index.m3u8` |
| Universidad Autónoma Temuco (UATV) (1080p) [Not 24/7] | variant HTTP 404 | `https://unlimited6-cl.dps.live/uatv/uatv.smil/playlist.m3u8` |
| Via X (576p) | HTTP 404 | `http://45.170.130.224:8000/play/a025/index.m3u8` |
| Zona Latina (576p) | HTTP 404 | `http://45.170.130.224:8000/play/a00x/index.m3u8` |
| CaliTV (1080p) | variant HTTP 404 | `https://tdcdigital-streams.github.io/iptv/CaliTV.m3u8` |
| MiTv Canal 20 | HTTP 404 | `http://190.60.32.178:8178/play/a034/index.m3u8` |
| Bebeto TV (1080p) | playlist only, HTTP 404 | `https://cloud5.livescast.com:19360/bebetotv/bebetotv.m3u8` |
| MegaVision TV (480p) | connection refused | `http://server3.prostudionetwork.com:1943/megavision/MV/playlist.m3u8` |
