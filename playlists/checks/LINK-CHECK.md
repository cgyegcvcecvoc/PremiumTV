# Deep link check

- **Run:** nightly deep link check (`20261002T201122Z-2518`)
- **Started:** 2026-10-02T20:11:22Z  |  **Finished:** 2026-10-02T20:14:38Z  |  **Duration:** 196.0s
- **Mode:** deep (playlist + segment probe)
- **Unique links checked:** 12286 from 24640 playlist entries in 179 playlists

| Result | Links | Share | Meaning |
|---|---:|---:|---|
| working | 20379 | 82.7% | answered with playable media |
| offline | 4143 | 16.8% | confirmed dead - removed when patching |
| unreachable | 96 | 0.4% | timeout or server error - kept, may recover |
| blocked | 22 | 0.1% | HTTP 401/403/451 - needs auth or is geo-blocked |

## Per playlist

| Playlist | Entries | Working | Offline | Unreachable | Blocked | Other |
|---|---:|---:|---:|---:|---:|---:|
| `playlists/PremiumTV.m3u` | 12286 | 10160 | 2067 | 48 | 11 | 0 |
| `playlists/AE_Channels.m3u` | 68 | 59 | 9 | 0 | 0 | 0 |
| `playlists/countries/Afghanistan.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Albania.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/Algeria.m3u` | 6 | 4 | 1 | 0 | 1 | 0 |
| `playlists/countries/Andorra.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Angola.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Arab_World.m3u` | 15 | 15 | 0 | 0 | 0 | 0 |
| `playlists/countries/Argentina.m3u` | 158 | 157 | 1 | 0 | 0 | 0 |
| `playlists/countries/Armenia.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Aruba.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/countries/Australia.m3u` | 39 | 16 | 23 | 0 | 0 | 0 |
| `playlists/countries/Austria.m3u` | 38 | 36 | 2 | 0 | 0 | 0 |
| `playlists/countries/Azerbaijan.m3u` | 14 | 14 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bahamas.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bahrain.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bangladesh.m3u` | 23 | 20 | 3 | 0 | 0 | 0 |
| `playlists/countries/Barbados.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Belarus.m3u` | 28 | 23 | 5 | 0 | 0 | 0 |
| `playlists/countries/Belgium.m3u` | 29 | 27 | 2 | 0 | 0 | 0 |
| `playlists/countries/Belize.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Benin.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bermuda.m3u` | 1 | 0 | 1 | 0 | 0 | 0 |
| `playlists/countries/Bolivia.m3u` | 49 | 49 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bosnia_and_Herzegovina.m3u` | 11 | 10 | 1 | 0 | 0 | 0 |
| `playlists/countries/Brazil.m3u` | 190 | 185 | 4 | 0 | 1 | 0 |
| `playlists/countries/British_Virgin_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bulgaria.m3u` | 28 | 28 | 0 | 0 | 0 | 0 |
| `playlists/countries/Burkina_Faso.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cambodia.m3u` | 19 | 14 | 5 | 0 | 0 | 0 |
| `playlists/countries/Cameroon.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Canada.m3u` | 143 | 133 | 10 | 0 | 0 | 0 |
| `playlists/countries/Cape_Verde.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Caribbean_Netherlands.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Chad.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Chile.m3u` | 204 | 193 | 11 | 0 | 0 | 0 |
| `playlists/countries/China.m3u` | 94 | 59 | 35 | 0 | 0 | 0 |
| `playlists/countries/Colombia.m3u` | 108 | 103 | 3 | 2 | 0 | 0 |
| `playlists/countries/Costa_Rica.m3u` | 56 | 55 | 1 | 0 | 0 | 0 |
| `playlists/countries/Croatia.m3u` | 18 | 15 | 3 | 0 | 0 | 0 |
| `playlists/countries/Cuba.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Curacao.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cyprus.m3u` | 21 | 21 | 0 | 0 | 0 | 0 |
| `playlists/countries/Czechia.m3u` | 88 | 76 | 0 | 12 | 0 | 0 |
| `playlists/countries/DR_Congo.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Denmark.m3u` | 11 | 6 | 5 | 0 | 0 | 0 |
| `playlists/countries/Dominican_Republic.m3u` | 202 | 195 | 6 | 1 | 0 | 0 |
| `playlists/countries/Ecuador.m3u` | 57 | 57 | 0 | 0 | 0 | 0 |
| `playlists/countries/Egypt.m3u` | 16 | 15 | 1 | 0 | 0 | 0 |
| `playlists/countries/El_Salvador.m3u` | 28 | 28 | 0 | 0 | 0 | 0 |
| `playlists/countries/Equatorial_Guinea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Eritrea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Estonia.m3u` | 22 | 20 | 2 | 0 | 0 | 0 |
| `playlists/countries/Ethiopia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Faroe_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Finland.m3u` | 33 | 28 | 4 | 1 | 0 | 0 |
| `playlists/countries/France.m3u` | 203 | 190 | 12 | 0 | 1 | 0 |
| `playlists/countries/French_Guiana.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Gambia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Georgia.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/countries/Germany.m3u` | 406 | 173 | 233 | 0 | 0 | 0 |
| `playlists/countries/Ghana.m3u` | 8 | 7 | 1 | 0 | 0 | 0 |
| `playlists/countries/Greece.m3u` | 88 | 86 | 1 | 1 | 0 | 0 |
| `playlists/countries/Guadeloupe.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guam.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guatemala.m3u` | 31 | 30 | 0 | 1 | 0 | 0 |
| `playlists/countries/Guinea.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guyana.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Haiti.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/countries/Honduras.m3u` | 50 | 49 | 1 | 0 | 0 | 0 |
| `playlists/countries/Hong_Kong.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/countries/Hungary.m3u` | 112 | 105 | 6 | 1 | 0 | 0 |
| `playlists/countries/Iceland.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/India.m3u` | 791 | 739 | 52 | 0 | 0 | 0 |
| `playlists/countries/Indonesia.m3u` | 120 | 117 | 3 | 0 | 0 | 0 |
| `playlists/countries/International.m3u` | 1198 | 974 | 221 | 3 | 0 | 0 |
| `playlists/countries/Iran.m3u` | 120 | 54 | 66 | 0 | 0 | 0 |
| `playlists/countries/Iraq.m3u` | 62 | 60 | 2 | 0 | 0 | 0 |
| `playlists/countries/Ireland.m3u` | 26 | 20 | 6 | 0 | 0 | 0 |
| `playlists/countries/Israel.m3u` | 31 | 31 | 0 | 0 | 0 | 0 |
| `playlists/countries/Italy.m3u` | 527 | 491 | 30 | 6 | 0 | 0 |
| `playlists/countries/Ivory_Coast.m3u` | 17 | 17 | 0 | 0 | 0 | 0 |
| `playlists/countries/Jamaica.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Japan.m3u` | 24 | 19 | 5 | 0 | 0 | 0 |
| `playlists/countries/Jordan.m3u` | 18 | 16 | 2 | 0 | 0 | 0 |
| `playlists/countries/Kazakhstan.m3u` | 39 | 38 | 0 | 1 | 0 | 0 |
| `playlists/countries/Kenya.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kosovo.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kuwait.m3u` | 15 | 14 | 1 | 0 | 0 | 0 |
| `playlists/countries/Kyrgyzstan.m3u` | 2 | 1 | 1 | 0 | 0 | 0 |
| `playlists/countries/Laos.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/countries/Latin_America.m3u` | 33 | 33 | 0 | 0 | 0 | 0 |
| `playlists/countries/Latvia.m3u` | 17 | 17 | 0 | 0 | 0 | 0 |
| `playlists/countries/Lebanon.m3u` | 30 | 28 | 2 | 0 | 0 | 0 |
| `playlists/countries/Libya.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Lithuania.m3u` | 17 | 17 | 0 | 0 | 0 | 0 |
| `playlists/countries/Luxembourg.m3u` | 15 | 13 | 2 | 0 | 0 | 0 |
| `playlists/countries/Macau.m3u` | 1 | 0 | 1 | 0 | 0 | 0 |
| `playlists/countries/Malaysia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Maldives.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mali.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Malta.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Martinique.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mauritania.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mexico.m3u` | 132 | 128 | 4 | 0 | 0 | 0 |
| `playlists/countries/Moldova.m3u` | 25 | 23 | 2 | 0 | 0 | 0 |
| `playlists/countries/Monaco.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mongolia.m3u` | 77 | 76 | 1 | 0 | 0 | 0 |
| `playlists/countries/Montenegro.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Morocco.m3u` | 12 | 9 | 3 | 0 | 0 | 0 |
| `playlists/countries/Mozambique.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Myanmar.m3u` | 5 | 4 | 1 | 0 | 0 | 0 |
| `playlists/countries/Namibia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nepal.m3u` | 9 | 7 | 2 | 0 | 0 | 0 |
| `playlists/countries/Netherlands.m3u` | 172 | 141 | 31 | 0 | 0 | 0 |
| `playlists/countries/New_Zealand.m3u` | 7 | 5 | 2 | 0 | 0 | 0 |
| `playlists/countries/Nicaragua.m3u` | 6 | 5 | 1 | 0 | 0 | 0 |
| `playlists/countries/Niger.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nigeria.m3u` | 37 | 35 | 2 | 0 | 0 | 0 |
| `playlists/countries/North_Korea.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/North_Macedonia.m3u` | 18 | 18 | 0 | 0 | 0 | 0 |
| `playlists/countries/Norway.m3u` | 6 | 5 | 1 | 0 | 0 | 0 |
| `playlists/countries/Oman.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Pakistan.m3u` | 61 | 60 | 1 | 0 | 0 | 0 |
| `playlists/countries/Palestine.m3u` | 21 | 21 | 0 | 0 | 0 | 0 |
| `playlists/countries/Panama.m3u` | 14 | 13 | 1 | 0 | 0 | 0 |
| `playlists/countries/Papua_New_Guinea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Paraguay.m3u` | 63 | 62 | 1 | 0 | 0 | 0 |
| `playlists/countries/Peru.m3u` | 153 | 153 | 0 | 0 | 0 | 0 |
| `playlists/countries/Philippines.m3u` | 11 | 9 | 2 | 0 | 0 | 0 |
| `playlists/countries/Poland.m3u` | 121 | 112 | 9 | 0 | 0 | 0 |
| `playlists/countries/Portugal.m3u` | 48 | 44 | 4 | 0 | 0 | 0 |
| `playlists/countries/Puerto_Rico.m3u` | 28 | 27 | 1 | 0 | 0 | 0 |
| `playlists/countries/Qatar.m3u` | 38 | 37 | 1 | 0 | 0 | 0 |
| `playlists/countries/Republic_of_the_Congo.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Romania.m3u` | 127 | 110 | 17 | 0 | 0 | 0 |
| `playlists/countries/Russia.m3u` | 441 | 419 | 21 | 1 | 0 | 0 |
| `playlists/countries/Rwanda.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Kitts_and_Nevis.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Lucia.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/San_Marino.m3u` | 2 | 0 | 2 | 0 | 0 | 0 |
| `playlists/countries/Saudi_Arabia.m3u` | 57 | 52 | 5 | 0 | 0 | 0 |
| `playlists/countries/Senegal.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Serbia.m3u` | 24 | 20 | 4 | 0 | 0 | 0 |
| `playlists/countries/Sierra_Leone.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Singapore.m3u` | 21 | 19 | 2 | 0 | 0 | 0 |
| `playlists/countries/Sint_Maarten.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Slovakia.m3u` | 56 | 44 | 1 | 11 | 0 | 0 |
| `playlists/countries/Slovenia.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Somalia.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/South_Africa.m3u` | 16 | 15 | 1 | 0 | 0 | 0 |
| `playlists/countries/South_Korea.m3u` | 76 | 65 | 3 | 1 | 7 | 0 |
| `playlists/countries/Spain.m3u` | 239 | 198 | 40 | 0 | 1 | 0 |
| `playlists/countries/Sri_Lanka.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sudan.m3u` | 3 | 2 | 1 | 0 | 0 | 0 |
| `playlists/countries/Suriname.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sweden.m3u` | 378 | 14 | 364 | 0 | 0 | 0 |
| `playlists/countries/Switzerland.m3u` | 26 | 16 | 10 | 0 | 0 | 0 |
| `playlists/countries/Syria.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Taiwan.m3u` | 14 | 14 | 0 | 0 | 0 | 0 |
| `playlists/countries/Tanzania.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Thailand.m3u` | 77 | 58 | 18 | 1 | 0 | 0 |
| `playlists/countries/Togo.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Trinidad_and_Tobago.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Tunisia.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Turkey.m3u` | 151 | 138 | 13 | 0 | 0 | 0 |
| `playlists/countries/Turkmenistan.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/UK.m3u` | 239 | 220 | 19 | 0 | 0 | 0 |
| `playlists/countries/USA.m3u` | 2810 | 2130 | 675 | 5 | 0 | 0 |
| `playlists/countries/Uganda.m3u` | 15 | 15 | 0 | 0 | 0 | 0 |
| `playlists/countries/Ukraine.m3u` | 177 | 172 | 5 | 0 | 0 | 0 |
| `playlists/countries/United_Arab_Emirates.m3u` | 40 | 37 | 3 | 0 | 0 | 0 |
| `playlists/countries/Uruguay.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Uzbekistan.m3u` | 34 | 32 | 2 | 0 | 0 | 0 |
| `playlists/countries/Venezuela.m3u` | 59 | 58 | 1 | 0 | 0 | 0 |
| `playlists/countries/Vietnam.m3u` | 63 | 50 | 13 | 0 | 0 | 0 |
| `playlists/countries/Western_Sahara.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Yemen.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Zimbabwe.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |

## Patches applied

- Removed **3402** confirmed-dead links across **74** playlists (working ratio 82.7%).
  - `PremiumTV.m3u`: -2067 (12286 -> 10219)
  - `AE_Channels.m3u`: -9 (68 -> 59)
  - `Algeria.m3u`: -1 (6 -> 5)
  - `Argentina.m3u`: -1 (158 -> 157)
  - `Austria.m3u`: -2 (38 -> 36)
  - `Bangladesh.m3u`: -3 (23 -> 20)
  - `Belarus.m3u`: -5 (28 -> 23)
  - `Belgium.m3u`: -2 (29 -> 27)
  - `Bosnia_and_Herzegovina.m3u`: -1 (11 -> 10)
  - `Brazil.m3u`: -4 (190 -> 186)
  - `Cambodia.m3u`: -5 (19 -> 14)
  - `Canada.m3u`: -10 (143 -> 133)
  - `Chile.m3u`: -11 (204 -> 193)
  - `Colombia.m3u`: -3 (108 -> 105)
  - `Costa_Rica.m3u`: -1 (56 -> 55)
  - `Croatia.m3u`: -3 (18 -> 15)
  - `Dominican_Republic.m3u`: -6 (202 -> 196)
  - `Egypt.m3u`: -1 (16 -> 15)
  - `Estonia.m3u`: -2 (22 -> 20)
  - `Finland.m3u`: -4 (33 -> 29)
  - `France.m3u`: -12 (203 -> 191)
  - `Ghana.m3u`: -1 (8 -> 7)
  - `Greece.m3u`: -1 (88 -> 87)
  - `Honduras.m3u`: -1 (50 -> 49)
  - `Hungary.m3u`: -6 (112 -> 106)
  - `India.m3u`: -52 (791 -> 739)
  - `Indonesia.m3u`: -3 (120 -> 117)
  - `International.m3u`: -221 (1198 -> 977)
  - `Iraq.m3u`: -2 (62 -> 60)
  - `Ireland.m3u`: -6 (26 -> 20)
  - `Italy.m3u`: -30 (527 -> 497)
  - `Japan.m3u`: -5 (24 -> 19)
  - `Jordan.m3u`: -2 (18 -> 16)
  - `Kuwait.m3u`: -1 (15 -> 14)
  - `Lebanon.m3u`: -2 (30 -> 28)
  - `Luxembourg.m3u`: -2 (15 -> 13)
  - `Mexico.m3u`: -4 (132 -> 128)
  - `Moldova.m3u`: -2 (25 -> 23)
  - `Mongolia.m3u`: -1 (77 -> 76)
  - `Morocco.m3u`: -3 (12 -> 9)
  - `Myanmar.m3u`: -1 (5 -> 4)
  - `Nepal.m3u`: -2 (9 -> 7)
  - `Netherlands.m3u`: -31 (172 -> 141)
  - `New_Zealand.m3u`: -2 (7 -> 5)
  - `Nicaragua.m3u`: -1 (6 -> 5)
  - `Nigeria.m3u`: -2 (37 -> 35)
  - `Norway.m3u`: -1 (6 -> 5)
  - `Pakistan.m3u`: -1 (61 -> 60)
  - `Panama.m3u`: -1 (14 -> 13)
  - `Paraguay.m3u`: -1 (63 -> 62)
  - `Philippines.m3u`: -2 (11 -> 9)
  - `Poland.m3u`: -9 (121 -> 112)
  - `Portugal.m3u`: -4 (48 -> 44)
  - `Puerto_Rico.m3u`: -1 (28 -> 27)
  - `Qatar.m3u`: -1 (38 -> 37)
  - `Romania.m3u`: -17 (127 -> 110)
  - `Russia.m3u`: -21 (441 -> 420)
  - `Saudi_Arabia.m3u`: -5 (57 -> 52)
  - `Serbia.m3u`: -4 (24 -> 20)
  - `Singapore.m3u`: -2 (21 -> 19)
  - `Slovakia.m3u`: -1 (56 -> 55)
  - `South_Africa.m3u`: -1 (16 -> 15)
  - `South_Korea.m3u`: -3 (76 -> 73)
  - `Spain.m3u`: -40 (239 -> 199)
  - `Sudan.m3u`: -1 (3 -> 2)
  - `Thailand.m3u`: -18 (77 -> 59)
  - `Turkey.m3u`: -13 (151 -> 138)
  - `UK.m3u`: -19 (239 -> 220)
  - `USA.m3u`: -675 (2810 -> 2135)
  - `Ukraine.m3u`: -5 (177 -> 172)
  - `United_Arab_Emirates.m3u`: -3 (40 -> 37)
  - `Uzbekistan.m3u`: -2 (34 -> 32)
  - `Venezuela.m3u`: -1 (59 -> 58)
  - `Vietnam.m3u`: -13 (63 -> 50)
  - skipped `Australia.m3u`: removing 23/39 entries exceeds --max-remove-ratio 35%
  - skipped `Bermuda.m3u`: removing 1/1 entries exceeds --max-remove-ratio 35%
  - skipped `China.m3u`: removing 35/94 entries exceeds --max-remove-ratio 35%
  - skipped `Denmark.m3u`: removing 5/11 entries exceeds --max-remove-ratio 35%
  - skipped `Germany.m3u`: removing 233/406 entries exceeds --max-remove-ratio 35%
  - skipped `Iran.m3u`: removing 66/120 entries exceeds --max-remove-ratio 35%
  - skipped `Kyrgyzstan.m3u`: removing 1/2 entries exceeds --max-remove-ratio 35%
  - skipped `Macau.m3u`: removing 1/1 entries exceeds --max-remove-ratio 35%
  - skipped `San_Marino.m3u`: removing 2/2 entries exceeds --max-remove-ratio 35%
  - skipped `Sweden.m3u`: removing 364/378 entries exceeds --max-remove-ratio 35%
  - skipped `Switzerland.m3u`: removing 10/26 entries exceeds --max-remove-ratio 35%

## Hosts with the most failing links

| Host | Offline | Unreachable |
|---|---:|---:|
| `jmp2.uk` | 2701 | 0 |
| `ncdn.telewebion.ir` | 116 | 0 |
| `playlist.xtemus.com` | 60 | 0 |
| `live.streamingfast.net` | 54 | 0 |
| `sktv.mxnticek.eu` | 0 | 46 |
| `cloudplay-sonyliv.pages.dev` | 38 | 0 |
| `dokagents.site` | 28 | 0 |
| `cdn4.skygo.mn` | 26 | 0 |
| `c.mjh.nz` | 24 | 0 |
| `38.75.136.137:98` | 24 | 0 |
| `www.rtmpcdn.com` | 24 | 0 |
| `74.91.26.218:82` | 22 | 0 |
| `livestreaming.b67buv2.tweedekamer.nl` | 22 | 0 |
| `dethich.pw` | 20 | 0 |
| `abcnews-streams.akamaized.net` | 20 | 0 |
| `i.mjh.nz` | 16 | 0 |
| `rtvelivestream.rtve.es` | 16 | 0 |
| `router.xdevel.com` | 14 | 0 |
| `ms2.mx-cd.net` | 14 | 0 |
| `live20.bozztv.com` | 4 | 10 |
| `ztnr.rtve.es` | 14 | 0 |
| `64b16f23efbee.streamlock.net` | 6 | 8 |
| `mdc.ott.alticeusa.net` | 10 | 4 |
| `jstre.am` | 14 | 0 |
| `stream.smotrim.ru` | 12 | 0 |

## Sample of confirmed-dead links

| Channel | Reason | URL |
|---|---|---|
| A&E Crime 360 (Pluto TV) | variant HTTP 404 | `https://jmp2.uk/plu-6000a5a9e767980007b497ca.m3u8` |
| A&E Crime 360 (Pluto TV Alt) | variant HTTP 404 | `https://jmp2.uk/plu-657880c46e4f6a00087404d0.m3u8` |
| Chaos on Cam by A&E (Roku) | variant HTTP 404 | `https://jmp2.uk/rok-99e44ea6699928b32c444dce774b9b32.m3u8` |
| Cold Case Files by A&E (Pluto TV) | variant HTTP 404 | `https://jmp2.uk/plu-5c37d6712de254456f7ec340.m3u8` |
| Home.Made.Nation by A&E (Pluto TV) | variant HTTP 404 | `https://jmp2.uk/plu-5dc1cb279c91420009db261d.m3u8` |
| A&E Crime 360 (Pluto TV) | variant HTTP 404 | `https://jmp2.uk/plu-6000a5a9e767980007b497ca.m3u8` |
| A&E Crime 360 (Pluto TV Alt) | variant HTTP 404 | `https://jmp2.uk/plu-657880c46e4f6a00087404d0.m3u8` |
| Chaos on Cam by A&E (Roku) | variant HTTP 404 | `https://jmp2.uk/rok-99e44ea6699928b32c444dce774b9b32.m3u8` |
| Cold Case Files by A&E (Pluto TV) | variant HTTP 404 | `https://jmp2.uk/plu-5c37d6712de254456f7ec340.m3u8` |
| Home.Made.Nation by A&E (Pluto TV) | variant HTTP 404 | `https://jmp2.uk/plu-5dc1cb279c91420009db261d.m3u8` |
| Elwatania TV (1080i) | playlist only, TimeoutError | `https://livesstream.work.gd:5443/WebRTCApp/streams/stream.m3u8` |
| Telefe Buenos Aires (1080p) | HTTP 404 | `http://45.134.141.161:2200/ARG/TELEFE_HD/index.m3u8` |
| 10 HD | playlist only, HTTP 403 | `https://i.mjh.nz/.r/10-nsw.m3u8` |
| 10 Peach | playlist only, HTTP 403 | `https://i.mjh.nz/.r/10peach-nsw.m3u8` |
| 7flix | playlist only, HTTP 403 | `https://i.mjh.nz/.r/7flix-syd.m3u8` |
| 7mate | playlist only, HTTP 403 | `https://i.mjh.nz/.r/7mate-syd.m3u8` |
| 7two | playlist only, HTTP 403 | `https://i.mjh.nz/.r/7two-syd.m3u8` |
| oe24 | playlist only, HTTP 503 | `https://oe24.mdn.ors.at/live/eds/oe24tv_hd/hls_nodrm/oe24tv_hd-nodrm.m3u8` |
| Servus TV Ⓖ | variant HTTP 404 | `https://rbmn-live.akamaized.net/hls/live/2002825/geoSTVATweb/master.m3u8` |
| Green TV (1080p) | playlist only, HTTP 500 | `https://app.ncare.live/c3VydmVyX8RpbEU9Mi8xNy8yMDE0GIDU6RgzQ6NTAgdEoaeFzbF92YWxIZTO0U0ezN1IzMyfvcGVMZEJCTEFWeVN3PTOmdFsaWRtaW51aiPhnPTI2/greentv.stream/live-orgin/greentv.stream/playlist.m3u8` |
| My TV (Bangladesh) | variant HTTP 500 | `https://app.ncare.live/c3VydmVyX8RpbEU9Mi8xNy8yMDE0GIDU6RgzQ6NTAgdEoaeFzbF92YWxIZTO0U0ezN1IzMyfvcGVMZEJCTEFWeVN3PTOmdFsaWRtaW51aiPhnPTI2/mytv-up-off.stream/live-orgin/mytv-up-off.stream/playlist.m3u8` |
| NAN TV | playlist only, HTTP 500 | `https://app.ncare.live/c3VydmVyX8RpbEU9Mi8xNy8yMDE0GIDU6RgzQ6NTAgdEoaeFzbF92YWxIZTO0U0ezN1IzMyfvcGVMZEJCTEFWeVN3PTOmdFsaWRtaW51aiPhnPTI2/nantv.stream/live-orgin/nantv.stream/playlist.m3u8` |
| Belros Ⓢ | playlist only, HTTP 404 | `https://live2.mediacdn.ru/sr1/tro/playlist.m3u8` |
| Беларусь 5 Интернет | variant HTTP 504 | `https://edge55.dc.beltelecom.by/ngtrk/smil:belarus5int.smil/playlist.m3u8` |
| ОНТ Ⓢ | variant HTTP 504 | `https://ngtrk.dc.beltelecom.by/ngtrk/smil:ont.smil/playlist.m3u8` |
