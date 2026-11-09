# Deep link check

- **Run:** nightly deep link check (`20261109T161048Z-3236`)
- **Started:** 2026-11-09T16:10:48Z  |  **Finished:** 2026-11-09T16:14:00Z  |  **Duration:** 192.0s
- **Mode:** deep (playlist + segment probe)
- **Unique links checked:** 12381 from 24255 playlist entries in 180 playlists

| Result | Links | Share | Meaning |
|---|---:|---:|---|
| working | 23102 | 95.2% | answered with playable media |
| offline | 590 | 2.4% | confirmed dead - removed when patching |
| unreachable | 287 | 1.2% | timeout or server error - kept, may recover |
| blocked | 276 | 1.1% | HTTP 401/403/451 - needs auth or is geo-blocked |

## Per playlist

| Playlist | Entries | Working | Offline | Unreachable | Blocked | Other |
|---|---:|---:|---:|---:|---:|---:|
| `playlists/PremiumTV.m3u` | 11805 | 11507 | 19 | 141 | 138 | 0 |
| `playlists/AE_Channels.m3u` | 71 | 70 | 0 | 1 | 0 | 0 |
| `playlists/countries/Afghanistan.m3u` | 10 | 7 | 3 | 0 | 0 | 0 |
| `playlists/countries/Albania.m3u` | 14 | 12 | 2 | 0 | 0 | 0 |
| `playlists/countries/Algeria.m3u` | 4 | 3 | 0 | 0 | 1 | 0 |
| `playlists/countries/Andorra.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Angola.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Antigua_and_Barbuda.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Arab_World.m3u` | 13 | 13 | 0 | 0 | 0 | 0 |
| `playlists/countries/Argentina.m3u` | 163 | 156 | 3 | 2 | 2 | 0 |
| `playlists/countries/Armenia.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Aruba.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Australia.m3u` | 44 | 33 | 11 | 0 | 0 | 0 |
| `playlists/countries/Austria.m3u` | 42 | 39 | 2 | 1 | 0 | 0 |
| `playlists/countries/Azerbaijan.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bahamas.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bahrain.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bangladesh.m3u` | 26 | 24 | 1 | 1 | 0 | 0 |
| `playlists/countries/Barbados.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Belarus.m3u` | 34 | 27 | 2 | 5 | 0 | 0 |
| `playlists/countries/Belgium.m3u` | 36 | 35 | 1 | 0 | 0 | 0 |
| `playlists/countries/Belize.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Benin.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bermuda.m3u` | 1 | 0 | 1 | 0 | 0 | 0 |
| `playlists/countries/Bolivia.m3u` | 46 | 41 | 3 | 2 | 0 | 0 |
| `playlists/countries/Bosnia_and_Herzegovina.m3u` | 9 | 8 | 1 | 0 | 0 | 0 |
| `playlists/countries/Brazil.m3u` | 181 | 179 | 1 | 0 | 1 | 0 |
| `playlists/countries/British_Virgin_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bulgaria.m3u` | 63 | 63 | 0 | 0 | 0 | 0 |
| `playlists/countries/Burkina_Faso.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Burundi.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cambodia.m3u` | 17 | 12 | 5 | 0 | 0 | 0 |
| `playlists/countries/Cameroon.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Canada.m3u` | 155 | 150 | 4 | 1 | 0 | 0 |
| `playlists/countries/Cape_Verde.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Caribbean_Netherlands.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Chad.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Chile.m3u` | 187 | 170 | 8 | 8 | 1 | 0 |
| `playlists/countries/China.m3u` | 97 | 90 | 6 | 1 | 0 | 0 |
| `playlists/countries/Colombia.m3u` | 115 | 106 | 7 | 0 | 2 | 0 |
| `playlists/countries/Costa_Rica.m3u` | 58 | 55 | 3 | 0 | 0 | 0 |
| `playlists/countries/Croatia.m3u` | 12 | 9 | 3 | 0 | 0 | 0 |
| `playlists/countries/Cuba.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Curacao.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cyprus.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Czechia.m3u` | 100 | 91 | 1 | 8 | 0 | 0 |
| `playlists/countries/DR_Congo.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Denmark.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Dominican_Republic.m3u` | 186 | 169 | 10 | 7 | 0 | 0 |
| `playlists/countries/Ecuador.m3u` | 45 | 44 | 0 | 1 | 0 | 0 |
| `playlists/countries/Egypt.m3u` | 18 | 16 | 1 | 0 | 1 | 0 |
| `playlists/countries/El_Salvador.m3u` | 15 | 14 | 1 | 0 | 0 | 0 |
| `playlists/countries/Equatorial_Guinea.m3u` | 1 | 0 | 1 | 0 | 0 | 0 |
| `playlists/countries/Eritrea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Estonia.m3u` | 22 | 22 | 0 | 0 | 0 | 0 |
| `playlists/countries/Ethiopia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Faroe_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Finland.m3u` | 26 | 26 | 0 | 0 | 0 | 0 |
| `playlists/countries/France.m3u` | 257 | 222 | 3 | 8 | 24 | 0 |
| `playlists/countries/French_Guiana.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Gambia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Georgia.m3u` | 14 | 13 | 1 | 0 | 0 | 0 |
| `playlists/countries/Germany.m3u` | 396 | 373 | 19 | 4 | 0 | 0 |
| `playlists/countries/Ghana.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Greece.m3u` | 86 | 80 | 4 | 0 | 2 | 0 |
| `playlists/countries/Guadeloupe.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guam.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guatemala.m3u` | 31 | 28 | 3 | 0 | 0 | 0 |
| `playlists/countries/Guinea.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guyana.m3u` | 10 | 9 | 1 | 0 | 0 | 0 |
| `playlists/countries/Haiti.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Honduras.m3u` | 42 | 40 | 1 | 1 | 0 | 0 |
| `playlists/countries/Hong_Kong.m3u` | 9 | 8 | 1 | 0 | 0 | 0 |
| `playlists/countries/Hungary.m3u` | 145 | 142 | 2 | 1 | 0 | 0 |
| `playlists/countries/Iceland.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/India.m3u` | 753 | 708 | 39 | 1 | 5 | 0 |
| `playlists/countries/Indonesia.m3u` | 109 | 100 | 6 | 3 | 0 | 0 |
| `playlists/countries/International.m3u` | 1110 | 1053 | 50 | 6 | 1 | 0 |
| `playlists/countries/Iran.m3u` | 116 | 89 | 27 | 0 | 0 | 0 |
| `playlists/countries/Iraq.m3u` | 62 | 57 | 5 | 0 | 0 | 0 |
| `playlists/countries/Ireland.m3u` | 23 | 19 | 4 | 0 | 0 | 0 |
| `playlists/countries/Israel.m3u` | 35 | 34 | 0 | 0 | 1 | 0 |
| `playlists/countries/Italy.m3u` | 540 | 510 | 7 | 20 | 3 | 0 |
| `playlists/countries/Ivory_Coast.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/countries/Jamaica.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Japan.m3u` | 24 | 18 | 5 | 1 | 0 | 0 |
| `playlists/countries/Jordan.m3u` | 19 | 16 | 3 | 0 | 0 | 0 |
| `playlists/countries/Kazakhstan.m3u` | 25 | 24 | 0 | 1 | 0 | 0 |
| `playlists/countries/Kenya.m3u` | 8 | 7 | 1 | 0 | 0 | 0 |
| `playlists/countries/Kosovo.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kuwait.m3u` | 14 | 13 | 1 | 0 | 0 | 0 |
| `playlists/countries/Laos.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Latin_America.m3u` | 33 | 33 | 0 | 0 | 0 | 0 |
| `playlists/countries/Latvia.m3u` | 16 | 7 | 0 | 0 | 9 | 0 |
| `playlists/countries/Lebanon.m3u` | 29 | 25 | 4 | 0 | 0 | 0 |
| `playlists/countries/Libya.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Lithuania.m3u` | 19 | 19 | 0 | 0 | 0 | 0 |
| `playlists/countries/Luxembourg.m3u` | 16 | 12 | 4 | 0 | 0 | 0 |
| `playlists/countries/Macau.m3u` | 1 | 0 | 1 | 0 | 0 | 0 |
| `playlists/countries/Malaysia.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Maldives.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Malta.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Martinique.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mauritania.m3u` | 1 | 0 | 1 | 0 | 0 | 0 |
| `playlists/countries/Mexico.m3u` | 122 | 114 | 6 | 2 | 0 | 0 |
| `playlists/countries/Moldova.m3u` | 20 | 18 | 0 | 0 | 2 | 0 |
| `playlists/countries/Monaco.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mongolia.m3u` | 80 | 78 | 2 | 0 | 0 | 0 |
| `playlists/countries/Montenegro.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Morocco.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mozambique.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Myanmar.m3u` | 13 | 9 | 0 | 4 | 0 | 0 |
| `playlists/countries/Namibia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nepal.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Netherlands.m3u` | 160 | 145 | 12 | 2 | 1 | 0 |
| `playlists/countries/New_Zealand.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nicaragua.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Niger.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nigeria.m3u` | 27 | 13 | 14 | 0 | 0 | 0 |
| `playlists/countries/North_Korea.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/North_Macedonia.m3u` | 19 | 19 | 0 | 0 | 0 | 0 |
| `playlists/countries/Norway.m3u` | 10 | 9 | 1 | 0 | 0 | 0 |
| `playlists/countries/Oman.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Pakistan.m3u` | 50 | 47 | 1 | 2 | 0 | 0 |
| `playlists/countries/Palestine.m3u` | 20 | 20 | 0 | 0 | 0 | 0 |
| `playlists/countries/Panama.m3u` | 15 | 14 | 0 | 1 | 0 | 0 |
| `playlists/countries/Papua_New_Guinea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Paraguay.m3u` | 55 | 53 | 2 | 0 | 0 | 0 |
| `playlists/countries/Peru.m3u` | 133 | 124 | 7 | 2 | 0 | 0 |
| `playlists/countries/Philippines.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Poland.m3u` | 185 | 182 | 1 | 2 | 0 | 0 |
| `playlists/countries/Portugal.m3u` | 50 | 50 | 0 | 0 | 0 | 0 |
| `playlists/countries/Puerto_Rico.m3u` | 25 | 21 | 1 | 0 | 3 | 0 |
| `playlists/countries/Qatar.m3u` | 37 | 36 | 1 | 0 | 0 | 0 |
| `playlists/countries/Republic_of_the_Congo.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Romania.m3u` | 149 | 148 | 1 | 0 | 0 | 0 |
| `playlists/countries/Russia.m3u` | 443 | 421 | 14 | 7 | 1 | 0 |
| `playlists/countries/Rwanda.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Kitts_and_Nevis.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Lucia.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/San_Marino.m3u` | 2 | 0 | 2 | 0 | 0 | 0 |
| `playlists/countries/Saudi_Arabia.m3u` | 54 | 49 | 5 | 0 | 0 | 0 |
| `playlists/countries/Senegal.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Serbia.m3u` | 21 | 19 | 2 | 0 | 0 | 0 |
| `playlists/countries/Sierra_Leone.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Singapore.m3u` | 36 | 35 | 1 | 0 | 0 | 0 |
| `playlists/countries/Sint_Maarten.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Slovakia.m3u` | 60 | 55 | 0 | 5 | 0 | 0 |
| `playlists/countries/Slovenia.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Somalia.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/South_Africa.m3u` | 16 | 13 | 3 | 0 | 0 | 0 |
| `playlists/countries/South_Korea.m3u` | 78 | 72 | 6 | 0 | 0 | 0 |
| `playlists/countries/Spain.m3u` | 229 | 198 | 30 | 0 | 1 | 0 |
| `playlists/countries/Sri_Lanka.m3u` | 6 | 4 | 2 | 0 | 0 | 0 |
| `playlists/countries/Sudan.m3u` | 4 | 3 | 1 | 0 | 0 | 0 |
| `playlists/countries/Suriname.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sweden.m3u` | 376 | 376 | 0 | 0 | 0 | 0 |
| `playlists/countries/Switzerland.m3u` | 31 | 30 | 0 | 0 | 1 | 0 |
| `playlists/countries/Syria.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Taiwan.m3u` | 17 | 17 | 0 | 0 | 0 | 0 |
| `playlists/countries/Tajikistan.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Tanzania.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Thailand.m3u` | 77 | 75 | 1 | 1 | 0 | 0 |
| `playlists/countries/Togo.m3u` | 7 | 3 | 0 | 0 | 4 | 0 |
| `playlists/countries/Trinidad_and_Tobago.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Tunisia.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Turkey.m3u` | 147 | 134 | 10 | 3 | 0 | 0 |
| `playlists/countries/Turkmenistan.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/UK.m3u` | 270 | 248 | 11 | 5 | 6 | 0 |
| `playlists/countries/USA.m3u` | 2937 | 2706 | 143 | 24 | 64 | 0 |
| `playlists/countries/Uganda.m3u` | 12 | 10 | 2 | 0 | 0 | 0 |
| `playlists/countries/Ukraine.m3u` | 172 | 168 | 4 | 0 | 0 | 0 |
| `playlists/countries/United_Arab_Emirates.m3u` | 46 | 42 | 4 | 0 | 0 | 0 |
| `playlists/countries/Uruguay.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Uzbekistan.m3u` | 30 | 30 | 0 | 0 | 0 | 0 |
| `playlists/countries/Venezuela.m3u` | 56 | 50 | 3 | 1 | 2 | 0 |
| `playlists/countries/Vietnam.m3u` | 65 | 61 | 3 | 1 | 0 | 0 |
| `playlists/countries/Western_Sahara.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Yemen.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Zimbabwe.m3u` | 1 | 0 | 1 | 0 | 0 | 0 |

## Patches applied

- Removed **576** confirmed-dead links across **80** playlists (working ratio 95.2%).
  - `PremiumTV.m3u`: -19 (11805 -> 11786)
  - `Afghanistan.m3u`: -3 (10 -> 7)
  - `Albania.m3u`: -2 (14 -> 12)
  - `Argentina.m3u`: -3 (163 -> 160)
  - `Australia.m3u`: -11 (44 -> 33)
  - `Austria.m3u`: -2 (42 -> 40)
  - `Bangladesh.m3u`: -1 (26 -> 25)
  - `Belarus.m3u`: -2 (34 -> 32)
  - `Belgium.m3u`: -1 (36 -> 35)
  - `Bermuda.m3u`: -1 (1 -> 0)
  - `Bolivia.m3u`: -3 (46 -> 43)
  - `Bosnia_and_Herzegovina.m3u`: -1 (9 -> 8)
  - `Brazil.m3u`: -1 (181 -> 180)
  - `Cambodia.m3u`: -5 (17 -> 12)
  - `Canada.m3u`: -4 (155 -> 151)
  - `Chile.m3u`: -8 (187 -> 179)
  - `China.m3u`: -6 (97 -> 91)
  - `Colombia.m3u`: -7 (115 -> 108)
  - `Costa_Rica.m3u`: -3 (58 -> 55)
  - `Croatia.m3u`: -3 (12 -> 9)
  - `Czechia.m3u`: -1 (100 -> 99)
  - `Dominican_Republic.m3u`: -10 (186 -> 176)
  - `Egypt.m3u`: -1 (18 -> 17)
  - `El_Salvador.m3u`: -1 (15 -> 14)
  - `Equatorial_Guinea.m3u`: -1 (1 -> 0)
  - `France.m3u`: -3 (257 -> 254)
  - `Georgia.m3u`: -1 (14 -> 13)
  - `Germany.m3u`: -19 (396 -> 377)
  - `Greece.m3u`: -4 (86 -> 82)
  - `Guatemala.m3u`: -3 (31 -> 28)
  - `Guyana.m3u`: -1 (10 -> 9)
  - `Honduras.m3u`: -1 (42 -> 41)
  - `Hong_Kong.m3u`: -1 (9 -> 8)
  - `Hungary.m3u`: -2 (145 -> 143)
  - `India.m3u`: -39 (753 -> 714)
  - `Indonesia.m3u`: -6 (109 -> 103)
  - `International.m3u`: -50 (1110 -> 1060)
  - `Iran.m3u`: -27 (116 -> 89)
  - `Iraq.m3u`: -5 (62 -> 57)
  - `Ireland.m3u`: -4 (23 -> 19)
  - `Italy.m3u`: -7 (540 -> 533)
  - `Japan.m3u`: -5 (24 -> 19)
  - `Jordan.m3u`: -3 (19 -> 16)
  - `Kenya.m3u`: -1 (8 -> 7)
  - `Kuwait.m3u`: -1 (14 -> 13)
  - `Lebanon.m3u`: -4 (29 -> 25)
  - `Luxembourg.m3u`: -4 (16 -> 12)
  - `Macau.m3u`: -1 (1 -> 0)
  - `Mauritania.m3u`: -1 (1 -> 0)
  - `Mexico.m3u`: -6 (122 -> 116)
  - `Mongolia.m3u`: -2 (80 -> 78)
  - `Netherlands.m3u`: -12 (160 -> 148)
  - `Norway.m3u`: -1 (10 -> 9)
  - `Pakistan.m3u`: -1 (50 -> 49)
  - `Paraguay.m3u`: -2 (55 -> 53)
  - `Peru.m3u`: -7 (133 -> 126)
  - `Poland.m3u`: -1 (185 -> 184)
  - `Puerto_Rico.m3u`: -1 (25 -> 24)
  - `Qatar.m3u`: -1 (37 -> 36)
  - `Romania.m3u`: -1 (149 -> 148)
  - `Russia.m3u`: -14 (443 -> 429)
  - `San_Marino.m3u`: -2 (2 -> 0)
  - `Saudi_Arabia.m3u`: -5 (54 -> 49)
  - `Serbia.m3u`: -2 (21 -> 19)
  - `Singapore.m3u`: -1 (36 -> 35)
  - `South_Africa.m3u`: -3 (16 -> 13)
  - `South_Korea.m3u`: -6 (78 -> 72)
  - `Spain.m3u`: -30 (229 -> 199)
  - `Sri_Lanka.m3u`: -2 (6 -> 4)
  - `Sudan.m3u`: -1 (4 -> 3)
  - `Thailand.m3u`: -1 (77 -> 76)
  - `Turkey.m3u`: -10 (147 -> 137)
  - `UK.m3u`: -11 (270 -> 259)
  - `USA.m3u`: -143 (2937 -> 2795)
  - `Uganda.m3u`: -2 (12 -> 10)
  - `Ukraine.m3u`: -4 (172 -> 168)
  - `United_Arab_Emirates.m3u`: -4 (46 -> 42)
  - `Venezuela.m3u`: -3 (56 -> 53)
  - `Vietnam.m3u`: -3 (65 -> 62)
  - `Zimbabwe.m3u`: -1 (1 -> 0)
  - skipped `Nigeria.m3u`: removing 14/27 entries exceeds --max-remove-ratio 35%

## Hosts with the most failing links

| Host | Offline | Unreachable |
|---|---:|---:|
| `rpn.bozztv.com` | 52 | 0 |
| `live20.bozztv.com` | 38 | 0 |
| `live.streamingfast.net` | 27 | 0 |
| `sktv.mxnticek.eu` | 2 | 22 |
| `ncdn.telewebion.ir` | 21 | 0 |
| `viewmedia7219.bozztv.com` | 19 | 0 |
| `103.135.253.32:8080` | 18 | 0 |
| `cdn4.skygo.mn` | 17 | 0 |
| `5f22d76e220e1.streamlock.net` | 0 | 16 |
| `tgn.bozztv.com` | 15 | 0 |
| `5.180.164.197:8080` | 0 | 14 |
| `64b16f23efbee.streamlock.net` | 0 | 14 |
| `23.239.31.26:8989` | 0 | 11 |
| `lbgo.bozztv.com` | 11 | 0 |
| `wdrlokalzeit.akamaized.net` | 11 | 0 |
| `livestreaming.b67buv2.tweedekamer.nl` | 11 | 0 |
| `30a-tv.com` | 2 | 8 |
| `45.14.84.37` | 0 | 10 |
| `3abn.bozztv.com` | 10 | 0 |
| `abcnews-streams.akamaized.net` | 10 | 0 |
| `origin.dpsgo.com` | 1 | 8 |
| `198.58.104.90:8989` | 0 | 8 |
| `cloud2.streaminglivehd.com:1936` | 3 | 5 |
| `mdc.ott.alticeusa.net` | 8 | 0 |
| `edge55.dc.beltelecom.by` | 0 | 8 |

## Sample of confirmed-dead links

| Channel | Reason | URL |
|---|---|---|
| Gazi TV (720p) | variant HTTP 404 | `https://app.ncare.live/c3VydmVyX8RpbEU9Mi8xNy8yMDE0GIDU6RgzQ6NTAgdEoaeFzbF92YWxIZTO0U0ezN1IzMyfvcGVMZEJCTEFWeVN3PTOmdFsaWRtaW51aiPhnPTI2/gazibdz.stream/live-orgin/gazibdz.stream/playlist.m3u8` |
| Mei Ah Movie Channel (1080p) | HTTP 404 | `http://103.172.187.30:12000/stream/mytv/null-2/master.m3u8` |
| Nova Cinema | html page, not a stream | `https://sktv.mxnticek.eu/new/stream.php?ch=NovaCinema` |
| LiraTV (720p) | HTTP 404 | `https://cloud2.streaminglivehd.com:1936/liratv/liratv/playlist.m3u8` |
| Millenium 109 FM | HTTP 404 | `https://videoserver.tmcreativos.com:19360/nqvnhujhrx/nqvnhujhrx.m3u8` |
| Tolo TV | dns lookup failed | `https://tgn.bozztv.com/eshgtv-dvrfl05/gin-tolohd/tracks-v1a1/mono.m3u8` |
| Lemar TV (720p) | dns lookup failed | `https://tgn.bozztv.com/eshgtv-dvrfl05/gin-lemar/index.m3u8` |
| TOLOnews (720p) | dns lookup failed | `https://tgn.bozztv.com/eshgtv-dvrfl05/gin-tolonews/index.m3u8` |
| TV 7 Albania | dns lookup failed | `https://rpn3.bozztv.com/albaniatv/Med7-TV7Tirana/index.m3u8` |
| AlbKanale Music TV HD (1080p) | variant HTTP dns lookup failed | `https://albportal.net/albkanalemusic.m3u8` |
| Ciudad Magica (720p) | dns lookup failed | `https://lbgo.bozztv.com/ssh101/ssh101/verycoolfgr/playlist.m3u8` |
| Canal 8 San Juan (720p) [Not 24/7] | dns lookup failed | `https://live20.bozztv.com/akamaissh101/ssh101/canal8sanjuan/playlist.m3u8` |
| Senal U | dns lookup failed | `https://live20.bozztv.com/giatv/giatv-canal30tda/canal30tda/chunks.m3u8` |
| Expo Channel (360p) | variant HTTP dns lookup failed | `https://tvsnhlslivetest.akamaized.net/hls/live/2034711/EXPO-MSL4/master.m3u8` |
| 10 HD | playlist only, HTTP 403 | `https://i.mjh.nz/.r/10-nsw.m3u8` |
| 10 Peach | playlist only, HTTP 403 | `https://i.mjh.nz/.r/10peach-nsw.m3u8` |
| 7flix | playlist only, HTTP 403 | `https://i.mjh.nz/.r/7flix-syd.m3u8` |
| 7mate | playlist only, HTTP 403 | `https://i.mjh.nz/.r/7mate-syd.m3u8` |
| ServusTV (576p) | HTTP 404 | `https://s6.hopslan.com/servuz1/index.m3u8` |
| ServusTV (Backup 1) | variant HTTP 404 | `https://rbmn-live.akamaized.net/hls/live/2002825/geoSTVATweb/master.m3u8` |
| Star News (1080p) | connection refused | `http://103.135.253.32:8080/Star-News/index.m3u8` |
| Первый Музыкальный Канал (Backup 1) | variant HTTP 404 | `https://ngtrk.dc.beltelecom.by/ngtrk/smil:ont.smil/playlist.m3u8` |
| Belros Ⓢ | playlist only, HTTP 404 | `https://live2.mediacdn.ru/sr1/tro/playlist.m3u8` |
| ☆ Surf Channel 🇪🇸 🏄 | playlist only, HTTP 400 | `https://jmp2.uk/stvp-ES3400002PY` |
| Channel 82 | variant HTTP 403 | `https://service.webvideocore.net/CL1olYogIrDWvwqiIKK7eBmnWbRkKKsu3nqabm9GlX02JOj3CDNXzodJMDEN2dk3/a_bq9clxfbupwg.m3u8` |
