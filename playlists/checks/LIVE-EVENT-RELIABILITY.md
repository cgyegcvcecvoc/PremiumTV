# Live-event reliability audit

- **Scrape snapshot:** 2026-11-27T20:12:14Z
- **Scrape run:** `20261127T200429Z-2995` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 6/61
- **Fixtures with a redundancy deficit:** 55

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Denver Broncos vs. Pittsburgh Steelers (American Football) | 2/2 | 2/2 | 0/1 | 2 | MP66, STRMGATE | doms9, doms9-events | **DEFICIT** |
| SC Rheindorf Altach vs. Grazer AK (AUT 1) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Netherlands vs. Israel (Basketball World Cup) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Slovenia vs. Finland (Basketball World Cup) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Sweden vs. Hungary (Basketball World Cup) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Emanuel Odiase vs. Mike Perez (Boxing) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Akron vs. Buffalo (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Fairfield vs. Navy (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Iowa State vs. St. John's (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Iowa vs. Nebraska (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Maine vs. Le Moyne (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Ohio vs. Toledo (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Ole Miss vs. Mississippi St. (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| TCU Horned Frogs vs. Georgia Tech Yellow Jackets (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| UCLA vs. Georgetown (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| UTSA vs. Tulsa (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Vanderbilt vs. Southern Univ. (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Wake Forest vs. Memphis (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| CD Sabadell vs. Leganés (ESP 2) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Poland vs. Croatia (FIBA World Cup Qualification, Europe) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Slovenia vs. Finland (FIBA World Cup Qualification, Europe) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Agen vs. Beziers (France Rugby Pro D2) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Angouleme vs. Nissa (France Rugby Pro D2) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Colomiers vs. Nevers (France Rugby Pro D2) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Valence Romans vs. Aurillac (France Rugby Pro D2) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Boston Bruins vs. Toronto Maple Leafs (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9, doms9-events | **PASS** |
| Calgary Flames vs. New Jersey Devils (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9, doms9-events | **PASS** |
| Dallas Stars vs. St. Louis Blues (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9, doms9-events | **PASS** |
| Detroit Red Wings vs. Columbus Blue Jackets (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Florida Panthers vs. Washington Capitals (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Nashville Predators vs. Utah Mammoth (NHL Hockey) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, STRMGATE | doms9, doms9-events | **PASS** |
| Ottawa Senators vs. Tampa Bay Lightning (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Vancouver Canucks vs. Philadelphia Flyers (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| C.D. Nacional vs. Maritimo (POR 1) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Al Ittihad vs. Neom SC (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Bologna vs. Venezia (Soccer) | 2/2 | 2/2 | 0/1 | 2 | ISTRMEAST, STRMGATE | doms9, doms9-events | **DEFICIT** |
| Borussia Mönchengladbach vs. Werder Bremen (Soccer) | 3/3 | 2/2 | 1/1 | 2 | SPRTSBITE, STRMGATE | doms9, doms9-events | **PASS** |
| Delfin vs. Orense (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Etoile-Carouge vs. Lausanne Ouchy (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| FC Groningen vs. Willem II (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Francs Borains vs. Eupen (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Genk U23 vs. Anderlecht U23 (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Grazer AK vs. Altach (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Gyor vs. Debrecen (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Jong Ajax vs. Heracles (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Kriens vs. Aarau (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Levante vs. Racing Santander (Soccer) | 2/2 | 2/2 | 0/1 | 2 | SPRTSBITE, STRMGATE | doms9, doms9-events | **DEFICIT** |
| MVV Maastricht vs. Jong PSV (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| NAC Breda vs. FC Den Bosch (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Nottingham Forest vs. Chelsea (Soccer) | 4/4 | 2/2 | 2/1 | 2 | SPRTSBITE, STRMGATE | doms9, doms9-events | **PASS** |
| Paris FC vs. Brest (Soccer) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Petrolul vs. FC Arges (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Sonderjyske vs. Brondby (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Werder Bremen vs. Monchengladbach (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Winterthur vs. Rapperswil-Jona (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Modo vs. Almtuna (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Nybro vs. Mora (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Oskarshamn vs. Kalmar (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Ostersund vs. Leksand (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Vasteras vs. AIK (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Visby Roma vs. Vimmerby (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |

## Deficits

- **Denver Broncos vs. Pittsburgh Steelers** — needs 1 more confirmed dedicated backup feed(s).
- **SC Rheindorf Altach vs. Grazer AK** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Netherlands vs. Israel** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Slovenia vs. Finland** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Sweden vs. Hungary** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Emanuel Odiase vs. Mike Perez** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Akron vs. Buffalo** — needs 1 more confirmed dedicated backup feed(s).
- **Fairfield vs. Navy** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Iowa State vs. St. John's** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Iowa vs. Nebraska** — needs 1 more confirmed dedicated backup feed(s).
- **Maine vs. Le Moyne** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ohio vs. Toledo** — needs 1 more confirmed dedicated backup feed(s).
- **Ole Miss vs. Mississippi St.** — needs 1 more confirmed dedicated backup feed(s).
- **TCU Horned Frogs vs. Georgia Tech Yellow Jackets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **UCLA vs. Georgetown** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **UTSA vs. Tulsa** — needs 1 more confirmed dedicated backup feed(s).
- **Vanderbilt vs. Southern Univ.** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Wake Forest vs. Memphis** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **CD Sabadell vs. Leganés** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Poland vs. Croatia** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Slovenia vs. Finland** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Agen vs. Beziers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Angouleme vs. Nissa** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Colomiers vs. Nevers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Valence Romans vs. Aurillac** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Detroit Red Wings vs. Columbus Blue Jackets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Florida Panthers vs. Washington Capitals** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ottawa Senators vs. Tampa Bay Lightning** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Vancouver Canucks vs. Philadelphia Flyers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **C.D. Nacional vs. Maritimo** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Al Ittihad vs. Neom SC** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Bologna vs. Venezia** — needs 1 more confirmed dedicated backup feed(s).
- **Delfin vs. Orense** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Etoile-Carouge vs. Lausanne Ouchy** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **FC Groningen vs. Willem II** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Francs Borains vs. Eupen** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Genk U23 vs. Anderlecht U23** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Grazer AK vs. Altach** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Gyor vs. Debrecen** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Jong Ajax vs. Heracles** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Kriens vs. Aarau** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Levante vs. Racing Santander** — needs 1 more confirmed dedicated backup feed(s).
- **MVV Maastricht vs. Jong PSV** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **NAC Breda vs. FC Den Bosch** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Paris FC vs. Brest** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Petrolul vs. FC Arges** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Sonderjyske vs. Brondby** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Werder Bremen vs. Monchengladbach** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Winterthur vs. Rapperswil-Jona** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Modo vs. Almtuna** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Nybro vs. Mora** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Oskarshamn vs. Kalmar** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ostersund vs. Leksand** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Vasteras vs. AIK** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Visby Roma vs. Vimmerby** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
