# Deep link check

- **Run:** nightly deep link check (`20261118T153735Z-3362`)
- **Started:** 2026-11-18T15:37:35Z  |  **Finished:** 2026-11-18T15:41:24Z  |  **Duration:** 228.4s
- **Mode:** deep (playlist + segment probe)
- **Unique links checked:** 12282 from 24554 playlist entries in 178 playlists

| Result | Links | Share | Meaning |
|---|---:|---:|---|
| working | 23875 | 97.2% | answered with playable media |
| offline | 143 | 0.6% | confirmed dead - removed when patching |
| unreachable | 218 | 0.9% | timeout or server error - kept, may recover |
| blocked | 318 | 1.3% | HTTP 401/403/451 - needs auth or is geo-blocked |

## Per playlist

| Playlist | Entries | Working | Offline | Unreachable | Blocked | Other |
|---|---:|---:|---:|---:|---:|---:|
| `playlists/PremiumTV.m3u` | 12158 | 11877 | 13 | 109 | 159 | 0 |
| `playlists/AE_Channels.m3u` | 114 | 113 | 1 | 0 | 0 | 0 |
| `playlists/countries/Afghanistan.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Albania.m3u` | 15 | 15 | 0 | 0 | 0 | 0 |
| `playlists/countries/Algeria.m3u` | 3 | 2 | 0 | 0 | 1 | 0 |
| `playlists/countries/Andorra.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Angola.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Arab_World.m3u` | 13 | 13 | 0 | 0 | 0 | 0 |
| `playlists/countries/Argentina.m3u` | 168 | 165 | 0 | 1 | 2 | 0 |
| `playlists/countries/Armenia.m3u` | 11 | 10 | 1 | 0 | 0 | 0 |
| `playlists/countries/Aruba.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Australia.m3u` | 32 | 32 | 0 | 0 | 0 | 0 |
| `playlists/countries/Austria.m3u` | 40 | 39 | 0 | 1 | 0 | 0 |
| `playlists/countries/Azerbaijan.m3u` | 13 | 12 | 1 | 0 | 0 | 0 |
| `playlists/countries/Bahamas.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bahrain.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bangladesh.m3u` | 23 | 21 | 1 | 0 | 1 | 0 |
| `playlists/countries/Barbados.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Belarus.m3u` | 30 | 26 | 0 | 4 | 0 | 0 |
| `playlists/countries/Belgium.m3u` | 37 | 36 | 0 | 1 | 0 | 0 |
| `playlists/countries/Belize.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Benin.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bolivia.m3u` | 37 | 36 | 1 | 0 | 0 | 0 |
| `playlists/countries/Bosnia_and_Herzegovina.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/countries/Brazil.m3u` | 177 | 173 | 1 | 1 | 2 | 0 |
| `playlists/countries/British_Virgin_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bulgaria.m3u` | 62 | 62 | 0 | 0 | 0 | 0 |
| `playlists/countries/Burkina_Faso.m3u` | 3 | 1 | 0 | 0 | 2 | 0 |
| `playlists/countries/Burundi.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cambodia.m3u` | 15 | 15 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cameroon.m3u` | 13 | 12 | 1 | 0 | 0 | 0 |
| `playlists/countries/Canada.m3u` | 152 | 151 | 1 | 0 | 0 | 0 |
| `playlists/countries/Cape_Verde.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Caribbean_Netherlands.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Chad.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Chile.m3u` | 177 | 174 | 1 | 2 | 0 | 0 |
| `playlists/countries/China.m3u` | 93 | 91 | 0 | 2 | 0 | 0 |
| `playlists/countries/Colombia.m3u` | 109 | 102 | 3 | 3 | 1 | 0 |
| `playlists/countries/Costa_Rica.m3u` | 57 | 57 | 0 | 0 | 0 | 0 |
| `playlists/countries/Croatia.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cuba.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Curacao.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cyprus.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Czechia.m3u` | 99 | 93 | 2 | 4 | 0 | 0 |
| `playlists/countries/DR_Congo.m3u` | 5 | 4 | 1 | 0 | 0 | 0 |
| `playlists/countries/Denmark.m3u` | 8 | 7 | 0 | 0 | 1 | 0 |
| `playlists/countries/Dominican_Republic.m3u` | 200 | 194 | 2 | 4 | 0 | 0 |
| `playlists/countries/Ecuador.m3u` | 52 | 45 | 0 | 1 | 6 | 0 |
| `playlists/countries/Egypt.m3u` | 17 | 16 | 0 | 0 | 1 | 0 |
| `playlists/countries/El_Salvador.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/Equatorial_Guinea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Eritrea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Estonia.m3u` | 21 | 21 | 0 | 0 | 0 | 0 |
| `playlists/countries/Ethiopia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Faroe_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Finland.m3u` | 31 | 31 | 0 | 0 | 0 | 0 |
| `playlists/countries/France.m3u` | 287 | 264 | 0 | 6 | 17 | 0 |
| `playlists/countries/French_Guiana.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Gambia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Georgia.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/Germany.m3u` | 389 | 378 | 1 | 1 | 9 | 0 |
| `playlists/countries/Ghana.m3u` | 6 | 5 | 1 | 0 | 0 | 0 |
| `playlists/countries/Greece.m3u` | 85 | 82 | 1 | 0 | 2 | 0 |
| `playlists/countries/Guadeloupe.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guam.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guatemala.m3u` | 36 | 34 | 1 | 1 | 0 | 0 |
| `playlists/countries/Guinea.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guyana.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Haiti.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Honduras.m3u` | 42 | 42 | 0 | 0 | 0 | 0 |
| `playlists/countries/Hong_Kong.m3u` | 9 | 6 | 0 | 3 | 0 | 0 |
| `playlists/countries/Hungary.m3u` | 160 | 159 | 0 | 1 | 0 | 0 |
| `playlists/countries/Iceland.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/India.m3u` | 804 | 797 | 1 | 3 | 3 | 0 |
| `playlists/countries/Indonesia.m3u` | 105 | 100 | 0 | 5 | 0 | 0 |
| `playlists/countries/International.m3u` | 1115 | 1055 | 51 | 8 | 1 | 0 |
| `playlists/countries/Iran.m3u` | 88 | 88 | 0 | 0 | 0 | 0 |
| `playlists/countries/Iraq.m3u` | 61 | 60 | 0 | 1 | 0 | 0 |
| `playlists/countries/Ireland.m3u` | 19 | 19 | 0 | 0 | 0 | 0 |
| `playlists/countries/Israel.m3u` | 72 | 41 | 31 | 0 | 0 | 0 |
| `playlists/countries/Italy.m3u` | 540 | 512 | 2 | 16 | 10 | 0 |
| `playlists/countries/Ivory_Coast.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/countries/Jamaica.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Japan.m3u` | 23 | 23 | 0 | 0 | 0 | 0 |
| `playlists/countries/Jordan.m3u` | 13 | 12 | 1 | 0 | 0 | 0 |
| `playlists/countries/Kazakhstan.m3u` | 36 | 35 | 0 | 1 | 0 | 0 |
| `playlists/countries/Kenya.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kosovo.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kuwait.m3u` | 14 | 14 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kyrgyzstan.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Laos.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Latin_America.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Latvia.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Lebanon.m3u` | 26 | 25 | 0 | 1 | 0 | 0 |
| `playlists/countries/Libya.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Lithuania.m3u` | 17 | 17 | 0 | 0 | 0 | 0 |
| `playlists/countries/Luxembourg.m3u` | 13 | 13 | 0 | 0 | 0 | 0 |
| `playlists/countries/Malaysia.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Maldives.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Malta.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Martinique.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mauritania.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mexico.m3u` | 122 | 118 | 3 | 1 | 0 | 0 |
| `playlists/countries/Moldova.m3u` | 18 | 18 | 0 | 0 | 0 | 0 |
| `playlists/countries/Monaco.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mongolia.m3u` | 77 | 77 | 0 | 0 | 0 | 0 |
| `playlists/countries/Montenegro.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Morocco.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mozambique.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Myanmar.m3u` | 13 | 13 | 0 | 0 | 0 | 0 |
| `playlists/countries/Namibia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nepal.m3u` | 5 | 4 | 1 | 0 | 0 | 0 |
| `playlists/countries/Netherlands.m3u` | 149 | 147 | 0 | 1 | 1 | 0 |
| `playlists/countries/New_Zealand.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nicaragua.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Niger.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nigeria.m3u` | 31 | 31 | 0 | 0 | 0 | 0 |
| `playlists/countries/North_Korea.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/North_Macedonia.m3u` | 19 | 19 | 0 | 0 | 0 | 0 |
| `playlists/countries/Norway.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/countries/Oman.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Pakistan.m3u` | 51 | 51 | 0 | 0 | 0 | 0 |
| `playlists/countries/Palestine.m3u` | 20 | 20 | 0 | 0 | 0 | 0 |
| `playlists/countries/Panama.m3u` | 16 | 14 | 0 | 2 | 0 | 0 |
| `playlists/countries/Papua_New_Guinea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Paraguay.m3u` | 53 | 46 | 1 | 0 | 6 | 0 |
| `playlists/countries/Peru.m3u` | 140 | 135 | 2 | 2 | 1 | 0 |
| `playlists/countries/Philippines.m3u` | 12 | 11 | 1 | 0 | 0 | 0 |
| `playlists/countries/Poland.m3u` | 182 | 179 | 0 | 3 | 0 | 0 |
| `playlists/countries/Portugal.m3u` | 51 | 50 | 1 | 0 | 0 | 0 |
| `playlists/countries/Puerto_Rico.m3u` | 27 | 22 | 2 | 1 | 2 | 0 |
| `playlists/countries/Qatar.m3u` | 38 | 37 | 0 | 0 | 1 | 0 |
| `playlists/countries/Republic_of_the_Congo.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Romania.m3u` | 158 | 158 | 0 | 0 | 0 | 0 |
| `playlists/countries/Russia.m3u` | 424 | 411 | 0 | 12 | 1 | 0 |
| `playlists/countries/Rwanda.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Kitts_and_Nevis.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Lucia.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saudi_Arabia.m3u` | 51 | 51 | 0 | 0 | 0 | 0 |
| `playlists/countries/Senegal.m3u` | 7 | 6 | 1 | 0 | 0 | 0 |
| `playlists/countries/Serbia.m3u` | 24 | 23 | 1 | 0 | 0 | 0 |
| `playlists/countries/Sierra_Leone.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Singapore.m3u` | 29 | 24 | 0 | 0 | 5 | 0 |
| `playlists/countries/Sint_Maarten.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Slovakia.m3u` | 64 | 64 | 0 | 0 | 0 | 0 |
| `playlists/countries/Slovenia.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Somalia.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/South_Africa.m3u` | 15 | 15 | 0 | 0 | 0 | 0 |
| `playlists/countries/South_Korea.m3u` | 70 | 69 | 1 | 0 | 0 | 0 |
| `playlists/countries/Spain.m3u` | 196 | 190 | 2 | 2 | 2 | 0 |
| `playlists/countries/Sri_Lanka.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sudan.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Suriname.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sweden.m3u` | 376 | 376 | 0 | 0 | 0 | 0 |
| `playlists/countries/Switzerland.m3u` | 35 | 32 | 0 | 0 | 3 | 0 |
| `playlists/countries/Syria.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Taiwan.m3u` | 17 | 16 | 0 | 1 | 0 | 0 |
| `playlists/countries/Tajikistan.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Tanzania.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Thailand.m3u` | 75 | 75 | 0 | 0 | 0 | 0 |
| `playlists/countries/Togo.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Trinidad_and_Tobago.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Tunisia.m3u` | 5 | 3 | 0 | 2 | 0 | 0 |
| `playlists/countries/Turkey.m3u` | 143 | 137 | 2 | 3 | 1 | 0 |
| `playlists/countries/Turkmenistan.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/UK.m3u` | 257 | 255 | 0 | 0 | 2 | 0 |
| `playlists/countries/USA.m3u` | 2888 | 2802 | 4 | 7 | 75 | 0 |
| `playlists/countries/Uganda.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Ukraine.m3u` | 174 | 174 | 0 | 0 | 0 | 0 |
| `playlists/countries/United_Arab_Emirates.m3u` | 44 | 44 | 0 | 0 | 0 | 0 |
| `playlists/countries/Uruguay.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Uzbekistan.m3u` | 30 | 30 | 0 | 0 | 0 | 0 |
| `playlists/countries/Vatican_City.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Venezuela.m3u` | 51 | 50 | 0 | 1 | 0 | 0 |
| `playlists/countries/Vietnam.m3u` | 68 | 67 | 1 | 0 | 0 | 0 |
| `playlists/countries/Western_Sahara.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Yemen.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Zimbabwe.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |

## Patches applied

- Removed **112** confirmed-dead links across **36** playlists (working ratio 97.2%).
  - `PremiumTV.m3u`: -13 (12158 -> 12145)
  - `AE_Channels.m3u`: -1 (114 -> 113)
  - `Armenia.m3u`: -1 (11 -> 10)
  - `Azerbaijan.m3u`: -1 (13 -> 12)
  - `Bangladesh.m3u`: -1 (23 -> 22)
  - `Bolivia.m3u`: -1 (37 -> 36)
  - `Brazil.m3u`: -1 (177 -> 176)
  - `Cameroon.m3u`: -1 (13 -> 12)
  - `Canada.m3u`: -1 (152 -> 151)
  - `Chile.m3u`: -1 (177 -> 176)
  - `Colombia.m3u`: -3 (109 -> 106)
  - `Czechia.m3u`: -2 (99 -> 97)
  - `DR_Congo.m3u`: -1 (5 -> 4)
  - `Dominican_Republic.m3u`: -2 (200 -> 198)
  - `Germany.m3u`: -1 (389 -> 388)
  - `Ghana.m3u`: -1 (6 -> 5)
  - `Greece.m3u`: -1 (85 -> 84)
  - `Guatemala.m3u`: -1 (36 -> 35)
  - `India.m3u`: -1 (804 -> 803)
  - `International.m3u`: -51 (1115 -> 1064)
  - `Italy.m3u`: -2 (540 -> 538)
  - `Jordan.m3u`: -1 (13 -> 12)
  - `Mexico.m3u`: -3 (122 -> 119)
  - `Nepal.m3u`: -1 (5 -> 4)
  - `Paraguay.m3u`: -1 (53 -> 52)
  - `Peru.m3u`: -2 (140 -> 138)
  - `Philippines.m3u`: -1 (12 -> 11)
  - `Portugal.m3u`: -1 (51 -> 50)
  - `Puerto_Rico.m3u`: -2 (27 -> 25)
  - `Senegal.m3u`: -1 (7 -> 6)
  - `Serbia.m3u`: -1 (24 -> 23)
  - `South_Korea.m3u`: -1 (70 -> 69)
  - `Spain.m3u`: -2 (196 -> 194)
  - `Turkey.m3u`: -2 (143 -> 141)
  - `USA.m3u`: -4 (2888 -> 2885)
  - `Vietnam.m3u`: -1 (68 -> 67)
  - skipped `Israel.m3u`: removing 31/72 entries exceeds --max-remove-ratio 35%

## Hosts with the most failing links

| Host | Offline | Unreachable |
|---|---:|---:|
| `ztf5jtil.zyntras.top` | 84 | 0 |
| `64b16f23efbee.streamlock.net` | 0 | 14 |
| `cityeden.catcast.tv` | 0 | 12 |
| `5f22d76e220e1.streamlock.net` | 0 | 12 |
| `sktv.mxnticek.eu` | 4 | 8 |
| `app24.jagobd.com.bd` | 0 | 10 |
| `185.228.163.146:8000` | 0 | 8 |
| `181.78.14.26:4000` | 0 | 8 |
| `103.172.187.30:12000` | 0 | 6 |
| `edge55.dc.beltelecom.by` | 0 | 6 |
| `202.150.172.59` | 0 | 6 |
| `181.79.86.130:8000` | 0 | 4 |
| `187.102.210.46` | 0 | 4 |
| `streaming102.interskytech.com` | 0 | 4 |
| `d39g1vxj2ef6in.cloudfront.net` | 0 | 4 |
| `edge.essastream.com` | 0 | 4 |
| `edge59.dc.beltelecom.by` | 0 | 2 |
| `cdnlivetv.tv` | 0 | 2 |
| `cc-vvkv6xjfc6w5v.akamaized.net` | 0 | 2 |
| `ert-ucdn.broadpeak-aas.com` | 2 | 0 |
| `dethich.pw` | 2 | 0 |
| `wapa.hostless.app` | 0 | 2 |
| `amg00416-amg00416c9-samsung-in-4882.playouts.now.amagi.tv` | 0 | 2 |
| `nbculocallive.akamaized.net` | 0 | 2 |
| `111.88.7.92:8000` | 0 | 2 |

## Sample of confirmed-dead links

| Channel | Reason | URL |
|---|---|---|
| ERT Sports 4 | HTTP 404 | `https://ert-ucdn.broadpeak-aas.com/bpk-tv/ERTSports4/default/index.mpd` |
| HTV Sports (1080p) | HTTP 404 | `https://dethich.pw/htvthethao/index.m3u8` |
| News12 Bronx (1080p) [Geo-blocked] | variant HTTP 404 | `https://mdc.ott.alticeusa.net/live4.ott.optimum.net/live4-uploads/N12XH_A1/index_new.m3u8?omap=https` |
| Gugak TV (1080p) | playlist only, HTTP 404 | `https://mgugaklive.nowcdn.co.kr/gugakvideo/gugakvideo.stream/playlist.m3u8` |
| VOTV (1080p) | HTTP 404 | `https://ingest2-video.streaming-pro.com/votv/streaming_web/playlist.m3u8` |
| ערוץ ההיסטוריה ישראל FHD (History) | HTTP 404 | `http://ztf5jtil.zyntras.top/iptv/KLEYQYC7TPZ8G7W822WQCXNQ/12265/index.m3u8` |
| Yerkir Media (1080p) | playlist only, HTTP 404 | `http://yerkirmedia.am/yerkirmedia/live.m3u8` |
| Xezer TV (720p) | playlist only, HTTP 403 | `https://xezer.tvstream.az/hls/stream/main_stream.m3u8` |
| Madani Channel Bangla (1080p) | HTTP 404 | `https://streaming.madanichannel.tv/static/streaming-playlists/hls/d3e49b76-ac06-4689-a641-9200445b647f/master.m3u8` |
| Imperial TV (720p) | HTTP 404 | `https://tv.centaurychile.com/imperial/streams/EnCyCiwNLsqEQ2kv2852222720686498.m3u8` |
| ConecTV Brasil (720p) | HTTP 404 | `https://stream01.msolutionbrasil.com.br/hls/conectv/live.m3u8` |
| Laura Dave Media TV (720p) | playlist only, HTTP 404 | `https://streaming.lauradavemedia.com/ldm/index.m3u8` |
| Watan-e-Maa TV (720p) | HTTP 404 | `https://5caf24a595d94.streamlock.net:1937/8132/8132/playlist.m3u8` |
| Radio Frecuencia Uno (720p) | HTTP 404 | `https://v1.tustreaming.cl/frecuencia1tv/index.m3u8` |
| Heliconia Radio TV (720p) | HTTP 404 | `https://eu1.servers10.com:8081/8178/index.m3u8` |
| Ultra Casanare TV (1080p) [Not 24/7] | HTTP 404 | `https://eu1.servers10.com:8081/8072/index.m3u8` |
| Canal TRO (Backup 1) | variant HTTP 404 | `https://liveingesta118.cdnmedia.tv/canaltro2live/smil:troplus.smil/playlist.m3u8` |
| Nova Fun | html page, not a stream | `https://sktv.mxnticek.eu/new/stream.php?ch=NovaFun` |
| Prima Krimi (Backup 1) | HTTP 404 | `https://sktv.mxnticek.eu/new/stream.php?ch=PrimaKrimi` |
| Le Monde en 24h | HTTP 404 | `https://stream.berosat.live/hls/monde24h-tv-index/monde24h-tv-index.m3u8` |
| Teleuniverso (720p) [Not 24/7] | HTTP 404 | `https://hls.tvabierta.net/hls/029.m3u8` |
| Ecovision (720p) | html page, not a stream | `https://streaming.grupomediosdelnorte.com:19360/ecovision/ecovision.m3u8` |
| RTL Zwei HD (Backup 1) | HTTP 404 | `http://ztf5jtil.zyntras.top/iptv/KLEYQYC7TPZ8G7W822WQCXNQ/32170/index.m3u8` |
| Faculty TV (720p) | HTTP 404 | `https://stream-server9-jupiter.muxlive.com/hls/facultytv/index.m3u8` |
| ERT Sports 4 | HTTP 404 | `https://ert-ucdn.broadpeak-aas.com/bpk-tv/ERTSports4/default/index.mpd` |
