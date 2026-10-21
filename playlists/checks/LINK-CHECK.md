# Deep link check

- **Run:** nightly deep link check (`20261021T101122Z-3228`)
- **Started:** 2026-10-21T10:11:22Z  |  **Finished:** 2026-10-21T10:17:30Z  |  **Duration:** 367.8s
- **Mode:** deep (playlist + segment probe)
- **Unique links checked:** 13348 from 26710 playlist entries in 178 playlists

| Result | Links | Share | Meaning |
|---|---:|---:|---|
| working | 22810 | 85.4% | answered with playable media |
| offline | 68 | 0.3% | confirmed dead - removed when patching |
| unreachable | 2100 | 7.9% | timeout or server error - kept, may recover |
| blocked | 1732 | 6.5% | HTTP 401/403/451 - needs auth or is geo-blocked |

## Per playlist

| Playlist | Entries | Working | Offline | Unreachable | Blocked | Other |
|---|---:|---:|---:|---:|---:|---:|
| `playlists/PremiumTV.m3u` | 13294 | 11366 | 13 | 1049 | 866 | 0 |
| `playlists/AE_Channels.m3u` | 68 | 67 | 0 | 1 | 0 | 0 |
| `playlists/countries/Afghanistan.m3u` | 10 | 9 | 0 | 1 | 0 | 0 |
| `playlists/countries/Albania.m3u` | 28 | 16 | 0 | 8 | 4 | 0 |
| `playlists/countries/Algeria.m3u` | 7 | 5 | 0 | 1 | 1 | 0 |
| `playlists/countries/Andorra.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Angola.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Arab_World.m3u` | 15 | 15 | 0 | 0 | 0 | 0 |
| `playlists/countries/Argentina.m3u` | 172 | 158 | 0 | 5 | 9 | 0 |
| `playlists/countries/Armenia.m3u` | 10 | 10 | 0 | 0 | 0 | 0 |
| `playlists/countries/Aruba.m3u` | 8 | 8 | 0 | 0 | 0 | 0 |
| `playlists/countries/Australia.m3u` | 45 | 34 | 0 | 4 | 7 | 0 |
| `playlists/countries/Austria.m3u` | 49 | 40 | 0 | 7 | 2 | 0 |
| `playlists/countries/Azerbaijan.m3u` | 18 | 11 | 0 | 2 | 5 | 0 |
| `playlists/countries/Bahamas.m3u` | 2 | 1 | 0 | 1 | 0 | 0 |
| `playlists/countries/Bahrain.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Bangladesh.m3u` | 28 | 19 | 0 | 8 | 1 | 0 |
| `playlists/countries/Barbados.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Belarus.m3u` | 31 | 25 | 0 | 6 | 0 | 0 |
| `playlists/countries/Belgium.m3u` | 40 | 28 | 0 | 0 | 12 | 0 |
| `playlists/countries/Belize.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Benin.m3u` | 5 | 3 | 0 | 2 | 0 | 0 |
| `playlists/countries/Bolivia.m3u` | 48 | 46 | 0 | 2 | 0 | 0 |
| `playlists/countries/Bosnia_and_Herzegovina.m3u` | 21 | 9 | 0 | 10 | 2 | 0 |
| `playlists/countries/Brazil.m3u` | 239 | 170 | 0 | 41 | 28 | 0 |
| `playlists/countries/British_Virgin_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Brunei.m3u` | 2 | 0 | 0 | 0 | 2 | 0 |
| `playlists/countries/Bulgaria.m3u` | 42 | 29 | 0 | 11 | 2 | 0 |
| `playlists/countries/Burkina_Faso.m3u` | 3 | 0 | 0 | 0 | 3 | 0 |
| `playlists/countries/Burundi.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Cambodia.m3u` | 14 | 12 | 1 | 1 | 0 | 0 |
| `playlists/countries/Cameroon.m3u` | 14 | 11 | 0 | 1 | 2 | 0 |
| `playlists/countries/Canada.m3u` | 192 | 145 | 0 | 17 | 30 | 0 |
| `playlists/countries/Cape_Verde.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Caribbean_Netherlands.m3u` | 6 | 4 | 0 | 2 | 0 | 0 |
| `playlists/countries/Chad.m3u` | 2 | 1 | 0 | 1 | 0 | 0 |
| `playlists/countries/Chile.m3u` | 214 | 186 | 2 | 11 | 15 | 0 |
| `playlists/countries/China.m3u` | 158 | 86 | 0 | 55 | 17 | 0 |
| `playlists/countries/Colombia.m3u` | 115 | 108 | 0 | 5 | 2 | 0 |
| `playlists/countries/Costa_Rica.m3u` | 65 | 60 | 1 | 0 | 4 | 0 |
| `playlists/countries/Croatia.m3u` | 15 | 13 | 0 | 2 | 0 | 0 |
| `playlists/countries/Cuba.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Curacao.m3u` | 4 | 2 | 0 | 2 | 0 | 0 |
| `playlists/countries/Cyprus.m3u` | 21 | 21 | 0 | 0 | 0 | 0 |
| `playlists/countries/Czechia.m3u` | 118 | 90 | 0 | 11 | 17 | 0 |
| `playlists/countries/DR_Congo.m3u` | 14 | 3 | 1 | 10 | 0 | 0 |
| `playlists/countries/Denmark.m3u` | 15 | 8 | 0 | 2 | 5 | 0 |
| `playlists/countries/Dominican_Republic.m3u` | 203 | 196 | 1 | 5 | 1 | 0 |
| `playlists/countries/Ecuador.m3u` | 61 | 49 | 3 | 8 | 1 | 0 |
| `playlists/countries/Egypt.m3u` | 17 | 15 | 0 | 0 | 2 | 0 |
| `playlists/countries/El_Salvador.m3u` | 23 | 15 | 0 | 7 | 1 | 0 |
| `playlists/countries/Equatorial_Guinea.m3u` | 2 | 1 | 0 | 1 | 0 | 0 |
| `playlists/countries/Eritrea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Estonia.m3u` | 26 | 22 | 0 | 3 | 1 | 0 |
| `playlists/countries/Ethiopia.m3u` | 2 | 1 | 0 | 1 | 0 | 0 |
| `playlists/countries/Faroe_Islands.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Finland.m3u` | 34 | 21 | 0 | 12 | 1 | 0 |
| `playlists/countries/France.m3u` | 261 | 204 | 1 | 19 | 37 | 0 |
| `playlists/countries/French_Guiana.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Gambia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Georgia.m3u` | 20 | 14 | 0 | 3 | 3 | 0 |
| `playlists/countries/Germany.m3u` | 409 | 357 | 2 | 15 | 35 | 0 |
| `playlists/countries/Ghana.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Greece.m3u` | 94 | 87 | 0 | 4 | 3 | 0 |
| `playlists/countries/Guadeloupe.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guam.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guatemala.m3u` | 37 | 31 | 1 | 5 | 0 | 0 |
| `playlists/countries/Guinea.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Guyana.m3u` | 10 | 8 | 0 | 1 | 1 | 0 |
| `playlists/countries/Haiti.m3u` | 10 | 6 | 0 | 3 | 1 | 0 |
| `playlists/countries/Honduras.m3u` | 56 | 45 | 0 | 10 | 1 | 0 |
| `playlists/countries/Hong_Kong.m3u` | 23 | 8 | 0 | 3 | 12 | 0 |
| `playlists/countries/Hungary.m3u` | 144 | 114 | 0 | 23 | 7 | 0 |
| `playlists/countries/Iceland.m3u` | 5 | 4 | 0 | 0 | 1 | 0 |
| `playlists/countries/India.m3u` | 734 | 672 | 5 | 37 | 20 | 0 |
| `playlists/countries/Indonesia.m3u` | 127 | 114 | 2 | 9 | 2 | 0 |
| `playlists/countries/International.m3u` | 1207 | 1142 | 0 | 23 | 42 | 0 |
| `playlists/countries/Iran.m3u` | 95 | 91 | 0 | 2 | 2 | 0 |
| `playlists/countries/Iraq.m3u` | 60 | 57 | 0 | 3 | 0 | 0 |
| `playlists/countries/Ireland.m3u` | 25 | 18 | 0 | 0 | 7 | 0 |
| `playlists/countries/Israel.m3u` | 41 | 31 | 0 | 0 | 10 | 0 |
| `playlists/countries/Italy.m3u` | 563 | 472 | 0 | 47 | 44 | 0 |
| `playlists/countries/Ivory_Coast.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/countries/Jamaica.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Japan.m3u` | 20 | 17 | 0 | 0 | 3 | 0 |
| `playlists/countries/Jordan.m3u` | 17 | 17 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kazakhstan.m3u` | 40 | 24 | 0 | 3 | 13 | 0 |
| `playlists/countries/Kenya.m3u` | 8 | 5 | 2 | 1 | 0 | 0 |
| `playlists/countries/Kosovo.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kuwait.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/countries/Kyrgyzstan.m3u` | 6 | 2 | 0 | 1 | 3 | 0 |
| `playlists/countries/Laos.m3u` | 7 | 7 | 0 | 0 | 0 | 0 |
| `playlists/countries/Latin_America.m3u` | 34 | 33 | 0 | 0 | 1 | 0 |
| `playlists/countries/Latvia.m3u` | 18 | 17 | 0 | 0 | 1 | 0 |
| `playlists/countries/Lebanon.m3u` | 30 | 27 | 0 | 2 | 1 | 0 |
| `playlists/countries/Libya.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Lithuania.m3u` | 23 | 18 | 0 | 0 | 5 | 0 |
| `playlists/countries/Luxembourg.m3u` | 15 | 12 | 0 | 2 | 1 | 0 |
| `playlists/countries/Macau.m3u` | 6 | 0 | 0 | 6 | 0 | 0 |
| `playlists/countries/Malaysia.m3u` | 6 | 4 | 0 | 0 | 2 | 0 |
| `playlists/countries/Maldives.m3u` | 5 | 4 | 0 | 0 | 1 | 0 |
| `playlists/countries/Mali.m3u` | 3 | 2 | 0 | 1 | 0 | 0 |
| `playlists/countries/Malta.m3u` | 7 | 3 | 0 | 0 | 4 | 0 |
| `playlists/countries/Martinique.m3u` | 6 | 5 | 0 | 1 | 0 | 0 |
| `playlists/countries/Mexico.m3u` | 151 | 116 | 0 | 11 | 24 | 0 |
| `playlists/countries/Moldova.m3u` | 21 | 21 | 0 | 0 | 0 | 0 |
| `playlists/countries/Monaco.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mongolia.m3u` | 76 | 76 | 0 | 0 | 0 | 0 |
| `playlists/countries/Montenegro.m3u` | 6 | 3 | 0 | 0 | 3 | 0 |
| `playlists/countries/Morocco.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/countries/Mozambique.m3u` | 4 | 2 | 0 | 2 | 0 | 0 |
| `playlists/countries/Myanmar.m3u` | 15 | 4 | 0 | 11 | 0 | 0 |
| `playlists/countries/Namibia.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Nepal.m3u` | 9 | 7 | 0 | 0 | 2 | 0 |
| `playlists/countries/Netherlands.m3u` | 160 | 145 | 1 | 7 | 7 | 0 |
| `playlists/countries/New_Zealand.m3u` | 9 | 7 | 0 | 0 | 2 | 0 |
| `playlists/countries/Nicaragua.m3u` | 12 | 5 | 0 | 2 | 5 | 0 |
| `playlists/countries/Niger.m3u` | 4 | 2 | 0 | 0 | 2 | 0 |
| `playlists/countries/Nigeria.m3u` | 42 | 30 | 0 | 7 | 5 | 0 |
| `playlists/countries/North_Korea.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/North_Macedonia.m3u` | 23 | 21 | 0 | 2 | 0 | 0 |
| `playlists/countries/Norway.m3u` | 12 | 7 | 0 | 0 | 5 | 0 |
| `playlists/countries/Oman.m3u` | 6 | 6 | 0 | 0 | 0 | 0 |
| `playlists/countries/Pakistan.m3u` | 86 | 40 | 0 | 43 | 3 | 0 |
| `playlists/countries/Palestine.m3u` | 21 | 20 | 0 | 0 | 1 | 0 |
| `playlists/countries/Panama.m3u` | 18 | 15 | 0 | 3 | 0 | 0 |
| `playlists/countries/Papua_New_Guinea.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |
| `playlists/countries/Paraguay.m3u` | 52 | 50 | 1 | 0 | 1 | 0 |
| `playlists/countries/Peru.m3u` | 139 | 126 | 0 | 5 | 8 | 0 |
| `playlists/countries/Philippines.m3u` | 12 | 11 | 1 | 0 | 0 | 0 |
| `playlists/countries/Poland.m3u` | 236 | 153 | 0 | 77 | 6 | 0 |
| `playlists/countries/Portugal.m3u` | 62 | 40 | 0 | 16 | 6 | 0 |
| `playlists/countries/Puerto_Rico.m3u` | 26 | 26 | 0 | 0 | 0 | 0 |
| `playlists/countries/Qatar.m3u` | 43 | 35 | 1 | 0 | 7 | 0 |
| `playlists/countries/Republic_of_the_Congo.m3u` | 3 | 1 | 0 | 1 | 1 | 0 |
| `playlists/countries/Romania.m3u` | 139 | 117 | 1 | 11 | 10 | 0 |
| `playlists/countries/Russia.m3u` | 500 | 391 | 2 | 96 | 11 | 0 |
| `playlists/countries/Rwanda.m3u` | 9 | 9 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Kitts_and_Nevis.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saint_Lucia.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Saudi_Arabia.m3u` | 59 | 51 | 0 | 0 | 8 | 0 |
| `playlists/countries/Senegal.m3u` | 9 | 5 | 1 | 2 | 1 | 0 |
| `playlists/countries/Serbia.m3u` | 31 | 18 | 6 | 6 | 1 | 0 |
| `playlists/countries/Singapore.m3u` | 24 | 22 | 0 | 0 | 2 | 0 |
| `playlists/countries/Sint_Maarten.m3u` | 5 | 5 | 0 | 0 | 0 | 0 |
| `playlists/countries/Slovakia.m3u` | 68 | 53 | 0 | 14 | 1 | 0 |
| `playlists/countries/Slovenia.m3u` | 11 | 7 | 0 | 4 | 0 | 0 |
| `playlists/countries/Somalia.m3u` | 9 | 4 | 0 | 5 | 0 | 0 |
| `playlists/countries/South_Africa.m3u` | 19 | 16 | 0 | 1 | 2 | 0 |
| `playlists/countries/South_Korea.m3u` | 80 | 64 | 0 | 14 | 2 | 0 |
| `playlists/countries/Spain.m3u` | 253 | 196 | 3 | 25 | 29 | 0 |
| `playlists/countries/Sri_Lanka.m3u` | 14 | 8 | 0 | 6 | 0 | 0 |
| `playlists/countries/Sudan.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Suriname.m3u` | 2 | 2 | 0 | 0 | 0 | 0 |
| `playlists/countries/Sweden.m3u` | 389 | 378 | 0 | 3 | 8 | 0 |
| `playlists/countries/Switzerland.m3u` | 36 | 25 | 0 | 5 | 6 | 0 |
| `playlists/countries/Syria.m3u` | 12 | 12 | 0 | 0 | 0 | 0 |
| `playlists/countries/Taiwan.m3u` | 22 | 15 | 0 | 5 | 2 | 0 |
| `playlists/countries/Tajikistan.m3u` | 14 | 0 | 0 | 14 | 0 | 0 |
| `playlists/countries/Tanzania.m3u` | 6 | 5 | 0 | 1 | 0 | 0 |
| `playlists/countries/Thailand.m3u` | 91 | 61 | 2 | 9 | 19 | 0 |
| `playlists/countries/Togo.m3u` | 7 | 2 | 0 | 1 | 4 | 0 |
| `playlists/countries/Trinidad_and_Tobago.m3u` | 5 | 4 | 0 | 1 | 0 | 0 |
| `playlists/countries/Tunisia.m3u` | 4 | 4 | 0 | 0 | 0 | 0 |
| `playlists/countries/Turkey.m3u` | 152 | 128 | 6 | 11 | 7 | 0 |
| `playlists/countries/Turkmenistan.m3u` | 16 | 16 | 0 | 0 | 0 | 0 |
| `playlists/countries/UK.m3u` | 347 | 226 | 0 | 31 | 90 | 0 |
| `playlists/countries/USA.m3u` | 2896 | 2706 | 5 | 75 | 110 | 0 |
| `playlists/countries/Uganda.m3u` | 15 | 11 | 1 | 2 | 1 | 0 |
| `playlists/countries/Ukraine.m3u` | 190 | 168 | 0 | 19 | 3 | 0 |
| `playlists/countries/United_Arab_Emirates.m3u` | 52 | 42 | 0 | 6 | 4 | 0 |
| `playlists/countries/Uruguay.m3u` | 5 | 4 | 0 | 0 | 1 | 0 |
| `playlists/countries/Uzbekistan.m3u` | 35 | 35 | 0 | 0 | 0 | 0 |
| `playlists/countries/Venezuela.m3u` | 59 | 52 | 0 | 5 | 2 | 0 |
| `playlists/countries/Vietnam.m3u` | 73 | 57 | 1 | 1 | 14 | 0 |
| `playlists/countries/Western_Sahara.m3u` | 3 | 3 | 0 | 0 | 0 | 0 |
| `playlists/countries/Yemen.m3u` | 4 | 3 | 1 | 0 | 0 | 0 |
| `playlists/countries/Zimbabwe.m3u` | 1 | 1 | 0 | 0 | 0 | 0 |

## Patches applied

- Removed **68** confirmed-dead links across **28** playlists (working ratio 85.4%).
  - `PremiumTV.m3u`: -13 (13294 -> 13281)
  - `Cambodia.m3u`: -1 (14 -> 13)
  - `Chile.m3u`: -2 (214 -> 212)
  - `Costa_Rica.m3u`: -1 (65 -> 64)
  - `DR_Congo.m3u`: -1 (14 -> 13)
  - `Dominican_Republic.m3u`: -1 (203 -> 202)
  - `Ecuador.m3u`: -3 (61 -> 58)
  - `France.m3u`: -1 (261 -> 260)
  - `Germany.m3u`: -2 (409 -> 407)
  - `Guatemala.m3u`: -1 (37 -> 36)
  - `India.m3u`: -5 (734 -> 729)
  - `Indonesia.m3u`: -2 (127 -> 125)
  - `Kenya.m3u`: -2 (8 -> 6)
  - `Netherlands.m3u`: -1 (160 -> 159)
  - `Paraguay.m3u`: -1 (52 -> 51)
  - `Philippines.m3u`: -1 (12 -> 11)
  - `Qatar.m3u`: -1 (43 -> 42)
  - `Romania.m3u`: -1 (139 -> 138)
  - `Russia.m3u`: -2 (500 -> 498)
  - `Senegal.m3u`: -1 (9 -> 8)
  - `Serbia.m3u`: -6 (31 -> 25)
  - `Spain.m3u`: -3 (253 -> 250)
  - `Thailand.m3u`: -2 (91 -> 89)
  - `Turkey.m3u`: -6 (152 -> 146)
  - `USA.m3u`: -5 (2896 -> 2892)
  - `Uganda.m3u`: -1 (15 -> 14)
  - `Vietnam.m3u`: -1 (73 -> 72)
  - `Yemen.m3u`: -1 (4 -> 3)

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
| `sktv.mxnticek.eu` | 0 | 25 |
| `cache0.wonvt.st` | 0 | 24 |
| `live-fi.tvkaista.net` | 0 | 22 |
| `tvsen7.aynascope.net` | 0 | 20 |
| `91.228.35.249:8001` | 0 | 20 |
| `znty.dyndns.org:5010` | 0 | 20 |
| `5f22d76e220e1.streamlock.net` | 0 | 20 |
| `cdn.rostelekom-tv.xyz` | 0 | 18 |
| `151.80.18.177:86` | 0 | 18 |
| `51.254.199.122:8080` | 0 | 18 |
| `64b16f23efbee.streamlock.net` | 0 | 18 |
| `103.72.101.252:8080` | 0 | 18 |
| `mumbai-edge.smartplaytv.in` | 0 | 16 |
| `mrtvott.com` | 0 | 14 |
| `190.197.41.183` | 0 | 14 |
| `39.134.115.163:8080` | 0 | 14 |
| `183.207.248.71` | 0 | 12 |
| `cdn.tvmatic.net` | 0 | 12 |

## Sample of confirmed-dead links

| Channel | Reason | URL |
|---|---|---|
| Pauta (1080p) | playlist only, HTTP 404 | `https://redirector.rudo.video/hls-video/ey6283je82983je9823je8jowowiekldk9838274/pautatv/pautatv.smil/playlist.m3u8` |
| Punjabi Hits (1080p) | variant HTTP 404 | `https://stream.ottlive.co.in/punjabihits/index.m3u8` |
| Baraka Television (720p) [Not 24/7] | HTTP 404 | `https://stream.berosat.live:19360/baraka-hd/baraka-hd.m3u8` |
| Channel 8 (1080p) [Not 24/7] | playlist only, HTTP 404 | `http://usa.login.in.th:1935/ch8/ch8/playlist.m3u8` |
| Northeast Live (720p) | HTTP 404 | `https://server.thelegitpro.in/northeastlive/northeastlive/index.fmp4.m3u8` |
| Bayon TV | playlist only, HTTP 403 | `https://live-evg2.tv360.metfone.com.kh/livebayontv/bayontvhd.stream/playlist.m3u8` |
| La Metro TV (1080p) | HTTP 404 | `https://jireh-8-hls-video-us-isp.dps.live/hls-video/931b584451fa6dd1313ee66efbfd5802e3f3bcea/metropolitanatv/metropolitanatv.smil/playlist.m3u8` |
| Pauta (1080p) | playlist only, HTTP 404 | `https://redirector.rudo.video/hls-video/ey6283je82983je9823je8jowowiekldk9838274/pautatv/pautatv.smil/playlist.m3u8` |
| Impact Channel | HTTP 404 | `https://5fe2654d6127d.streamlock.net/impactchannel/videoimpactchannel/playlist.m3u8` |
| Baraka Television (720p) [Not 24/7] | HTTP 404 | `https://stream.berosat.live:19360/baraka-hd/baraka-hd.m3u8` |
| Tele Poder TV (720p) [Not 24/7] | HTTP 404 | `https://cdn.telepoder.online:3229/dash/stream.m3u8` |
| Radio Monumental TV (720p) [Not 24/7] | connection refused | `https://cloud37.ecuatel.com/monumentaltv/live/manifest.m3u8` |
| IeanJesus Ecuador (720p) | connection refused | `https://cloud37.ecuatel.com/iglesia2020/Stream1/playlist.m3u8` |
| Ciracu TV (720p) [Not 24/7] | connection refused | `https://cloud37.ecuatel.com/ciracutv/live/manifest.m3u8` |
| Eurosport 1 Turkiye | dns lookup failed | `https://andro.mangeinde4.lat/checklist/androstreamlivees1.m3u8` |
| Terra Mater WILD English (1080p) | dns lookup failed | `https://amg01775-amg01775c1-amgplt0343.playout.now3.amagi.tv/playlist/amg01775-amg01775c1-amgplt0343/playlist.m3u8` |
| RTL | playlist only, empty segment | `https://ma.anixa.tv/clips/stream/rtl/playlist.php` |
| Nuestra Imagen TV | HTTP 404 | `https://live.tvcontrolcp.com:1936/tvnitelevision/tvnitelevision/playlist.m3u8` |
| Northeast Live (720p) | HTTP 404 | `https://server.thelegitpro.in/northeastlive/northeastlive/index.fmp4.m3u8` |
| Times Now (Backup 1) | variant HTTP 404 | `https://pubads.g.doubleclick.net/ssai/event/1mR1QUQ3Tg-VuKfiyjwNuA/master.m3u8` |
| Oscar Movies Bhojpuri (720p) | playlist only, HTTP 404 | `https://cdn.pishow.tv/ott/live/233/master.m3u8` |
| Punjabi Hits (1080p) | variant HTTP 404 | `https://stream.ottlive.co.in/punjabihits/index.m3u8` |
| Chithiram (576p) | playlist only, HTTP 404 | `https://cdn.pishow.tv/ott/live/1243/master.m3u8` |
| Astha TV (1080p) | playlist only, HTTP 404 | `https://hgmtv.com:2020/hls/asthalive/asthalive.m3u8` |
| Sampit TV (720p) [Not 24/7] | HTTP 404 | `https://sampit-tv.siar.us/live/sampit-tv.m3u8` |
