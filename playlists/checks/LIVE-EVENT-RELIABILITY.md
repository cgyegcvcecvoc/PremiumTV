# Live-event reliability audit

- **Scrape snapshot:** 2026-11-27T18:14:14Z
- **Scrape run:** `20261127T180627Z-3184` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 0/54
- **Fixtures with a redundancy deficit:** 54

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| SC Rheindorf Altach vs. Grazer AK (AUT 1) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Estonia vs. France (Basketball World Cup) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Latvia vs. Germany (Basketball World Cup) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Palestine vs. United Arab Emirates (Basketball World Cup) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Sweden vs. Hungary (Basketball World Cup) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Emanuel Odiase vs. Mike Perez (Boxing) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Akron vs. Buffalo (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Florida International Panthers vs. North Dakota Fighting Hawks (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Iowa vs. Nebraska (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Louisville Cardinals vs. Akron Zips (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Northwestern Wildcats vs. DePaul Blue Demons (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Ohio vs. Toledo (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Ole Miss vs. Mississippi St. (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| UTSA vs. Tulsa (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Xavier vs. Virginia (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| US Dax vs. US Oyonnax (France Rugby Pro D2) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| 1. FC Nürnberg vs. 1. FC Heidenheim 1846 (GER 2) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| SV Darmstadt vs. VfL Bochum (GER 2) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Boston Bruins vs. Toronto Maple Leafs (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9, doms9-events | **DEFICIT** |
| Calgary Flames vs. New Jersey Devils (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9, doms9-events | **DEFICIT** |
| Nashville Predators vs. Utah Mammoth (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9, doms9-events | **DEFICIT** |
| Italy vs. Fiji (Rugby Nations Championship) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| AB Copenhagen vs. Vejle (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| AEK Larnaca vs. Apollon (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| AEL Limassol vs. Ol Nicosia (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Al Ittihad vs. Neom SC (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Alanyaspor vs. Konyaspor (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Artis Brno vs. Slovacko (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Bochum vs. Darmstadt (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Celik Zenica vs. BSK Banja Luka (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Feirense vs. Portimonense (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Hansa Rostock vs. TSV Havelse (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Heidenheim vs. Nurnberg (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Hvidovre IF vs. Kolding IF (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Istra 1961 vs. Varazdin (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Lokomotiv Sofia vs. Slavia Sofia (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Omonia 29th May vs. Omonia Aradippou (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Radomlje vs. Nafta (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Rakow vs. Piast Gliwice (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Rizespor vs. Kasimpasa (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Sariyer vs. Istanbulspor AS (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Sonderjyske vs. Brondby (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Stellenbosch vs. TS Galaxy (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Umraniyespor vs. Manisa FK (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Warta Poznan vs. Pogon Siedlce (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Modo vs. Almtuna (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Nybro vs. Mora (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Oskarshamn vs. Kalmar (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Ostersund vs. Leksand (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Vasteras vs. AIK (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Visby Roma vs. Vimmerby (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Kasimpasa vs. Caykur Rizespor (TUR 1) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Konyaspor vs. Alanyaspor (TUR 1) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Romania U17 vs. Cameroon U17 (World Cup U17) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |

## Deficits

- **SC Rheindorf Altach vs. Grazer AK** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Estonia vs. France** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Latvia vs. Germany** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Palestine vs. United Arab Emirates** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Sweden vs. Hungary** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Emanuel Odiase vs. Mike Perez** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Akron vs. Buffalo** — needs 1 more confirmed dedicated backup feed(s).
- **Florida International Panthers vs. North Dakota Fighting Hawks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Iowa vs. Nebraska** — needs 1 more confirmed dedicated backup feed(s).
- **Louisville Cardinals vs. Akron Zips** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Northwestern Wildcats vs. DePaul Blue Demons** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ohio vs. Toledo** — needs 1 more confirmed dedicated backup feed(s).
- **Ole Miss vs. Mississippi St.** — needs 1 more confirmed dedicated backup feed(s).
- **UTSA vs. Tulsa** — needs 1 more confirmed dedicated backup feed(s).
- **Xavier vs. Virginia** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **US Dax vs. US Oyonnax** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **1. FC Nürnberg vs. 1. FC Heidenheim 1846** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **SV Darmstadt vs. VfL Bochum** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Boston Bruins vs. Toronto Maple Leafs** — needs 1 more confirmed dedicated backup feed(s).
- **Calgary Flames vs. New Jersey Devils** — needs 1 more confirmed dedicated backup feed(s).
- **Nashville Predators vs. Utah Mammoth** — needs 1 more confirmed dedicated backup feed(s).
- **Italy vs. Fiji** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **AB Copenhagen vs. Vejle** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **AEK Larnaca vs. Apollon** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **AEL Limassol vs. Ol Nicosia** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Al Ittihad vs. Neom SC** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Alanyaspor vs. Konyaspor** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Artis Brno vs. Slovacko** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Bochum vs. Darmstadt** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Celik Zenica vs. BSK Banja Luka** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Feirense vs. Portimonense** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Hansa Rostock vs. TSV Havelse** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Heidenheim vs. Nurnberg** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Hvidovre IF vs. Kolding IF** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Istra 1961 vs. Varazdin** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Lokomotiv Sofia vs. Slavia Sofia** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Omonia 29th May vs. Omonia Aradippou** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Radomlje vs. Nafta** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Rakow vs. Piast Gliwice** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Rizespor vs. Kasimpasa** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Sariyer vs. Istanbulspor AS** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Sonderjyske vs. Brondby** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Stellenbosch vs. TS Galaxy** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Umraniyespor vs. Manisa FK** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Warta Poznan vs. Pogon Siedlce** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Modo vs. Almtuna** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Nybro vs. Mora** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Oskarshamn vs. Kalmar** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ostersund vs. Leksand** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Vasteras vs. AIK** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Visby Roma vs. Vimmerby** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Kasimpasa vs. Caykur Rizespor** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Konyaspor vs. Alanyaspor** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Romania U17 vs. Cameroon U17** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
