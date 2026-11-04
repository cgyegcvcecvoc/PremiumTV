# Deep link check

- **Run:** nightly deep link check (`20261104T111845Z-3418`)
- **Started:** 2026-11-04T11:18:45Z  |  **Finished:** 2026-11-04T11:22:43Z  |  **Duration:** 237.6s
- **Mode:** deep (playlist + segment probe)
- **Unique links checked:** 12218 from 24296 playlist entries in 174 playlists

| Result | Links | Share | Meaning |
|---|---:|---:|---|
| working | 23530 | 96.8% | answered with playable media |
| offline | 204 | 0.8% | confirmed dead - removed when patching |
| unreachable | 254 | 1.0% | timeout or server error - kept, may recover |
| blocked | 308 | 1.3% | HTTP 401/403/451 - needs auth or is geo-blocked |

## Per playlist

| Playlist | Entries | Working | Offline | Unreachable | Blocked | Other |
|---|---:|---:|---:|---:|---:|---:|
| `playlists/PremiumTV.m3u` | 12009 | 11711 | 18 | 126 | 154 | 0 |
| `playlists/AE_Channels.m3u` | 69 | 68 | 0 | 1 | 0 | 0 |
| `playlists/countries/Afghanistan.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Albania.m3u` | 16 | 15 | 0 | 1 | 0 | 0 |
| `playlists/countries/Algeria.m3u` | 4 | 3 | 0 | 0 | 1 | 0 |
| `playlists/countries/Andorra.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Angola.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Antigua_and_Barbuda.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Arab_World.m3u` | 13 | 13 | 0 | 0 | 0 | 0 |
| `playlists/countries/Argentina.m3u` | 164 | 162 | 1 | 1 | 0 | 0 |
| `playlists/countries/Armenia.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Aruba.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Australia.m3u` | 33 | 32 | 1 | 0 | 0 | 0 |
| `playlists/countries/Austria.m3u` | 40 | 39 | 0 | 1 | 0 | 0 |
| `playlists/countries/Azerbaijan.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bahamas.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bahrain.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bangladesh.m3u` | 23 | 22 | 0 | 1 | 0 | 0 |
| `playlists/countries/Barbados.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Belarus.m3u` | 32 | 24 | 0 | 8 | 0 | 0 |
| `playlists/countries/Belgium.m3u` | 35 | 35 | 0 | 0 | 0 | 0 |
| `playlists/countries/Belize.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Benin.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bolivia.m3u` | 48 | 43 | 3 | 2 | 0 | 0 |
| `playlists/countries/Bosnia_and_Herzegovina.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Brazil.m3u` | 180 | 171 | 5 | 3 | 1 | 0 |
| `playlists/countries/British_Virgin_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bulgaria.m3u` | 62 | 59 | 1 | 0 | 2 | 0 |
| `playlists/countries/Burkina_Faso.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Burundi.m3u` | 2 | 1 | 0 | 1 | 0 | 0 |
| `playlists/countries/Cambodia.m3u` | 14 | 13 | 1 | 0 | 0 | 0 |
| `playlists/countries/Cameroon.m3u` | 13 | 12 | 1 | 0 | 0 | 0 |
| `playlists/countries/Canada.m3u` | 139 | 137 | 2 | 0 | 0 | 0 |
| `playlists/countries/Cape_Verde.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Caribbean_Netherlands.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Chad.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Chile.m3u` | 196 | 190 | 6 | 0 | 0 | 0 |
| `playlists/countries/China.m3u` | 88 | 86 | 0 | 2 | 0 | 0 |
| `playlists/countries/Colombia.m3u` | 113 | 110 | 1 | 1 | 1 | 0 |
| `playlists/countries/Costa_Rica.m3u` | 60 | 58 | 2 | 0 | 0 | 0 |
| `playlists/countries/Croatia.m3u` | 14 | 9 | 1 | 0 | 4 | 0 |
| `playlists/countries/Cuba.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Curacao.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cyprus.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/countries/Czechia.m3u` | 99 | 98 | 1 | 0 | 0 | 0 |
| `playlists/countries/DR_Congo.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Denmark.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Dominican_Republic.m3u` | 210 | 197 | 11 | 2 | 0 | 0 |
| `playlists/countries/Ecuador.m3u` | 54 | 52 | 1 | 1 | 0 | 0 |
| `playlists/countries/Egypt.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/El_Salvador.m3u` | 19 | 16 | 3 | 0 | 0 | 0 |
| `playlists/countries/Eritrea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Estonia.m3u` | 21 | 21 | 0 | 0 | 0 | 0 |
| `playlists/countries/Ethiopia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Faroe_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Finland.m3u` | 32 | 26 | 6 | 0 | 0 | 0 |
| `playlists/countries/France.m3u` | 222 | 195 | 0 | 2 | 25 | 0 |
| `playlists/countries/French_Guiana.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Georgia.m3u` | 14 | 14 | 0 | 0 | 0 | 0 |
| `playlists/countries/Germany.m3u` | 352 | 351 | 0 | 0 | 1 | 0 |
| `playlists/countries/Ghana.m3u` | 7 | 6 | 1 | 0 | 0 | 0 |
| `playlists/countries/Greece.m3u` | 91 | 88 | 2 | 1 | 0 | 0 |
| `playlists/countries/Guadeloupe.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guam.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guatemala.m3u` | 34 | 32 | 2 | 0 | 0 | 0 |
| `playlists/countries/Guinea.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guyana.m3u` | 11 | 9 | 1 | 1 | 0 | 0 |
| `playlists/countries/Haiti.m3u` | 7 | 6 | 1 | 0 | 0 | 0 |
| `playlists/countries/Honduras.m3u` | 48 | 43 | 4 | 1 | 0 | 0 |
| `playlists/countries/Hong_Kong.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Hungary.m3u` | 164 | 157 | 6 | 1 | 0 | 0 |
| `playlists/countries/Iceland.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/India.m3u` | 785 | 683 | 37 | 2 | 63 | 0 |
| `playlists/countries/Indonesia.m3u` | 105 | 102 | 0 | 3 | 0 | 0 |
| `playlists/countries/International.m3u` | 1296 | 1281 | 5 | 9 | 1 | 0 |
| `playlists/countries/Iran.m3u` | 90 | 90 | 0 | 0 | 0 | 0 |
| `playlists/countries/Iraq.m3u` | 61 | 56 | 3 | 2 | 0 | 0 |
| `playlists/countries/Ireland.m3u` | 18 | 18 | 0 | 0 | 0 | 0 |
| `playlists/countries/Israel.m3u` | 44 | 43 | 1 | 0 | 0 | 0 |
| `playlists/countries/Italy.m3u` | 530 | 512 | 3 | 15 | 0 | 0 |
| `playlists/countries/Ivory_Coast.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/countries/Jamaica.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Japan.m3u` | 15 | 15 | 0 | 0 | 0 | 0 |
| `playlists/countries/Jordan.m3u` | 18 | 18 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kazakhstan.m3u` | 25 | 22 | 0 | 3 | 0 | 0 |
| `playlists/countries/Kenya.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kosovo.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kuwait.m3u` | 13 | 13 | 0 | 0 | 0 | 0 |
| `playlists/countries/Laos.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Latin_America.m3u` | 33 | 33 | 0 | 0 | 0 | 0 |
| `playlists/countries/Latvia.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/Lebanon.m3u` | 27 | 26 | 0 | 1 | 0 | 0 |
| `playlists/countries/Libya.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Lithuania.m3u` | 19 | 19 | 0 | 0 | 0 | 0 |
| `playlists/countries/Luxembourg.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/countries/Malaysia.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Maldives.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mali.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Malta.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Martinique.m3u` | 5 | 4 | 1 | 0 | 0 | 0 |
| `playlists/countries/Mexico.m3u` | 127 | 113 | 11 | 3 | 0 | 0 |
| `playlists/countries/Moldova.m3u` | 20 | 20 | 0 | 0 | 0 | 0 |
| `playlists/countries/Monaco.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mongolia.m3u` | 77 | 77 | 0 | 0 | 0 | 0 |
| `playlists/countries/Montenegro.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Morocco.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mozambique.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Myanmar.m3u` | 14 | 13 | 1 | 0 | 0 | 0 |
| `playlists/countries/Namibia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nepal.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Netherlands.m3u` | 150 | 144 | 1 | 5 | 0 | 0 |
| `playlists/countries/New_Zealand.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nicaragua.m3u` | 7 | 6 | 1 | 0 | 0 | 0 |
| `playlists/countries/Niger.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nigeria.m3u` | 31 | 29 | 0 | 1 | 1 | 0 |
| `playlists/countries/North_Korea.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/North_Macedonia.m3u` | 19 | 19 | 0 | 0 | 0 | 0 |
| `playlists/countries/Norway.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Oman.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Pakistan.m3u` | 53 | 50 | 2 | 1 | 0 | 0 |
| `playlists/countries/Palestine.m3u` | 20 | 20 | 0 | 0 | 0 | 0 |
| `playlists/countries/Panama.m3u` | 13 | 13 | 0 | 0 | 0 | 0 |
| `playlists/countries/Papua_New_Guinea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Paraguay.m3u` | 56 | 55 | 1 | 0 | 0 | 0 |
| `playlists/countries/Peru.m3u` | 150 | 141 | 6 | 3 | 0 | 0 |
| `playlists/countries/Philippines.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Poland.m3u` | 172 | 167 | 0 | 5 | 0 | 0 |
| `playlists/countries/Portugal.m3u` | 44 | 44 | 0 | 0 | 0 | 0 |
| `playlists/countries/Puerto_Rico.m3u` | 29 | 25 | 3 | 0 | 1 | 0 |
| `playlists/countries/Qatar.m3u` | 36 | 36 | 0 | 0 | 0 | 0 |
| `playlists/countries/Republic_of_the_Congo.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Romania.m3u` | 145 | 135 | 2 | 0 | 8 | 0 |
| `playlists/countries/Russia.m3u` | 427 | 423 | 1 | 3 | 0 | 0 |
| `playlists/countries/Rwanda.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Kitts_and_Nevis.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Lucia.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saudi_Arabia.m3u` | 51 | 50 | 1 | 0 | 0 | 0 |
| `playlists/countries/Senegal.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Serbia.m3u` | 20 | 20 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sierra_Leone.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Singapore.m3u` | 29 | 29 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sint_Maarten.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Slovakia.m3u` | 58 | 58 | 0 | 0 | 0 | 0 |
| `playlists/countries/Slovenia.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Somalia.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/South_Africa.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/South_Korea.m3u` | 70 | 66 | 1 | 0 | 3 | 0 |
| `playlists/countries/Spain.m3u` | 193 | 189 | 2 | 2 | 0 | 0 |
| `playlists/countries/Sri_Lanka.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sudan.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Suriname.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sweden.m3u` | 376 | 376 | 0 | 0 | 0 | 0 |
| `playlists/countries/Switzerland.m3u` | 28 | 25 | 0 | 0 | 3 | 0 |
| `playlists/countries/Syria.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Taiwan.m3u` | 20 | 17 | 0 | 3 | 0 | 0 |
| `playlists/countries/Tanzania.m3u` | 5 | 3 | 2 | 0 | 0 | 0 |
| `playlists/countries/Thailand.m3u` | 68 | 68 | 0 | 0 | 0 | 0 |
| `playlists/countries/Togo.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Trinidad_and_Tobago.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Tunisia.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Turkey.m3u` | 141 | 136 | 1 | 2 | 2 | 0 |
| `playlists/countries/Turkmenistan.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/UK.m3u` | 246 | 232 | 1 | 0 | 13 | 0 |
| `playlists/countries/USA.m3u` | 2784 | 2698 | 35 | 33 | 18 | 0 |
| `playlists/countries/Uganda.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Ukraine.m3u` | 170 | 169 | 0 | 0 | 1 | 0 |
| `playlists/countries/United_Arab_Emirates.m3u` | 42 | 42 | 0 | 0 | 0 | 0 |
| `playlists/countries/Uruguay.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Uzbekistan.m3u` | 35 | 30 | 0 | 0 | 5 | 0 |
| `playlists/countries/Venezuela.m3u` | 49 | 48 | 0 | 1 | 0 | 0 |
| `playlists/countries/Vietnam.m3u` | 70 | 70 | 0 | 0 | 0 | 0 |
| `playlists/countries/Western_Sahara.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Yemen.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Zimbabwe.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |

## Patches applied

- Removed **204** confirmed-dead links across **48** playlists (working ratio 96.9%).
  - `PremiumTV.m3u`: -18 (12009 -> 11991)
  - `Argentina.m3u`: -1 (164 -> 163)
  - `Australia.m3u`: -1 (33 -> 32)
  - `Bolivia.m3u`: -3 (48 -> 45)
  - `Brazil.m3u`: -5 (180 -> 175)
  - `Bulgaria.m3u`: -1 (62 -> 61)
  - `Cambodia.m3u`: -1 (14 -> 13)
  - `Cameroon.m3u`: -1 (13 -> 12)
  - `Canada.m3u`: -2 (139 -> 137)
  - `Chile.m3u`: -6 (196 -> 190)
  - `Colombia.m3u`: -1 (113 -> 112)
  - `Costa_Rica.m3u`: -2 (60 -> 58)
  - `Croatia.m3u`: -1 (14 -> 13)
  - `Czechia.m3u`: -1 (99 -> 98)
  - `Dominican_Republic.m3u`: -11 (210 -> 199)
  - `Ecuador.m3u`: -1 (54 -> 53)
  - `El_Salvador.m3u`: -3 (19 -> 16)
  - `Finland.m3u`: -6 (32 -> 26)
  - `Ghana.m3u`: -1 (7 -> 6)
  - `Greece.m3u`: -2 (91 -> 89)
  - `Guatemala.m3u`: -2 (34 -> 32)
  - `Guyana.m3u`: -1 (11 -> 10)
  - `Haiti.m3u`: -1 (7 -> 6)
  - `Honduras.m3u`: -4 (48 -> 44)
  - `Hungary.m3u`: -6 (164 -> 158)
  - `India.m3u`: -37 (785 -> 748)
  - `International.m3u`: -5 (1296 -> 1291)
  - `Iraq.m3u`: -3 (61 -> 58)
  - `Israel.m3u`: -1 (44 -> 43)
  - `Italy.m3u`: -3 (530 -> 527)
  - `Martinique.m3u`: -1 (5 -> 4)
  - `Mexico.m3u`: -11 (127 -> 116)
  - `Myanmar.m3u`: -1 (14 -> 13)
  - `Netherlands.m3u`: -1 (150 -> 149)
  - `Nicaragua.m3u`: -1 (7 -> 6)
  - `Pakistan.m3u`: -2 (53 -> 51)
  - `Paraguay.m3u`: -1 (56 -> 55)
  - `Peru.m3u`: -6 (150 -> 144)
  - `Puerto_Rico.m3u`: -3 (29 -> 26)
  - `Romania.m3u`: -2 (145 -> 143)
  - `Russia.m3u`: -1 (427 -> 426)
  - `Saudi_Arabia.m3u`: -1 (51 -> 50)
  - `South_Korea.m3u`: -1 (70 -> 69)
  - `Spain.m3u`: -2 (193 -> 191)
  - `Tanzania.m3u`: -2 (5 -> 3)
  - `Turkey.m3u`: -1 (141 -> 140)
  - `UK.m3u`: -1 (246 -> 245)
  - `USA.m3u`: -35 (2784 -> 2750)

## Hosts with the most failing links

| Host | Offline | Unreachable |
|---|---:|---:|
| `mumt07.tangotv.in` | 17 | 0 |
| `64b16f23efbee.streamlock.net` | 0 | 14 |
| `23.239.31.26:8989` | 0 | 13 |
| `5f22d76e220e1.streamlock.net` | 0 | 12 |
| `tg0o4gr4uqmtt8y41hcjzgezdrmmbqbh8c3toq73u1cjqxfozr5udctzy.100ycdn.com` | 1 | 10 |
| `198.58.104.90:8989` | 0 | 10 |
| `cdn.pishow.tv` | 9 | 0 |
| `edge55.dc.beltelecom.by` | 0 | 8 |
| `www.rtmpcdn.com` | 7 | 0 |
| `38.65.175.84:8000` | 0 | 6 |
| `111.59.139.85:11888` | 0 | 6 |
| `168.196.127.137:6001` | 6 | 0 |
| `live.ahsz.tv` | 0 | 6 |
| `l.cztvcloud.com` | 0 | 6 |
| `live-fi.tvkaista.net` | 6 | 0 |
| `141.94.193.53:80` | 6 | 0 |
| `samitaorigin.tangotv.in` | 6 | 0 |
| `live20.bozztv.com` | 1 | 4 |
| `ngtrk.dc.beltelecom.by` | 0 | 5 |
| `193.47.62.41` | 5 | 0 |
| `chatgpt.hereisman.net` | 5 | 0 |
| `30a-tv.com` | 0 | 4 |
| `92.63.196.180:8080` | 0 | 4 |
| `salto-streams.nl` | 0 | 4 |
| `app.ncare.live` | 0 | 4 |

## Sample of confirmed-dead links

| Channel | Reason | URL |
|---|---|---|
| ☆ Darcizzle Offshore 🇺🇸 | HTTP 422 | `https://ssai.aniview.com/api/v1/hls/stream.m3u8?AVS_SSAIID=69099f3b30a6ba46360d7c72&AV_CHANNEL_NAME=Fishing-Offshore&AV_CONTENT_LANGUAGE=en&AV_CONTENT_RATING=TV-14&cb=MX_CACHEBUSTER&AV_APPPKGNAME=MX_APP_BUNDLE&AV_APPNAME=MX_APP_NAME&AV_APPSTOREURL=MX_APP_STORE_URL&AV_WIDTH=MX_WIDTH&AV_HEIGHT=MX_HEIGHT&AV_LANGUAGE=MX_DEVICE_LANGUAGE&AV_IFA_TYPE=MX_IFA_TYPE&AV_CATEGORY=IAB17-32&AV_TITLE=Fishing-Offshore&AV_EPISODE=MX_CONTENT_EPISODE&AV_CONTENT_GENRE=Fishing&AV_GDPR=MX_GDPR&AV_CONSENT=MX_CONSENT&AV_COPPA=MX_COPPA&AV_IDFA=MX_IFA&AV_CCPA=MX_US_PRIVACY&AV_CONTENT_CHANNEL=Fishing-Offshore&AV_CUSTOM17=Google--520678__193__13827__0__0__0____MP&AV_CUSTOM18=MX_GIVN&AV_CUSTOM19=pn%3D2v2lTwj4%26context%3Dmid-13827` |
| MRTV Sports [Not 24/7] | playlist only, HTTP 404 | `https://mrtvott.com/cache/MRTV-SPORT/master.m3u8` |
| ADN TV (720p) | playlist only, HTTP 404 | `https://redirector.rudo.video/hls-video/931b584451fa6dd1313ee66efbfd5802e3f3bcea/adntv/adntv.smil/playlist.m3u8` |
| Fakt Marathi (576p) | connection refused | `https://mumt07.tangotv.in/zHjX9OFlFAKTMARATHI/index.m3u8` |
| Magnavision TV (720p) | playlist only, HTTP 404 | `https://manatv.akamaized.net/120723/smil:magnavision.smil/playlist.m3u8` |
| Radio UP (1080p) | HTTP 404 | `https://iptv.ixfo.com.ar:30443/live/RadioUpTvStreaming/playlist.m3u8` |
| JonmoBhumi TV (720p) | HTTP 404 | `https://jtvs.ncare.live/Gznr84Woj7UEye3OPVeWq2ForboWAgdV/jonmobhumitv.stream/playlist.m3u8` |
| FTV (Bolivia) (720p) | HTTP 404 | `https://master.tucableip.com/ftvhd/index.m3u8` |
| UPEA TV (720p) | dns lookup failed | `https://tvstream.upea.bo/hls/oSs0jSWumTFIIVY97559.m3u8` |
| Radio Mega TV Amazonia (720p) | HTTP 404 | `https://ares.disfrutaenlared.com:1936/megatv/megatv/playlist.m3u8` |
| SOU TV | HTTP 404 | `https://video10.logicahost.com.br/soutv/soutv/playlist.m3u8` |
| TV Arapuan (720p) | HTTP 404 | `https://5b7f3c45ab7c2.streamlock.net/arapuan/ngrp:arapuan_all/playlist.m3u8` |
| TV Modelo (720p) | HTTP 404 | `https://video09.logicahost.com.br/tvmodelo/tvmodelo/playlist.m3u` |
| TV Sul Bahia (320p) | HTTP 404 | `https://live.cdn.upx.com/00046/myStream.sdp/playlist.m3u8` |
| ISTV | HTTP 404 | `https://video08.logicahost.com.br/istvnacional/srt.stream/istvnacional.m3u8` |
| Light Channel (Bulgaria) (480p) [Not 24/7] | HTTP 404 | `https://streamer1.streamhost.org/salive/GMIlcbgM/playlist.m3u8` |
| EAC News TV | HTTP 404 | `https://live.eac-news.com/LiveApp/streams/eacnews.m3u8` |
| CTV Afrique (720p) | HTTP 404 | `https://stream.it-innov.com/ctv/index.m3u8` |
| Channel Y (720p) [Not 24/7] | variant HTTP 404 | `http://cdn19.live247stream.com/channely/tv/playlist.m3u8` |
| Dukh Nivaran (720p) [Not 24/7] | HTTP 404 | `http://cdn12.henico.net:8080/live/dncal/index.m3u8` |
| Canal 30 Loncomilla (720p) | HTTP 404 | `https://v1.tustreaming.cl/canal30loncomilla/index.m3u8` |
| Radio Edelweiss (720p) | connection refused | `https://vmix.dyndns.biz/Edelweiss/index.m3u8` |
| ADN TV (720p) | playlist only, HTTP 404 | `https://redirector.rudo.video/hls-video/931b584451fa6dd1313ee66efbfd5802e3f3bcea/adntv/adntv.smil/playlist.m3u8` |
| Chiloe Red 25 (720p) | HTTP 404 | `https://v2.tustreaming.cl/chiloered/index.m3u8` |
| Tevex (1080p) | HTTP 404 | `https://v2.tustreaming.cl/tevex/index.m3u8` |
