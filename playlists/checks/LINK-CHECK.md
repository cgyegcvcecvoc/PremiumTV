# Deep link check

- **Run:** nightly deep link check (`20261024T122328Z-2899`)
- **Started:** 2026-10-24T12:23:28Z  |  **Finished:** 2026-10-24T12:29:22Z  |  **Duration:** 354.4s
- **Mode:** deep (playlist + segment probe)
- **Unique links checked:** 13463 from 26765 playlist entries in 182 playlists

| Result | Links | Share | Meaning |
|---|---:|---:|---|
| working | 22901 | 85.6% | answered with playable media |
| offline | 232 | 0.9% | confirmed dead - removed when patching |
| unreachable | 1946 | 7.3% | timeout or server error - kept, may recover |
| blocked | 1686 | 6.3% | HTTP 401/403/451 - needs auth or is geo-blocked |

## Per playlist

| Playlist | Entries | Working | Offline | Unreachable | Blocked | Other |
|---|---:|---:|---:|---:|---:|---:|
| `playlists/PremiumTV.m3u` | 13234 | 11407 | 12 | 972 | 843 | 0 |
| `playlists/AE_Channels.m3u` | 69 | 69 | 0 | 0 | 0 | 0 |
| `playlists/countries/Afghanistan.m3u` | 11 | 10 | 0 | 1 | 0 | 0 |
| `playlists/countries/Albania.m3u` | 25 | 15 | 1 | 8 | 1 | 0 |
| `playlists/countries/Algeria.m3u` | 7 | 4 | 0 | 2 | 1 | 0 |
| `playlists/countries/Andorra.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Angola.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Antigua_and_Barbuda.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Arab_World.m3u` | 14 | 14 | 0 | 0 | 0 | 0 |
| `playlists/countries/Argentina.m3u` | 167 | 149 | 3 | 6 | 9 | 0 |
| `playlists/countries/Armenia.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Aruba.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Australia.m3u` | 51 | 34 | 5 | 4 | 8 | 0 |
| `playlists/countries/Austria.m3u` | 49 | 38 | 1 | 7 | 3 | 0 |
| `playlists/countries/Azerbaijan.m3u` | 18 | 11 | 0 | 2 | 5 | 0 |
| `playlists/countries/Bahamas.m3u` | 3 | 2 | 0 | 1 | 0 | 0 |
| `playlists/countries/Bahrain.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bangladesh.m3u` | 26 | 17 | 0 | 8 | 1 | 0 |
| `playlists/countries/Barbados.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Belarus.m3u` | 36 | 29 | 0 | 7 | 0 | 0 |
| `playlists/countries/Belgium.m3u` | 44 | 31 | 1 | 0 | 12 | 0 |
| `playlists/countries/Belize.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Benin.m3u` | 4 | 3 | 0 | 1 | 0 | 0 |
| `playlists/countries/Bermuda.m3u` | 1 | 0 | 1 | 0 | 0 | 0 |
| `playlists/countries/Bolivia.m3u` | 48 | 47 | 0 | 1 | 0 | 0 |
| `playlists/countries/Bosnia_and_Herzegovina.m3u` | 21 | 10 | 0 | 9 | 2 | 0 |
| `playlists/countries/Brazil.m3u` | 246 | 178 | 0 | 40 | 28 | 0 |
| `playlists/countries/British_Virgin_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Brunei.m3u` | 2 | 0 | 0 | 0 | 2 | 0 |
| `playlists/countries/Bulgaria.m3u` | 42 | 29 | 0 | 11 | 2 | 0 |
| `playlists/countries/Burkina_Faso.m3u` | 4 | 3 | 0 | 0 | 1 | 0 |
| `playlists/countries/Burundi.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cambodia.m3u` | 20 | 14 | 5 | 1 | 0 | 0 |
| `playlists/countries/Cameroon.m3u` | 14 | 13 | 0 | 0 | 1 | 0 |
| `playlists/countries/Canada.m3u` | 186 | 139 | 1 | 16 | 30 | 0 |
| `playlists/countries/Cape_Verde.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Caribbean_Netherlands.m3u` | 6 | 4 | 0 | 2 | 0 | 0 |
| `playlists/countries/Chad.m3u` | 2 | 1 | 0 | 1 | 0 | 0 |
| `playlists/countries/Chile.m3u` | 223 | 190 | 2 | 16 | 15 | 0 |
| `playlists/countries/China.m3u` | 164 | 87 | 5 | 55 | 17 | 0 |
| `playlists/countries/Colombia.m3u` | 120 | 106 | 2 | 9 | 3 | 0 |
| `playlists/countries/Costa_Rica.m3u` | 61 | 56 | 0 | 1 | 4 | 0 |
| `playlists/countries/Croatia.m3u` | 18 | 13 | 3 | 2 | 0 | 0 |
| `playlists/countries/Cuba.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Curacao.m3u` | 4 | 3 | 0 | 1 | 0 | 0 |
| `playlists/countries/Cyprus.m3u` | 17 | 14 | 0 | 3 | 0 | 0 |
| `playlists/countries/Czechia.m3u` | 64 | 44 | 0 | 3 | 17 | 0 |
| `playlists/countries/DR_Congo.m3u` | 16 | 5 | 0 | 10 | 1 | 0 |
| `playlists/countries/Denmark.m3u` | 15 | 7 | 0 | 2 | 6 | 0 |
| `playlists/countries/Dominican_Republic.m3u` | 207 | 201 | 1 | 4 | 1 | 0 |
| `playlists/countries/Ecuador.m3u` | 57 | 48 | 0 | 8 | 1 | 0 |
| `playlists/countries/Egypt.m3u` | 18 | 15 | 1 | 0 | 2 | 0 |
| `playlists/countries/El_Salvador.m3u` | 25 | 17 | 0 | 7 | 1 | 0 |
| `playlists/countries/Equatorial_Guinea.m3u` | 2 | 0 | 0 | 2 | 0 | 0 |
| `playlists/countries/Eritrea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Estonia.m3u` | 25 | 20 | 0 | 4 | 1 | 0 |
| `playlists/countries/Ethiopia.m3u` | 2 | 1 | 0 | 1 | 0 | 0 |
| `playlists/countries/Faroe_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Finland.m3u` | 31 | 29 | 0 | 1 | 1 | 0 |
| `playlists/countries/France.m3u` | 249 | 198 | 2 | 18 | 31 | 0 |
| `playlists/countries/French_Guiana.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Georgia.m3u` | 20 | 14 | 0 | 3 | 3 | 0 |
| `playlists/countries/Germany.m3u` | 423 | 356 | 17 | 15 | 35 | 0 |
| `playlists/countries/Ghana.m3u` | 6 | 5 | 0 | 1 | 0 | 0 |
| `playlists/countries/Greece.m3u` | 97 | 90 | 0 | 4 | 3 | 0 |
| `playlists/countries/Guadeloupe.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guam.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guatemala.m3u` | 36 | 31 | 0 | 5 | 0 | 0 |
| `playlists/countries/Guinea.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guyana.m3u` | 12 | 11 | 0 | 0 | 1 | 0 |
| `playlists/countries/Haiti.m3u` | 12 | 8 | 0 | 3 | 1 | 0 |
| `playlists/countries/Honduras.m3u` | 59 | 48 | 0 | 10 | 1 | 0 |
| `playlists/countries/Hong_Kong.m3u` | 23 | 9 | 0 | 3 | 11 | 0 |
| `playlists/countries/Hungary.m3u` | 94 | 64 | 2 | 21 | 7 | 0 |
| `playlists/countries/Iceland.m3u` | 5 | 4 | 0 | 0 | 1 | 0 |
| `playlists/countries/India.m3u` | 805 | 743 | 13 | 29 | 20 | 0 |
| `playlists/countries/Indonesia.m3u` | 129 | 117 | 3 | 7 | 2 | 0 |
| `playlists/countries/International.m3u` | 1237 | 1155 | 30 | 28 | 24 | 0 |
| `playlists/countries/Iran.m3u` | 98 | 90 | 4 | 2 | 2 | 0 |
| `playlists/countries/Iraq.m3u` | 64 | 59 | 2 | 3 | 0 | 0 |
| `playlists/countries/Ireland.m3u` | 26 | 19 | 0 | 0 | 7 | 0 |
| `playlists/countries/Israel.m3u` | 41 | 31 | 0 | 0 | 10 | 0 |
| `playlists/countries/Italy.m3u` | 584 | 477 | 6 | 57 | 44 | 0 |
| `playlists/countries/Ivory_Coast.m3u` | 13 | 13 | 0 | 0 | 0 | 0 |
| `playlists/countries/Jamaica.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Japan.m3u` | 22 | 17 | 2 | 0 | 3 | 0 |
| `playlists/countries/Jordan.m3u` | 17 | 17 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kazakhstan.m3u` | 41 | 25 | 0 | 3 | 13 | 0 |
| `playlists/countries/Kenya.m3u` | 6 | 5 | 0 | 1 | 0 | 0 |
| `playlists/countries/Kosovo.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kuwait.m3u` | 14 | 13 | 1 | 0 | 0 | 0 |
| `playlists/countries/Kyrgyzstan.m3u` | 7 | 0 | 1 | 3 | 3 | 0 |
| `playlists/countries/Laos.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Latin_America.m3u` | 34 | 33 | 0 | 0 | 1 | 0 |
| `playlists/countries/Latvia.m3u` | 17 | 16 | 0 | 0 | 1 | 0 |
| `playlists/countries/Lebanon.m3u` | 31 | 28 | 0 | 2 | 1 | 0 |
| `playlists/countries/Libya.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Lithuania.m3u` | 25 | 19 | 0 | 0 | 6 | 0 |
| `playlists/countries/Luxembourg.m3u` | 16 | 12 | 2 | 2 | 0 | 0 |
| `playlists/countries/Macau.m3u` | 6 | 0 | 0 | 6 | 0 | 0 |
| `playlists/countries/Malaysia.m3u` | 6 | 4 | 0 | 0 | 2 | 0 |
| `playlists/countries/Maldives.m3u` | 6 | 4 | 0 | 1 | 1 | 0 |
| `playlists/countries/Mali.m3u` | 3 | 2 | 0 | 1 | 0 | 0 |
| `playlists/countries/Malta.m3u` | 7 | 3 | 0 | 0 | 4 | 0 |
| `playlists/countries/Martinique.m3u` | 6 | 5 | 0 | 1 | 0 | 0 |
| `playlists/countries/Mauritania.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mexico.m3u` | 159 | 123 | 2 | 10 | 24 | 0 |
| `playlists/countries/Moldova.m3u` | 20 | 20 | 0 | 0 | 0 | 0 |
| `playlists/countries/Monaco.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mongolia.m3u` | 79 | 79 | 0 | 0 | 0 | 0 |
| `playlists/countries/Montenegro.m3u` | 6 | 3 | 0 | 0 | 3 | 0 |
| `playlists/countries/Morocco.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mozambique.m3u` | 5 | 3 | 0 | 2 | 0 | 0 |
| `playlists/countries/Myanmar.m3u` | 17 | 5 | 0 | 12 | 0 | 0 |
| `playlists/countries/Namibia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nepal.m3u` | 10 | 8 | 0 | 0 | 2 | 0 |
| `playlists/countries/Netherlands.m3u` | 160 | 144 | 0 | 9 | 7 | 0 |
| `playlists/countries/New_Zealand.m3u` | 9 | 7 | 0 | 0 | 2 | 0 |
| `playlists/countries/Nicaragua.m3u` | 12 | 5 | 0 | 2 | 5 | 0 |
| `playlists/countries/Niger.m3u` | 3 | 1 | 0 | 0 | 2 | 0 |
| `playlists/countries/Nigeria.m3u` | 47 | 35 | 0 | 7 | 5 | 0 |
| `playlists/countries/North_Korea.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/North_Macedonia.m3u` | 23 | 21 | 0 | 2 | 0 | 0 |
| `playlists/countries/Norway.m3u` | 13 | 7 | 1 | 0 | 5 | 0 |
| `playlists/countries/Oman.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Pakistan.m3u` | 90 | 43 | 1 | 43 | 3 | 0 |
| `playlists/countries/Palestine.m3u` | 21 | 20 | 0 | 0 | 1 | 0 |
| `playlists/countries/Panama.m3u` | 18 | 15 | 0 | 3 | 0 | 0 |
| `playlists/countries/Papua_New_Guinea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Paraguay.m3u` | 57 | 55 | 1 | 0 | 1 | 0 |
| `playlists/countries/Peru.m3u` | 154 | 142 | 1 | 4 | 7 | 0 |
| `playlists/countries/Philippines.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Poland.m3u` | 186 | 152 | 0 | 28 | 6 | 0 |
| `playlists/countries/Portugal.m3u` | 70 | 48 | 0 | 16 | 6 | 0 |
| `playlists/countries/Puerto_Rico.m3u` | 25 | 23 | 0 | 1 | 1 | 0 |
| `playlists/countries/Qatar.m3u` | 43 | 36 | 0 | 0 | 7 | 0 |
| `playlists/countries/Republic_of_the_Congo.m3u` | 3 | 1 | 0 | 1 | 1 | 0 |
| `playlists/countries/Romania.m3u` | 141 | 117 | 3 | 11 | 10 | 0 |
| `playlists/countries/Russia.m3u` | 508 | 404 | 1 | 92 | 11 | 0 |
| `playlists/countries/Rwanda.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Kitts_and_Nevis.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Lucia.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/San_Marino.m3u` | 2 | 0 | 2 | 0 | 0 | 0 |
| `playlists/countries/Saudi_Arabia.m3u` | 66 | 52 | 6 | 0 | 8 | 0 |
| `playlists/countries/Senegal.m3u` | 7 | 6 | 0 | 1 | 0 | 0 |
| `playlists/countries/Serbia.m3u` | 27 | 18 | 3 | 5 | 1 | 0 |
| `playlists/countries/Sierra_Leone.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Singapore.m3u` | 25 | 23 | 0 | 0 | 2 | 0 |
| `playlists/countries/Sint_Maarten.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Slovakia.m3u` | 57 | 46 | 0 | 10 | 1 | 0 |
| `playlists/countries/Slovenia.m3u` | 9 | 5 | 0 | 4 | 0 | 0 |
| `playlists/countries/Somalia.m3u` | 9 | 4 | 0 | 5 | 0 | 0 |
| `playlists/countries/South_Africa.m3u` | 19 | 16 | 0 | 1 | 2 | 0 |
| `playlists/countries/South_Korea.m3u` | 92 | 67 | 7 | 15 | 3 | 0 |
| `playlists/countries/Spain.m3u` | 256 | 194 | 9 | 24 | 29 | 0 |
| `playlists/countries/Sri_Lanka.m3u` | 14 | 7 | 0 | 6 | 1 | 0 |
| `playlists/countries/Sudan.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Suriname.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sweden.m3u` | 385 | 374 | 0 | 3 | 8 | 0 |
| `playlists/countries/Switzerland.m3u` | 36 | 25 | 0 | 5 | 6 | 0 |
| `playlists/countries/Syria.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/countries/Taiwan.m3u` | 22 | 15 | 0 | 5 | 2 | 0 |
| `playlists/countries/Tajikistan.m3u` | 14 | 0 | 0 | 14 | 0 | 0 |
| `playlists/countries/Tanzania.m3u` | 6 | 5 | 0 | 1 | 0 | 0 |
| `playlists/countries/Thailand.m3u` | 89 | 63 | 1 | 9 | 16 | 0 |
| `playlists/countries/Togo.m3u` | 7 | 2 | 0 | 1 | 4 | 0 |
| `playlists/countries/Trinidad_and_Tobago.m3u` | 6 | 5 | 0 | 1 | 0 | 0 |
| `playlists/countries/Tunisia.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Turkey.m3u` | 154 | 132 | 4 | 12 | 6 | 0 |
| `playlists/countries/Turkmenistan.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/UK.m3u` | 334 | 219 | 4 | 21 | 90 | 0 |
| `playlists/countries/USA.m3u` | 2900 | 2670 | 48 | 69 | 113 | 0 |
| `playlists/countries/Uganda.m3u` | 13 | 10 | 0 | 2 | 1 | 0 |
| `playlists/countries/Ukraine.m3u` | 198 | 175 | 1 | 19 | 3 | 0 |
| `playlists/countries/United_Arab_Emirates.m3u` | 56 | 43 | 3 | 6 | 4 | 0 |
| `playlists/countries/Uruguay.m3u` | 11 | 9 | 1 | 0 | 1 | 0 |
| `playlists/countries/Uzbekistan.m3u` | 35 | 35 | 0 | 0 | 0 | 0 |
| `playlists/countries/Venezuela.m3u` | 60 | 51 | 1 | 5 | 3 | 0 |
| `playlists/countries/Vietnam.m3u` | 85 | 65 | 3 | 1 | 16 | 0 |
| `playlists/countries/Western_Sahara.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Yemen.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Zimbabwe.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |

## Patches applied

- Removed **229** confirmed-dead links across **47** playlists (working ratio 85.6%).
  - `PremiumTV.m3u`: -12 (13234 -> 13222)
  - `Albania.m3u`: -1 (25 -> 24)
  - `Argentina.m3u`: -3 (167 -> 164)
  - `Australia.m3u`: -5 (51 -> 46)
  - `Austria.m3u`: -1 (49 -> 48)
  - `Belgium.m3u`: -1 (44 -> 43)
  - `Cambodia.m3u`: -5 (20 -> 15)
  - `Canada.m3u`: -1 (186 -> 185)
  - `Chile.m3u`: -2 (223 -> 221)
  - `China.m3u`: -5 (164 -> 159)
  - `Colombia.m3u`: -2 (120 -> 118)
  - `Croatia.m3u`: -3 (18 -> 15)
  - `Dominican_Republic.m3u`: -1 (207 -> 206)
  - `Egypt.m3u`: -1 (18 -> 17)
  - `France.m3u`: -2 (249 -> 247)
  - `Germany.m3u`: -17 (423 -> 406)
  - `Hungary.m3u`: -2 (94 -> 92)
  - `India.m3u`: -13 (805 -> 792)
  - `Indonesia.m3u`: -3 (129 -> 126)
  - `International.m3u`: -30 (1237 -> 1207)
  - `Iran.m3u`: -4 (98 -> 94)
  - `Iraq.m3u`: -2 (64 -> 62)
  - `Italy.m3u`: -6 (584 -> 578)
  - `Japan.m3u`: -2 (22 -> 20)
  - `Kuwait.m3u`: -1 (14 -> 13)
  - `Kyrgyzstan.m3u`: -1 (7 -> 6)
  - `Luxembourg.m3u`: -2 (16 -> 14)
  - `Mexico.m3u`: -2 (159 -> 157)
  - `Norway.m3u`: -1 (13 -> 12)
  - `Pakistan.m3u`: -1 (90 -> 89)
  - `Paraguay.m3u`: -1 (57 -> 56)
  - `Peru.m3u`: -1 (154 -> 153)
  - `Romania.m3u`: -3 (141 -> 138)
  - `Russia.m3u`: -1 (508 -> 507)
  - `Saudi_Arabia.m3u`: -6 (66 -> 60)
  - `Serbia.m3u`: -3 (27 -> 24)
  - `South_Korea.m3u`: -7 (92 -> 85)
  - `Spain.m3u`: -9 (256 -> 247)
  - `Thailand.m3u`: -1 (89 -> 88)
  - `Turkey.m3u`: -4 (154 -> 150)
  - `UK.m3u`: -4 (334 -> 330)
  - `USA.m3u`: -48 (2900 -> 2853)
  - `Ukraine.m3u`: -1 (198 -> 197)
  - `United_Arab_Emirates.m3u`: -3 (56 -> 53)
  - `Uruguay.m3u`: -1 (11 -> 10)
  - `Venezuela.m3u`: -1 (60 -> 59)
  - `Vietnam.m3u`: -3 (85 -> 82)
  - skipped `Bermuda.m3u`: removing 1/1 entries exceeds --max-remove-ratio 35%
  - skipped `San_Marino.m3u`: removing 2/2 entries exceeds --max-remove-ratio 35%

## Hosts with the most failing links

| Host | Offline | Unreachable |
|---|---:|---:|
| `hls127.freeott.top:8080` | 0 | 96 |
| `31.148.48.15` | 0 | 94 |
| `103.250.28.74:8000` | 0 | 60 |
| `playlist.xtemus.com` | 0 | 30 |
| `57.128.210.196:8080` | 0 | 28 |
| `live.teleradiocom.tj` | 0 | 28 |
| `live.streamingfast.net` | 27 | 0 |
| `tvsen7.aynascope.net` | 0 | 22 |
| `91.228.35.249:8001` | 0 | 20 |
| `znty.dyndns.org:5010` | 0 | 20 |
| `5f22d76e220e1.streamlock.net` | 0 | 20 |
| `cdn.rostelekom-tv.xyz` | 0 | 18 |
| `51.254.199.122:8080` | 0 | 18 |
| `103.72.101.252:8080` | 0 | 18 |
| `mrtvott.com` | 0 | 16 |
| `151.80.18.177:86` | 0 | 16 |
| `64b16f23efbee.streamlock.net` | 0 | 16 |
| `190.197.41.183` | 0 | 14 |
| `jmp2.uk` | 2 | 12 |
| `mumbai-edge.smartplaytv.in` | 0 | 14 |
| `39.134.115.163:8080` | 0 | 14 |
| `183.207.248.71` | 0 | 12 |
| `cdn.tvmatic.net` | 0 | 12 |
| `atlantida1.aquax1.cfd` | 0 | 12 |
| `origin.dpsgo.com` | 2 | 10 |

## Sample of confirmed-dead links

| Channel | Reason | URL |
|---|---|---|
| Hallmark Mystery | HTTP 404 | `http://41.205.93.154/HALLMARK/index.m3u8` |
| News12+ Hudson Valley | variant HTTP 404 | `https://mdc.ott.alticeusa.net/live4.ott.optimum.net/live4-uploads/N12PLUS_H_WC_A1/index_new.m3u8` |
| Such TV | variant HTTP 404 | `https://video.primexsports.com/suchnews/live/playlist.m3u8` |
| TGRT Haber | playlist only, HTTP 404 | `https://canli.tgrthaber.com/tgrt.m3u8` |
| Vinh Long TV 1 (720p) | HTTP 404 | `https://dethich.pw/thvl1/index.m3u8` |
| Vizion Plus (1080p) | playlist only, HTTP 404 | `https://tringliveviz.akamaized.net/delta/105/out/u/qwaszxerdfcvrtryuy.m3u8` |
| Canal 4 Posadas (1080p) | HTTP 404 | `http://190.128.214.97:64333/play/a06l/index.m3u8` |
| Canal 7 Salta (1080p) | HTTP 404 | `https://vivo.solumedia.com:19360/cooperativa/cooperativa.m3u8` |
| Azahares Radiovisual Multimedia (720p) | HTTP 404 | `https://streamyes.alsolnet.com/azaharesfm/live/playlist.m3u8` |
| Expo Channel (360p) | variant HTTP dns lookup failed | `https://tvsnhlslivetest.akamaized.net/hls/live/2034711/EXPO-MSL4/master.m3u8` |
| TVSN | variant HTTP 404 | `https://tvsnhlslivetest.akamaized.net/hls/live/2034711/TVSN-MSL4/master.m3u8` |
| 2GB (1080p) | variant HTTP 404 | `https://2gblive.akamaized.net/hls/live/2033805/2GB/index.m3u8` |
| 3AW (1080p) | variant HTTP 404 | `https://3awlive.akamaized.net/hls/live/2032295/3AW/index.m3u8` |
| 6PR (1080p) | variant HTTP 404 | `https://6prlive.akamaized.net/hls/live/2033806/6PR/index.m3u8` |
| ServusTV (Backup 1) | variant HTTP 404 | `https://rbmn-live.akamaized.net/hls/live/2002825/geoSTVATweb/master.m3u8` |
| ☆ Surf Channel 🇪🇸 🏄 | playlist only, HTTP 400 | `https://jmp2.uk/stvp-ES3400002PY` |
| Channel 82 | variant HTTP 403 | `https://service.webvideocore.net/CL1olYogIrDWvwqiIKK7eBmnWbRkKKsu3nqabm9GlX02JOj3CDNXzodJMDEN2dk3/a_bq9clxfbupwg.m3u8` |
| Hang Meas HDTV (720p) | variant HTTP 404 | `http://clive.malisresidences.com:1935/hm_hdtv/_definst_/smil:hmhdt12356.smil/playlist.m3u8` |
| Hang Meas HDTV (Backup 1) | variant HTTP 404 | `http://clive.malisresidences.com:1935/hmcine/_definst_/smil:hmcine.smil/playlist.m3u8` |
| Hang Meas HDTV (Backup 2) | variant HTTP 404 | `http://clive.malisresidences.com:1935/hmgo/_definst_/smil:hmgo.smil/playlist.m3u8` |
| Hang Meas HDTV (Backup 3) | variant HTTP 404 | `http://clive.malisresidences.com:1935/hmnow/_definst_/smil:hmnow.smil/playlist.m3u8` |
| Hang Meas HDTV (Backup 4) | variant HTTP 404 | `http://clive.malisresidences.com:1935/hmplay/_definst_/smil:hmplay.smil/playlist.m3u8` |
| NatureTime ES (1080p) | variant HTTP 404 | `https://shls-live-ak.akamaized.net/out/v1/b06a89a463764d3688cda337d40dc5bf/index.m3u8` |
| 13P (720p) | variant HTTP 404 | `https://origin.dpsgo.com/ssai/event/p4mmBxEzSmKAxY1GusOHrw/master.m3u8` |
| 13E (720p) | variant HTTP 404 | `https://origin.dpsgo.com/ssai/event/BBp0VeP6QtOOlH8nu3bWTg/master.m3u8` |
