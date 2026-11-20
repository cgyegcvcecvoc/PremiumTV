# Live-event reliability audit

- **Scrape snapshot:** 2026-11-20T19:14:32Z
- **Scrape run:** `20261120T191043Z-3101` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 0/56
- **Fixtures with a redundancy deficit:** 56

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Anadolu Efes vs. Lyon-Villeurbanne (Basketball Euroleague) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Olympiacos vs. Real Madrid (Basketball Euroleague) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Lauren Price vs. Michaela Kotaskova (Boxing) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Florida St vs. UWGB (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Middle Tennessee St. vs. Temple (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Oklahoma State vs. Minnesota (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| PAEEK vs. Halkanoras (Cyprus Division 2) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Leganés vs. FC Andorra (ESP 2) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Aurillac vs. Colomiers (France Rugby Pro D2) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Beziers vs. US Dax (France Rugby Pro D2) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Montauban vs. Agen (France Rugby Pro D2) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Nevers vs. Angouleme (France Rugby Pro D2) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Nissa vs. Valence Romans (France Rugby Pro D2) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| 1. FC Heidenheim 1846 vs. SV Darmstadt (GER 2) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| 1. FC Magdeburg vs. Arminia Bielefeld (GER 2) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Aarhus Fremad vs. Hobro (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Aarhus vs. Lyngby (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Al Ahli SC vs. Al Nassr (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Al-Ahli vs. Al-Nassr (Soccer) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Almere City vs. NAC Breda (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Annecy vs. Clermont (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Arminia Bielefeld vs. Magdeburg (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Azam vs. Singida Black Stars (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Club Brugge KV U23 vs. Virton (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Darmstadt vs. Heidenheim (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| De Graafschap vs. MVV Maastricht (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| FC Botosani vs. FC Voluntari (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| FC Cologne vs. Bayern Munich (Soccer) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| FC Den Bosch vs. VVV Venlo (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| FC Volendam vs. Jong Ajax (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Guingamp vs. Rodez (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Helmond Sport vs. FC Dordrecht (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Heracles vs. Jong PSV (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Ind del Valle vs. Macara (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Kolding IF vs. Aalborg (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Lausanne Ouchy vs. Kriens (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Lierse vs. Sporting Lokeren (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Metz vs. Boulogne (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Molde vs. Bodo Glimt (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Nancy vs. Dijon (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Piast Gliwice vs. Korona Kielce (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Rapperswil-Jona vs. Aarau (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Red Star vs. Pau FC (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Stade Nyonnais vs. Wil (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| TOP Oss vs. Roda JC (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| TSV Havelse vs. Viktoria Koln (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Union Berlin W vs. Bayer Leverkusen W (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Vitesse vs. Jong AZ (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Xamax vs. Etoile-Carouge (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| AIK vs. Sodertalje (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Kalmar vs. Almtuna (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Leksand vs. Visby Roma (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Mora vs. Modo (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Oskarshamn vs. Nybro (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Ostersund vs. Vimmerby (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Vasteras vs. BIK Karlskoga (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **Anadolu Efes vs. Lyon-Villeurbanne** — needs 1 more confirmed dedicated backup feed(s).
- **Olympiacos vs. Real Madrid** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Lauren Price vs. Michaela Kotaskova** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Florida St vs. UWGB** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Middle Tennessee St. vs. Temple** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Oklahoma State vs. Minnesota** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **PAEEK vs. Halkanoras** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Leganés vs. FC Andorra** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Aurillac vs. Colomiers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Beziers vs. US Dax** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Montauban vs. Agen** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Nevers vs. Angouleme** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Nissa vs. Valence Romans** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **1. FC Heidenheim 1846 vs. SV Darmstadt** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **1. FC Magdeburg vs. Arminia Bielefeld** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Aarhus Fremad vs. Hobro** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Aarhus vs. Lyngby** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Al Ahli SC vs. Al Nassr** — needs 1 more confirmed dedicated backup feed(s).
- **Al-Ahli vs. Al-Nassr** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Almere City vs. NAC Breda** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Annecy vs. Clermont** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Arminia Bielefeld vs. Magdeburg** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Azam vs. Singida Black Stars** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Club Brugge KV U23 vs. Virton** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Darmstadt vs. Heidenheim** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **De Graafschap vs. MVV Maastricht** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **FC Botosani vs. FC Voluntari** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **FC Cologne vs. Bayern Munich** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **FC Den Bosch vs. VVV Venlo** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **FC Volendam vs. Jong Ajax** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Guingamp vs. Rodez** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Helmond Sport vs. FC Dordrecht** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Heracles vs. Jong PSV** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ind del Valle vs. Macara** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Kolding IF vs. Aalborg** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Lausanne Ouchy vs. Kriens** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Lierse vs. Sporting Lokeren** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Metz vs. Boulogne** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Molde vs. Bodo Glimt** — needs 1 more confirmed dedicated backup feed(s).
- **Nancy vs. Dijon** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Piast Gliwice vs. Korona Kielce** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Rapperswil-Jona vs. Aarau** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Red Star vs. Pau FC** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Stade Nyonnais vs. Wil** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **TOP Oss vs. Roda JC** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **TSV Havelse vs. Viktoria Koln** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Union Berlin W vs. Bayer Leverkusen W** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Vitesse vs. Jong AZ** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Xamax vs. Etoile-Carouge** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **AIK vs. Sodertalje** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Kalmar vs. Almtuna** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Leksand vs. Visby Roma** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Mora vs. Modo** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Oskarshamn vs. Nybro** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ostersund vs. Vimmerby** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Vasteras vs. BIK Karlskoga** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
