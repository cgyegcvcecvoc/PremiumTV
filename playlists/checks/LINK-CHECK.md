# Deep link check

- **Run:** nightly deep link check (`20261022T101321Z-3192`)
- **Started:** 2026-10-22T10:13:21Z  |  **Finished:** 2026-10-22T10:19:47Z  |  **Duration:** 386.2s
- **Mode:** deep (playlist + segment probe)
- **Unique links checked:** 13368 from 26737 playlist entries in 181 playlists

| Result | Links | Share | Meaning |
|---|---:|---:|---|
| working | 22856 | 85.5% | answered with playable media |
| offline | 68 | 0.3% | confirmed dead - removed when patching |
| unreachable | 2083 | 7.8% | timeout or server error - kept, may recover |
| blocked | 1730 | 6.5% | HTTP 401/403/451 - needs auth or is geo-blocked |

## Per playlist

| Playlist | Entries | Working | Offline | Unreachable | Blocked | Other |
|---|---:|---:|---:|---:|---:|---:|
| `playlists/PremiumTV.m3u` | 13300 | 11389 | 6 | 1040 | 865 | 0 |
| `playlists/AE_Channels.m3u` | 69 | 67 | 0 | 2 | 0 | 0 |
| `playlists/countries/Afghanistan.m3u` | 11 | 10 | 0 | 1 | 0 | 0 |
| `playlists/countries/Albania.m3u` | 27 | 14 | 0 | 9 | 4 | 0 |
| `playlists/countries/Algeria.m3u` | 7 | 4 | 0 | 2 | 1 | 0 |
| `playlists/countries/Andorra.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Angola.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Antigua_and_Barbuda.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Arab_World.m3u` | 14 | 14 | 0 | 0 | 0 | 0 |
| `playlists/countries/Argentina.m3u` | 171 | 152 | 4 | 5 | 10 | 0 |
| `playlists/countries/Armenia.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Aruba.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Australia.m3u` | 45 | 34 | 0 | 4 | 7 | 0 |
| `playlists/countries/Austria.m3u` | 49 | 40 | 0 | 7 | 2 | 0 |
| `playlists/countries/Azerbaijan.m3u` | 18 | 11 | 0 | 2 | 5 | 0 |
| `playlists/countries/Bahamas.m3u` | 3 | 2 | 0 | 1 | 0 | 0 |
| `playlists/countries/Bahrain.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bangladesh.m3u` | 28 | 18 | 0 | 9 | 1 | 0 |
| `playlists/countries/Barbados.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Belarus.m3u` | 33 | 27 | 0 | 6 | 0 | 0 |
| `playlists/countries/Belgium.m3u` | 40 | 28 | 0 | 0 | 12 | 0 |
| `playlists/countries/Belize.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Benin.m3u` | 4 | 3 | 0 | 1 | 0 | 0 |
| `playlists/countries/Bolivia.m3u` | 48 | 46 | 0 | 2 | 0 | 0 |
| `playlists/countries/Bosnia_and_Herzegovina.m3u` | 21 | 9 | 0 | 10 | 2 | 0 |
| `playlists/countries/Brazil.m3u` | 237 | 167 | 1 | 41 | 28 | 0 |
| `playlists/countries/British_Virgin_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Brunei.m3u` | 2 | 0 | 0 | 0 | 2 | 0 |
| `playlists/countries/Bulgaria.m3u` | 42 | 28 | 1 | 11 | 2 | 0 |
| `playlists/countries/Burkina_Faso.m3u` | 3 | 0 | 0 | 0 | 3 | 0 |
| `playlists/countries/Burundi.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cambodia.m3u` | 15 | 13 | 0 | 1 | 1 | 0 |
| `playlists/countries/Cameroon.m3u` | 13 | 10 | 0 | 1 | 2 | 0 |
| `playlists/countries/Canada.m3u` | 192 | 147 | 0 | 15 | 30 | 0 |
| `playlists/countries/Cape_Verde.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Caribbean_Netherlands.m3u` | 6 | 4 | 0 | 2 | 0 | 0 |
| `playlists/countries/Chad.m3u` | 2 | 1 | 0 | 1 | 0 | 0 |
| `playlists/countries/Chile.m3u` | 219 | 196 | 0 | 10 | 13 | 0 |
| `playlists/countries/China.m3u` | 157 | 85 | 0 | 55 | 17 | 0 |
| `playlists/countries/Colombia.m3u` | 114 | 107 | 0 | 5 | 2 | 0 |
| `playlists/countries/Costa_Rica.m3u` | 63 | 58 | 1 | 0 | 4 | 0 |
| `playlists/countries/Croatia.m3u` | 16 | 13 | 1 | 2 | 0 | 0 |
| `playlists/countries/Cuba.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Curacao.m3u` | 4 | 2 | 0 | 2 | 0 | 0 |
| `playlists/countries/Cyprus.m3u` | 20 | 19 | 0 | 1 | 0 | 0 |
| `playlists/countries/Czechia.m3u` | 118 | 93 | 0 | 8 | 17 | 0 |
| `playlists/countries/DR_Congo.m3u` | 14 | 4 | 0 | 10 | 0 | 0 |
| `playlists/countries/Denmark.m3u` | 15 | 8 | 0 | 2 | 5 | 0 |
| `playlists/countries/Dominican_Republic.m3u` | 203 | 192 | 2 | 8 | 1 | 0 |
| `playlists/countries/Ecuador.m3u` | 58 | 48 | 1 | 8 | 1 | 0 |
| `playlists/countries/Egypt.m3u` | 17 | 15 | 0 | 0 | 2 | 0 |
| `playlists/countries/El_Salvador.m3u` | 23 | 15 | 0 | 7 | 1 | 0 |
| `playlists/countries/Equatorial_Guinea.m3u` | 2 | 1 | 0 | 1 | 0 | 0 |
| `playlists/countries/Eritrea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Estonia.m3u` | 26 | 22 | 0 | 3 | 1 | 0 |
| `playlists/countries/Ethiopia.m3u` | 2 | 1 | 0 | 1 | 0 | 0 |
| `playlists/countries/Faroe_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Finland.m3u` | 36 | 22 | 0 | 13 | 1 | 0 |
| `playlists/countries/France.m3u` | 259 | 200 | 0 | 19 | 40 | 0 |
| `playlists/countries/French_Guiana.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Gambia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Georgia.m3u` | 20 | 14 | 0 | 3 | 3 | 0 |
| `playlists/countries/Germany.m3u` | 409 | 357 | 2 | 14 | 36 | 0 |
| `playlists/countries/Ghana.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Greece.m3u` | 93 | 83 | 0 | 5 | 5 | 0 |
| `playlists/countries/Guadeloupe.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guam.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guatemala.m3u` | 37 | 32 | 0 | 5 | 0 | 0 |
| `playlists/countries/Guinea.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guyana.m3u` | 10 | 9 | 0 | 0 | 1 | 0 |
| `playlists/countries/Haiti.m3u` | 10 | 6 | 0 | 3 | 1 | 0 |
| `playlists/countries/Honduras.m3u` | 55 | 44 | 0 | 10 | 1 | 0 |
| `playlists/countries/Hong_Kong.m3u` | 24 | 10 | 0 | 3 | 11 | 0 |
| `playlists/countries/Hungary.m3u` | 143 | 94 | 18 | 24 | 7 | 0 |
| `playlists/countries/Iceland.m3u` | 5 | 4 | 0 | 0 | 1 | 0 |
| `playlists/countries/India.m3u` | 732 | 675 | 3 | 34 | 20 | 0 |
| `playlists/countries/Indonesia.m3u` | 127 | 113 | 2 | 10 | 2 | 0 |
| `playlists/countries/International.m3u` | 1218 | 1149 | 0 | 27 | 42 | 0 |
| `playlists/countries/Iran.m3u` | 95 | 91 | 0 | 2 | 2 | 0 |
| `playlists/countries/Iraq.m3u` | 62 | 59 | 0 | 3 | 0 | 0 |
| `playlists/countries/Ireland.m3u` | 26 | 19 | 0 | 0 | 7 | 0 |
| `playlists/countries/Israel.m3u` | 39 | 29 | 0 | 0 | 10 | 0 |
| `playlists/countries/Italy.m3u` | 568 | 486 | 0 | 50 | 32 | 0 |
| `playlists/countries/Ivory_Coast.m3u` | 11 | 10 | 0 | 0 | 1 | 0 |
| `playlists/countries/Jamaica.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Japan.m3u` | 20 | 17 | 0 | 0 | 3 | 0 |
| `playlists/countries/Jordan.m3u` | 17 | 17 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kazakhstan.m3u` | 40 | 23 | 0 | 4 | 13 | 0 |
| `playlists/countries/Kenya.m3u` | 6 | 5 | 0 | 1 | 0 | 0 |
| `playlists/countries/Kosovo.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kuwait.m3u` | 13 | 13 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kyrgyzstan.m3u` | 6 | 0 | 0 | 3 | 3 | 0 |
| `playlists/countries/Laos.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Latin_America.m3u` | 34 | 33 | 0 | 0 | 1 | 0 |
| `playlists/countries/Latvia.m3u` | 18 | 17 | 1 | 0 | 0 | 0 |
| `playlists/countries/Lebanon.m3u` | 30 | 28 | 0 | 1 | 1 | 0 |
| `playlists/countries/Libya.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Lithuania.m3u` | 23 | 18 | 0 | 0 | 5 | 0 |
| `playlists/countries/Luxembourg.m3u` | 15 | 12 | 0 | 2 | 1 | 0 |
| `playlists/countries/Macau.m3u` | 6 | 0 | 0 | 6 | 0 | 0 |
| `playlists/countries/Malaysia.m3u` | 6 | 4 | 0 | 0 | 2 | 0 |
| `playlists/countries/Maldives.m3u` | 5 | 3 | 0 | 1 | 1 | 0 |
| `playlists/countries/Mali.m3u` | 3 | 2 | 0 | 1 | 0 | 0 |
| `playlists/countries/Malta.m3u` | 7 | 3 | 0 | 0 | 4 | 0 |
| `playlists/countries/Martinique.m3u` | 6 | 5 | 0 | 1 | 0 | 0 |
| `playlists/countries/Mauritania.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mexico.m3u` | 153 | 117 | 0 | 12 | 24 | 0 |
| `playlists/countries/Moldova.m3u` | 21 | 21 | 0 | 0 | 0 | 0 |
| `playlists/countries/Monaco.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mongolia.m3u` | 77 | 77 | 0 | 0 | 0 | 0 |
| `playlists/countries/Montenegro.m3u` | 6 | 3 | 0 | 0 | 3 | 0 |
| `playlists/countries/Morocco.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mozambique.m3u` | 4 | 2 | 0 | 2 | 0 | 0 |
| `playlists/countries/Myanmar.m3u` | 16 | 7 | 0 | 9 | 0 | 0 |
| `playlists/countries/Namibia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nepal.m3u` | 10 | 8 | 0 | 0 | 2 | 0 |
| `playlists/countries/Netherlands.m3u` | 157 | 142 | 0 | 8 | 7 | 0 |
| `playlists/countries/New_Zealand.m3u` | 9 | 7 | 0 | 0 | 2 | 0 |
| `playlists/countries/Nicaragua.m3u` | 12 | 5 | 0 | 2 | 5 | 0 |
| `playlists/countries/Niger.m3u` | 4 | 1 | 1 | 0 | 2 | 0 |
| `playlists/countries/Nigeria.m3u` | 43 | 31 | 0 | 7 | 5 | 0 |
| `playlists/countries/North_Korea.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/North_Macedonia.m3u` | 23 | 21 | 0 | 2 | 0 | 0 |
| `playlists/countries/Norway.m3u` | 12 | 7 | 0 | 0 | 5 | 0 |
| `playlists/countries/Oman.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Pakistan.m3u` | 88 | 41 | 0 | 43 | 4 | 0 |
| `playlists/countries/Palestine.m3u` | 18 | 17 | 0 | 0 | 1 | 0 |
| `playlists/countries/Panama.m3u` | 18 | 15 | 0 | 3 | 0 | 0 |
| `playlists/countries/Papua_New_Guinea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Paraguay.m3u` | 53 | 49 | 3 | 0 | 1 | 0 |
| `playlists/countries/Peru.m3u` | 144 | 130 | 2 | 4 | 8 | 0 |
| `playlists/countries/Philippines.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Poland.m3u` | 238 | 155 | 0 | 77 | 6 | 0 |
| `playlists/countries/Portugal.m3u` | 62 | 40 | 0 | 16 | 6 | 0 |
| `playlists/countries/Puerto_Rico.m3u` | 27 | 23 | 2 | 1 | 1 | 0 |
| `playlists/countries/Qatar.m3u` | 42 | 35 | 0 | 0 | 7 | 0 |
| `playlists/countries/Republic_of_the_Congo.m3u` | 4 | 2 | 0 | 1 | 1 | 0 |
| `playlists/countries/Romania.m3u` | 137 | 114 | 2 | 11 | 10 | 0 |
| `playlists/countries/Russia.m3u` | 510 | 405 | 0 | 94 | 11 | 0 |
| `playlists/countries/Rwanda.m3u` | 9 | 8 | 1 | 0 | 0 | 0 |
| `playlists/countries/Saint_Kitts_and_Nevis.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Lucia.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saudi_Arabia.m3u` | 59 | 51 | 0 | 0 | 8 | 0 |
| `playlists/countries/Senegal.m3u` | 8 | 5 | 0 | 2 | 1 | 0 |
| `playlists/countries/Serbia.m3u` | 25 | 18 | 0 | 6 | 1 | 0 |
| `playlists/countries/Sierra_Leone.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Singapore.m3u` | 25 | 22 | 0 | 0 | 3 | 0 |
| `playlists/countries/Sint_Maarten.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Slovakia.m3u` | 67 | 55 | 0 | 11 | 1 | 0 |
| `playlists/countries/Slovenia.m3u` | 11 | 7 | 0 | 4 | 0 | 0 |
| `playlists/countries/Somalia.m3u` | 9 | 4 | 0 | 5 | 0 | 0 |
| `playlists/countries/South_Africa.m3u` | 19 | 16 | 0 | 1 | 2 | 0 |
| `playlists/countries/South_Korea.m3u` | 81 | 65 | 0 | 13 | 3 | 0 |
| `playlists/countries/Spain.m3u` | 250 | 195 | 1 | 25 | 29 | 0 |
| `playlists/countries/Sri_Lanka.m3u` | 14 | 7 | 0 | 6 | 1 | 0 |
| `playlists/countries/Sudan.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Suriname.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sweden.m3u` | 389 | 378 | 0 | 3 | 8 | 0 |
| `playlists/countries/Switzerland.m3u` | 36 | 25 | 0 | 5 | 6 | 0 |
| `playlists/countries/Syria.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/countries/Taiwan.m3u` | 22 | 16 | 0 | 4 | 2 | 0 |
| `playlists/countries/Tajikistan.m3u` | 14 | 0 | 0 | 14 | 0 | 0 |
| `playlists/countries/Tanzania.m3u` | 6 | 5 | 0 | 1 | 0 | 0 |
| `playlists/countries/Thailand.m3u` | 90 | 62 | 0 | 9 | 19 | 0 |
| `playlists/countries/Togo.m3u` | 8 | 3 | 0 | 1 | 4 | 0 |
| `playlists/countries/Trinidad_and_Tobago.m3u` | 5 | 4 | 0 | 1 | 0 | 0 |
| `playlists/countries/Tunisia.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Turkey.m3u` | 147 | 130 | 1 | 10 | 6 | 0 |
| `playlists/countries/Turkmenistan.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/UK.m3u` | 346 | 224 | 0 | 32 | 90 | 0 |
| `playlists/countries/USA.m3u` | 2899 | 2717 | 8 | 65 | 109 | 0 |
| `playlists/countries/Uganda.m3u` | 14 | 11 | 0 | 2 | 1 | 0 |
| `playlists/countries/Ukraine.m3u` | 190 | 169 | 0 | 18 | 3 | 0 |
| `playlists/countries/United_Arab_Emirates.m3u` | 53 | 43 | 0 | 6 | 4 | 0 |
| `playlists/countries/Uruguay.m3u` | 5 | 4 | 0 | 0 | 1 | 0 |
| `playlists/countries/Uzbekistan.m3u` | 35 | 35 | 0 | 0 | 0 | 0 |
| `playlists/countries/Venezuela.m3u` | 59 | 48 | 4 | 5 | 2 | 0 |
| `playlists/countries/Vietnam.m3u` | 79 | 61 | 0 | 1 | 17 | 0 |
| `playlists/countries/Western_Sahara.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Yemen.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Zimbabwe.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |

## Patches applied

- Removed **68** confirmed-dead links across **23** playlists (working ratio 85.5%).
  - `PremiumTV.m3u`: -6 (13300 -> 13294)
  - `Argentina.m3u`: -4 (171 -> 167)
  - `Brazil.m3u`: -1 (237 -> 236)
  - `Bulgaria.m3u`: -1 (42 -> 41)
  - `Costa_Rica.m3u`: -1 (63 -> 62)
  - `Croatia.m3u`: -1 (16 -> 15)
  - `Dominican_Republic.m3u`: -2 (203 -> 201)
  - `Ecuador.m3u`: -1 (58 -> 57)
  - `Germany.m3u`: -2 (409 -> 407)
  - `Hungary.m3u`: -18 (143 -> 125)
  - `India.m3u`: -3 (732 -> 729)
  - `Indonesia.m3u`: -2 (127 -> 125)
  - `Latvia.m3u`: -1 (18 -> 17)
  - `Niger.m3u`: -1 (4 -> 3)
  - `Paraguay.m3u`: -3 (53 -> 50)
  - `Peru.m3u`: -2 (144 -> 142)
  - `Puerto_Rico.m3u`: -2 (27 -> 25)
  - `Romania.m3u`: -2 (137 -> 135)
  - `Rwanda.m3u`: -1 (9 -> 8)
  - `Spain.m3u`: -1 (250 -> 249)
  - `Turkey.m3u`: -1 (147 -> 146)
  - `USA.m3u`: -8 (2899 -> 2892)
  - `Venezuela.m3u`: -4 (59 -> 55)

## Hosts with the most failing links

| Host | Offline | Unreachable |
|---|---:|---:|
| `57.128.231.171:8080` | 0 | 101 |
| `31.148.48.15` | 0 | 96 |
| `hls127.freeott.top:8080` | 0 | 96 |
| `103.250.28.74:8000` | 0 | 60 |
| `57.128.210.196:8080` | 0 | 54 |
| `playlist.xtemus.com` | 0 | 30 |
| `live.teleradiocom.tj` | 0 | 28 |
| `live-fi.tvkaista.net` | 0 | 24 |
| `cloudfront44.lexanetwork.com:1344` | 17 | 4 |
| `tvsen7.aynascope.net` | 0 | 20 |
| `91.228.35.249:8001` | 0 | 20 |
| `znty.dyndns.org:5010` | 0 | 20 |
| `5f22d76e220e1.streamlock.net` | 0 | 20 |
| `cdn.rostelekom-tv.xyz` | 0 | 18 |
| `151.80.18.177:86` | 0 | 18 |
| `51.254.199.122:8080` | 0 | 18 |
| `64b16f23efbee.streamlock.net` | 0 | 18 |
| `103.72.101.252:8080` | 0 | 18 |
| `190.197.41.183` | 0 | 14 |
| `mumbai-edge.smartplaytv.in` | 0 | 14 |
| `sktv.mxnticek.eu` | 0 | 14 |
| `39.134.115.163:8080` | 0 | 14 |
| `183.207.248.71` | 0 | 12 |
| `cdn.tvmatic.net` | 0 | 12 |
| `tvsen5.aynascope.net` | 0 | 12 |

## Sample of confirmed-dead links

| Channel | Reason | URL |
|---|---|---|
| Fox Sports (1080p) | HTTP 404 | `http://138.59.227.20:8000/play/a085/index.m3u8` |
| A24 (1080p) | HTTP 404 | `http://138.59.227.20:8000/play/a05u/index.m3u8` |
| Tal TV (1080p) | playlist only, HTTP 404 | `https://mediaserver1.castpin.com/hls/taltv/index.m3u8` |
| Pakapaka (1080p) | HTTP 404 | `http://138.59.227.20:8000/play/a05t/index.m3u8` |
| Encuentro (720p) | HTTP 404 | `http://138.59.227.20:8000/play/a05s/index.m3u8` |
| Fox Sports (1080p) | HTTP 404 | `http://138.59.227.20:8000/play/a085/index.m3u8` |
| A24 (1080p) | HTTP 404 | `http://138.59.227.20:8000/play/a05u/index.m3u8` |
| Encuentro (720p) | HTTP 404 | `http://138.59.227.20:8000/play/a05s/index.m3u8` |
| Pakapaka (1080p) | HTTP 404 | `http://138.59.227.20:8000/play/a05t/index.m3u8` |
| Telecine Action (1080p) | connection refused | `http://46.151.196.223:14326/` |
| RMTV (288p) | connection refused | `https://transcoder1.bitcare.eu/streaming/rimextv/rmtv.m3u8` |
| Super Cable | playlist only, empty segment | `http://191.102.39.254:5000/live/5up3r5/playlist.m3u8` |
| Diadora TV | HTTP 404 | `https://diadoratv.stream/live/diadora/playlist.m3u8` |
| GH Television (1080p) [Not 24/7] | HTTP 404 | `https://fox.hostlagarto.com:8081/ghtelevision/tracks-v1a1/mono.m3u8` |
| TVN (Dominican Republic) (1080p) [Not 24/7] | HTTP 404 | `https://5790d294af2dc.streamlock.net/tvn/tvn/playlist.m3u8` |
| La Nueva Radio TV 97.7 (1080p) | HTTP 404 | `https://sv72.ecuaradiotv.net/lanuevatv/live/playlist.m3u8` |
| Handystar (404p) [Not 24/7] | dns lookup failed | `https://sparhandytv.cdn.ses-ps.com/live/channel01/hls/index.m3u8` |
| Sonnenklar TV (1080p) | dns lookup failed | `http://euvia.cdn.ses-ps.com/HLS-Live/index.m3u8` |
| SIXO TV (360p) | connection refused | `https://cloudfront44.lexanetwork.com:1344/relay01/HDE038.sdp/playlist.m3u8` |
| Szolnok TV (1080p) | connection refused | `https://cloudfront44.lexanetwork.com:1344/relay01/livestream004.sdp/playlist.m3u8` |
| Tatai TV (1080p) | connection refused | `https://cloudfront44.lexanetwork.com:1344/relay01/broadcast006.sdp/playlist.m3u8` |
| TelePaks (396p) | connection refused | `https://cloudfront44.lexanetwork.com:1344/relay02/livestream004.sdp/playlist.m3u8` |
| TV Keszthely (360p) | connection refused | `https://cloudfront44.lexanetwork.com:1344/freerelay/keszthelyivtv.sdp/playlist.m3u8` |
| Mirror Now (Backup 1) | variant HTTP 404 | `https://pubads.g.doubleclick.net/ssai/event/DXkHhH2QSnma-HnE3QJqlA/master.m3u8` |
| DD Bihar (720p) | playlist only, HTTP 404 | `https://cdn.pishow.tv/ott/live/35/master.m3u8` |
