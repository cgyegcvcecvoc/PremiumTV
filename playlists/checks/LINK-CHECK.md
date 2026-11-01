# Deep link check

- **Run:** nightly deep link check (`20261101T115312Z-3088`)
- **Started:** 2026-11-01T11:53:12Z  |  **Finished:** 2026-11-01T11:56:39Z  |  **Duration:** 207.3s
- **Mode:** deep (playlist + segment probe)
- **Unique links checked:** 12522 from 24662 playlist entries in 180 playlists

| Result | Links | Share | Meaning |
|---|---:|---:|---|
| working | 23778 | 96.4% | answered with playable media |
| offline | 480 | 1.9% | confirmed dead - removed when patching |
| unreachable | 282 | 1.1% | timeout or server error - kept, may recover |
| blocked | 122 | 0.5% | HTTP 401/403/451 - needs auth or is geo-blocked |

## Per playlist

| Playlist | Entries | Working | Offline | Unreachable | Blocked | Other |
|---|---:|---:|---:|---:|---:|---:|
| `playlists/PremiumTV.m3u` | 12069 | 11844 | 25 | 139 | 61 | 0 |
| `playlists/AE_Channels.m3u` | 71 | 71 | 0 | 0 | 0 | 0 |
| `playlists/countries/Afghanistan.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Albania.m3u` | 17 | 13 | 1 | 3 | 0 | 0 |
| `playlists/countries/Algeria.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Andorra.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Angola.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Antigua_and_Barbuda.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Arab_World.m3u` | 14 | 14 | 0 | 0 | 0 | 0 |
| `playlists/countries/Argentina.m3u` | 173 | 167 | 5 | 1 | 0 | 0 |
| `playlists/countries/Armenia.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Aruba.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Australia.m3u` | 48 | 37 | 11 | 0 | 0 | 0 |
| `playlists/countries/Austria.m3u` | 43 | 41 | 1 | 1 | 0 | 0 |
| `playlists/countries/Azerbaijan.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bahamas.m3u` | 3 | 2 | 1 | 0 | 0 | 0 |
| `playlists/countries/Bahrain.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bangladesh.m3u` | 22 | 19 | 0 | 3 | 0 | 0 |
| `playlists/countries/Barbados.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Belarus.m3u` | 34 | 26 | 2 | 6 | 0 | 0 |
| `playlists/countries/Belgium.m3u` | 37 | 36 | 1 | 0 | 0 | 0 |
| `playlists/countries/Belize.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Benin.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bermuda.m3u` | 1 | 0 | 1 | 0 | 0 | 0 |
| `playlists/countries/Bolivia.m3u` | 42 | 40 | 1 | 1 | 0 | 0 |
| `playlists/countries/Bosnia_and_Herzegovina.m3u` | 11 | 9 | 2 | 0 | 0 | 0 |
| `playlists/countries/Brazil.m3u` | 188 | 182 | 2 | 4 | 0 | 0 |
| `playlists/countries/British_Virgin_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bulgaria.m3u` | 63 | 61 | 0 | 0 | 2 | 0 |
| `playlists/countries/Burkina_Faso.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Burundi.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cambodia.m3u` | 20 | 14 | 5 | 0 | 1 | 0 |
| `playlists/countries/Cameroon.m3u` | 14 | 14 | 0 | 0 | 0 | 0 |
| `playlists/countries/Canada.m3u` | 142 | 137 | 5 | 0 | 0 | 0 |
| `playlists/countries/Cape_Verde.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Caribbean_Netherlands.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Chad.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Chile.m3u` | 199 | 188 | 7 | 4 | 0 | 0 |
| `playlists/countries/China.m3u` | 98 | 87 | 8 | 2 | 1 | 0 |
| `playlists/countries/Colombia.m3u` | 117 | 112 | 3 | 0 | 2 | 0 |
| `playlists/countries/Costa_Rica.m3u` | 61 | 58 | 3 | 0 | 0 | 0 |
| `playlists/countries/Croatia.m3u` | 17 | 10 | 3 | 0 | 4 | 0 |
| `playlists/countries/Cuba.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Curacao.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cyprus.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/countries/Czechia.m3u` | 98 | 98 | 0 | 0 | 0 | 0 |
| `playlists/countries/DR_Congo.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Denmark.m3u` | 11 | 7 | 4 | 0 | 0 | 0 |
| `playlists/countries/Dominican_Republic.m3u` | 213 | 210 | 0 | 3 | 0 | 0 |
| `playlists/countries/Ecuador.m3u` | 54 | 54 | 0 | 0 | 0 | 0 |
| `playlists/countries/Egypt.m3u` | 17 | 16 | 1 | 0 | 0 | 0 |
| `playlists/countries/El_Salvador.m3u` | 15 | 14 | 1 | 0 | 0 | 0 |
| `playlists/countries/Equatorial_Guinea.m3u` | 1 | 0 | 1 | 0 | 0 | 0 |
| `playlists/countries/Eritrea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Estonia.m3u` | 21 | 21 | 0 | 0 | 0 | 0 |
| `playlists/countries/Ethiopia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Faroe_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Finland.m3u` | 29 | 23 | 1 | 5 | 0 | 0 |
| `playlists/countries/France.m3u` | 217 | 214 | 2 | 1 | 0 | 0 |
| `playlists/countries/French_Guiana.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Georgia.m3u` | 14 | 14 | 0 | 0 | 0 | 0 |
| `playlists/countries/Germany.m3u` | 393 | 369 | 22 | 1 | 1 | 0 |
| `playlists/countries/Ghana.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Greece.m3u` | 93 | 91 | 0 | 1 | 1 | 0 |
| `playlists/countries/Guadeloupe.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guam.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guatemala.m3u` | 34 | 33 | 1 | 0 | 0 | 0 |
| `playlists/countries/Guinea.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guyana.m3u` | 10 | 9 | 0 | 1 | 0 | 0 |
| `playlists/countries/Haiti.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Honduras.m3u` | 47 | 46 | 0 | 1 | 0 | 0 |
| `playlists/countries/Hong_Kong.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/countries/Hungary.m3u` | 155 | 150 | 4 | 1 | 0 | 0 |
| `playlists/countries/Iceland.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/India.m3u` | 813 | 766 | 24 | 4 | 19 | 0 |
| `playlists/countries/Indonesia.m3u` | 123 | 117 | 4 | 2 | 0 | 0 |
| `playlists/countries/International.m3u` | 1205 | 1147 | 48 | 9 | 1 | 0 |
| `playlists/countries/Iran.m3u` | 113 | 86 | 27 | 0 | 0 | 0 |
| `playlists/countries/Iraq.m3u` | 62 | 57 | 4 | 1 | 0 | 0 |
| `playlists/countries/Ireland.m3u` | 23 | 18 | 4 | 0 | 1 | 0 |
| `playlists/countries/Israel.m3u` | 31 | 30 | 0 | 0 | 1 | 0 |
| `playlists/countries/Italy.m3u` | 533 | 507 | 8 | 15 | 3 | 0 |
| `playlists/countries/Ivory_Coast.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/countries/Jamaica.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Japan.m3u` | 22 | 15 | 5 | 0 | 2 | 0 |
| `playlists/countries/Jordan.m3u` | 20 | 18 | 2 | 0 | 0 | 0 |
| `playlists/countries/Kazakhstan.m3u` | 26 | 23 | 0 | 3 | 0 | 0 |
| `playlists/countries/Kenya.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kosovo.m3u` | 8 | 7 | 1 | 0 | 0 | 0 |
| `playlists/countries/Kuwait.m3u` | 15 | 14 | 1 | 0 | 0 | 0 |
| `playlists/countries/Kyrgyzstan.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Laos.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Latin_America.m3u` | 33 | 33 | 0 | 0 | 0 | 0 |
| `playlists/countries/Latvia.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/Lebanon.m3u` | 30 | 27 | 2 | 1 | 0 | 0 |
| `playlists/countries/Libya.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Lithuania.m3u` | 19 | 19 | 0 | 0 | 0 | 0 |
| `playlists/countries/Luxembourg.m3u` | 16 | 12 | 4 | 0 | 0 | 0 |
| `playlists/countries/Macau.m3u` | 1 | 0 | 1 | 0 | 0 | 0 |
| `playlists/countries/Malaysia.m3u` | 6 | 3 | 3 | 0 | 0 | 0 |
| `playlists/countries/Maldives.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mali.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Malta.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Martinique.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mauritania.m3u` | 1 | 0 | 1 | 0 | 0 | 0 |
| `playlists/countries/Mexico.m3u` | 124 | 119 | 2 | 3 | 0 | 0 |
| `playlists/countries/Moldova.m3u` | 20 | 20 | 0 | 0 | 0 | 0 |
| `playlists/countries/Monaco.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mongolia.m3u` | 79 | 79 | 0 | 0 | 0 | 0 |
| `playlists/countries/Montenegro.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Morocco.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mozambique.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Myanmar.m3u` | 14 | 6 | 0 | 8 | 0 | 0 |
| `playlists/countries/Namibia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nepal.m3u` | 6 | 3 | 3 | 0 | 0 | 0 |
| `playlists/countries/Netherlands.m3u` | 159 | 143 | 12 | 4 | 0 | 0 |
| `playlists/countries/New_Zealand.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nicaragua.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Niger.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nigeria.m3u` | 34 | 33 | 1 | 0 | 0 | 0 |
| `playlists/countries/North_Korea.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/North_Macedonia.m3u` | 22 | 19 | 0 | 0 | 3 | 0 |
| `playlists/countries/Norway.m3u` | 9 | 8 | 1 | 0 | 0 | 0 |
| `playlists/countries/Oman.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Pakistan.m3u` | 52 | 51 | 0 | 1 | 0 | 0 |
| `playlists/countries/Palestine.m3u` | 20 | 19 | 0 | 1 | 0 | 0 |
| `playlists/countries/Panama.m3u` | 16 | 13 | 3 | 0 | 0 | 0 |
| `playlists/countries/Papua_New_Guinea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Paraguay.m3u` | 59 | 56 | 3 | 0 | 0 | 0 |
| `playlists/countries/Peru.m3u` | 134 | 132 | 2 | 0 | 0 | 0 |
| `playlists/countries/Philippines.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/countries/Poland.m3u` | 171 | 165 | 2 | 4 | 0 | 0 |
| `playlists/countries/Portugal.m3u` | 50 | 45 | 5 | 0 | 0 | 0 |
| `playlists/countries/Puerto_Rico.m3u` | 27 | 25 | 0 | 0 | 2 | 0 |
| `playlists/countries/Qatar.m3u` | 38 | 37 | 1 | 0 | 0 | 0 |
| `playlists/countries/Republic_of_the_Congo.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Romania.m3u` | 140 | 138 | 2 | 0 | 0 | 0 |
| `playlists/countries/Russia.m3u` | 442 | 422 | 12 | 8 | 0 | 0 |
| `playlists/countries/Rwanda.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Kitts_and_Nevis.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Lucia.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/San_Marino.m3u` | 2 | 0 | 2 | 0 | 0 | 0 |
| `playlists/countries/Saudi_Arabia.m3u` | 57 | 51 | 6 | 0 | 0 | 0 |
| `playlists/countries/Senegal.m3u` | 7 | 6 | 1 | 0 | 0 | 0 |
| `playlists/countries/Serbia.m3u` | 24 | 21 | 2 | 0 | 1 | 0 |
| `playlists/countries/Sierra_Leone.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Singapore.m3u` | 29 | 28 | 1 | 0 | 0 | 0 |
| `playlists/countries/Sint_Maarten.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Slovakia.m3u` | 59 | 59 | 0 | 0 | 0 | 0 |
| `playlists/countries/Slovenia.m3u` | 6 | 5 | 0 | 0 | 1 | 0 |
| `playlists/countries/Somalia.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/South_Africa.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/South_Korea.m3u` | 77 | 71 | 6 | 0 | 0 | 0 |
| `playlists/countries/Spain.m3u` | 231 | 198 | 32 | 1 | 0 | 0 |
| `playlists/countries/Sri_Lanka.m3u` | 7 | 6 | 0 | 1 | 0 | 0 |
| `playlists/countries/Sudan.m3u` | 3 | 2 | 1 | 0 | 0 | 0 |
| `playlists/countries/Suriname.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sweden.m3u` | 376 | 376 | 0 | 0 | 0 | 0 |
| `playlists/countries/Switzerland.m3u` | 28 | 25 | 0 | 0 | 3 | 0 |
| `playlists/countries/Syria.m3u` | 11 | 11 | 0 | 0 | 0 | 0 |
| `playlists/countries/Taiwan.m3u` | 20 | 17 | 0 | 3 | 0 | 0 |
| `playlists/countries/Tanzania.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Thailand.m3u` | 67 | 65 | 1 | 1 | 0 | 0 |
| `playlists/countries/Togo.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Trinidad_and_Tobago.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Tunisia.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Turkey.m3u` | 151 | 136 | 11 | 2 | 2 | 0 |
| `playlists/countries/Turkmenistan.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/UK.m3u` | 262 | 245 | 10 | 5 | 2 | 0 |
| `playlists/countries/USA.m3u` | 2831 | 2722 | 82 | 26 | 1 | 0 |
| `playlists/countries/Uganda.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/countries/Ukraine.m3u` | 179 | 176 | 2 | 0 | 1 | 0 |
| `playlists/countries/United_Arab_Emirates.m3u` | 46 | 42 | 4 | 0 | 0 | 0 |
| `playlists/countries/Uruguay.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Uzbekistan.m3u` | 35 | 30 | 0 | 0 | 5 | 0 |
| `playlists/countries/Venezuela.m3u` | 55 | 51 | 2 | 1 | 1 | 0 |
| `playlists/countries/Vietnam.m3u` | 78 | 73 | 5 | 0 | 0 | 0 |
| `playlists/countries/Western_Sahara.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Yemen.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Zimbabwe.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |

## Patches applied

- Removed **470** confirmed-dead links across **70** playlists (working ratio 96.4%).
  - `PremiumTV.m3u`: -25 (12069 -> 12044)
  - `Albania.m3u`: -1 (17 -> 16)
  - `Argentina.m3u`: -5 (173 -> 168)
  - `Australia.m3u`: -11 (48 -> 37)
  - `Austria.m3u`: -1 (43 -> 42)
  - `Bahamas.m3u`: -1 (3 -> 2)
  - `Belarus.m3u`: -2 (34 -> 32)
  - `Belgium.m3u`: -1 (37 -> 36)
  - `Bermuda.m3u`: -1 (1 -> 0)
  - `Bolivia.m3u`: -1 (42 -> 41)
  - `Bosnia_and_Herzegovina.m3u`: -2 (11 -> 9)
  - `Brazil.m3u`: -2 (188 -> 186)
  - `Cambodia.m3u`: -5 (20 -> 15)
  - `Canada.m3u`: -5 (142 -> 137)
  - `Chile.m3u`: -7 (199 -> 192)
  - `China.m3u`: -8 (98 -> 90)
  - `Colombia.m3u`: -3 (117 -> 114)
  - `Costa_Rica.m3u`: -3 (61 -> 58)
  - `Croatia.m3u`: -3 (17 -> 14)
  - `Egypt.m3u`: -1 (17 -> 16)
  - `El_Salvador.m3u`: -1 (15 -> 14)
  - `Equatorial_Guinea.m3u`: -1 (1 -> 0)
  - `Finland.m3u`: -1 (29 -> 28)
  - `France.m3u`: -2 (217 -> 215)
  - `Germany.m3u`: -22 (393 -> 371)
  - `Guatemala.m3u`: -1 (34 -> 33)
  - `Hungary.m3u`: -4 (155 -> 151)
  - `India.m3u`: -24 (813 -> 789)
  - `Indonesia.m3u`: -4 (123 -> 119)
  - `International.m3u`: -48 (1205 -> 1157)
  - `Iran.m3u`: -27 (113 -> 86)
  - `Iraq.m3u`: -4 (62 -> 58)
  - `Ireland.m3u`: -4 (23 -> 19)
  - `Italy.m3u`: -8 (533 -> 525)
  - `Japan.m3u`: -5 (22 -> 17)
  - `Jordan.m3u`: -2 (20 -> 18)
  - `Kosovo.m3u`: -1 (8 -> 7)
  - `Kuwait.m3u`: -1 (15 -> 14)
  - `Lebanon.m3u`: -2 (30 -> 28)
  - `Luxembourg.m3u`: -4 (16 -> 12)
  - `Macau.m3u`: -1 (1 -> 0)
  - `Mauritania.m3u`: -1 (1 -> 0)
  - `Mexico.m3u`: -2 (124 -> 122)
  - `Netherlands.m3u`: -12 (159 -> 147)
  - `Nigeria.m3u`: -1 (34 -> 33)
  - `Norway.m3u`: -1 (9 -> 8)
  - `Panama.m3u`: -3 (16 -> 13)
  - `Paraguay.m3u`: -3 (59 -> 56)
  - `Peru.m3u`: -2 (134 -> 132)
  - `Poland.m3u`: -2 (171 -> 169)
  - `Portugal.m3u`: -5 (50 -> 45)
  - `Qatar.m3u`: -1 (38 -> 37)
  - `Romania.m3u`: -2 (140 -> 138)
  - `Russia.m3u`: -12 (442 -> 430)
  - `San_Marino.m3u`: -2 (2 -> 0)
  - `Saudi_Arabia.m3u`: -6 (57 -> 51)
  - `Senegal.m3u`: -1 (7 -> 6)
  - `Serbia.m3u`: -2 (24 -> 22)
  - `Singapore.m3u`: -1 (29 -> 28)
  - `South_Korea.m3u`: -6 (77 -> 71)
  - `Spain.m3u`: -32 (231 -> 199)
  - `Sudan.m3u`: -1 (3 -> 2)
  - `Thailand.m3u`: -1 (67 -> 66)
  - `Turkey.m3u`: -11 (151 -> 140)
  - `UK.m3u`: -10 (262 -> 252)
  - `USA.m3u`: -82 (2831 -> 2750)
  - `Ukraine.m3u`: -2 (179 -> 177)
  - `United_Arab_Emirates.m3u`: -4 (46 -> 42)
  - `Venezuela.m3u`: -2 (55 -> 53)
  - `Vietnam.m3u`: -5 (78 -> 73)
  - skipped `Denmark.m3u`: removing 4/11 entries exceeds --max-remove-ratio 35%
  - skipped `Malaysia.m3u`: removing 3/6 entries exceeds --max-remove-ratio 35%
  - skipped `Nepal.m3u`: removing 3/6 entries exceeds --max-remove-ratio 35%

## Hosts with the most failing links

| Host | Offline | Unreachable |
|---|---:|---:|
| `live.streamingfast.net` | 27 | 0 |
| `tvsen7.aynascope.net` | 0 | 22 |
| `ncdn.telewebion.ir` | 22 | 0 |
| `mrtvott.com` | 0 | 16 |
| `live20.bozztv.com` | 0 | 16 |
| `64b16f23efbee.streamlock.net` | 0 | 14 |
| `mdc.ott.alticeusa.net` | 10 | 3 |
| `cdn4.skygo.mn` | 13 | 0 |
| `tvsen5.aynascope.net` | 0 | 12 |
| `5f22d76e220e1.streamlock.net` | 0 | 12 |
| `wdrlokalzeit.akamaized.net` | 11 | 0 |
| `livestreaming.b67buv2.tweedekamer.nl` | 11 | 0 |
| `live-fi.tvkaista.net` | 0 | 10 |
| `edge55.dc.beltelecom.by` | 0 | 10 |
| `abcnews-streams.akamaized.net` | 10 | 0 |
| `tvsen3.aynaott.com` | 9 | 0 |
| `tvsen6.aynaott.com` | 8 | 0 |
| `30a-tv.com` | 2 | 4 |
| `cdnlivetv.tv` | 0 | 6 |
| `ztnr.rtve.es` | 6 | 0 |
| `origin.dpsgo.com` | 2 | 4 |
| `cityeden.catcast.tv` | 0 | 6 |
| `38.65.175.84:8000` | 0 | 6 |
| `111.59.139.85:11888` | 0 | 6 |
| `redirector.rudo.video` | 4 | 2 |

## Sample of confirmed-dead links

| Channel | Reason | URL |
|---|---|---|
| HTV Sports (1080i) | HTTP 404 | `https://vmttv.dpdns.org/tv360/?id=htv-the-thao` |
| La 2 Canarias (720p) | playlist only, HTTP 403 | `https://ztnr.rtve.es/ztnr/5468585.m3u8` |
| Pindin TV | HTTP 404 | `https://sistemastr.tropicalmoonmedia.com/live/7C452409423F57ADC960F6405635267F/7.m3u8` |
| India Today (720p) | playlist only, HTTP 416 | `https://d1rc86nwwc9fag.cloudfront.net/vglive-sk-293160/master.m3u8` |
| News12 Brooklyn [Geo-blocked] | variant HTTP 404 | `https://mdc.ott.alticeusa.net/live4.ott.optimum.net/live4-uploads/N12KH_A1/index_new.m3u8?omap=https` |
| Fieri Tv (720p) | connection refused | `http://valashop.online:8090/fieritv.m3u8` |
| Canal 5 TV Chepes | HTTP 404 | `https://videostream.shockmedia.com.ar:19360/canal5alfatvchepes/canal5alfatvchepes.m3u8` |
| Canal 7 Salta (1080p) | HTTP 404 | `https://vivo.solumedia.com:19360/cooperativa/cooperativa.m3u8` |
| Misiones Cuatro | HTTP 404 | `https://iptv.ixfo.com.ar:30443/live-HD/MISIONES4/playlist.m3u8` |
| Telefe Buenos Aires (1080p) | HTTP 404 | `http://45.134.141.161:2200/ARG/TELEFE_HD/index.m3u8` |
| Radio Conexion Web TV (720p) | HTTP 404 | `https://tuvideoonline.com.ar:3391/live/radioconexionlive.m3u8` |
| Expo Channel (360p) | variant HTTP dns lookup failed | `https://tvsnhlslivetest.akamaized.net/hls/live/2034711/EXPO-MSL4/master.m3u8` |
| 10 HD | playlist only, HTTP 403 | `https://i.mjh.nz/.r/10-nsw.m3u8` |
| 10 Peach | playlist only, HTTP 403 | `https://i.mjh.nz/.r/10peach-nsw.m3u8` |
| 7flix | playlist only, HTTP 403 | `https://i.mjh.nz/.r/7flix-syd.m3u8` |
| 7mate | playlist only, HTTP 403 | `https://i.mjh.nz/.r/7mate-syd.m3u8` |
| ServusTV (Backup 1) | variant HTTP 404 | `https://rbmn-live.akamaized.net/hls/live/2002825/geoSTVATweb/master.m3u8` |
| Guardian Talk Radio (1080p) | HTTP 404 | `https://cdn-edge1.streamcomedia.com/abr_tngr969fm/abr-tngr969fm_streams/playlist.m3u8` |
| Первый Музыкальный Канал (Backup 1) | variant HTTP 404 | `https://ngtrk.dc.beltelecom.by/ngtrk/smil:ont.smil/playlist.m3u8` |
| Belros Ⓢ | playlist only, HTTP 404 | `https://live2.mediacdn.ru/sr1/tro/playlist.m3u8` |
| ☆ Surf Channel 🇪🇸 🏄 | playlist only, HTTP 400 | `https://jmp2.uk/stvp-ES3400002PY` |
| Channel 82 | variant HTTP 403 | `https://service.webvideocore.net/CL1olYogIrDWvwqiIKK7eBmnWbRkKKsu3nqabm9GlX02JOj3CDNXzodJMDEN2dk3/a_bq9clxfbupwg.m3u8` |
| UMSA TVU LP (720p) | HTTP 404 | `https://edge.enhdtv.com/8190/index.m3u8` |
| RTRS TV (576p) [Not 24/7] | HTTP 404 | `https://uzivo.rtrs.tv/tv/live/index.m3u8` |
| Maria+Vision Medjugorje (720p) | variant HTTP 404 | `https://1601580044.rsc.cdn77.org/live/_jcn_/amlst:Italiasette/playlist.m3u8` |
