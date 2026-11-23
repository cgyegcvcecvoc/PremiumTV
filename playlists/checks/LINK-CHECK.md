# Deep link check

- **Run:** nightly deep link check (`20261123T180232Z-3215`)
- **Started:** 2026-11-23T18:02:32Z  |  **Finished:** 2026-11-23T18:06:21Z  |  **Duration:** 229.2s
- **Mode:** deep (playlist + segment probe)
- **Unique links checked:** 13373 from 26452 playlist entries in 181 playlists

| Result | Links | Share | Meaning |
|---|---:|---:|---|
| working | 24959 | 94.4% | answered with playable media |
| offline | 436 | 1.6% | confirmed dead - removed when patching |
| unreachable | 468 | 1.8% | timeout or server error - kept, may recover |
| blocked | 589 | 2.2% | HTTP 401/403/451 - needs auth or is geo-blocked |

## Per playlist

| Playlist | Entries | Working | Offline | Unreachable | Blocked | Other |
|---|---:|---:|---:|---:|---:|---:|
| `playlists/PremiumTV.m3u` | 12947 | 12408 | 14 | 231 | 294 | 0 |
| `playlists/AE_Channels.m3u` | 134 | 129 | 0 | 4 | 1 | 0 |
| `playlists/countries/Afghanistan.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Albania.m3u` | 21 | 20 | 0 | 1 | 0 | 0 |
| `playlists/countries/Algeria.m3u` | 5 | 3 | 0 | 1 | 1 | 0 |
| `playlists/countries/Andorra.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Angola.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Arab_World.m3u` | 14 | 14 | 0 | 0 | 0 | 0 |
| `playlists/countries/Argentina.m3u` | 166 | 162 | 0 | 2 | 2 | 0 |
| `playlists/countries/Armenia.m3u` | 10 | 5 | 0 | 0 | 5 | 0 |
| `playlists/countries/Aruba.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Australia.m3u` | 43 | 31 | 11 | 1 | 0 | 0 |
| `playlists/countries/Austria.m3u` | 39 | 37 | 1 | 1 | 0 | 0 |
| `playlists/countries/Azerbaijan.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bahamas.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bahrain.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bangladesh.m3u` | 17 | 17 | 0 | 0 | 0 | 0 |
| `playlists/countries/Barbados.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Belarus.m3u` | 34 | 28 | 3 | 3 | 0 | 0 |
| `playlists/countries/Belgium.m3u` | 38 | 37 | 1 | 0 | 0 | 0 |
| `playlists/countries/Belize.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Benin.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bermuda.m3u` | 1 | 0 | 1 | 0 | 0 | 0 |
| `playlists/countries/Bolivia.m3u` | 62 | 62 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bosnia_and_Herzegovina.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/countries/Brazil.m3u` | 182 | 174 | 4 | 3 | 1 | 0 |
| `playlists/countries/British_Virgin_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bulgaria.m3u` | 63 | 61 | 0 | 1 | 1 | 0 |
| `playlists/countries/Burkina_Faso.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Burundi.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cambodia.m3u` | 21 | 16 | 5 | 0 | 0 | 0 |
| `playlists/countries/Cameroon.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Canada.m3u` | 202 | 188 | 1 | 13 | 0 | 0 |
| `playlists/countries/Cape_Verde.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Caribbean_Netherlands.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Chad.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Chile.m3u` | 194 | 186 | 8 | 0 | 0 | 0 |
| `playlists/countries/China.m3u` | 105 | 93 | 7 | 5 | 0 | 0 |
| `playlists/countries/Colombia.m3u` | 117 | 115 | 0 | 1 | 1 | 0 |
| `playlists/countries/Costa_Rica.m3u` | 61 | 60 | 0 | 0 | 1 | 0 |
| `playlists/countries/Croatia.m3u` | 14 | 11 | 3 | 0 | 0 | 0 |
| `playlists/countries/Cuba.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Curacao.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cyprus.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Czechia.m3u` | 110 | 110 | 0 | 0 | 0 | 0 |
| `playlists/countries/DR_Congo.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Denmark.m3u` | 12 | 8 | 4 | 0 | 0 | 0 |
| `playlists/countries/Dominican_Republic.m3u` | 222 | 215 | 3 | 1 | 3 | 0 |
| `playlists/countries/Ecuador.m3u` | 52 | 47 | 0 | 0 | 5 | 0 |
| `playlists/countries/Egypt.m3u` | 18 | 17 | 1 | 0 | 0 | 0 |
| `playlists/countries/El_Salvador.m3u` | 20 | 20 | 0 | 0 | 0 | 0 |
| `playlists/countries/Equatorial_Guinea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Eritrea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Estonia.m3u` | 24 | 23 | 0 | 0 | 1 | 0 |
| `playlists/countries/Ethiopia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Faroe_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Finland.m3u` | 31 | 29 | 1 | 1 | 0 | 0 |
| `playlists/countries/France.m3u` | 277 | 264 | 1 | 8 | 4 | 0 |
| `playlists/countries/French_Guiana.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Gambia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Georgia.m3u` | 17 | 17 | 0 | 0 | 0 | 0 |
| `playlists/countries/Germany.m3u` | 386 | 366 | 19 | 0 | 1 | 0 |
| `playlists/countries/Ghana.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Greece.m3u` | 85 | 83 | 0 | 2 | 0 | 0 |
| `playlists/countries/Guadeloupe.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guam.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guatemala.m3u` | 35 | 34 | 1 | 0 | 0 | 0 |
| `playlists/countries/Guinea.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guyana.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Haiti.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Honduras.m3u` | 45 | 44 | 1 | 0 | 0 | 0 |
| `playlists/countries/Hong_Kong.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Hungary.m3u` | 167 | 164 | 2 | 1 | 0 | 0 |
| `playlists/countries/Iceland.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/India.m3u` | 837 | 784 | 28 | 6 | 19 | 0 |
| `playlists/countries/Indonesia.m3u` | 122 | 109 | 11 | 2 | 0 | 0 |
| `playlists/countries/International.m3u` | 1293 | 1243 | 45 | 4 | 1 | 0 |
| `playlists/countries/Iran.m3u` | 121 | 92 | 29 | 0 | 0 | 0 |
| `playlists/countries/Iraq.m3u` | 62 | 58 | 4 | 0 | 0 | 0 |
| `playlists/countries/Ireland.m3u` | 32 | 22 | 4 | 4 | 2 | 0 |
| `playlists/countries/Israel.m3u` | 56 | 43 | 0 | 0 | 13 | 0 |
| `playlists/countries/Italy.m3u` | 557 | 521 | 10 | 17 | 9 | 0 |
| `playlists/countries/Ivory_Coast.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Jamaica.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Japan.m3u` | 28 | 24 | 4 | 0 | 0 | 0 |
| `playlists/countries/Jordan.m3u` | 15 | 12 | 3 | 0 | 0 | 0 |
| `playlists/countries/Kazakhstan.m3u` | 37 | 18 | 0 | 1 | 18 | 0 |
| `playlists/countries/Kenya.m3u` | 9 | 8 | 1 | 0 | 0 | 0 |
| `playlists/countries/Kosovo.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kuwait.m3u` | 15 | 14 | 1 | 0 | 0 | 0 |
| `playlists/countries/Kyrgyzstan.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Laos.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Latin_America.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Latvia.m3u` | 7 | 5 | 0 | 0 | 2 | 0 |
| `playlists/countries/Lebanon.m3u` | 29 | 26 | 3 | 0 | 0 | 0 |
| `playlists/countries/Libya.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Lithuania.m3u` | 19 | 12 | 0 | 0 | 7 | 0 |
| `playlists/countries/Luxembourg.m3u` | 17 | 13 | 4 | 0 | 0 | 0 |
| `playlists/countries/Macau.m3u` | 1 | 0 | 1 | 0 | 0 | 0 |
| `playlists/countries/Malaysia.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Maldives.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Malta.m3u` | 9 | 3 | 0 | 6 | 0 | 0 |
| `playlists/countries/Martinique.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mauritania.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mexico.m3u` | 135 | 126 | 8 | 1 | 0 | 0 |
| `playlists/countries/Moldova.m3u` | 18 | 18 | 0 | 0 | 0 | 0 |
| `playlists/countries/Monaco.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mongolia.m3u` | 80 | 78 | 2 | 0 | 0 | 0 |
| `playlists/countries/Montenegro.m3u` | 10 | 4 | 0 | 6 | 0 | 0 |
| `playlists/countries/Morocco.m3u` | 11 | 10 | 1 | 0 | 0 | 0 |
| `playlists/countries/Mozambique.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Myanmar.m3u` | 14 | 13 | 1 | 0 | 0 | 0 |
| `playlists/countries/Namibia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nepal.m3u` | 6 | 4 | 2 | 0 | 0 | 0 |
| `playlists/countries/Netherlands.m3u` | 173 | 156 | 11 | 6 | 0 | 0 |
| `playlists/countries/New_Zealand.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nicaragua.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Niger.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nigeria.m3u` | 31 | 31 | 0 | 0 | 0 | 0 |
| `playlists/countries/North_Korea.m3u` | 5 | 1 | 0 | 0 | 4 | 0 |
| `playlists/countries/North_Macedonia.m3u` | 20 | 20 | 0 | 0 | 0 | 0 |
| `playlists/countries/Norway.m3u` | 18 | 9 | 1 | 8 | 0 | 0 |
| `playlists/countries/Oman.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Pakistan.m3u` | 52 | 47 | 0 | 4 | 1 | 0 |
| `playlists/countries/Palestine.m3u` | 21 | 21 | 0 | 0 | 0 | 0 |
| `playlists/countries/Panama.m3u` | 14 | 13 | 0 | 1 | 0 | 0 |
| `playlists/countries/Papua_New_Guinea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Paraguay.m3u` | 53 | 46 | 1 | 0 | 6 | 0 |
| `playlists/countries/Peru.m3u` | 154 | 149 | 3 | 2 | 0 | 0 |
| `playlists/countries/Philippines.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Poland.m3u` | 202 | 191 | 2 | 8 | 1 | 0 |
| `playlists/countries/Portugal.m3u` | 48 | 43 | 4 | 1 | 0 | 0 |
| `playlists/countries/Puerto_Rico.m3u` | 28 | 25 | 1 | 1 | 1 | 0 |
| `playlists/countries/Qatar.m3u` | 38 | 36 | 1 | 0 | 1 | 0 |
| `playlists/countries/Republic_of_the_Congo.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Romania.m3u` | 170 | 167 | 0 | 2 | 1 | 0 |
| `playlists/countries/Russia.m3u` | 471 | 360 | 11 | 23 | 77 | 0 |
| `playlists/countries/Rwanda.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Kitts_and_Nevis.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Lucia.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/San_Marino.m3u` | 2 | 0 | 2 | 0 | 0 | 0 |
| `playlists/countries/Saudi_Arabia.m3u` | 57 | 51 | 6 | 0 | 0 | 0 |
| `playlists/countries/Senegal.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Serbia.m3u` | 30 | 28 | 2 | 0 | 0 | 0 |
| `playlists/countries/Sierra_Leone.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Singapore.m3u` | 35 | 29 | 1 | 0 | 5 | 0 |
| `playlists/countries/Sint_Maarten.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Slovakia.m3u` | 66 | 65 | 1 | 0 | 0 | 0 |
| `playlists/countries/Slovenia.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Somalia.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/South_Africa.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/South_Korea.m3u` | 104 | 89 | 8 | 7 | 0 | 0 |
| `playlists/countries/Spain.m3u` | 221 | 185 | 22 | 5 | 9 | 0 |
| `playlists/countries/Sri_Lanka.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sudan.m3u` | 3 | 2 | 1 | 0 | 0 | 0 |
| `playlists/countries/Suriname.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sweden.m3u` | 277 | 277 | 0 | 0 | 0 | 0 |
| `playlists/countries/Switzerland.m3u` | 47 | 46 | 0 | 0 | 1 | 0 |
| `playlists/countries/Syria.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Taiwan.m3u` | 17 | 17 | 0 | 0 | 0 | 0 |
| `playlists/countries/Tajikistan.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Tanzania.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Thailand.m3u` | 79 | 77 | 1 | 1 | 0 | 0 |
| `playlists/countries/Togo.m3u` | 7 | 6 | 1 | 0 | 0 | 0 |
| `playlists/countries/Trinidad_and_Tobago.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Tunisia.m3u` | 5 | 3 | 0 | 2 | 0 | 0 |
| `playlists/countries/Turkey.m3u` | 165 | 151 | 9 | 5 | 0 | 0 |
| `playlists/countries/Turkmenistan.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/UK.m3u` | 278 | 262 | 11 | 4 | 1 | 0 |
| `playlists/countries/USA.m3u` | 3265 | 3127 | 63 | 59 | 16 | 0 |
| `playlists/countries/Uganda.m3u` | 13 | 12 | 1 | 0 | 0 | 0 |
| `playlists/countries/Ukraine.m3u` | 175 | 97 | 3 | 2 | 73 | 0 |
| `playlists/countries/United_Arab_Emirates.m3u` | 48 | 44 | 4 | 0 | 0 | 0 |
| `playlists/countries/Uruguay.m3u` | 7 | 6 | 1 | 0 | 0 | 0 |
| `playlists/countries/Uzbekistan.m3u` | 30 | 30 | 0 | 0 | 0 | 0 |
| `playlists/countries/Vatican_City.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Venezuela.m3u` | 59 | 53 | 6 | 0 | 0 | 0 |
| `playlists/countries/Vietnam.m3u` | 79 | 75 | 4 | 0 | 0 | 0 |
| `playlists/countries/Western_Sahara.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Yemen.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Zimbabwe.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |

## Patches applied

- Removed **436** confirmed-dead links across **68** playlists (working ratio 94.4%).
  - `PremiumTV.m3u`: -14 (12947 -> 12933)
  - `Australia.m3u`: -11 (43 -> 32)
  - `Austria.m3u`: -1 (39 -> 38)
  - `Belarus.m3u`: -3 (34 -> 31)
  - `Belgium.m3u`: -1 (38 -> 37)
  - `Bermuda.m3u`: -1 (1 -> 0)
  - `Brazil.m3u`: -4 (182 -> 178)
  - `Cambodia.m3u`: -5 (21 -> 16)
  - `Canada.m3u`: -1 (202 -> 201)
  - `Chile.m3u`: -8 (194 -> 186)
  - `China.m3u`: -7 (105 -> 98)
  - `Croatia.m3u`: -3 (14 -> 11)
  - `Denmark.m3u`: -4 (12 -> 8)
  - `Dominican_Republic.m3u`: -3 (222 -> 219)
  - `Egypt.m3u`: -1 (18 -> 17)
  - `Finland.m3u`: -1 (31 -> 30)
  - `France.m3u`: -1 (277 -> 276)
  - `Germany.m3u`: -19 (386 -> 367)
  - `Guatemala.m3u`: -1 (35 -> 34)
  - `Honduras.m3u`: -1 (45 -> 44)
  - `Hungary.m3u`: -2 (167 -> 165)
  - `India.m3u`: -28 (837 -> 809)
  - `Indonesia.m3u`: -11 (122 -> 111)
  - `International.m3u`: -45 (1293 -> 1248)
  - `Iran.m3u`: -29 (121 -> 92)
  - `Iraq.m3u`: -4 (62 -> 58)
  - `Ireland.m3u`: -4 (32 -> 28)
  - `Italy.m3u`: -10 (557 -> 547)
  - `Japan.m3u`: -4 (28 -> 24)
  - `Jordan.m3u`: -3 (15 -> 12)
  - `Kenya.m3u`: -1 (9 -> 8)
  - `Kuwait.m3u`: -1 (15 -> 14)
  - `Lebanon.m3u`: -3 (29 -> 26)
  - `Luxembourg.m3u`: -4 (17 -> 13)
  - `Macau.m3u`: -1 (1 -> 0)
  - `Mexico.m3u`: -8 (135 -> 127)
  - `Mongolia.m3u`: -2 (80 -> 78)
  - `Morocco.m3u`: -1 (11 -> 10)
  - `Myanmar.m3u`: -1 (14 -> 13)
  - `Nepal.m3u`: -2 (6 -> 4)
  - `Netherlands.m3u`: -11 (173 -> 162)
  - `Norway.m3u`: -1 (18 -> 17)
  - `Paraguay.m3u`: -1 (53 -> 52)
  - `Peru.m3u`: -3 (154 -> 151)
  - `Poland.m3u`: -2 (202 -> 200)
  - `Portugal.m3u`: -4 (48 -> 44)
  - `Puerto_Rico.m3u`: -1 (28 -> 27)
  - `Qatar.m3u`: -1 (38 -> 37)
  - `Russia.m3u`: -11 (471 -> 460)
  - `San_Marino.m3u`: -2 (2 -> 0)
  - `Saudi_Arabia.m3u`: -6 (57 -> 51)
  - `Serbia.m3u`: -2 (30 -> 28)
  - `Singapore.m3u`: -1 (35 -> 34)
  - `Slovakia.m3u`: -1 (66 -> 65)
  - `South_Korea.m3u`: -8 (104 -> 96)
  - `Spain.m3u`: -22 (221 -> 199)
  - `Sudan.m3u`: -1 (3 -> 2)
  - `Thailand.m3u`: -1 (79 -> 78)
  - `Togo.m3u`: -1 (7 -> 6)
  - `Turkey.m3u`: -9 (165 -> 156)
  - `UK.m3u`: -11 (278 -> 267)
  - `USA.m3u`: -63 (3265 -> 3203)
  - `Uganda.m3u`: -1 (13 -> 12)
  - `Ukraine.m3u`: -3 (175 -> 172)
  - `United_Arab_Emirates.m3u`: -4 (48 -> 44)
  - `Uruguay.m3u`: -1 (7 -> 6)
  - `Venezuela.m3u`: -6 (59 -> 53)
  - `Vietnam.m3u`: -4 (79 -> 75)

## Hosts with the most failing links

| Host | Offline | Unreachable |
|---|---:|---:|
| `23.237.104.106:8080` | 0 | 80 |
| `line.iptvhunt.com:80` | 0 | 74 |
| `vuvuu-geil-m3u8.yaskar661.workers.dev` | 0 | 38 |
| `live.streamingfast.net` | 27 | 0 |
| `116.90.120.149:8000` | 0 | 25 |
| `ncdn.telewebion.ir` | 25 | 0 |
| `64b16f23efbee.streamlock.net` | 0 | 16 |
| `cdn4.skygo.mn` | 13 | 0 |
| `121.149.218.55:9981` | 0 | 12 |
| `5f22d76e220e1.streamlock.net` | 0 | 12 |
| `wdrlokalzeit.akamaized.net` | 11 | 0 |
| `livestreaming.b67buv2.tweedekamer.nl` | 11 | 0 |
| `mdc.ott.alticeusa.net` | 4 | 6 |
| `securestream11.champds.com` | 0 | 10 |
| `abcnews-streams.akamaized.net` | 10 | 0 |
| `cache0.wonvt.st` | 0 | 9 |
| `185.228.163.146:8000` | 0 | 8 |
| `raw.githubusercontent.com` | 8 | 0 |
| `i.mjh.nz` | 7 | 0 |
| `jmp2.uk` | 2 | 4 |
| `cdn.pishow.tv` | 6 | 0 |
| `news.cgtn.com` | 6 | 0 |
| `amagi-streams.akamaized.net` | 6 | 0 |
| `193.47.62.41` | 6 | 0 |
| `clive.malisresidences.com:1935` | 5 | 0 |

## Sample of confirmed-dead links

| Channel | Reason | URL |
|---|---|---|
| Garuda TV (1080p) | playlist only, HTTP 404 | `https://hgmtv.com:19360/garudatvlivestreaming/garudatvlivestreaming.m3u8` |
| STVR Live | html page, not a stream | `https://sktv.mxnticek.eu/new/stream.php?ch=STVR+Live` |
| News12 Hudson Valley (Backup 1) | HTTP 400 | `https://mdc.ott.alticeusa.net/live4.ott.optimum.net/live4-uploads/N12PLUS_H_WC_A1/index_new.m3u8` |
| La-X (720p) | HTTP 404 | `https://stream.eleden.com/livelax/ngrp:livelax_all/playlist.m3u8` |
| Sabor TV (720p) | HTTP 404 | `https://v1.tustreaming.cl/sabortv/index.m3u8` |
| Expo Channel (360p) | variant HTTP dns lookup failed | `https://tvsnhlslivetest.akamaized.net/hls/live/2034711/EXPO-MSL4/master.m3u8` |
| 10 HD | playlist only, HTTP 403 | `https://i.mjh.nz/.r/10-nsw.m3u8` |
| 10 Peach | playlist only, HTTP 403 | `https://i.mjh.nz/.r/10peach-nsw.m3u8` |
| 7flix | playlist only, HTTP 403 | `https://i.mjh.nz/.r/7flix-syd.m3u8` |
| 7mate | playlist only, HTTP 403 | `https://i.mjh.nz/.r/7mate-syd.m3u8` |
| ServusTV (Backup 1) | variant HTTP 404 | `https://rbmn-live.akamaized.net/hls/live/2002825/geoSTVATweb/master.m3u8` |
| Первый Музыкальный Канал (Backup 1) | variant HTTP 404 | `https://ngtrk.dc.beltelecom.by/ngtrk/smil:ont.smil/playlist.m3u8` |
| Беларусь 5 Интернет (1080p) [Not 24/7] | variant HTTP 404 | `https://ngtrk.dc.beltelecom.by/ngtrk/smil:belarus5int.smil/playlist.m3u8` |
| Belros Ⓢ | playlist only, HTTP 404 | `https://live2.mediacdn.ru/sr1/tro/playlist.m3u8` |
| ☆ Surf Channel 🇪🇸 🏄 | playlist only, HTTP 400 | `https://jmp2.uk/stvp-ES3400002PY` |
| Channel 82 | variant HTTP 403 | `https://service.webvideocore.net/CL1olYogIrDWvwqiIKK7eBmnWbRkKKsu3nqabm9GlX02JOj3CDNXzodJMDEN2dk3/a_bq9clxfbupwg.m3u8` |
| Boas Novas (1080p) | HTTP 404 | `https://cdn.jmvstream.com/w/LVW-9375/LVW9375_6i0wPBCHYc/playlist.m3u8` |
| TV Globo Brasilia (1080p) | connection refused | `http://79.127.238.228:14173` |
| TV A Folha (720p) | variant HTTP 404 | `https://video01.logicahost.com.br/tvafolha/tvafolha/playlist.m3u8` |
| TV Cultura | HTTP 404 | `https://player-tvcultura.stream.uol.com.br/live/tvcultura.m3u8` |
| Hang Meas HDTV (720p) | variant HTTP 404 | `http://clive.malisresidences.com:1935/hm_hdtv/_definst_/smil:hmhdt12356.smil/playlist.m3u8` |
| Hang Meas HDTV (Backup 1) | variant HTTP 404 | `http://clive.malisresidences.com:1935/hmcine/_definst_/smil:hmcine.smil/playlist.m3u8` |
| Hang Meas HDTV (Backup 2) | variant HTTP 404 | `http://clive.malisresidences.com:1935/hmgo/_definst_/smil:hmgo.smil/playlist.m3u8` |
| Hang Meas HDTV (Backup 3) | variant HTTP 404 | `http://clive.malisresidences.com:1935/hmnow/_definst_/smil:hmnow.smil/playlist.m3u8` |
| Hang Meas HDTV (Backup 4) | variant HTTP 404 | `http://clive.malisresidences.com:1935/hmplay/_definst_/smil:hmplay.smil/playlist.m3u8` |
