# Live-event reliability audit

- **Scrape snapshot:** 2026-11-22T18:40:52Z
- **Scrape run:** `20261122T183555Z-2976` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 9/45
- **Fixtures with a redundancy deficit:** 36

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Arizona Cardinals vs. Kansas City Chiefs (American Football) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, KINGDOME, STRMGATE | doms9 | **PASS** |
| Baltimore Ravens vs. Carolina Panthers (American Football) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, KINGDOME, STRMGATE | doms9 | **PASS** |
| Buffalo Bills vs. Miami Dolphins (American Football) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, KINGDOME, STRMGATE | doms9 | **PASS** |
| Chicago Bears vs. New Orleans Saints (American Football) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, KINGDOME, STRMGATE | doms9 | **PASS** |
| Dallas Cowboys vs. Tennessee Titans (American Football) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, KINGDOME, STRMGATE | doms9 | **PASS** |
| Detroit Lions vs. Tampa Bay Buccaneers (American Football) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, KINGDOME, STRMGATE | doms9 | **PASS** |
| Philadelphia Eagles vs. Pittsburgh Steelers (American Football) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, KINGDOME, STRMGATE | doms9 | **PASS** |
| TBD vs. NFL RedZone (American Football) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| American Univ. vs. Towson (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Canisius vs. Western Illinois (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Dayton vs. NW Wildcats (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Marquette vs. Chicago State (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Nebraska vs. Butler (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Texas Longhorns vs. Ohio State Buckeyes (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Carolina Hurricanes vs. New York Rangers (NHL Hockey) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| AC Milan vs. Frosinone (Soccer) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, STRMGATE | doms9 | **PASS** |
| Apollon vs. Omonia 29th May (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Augsburg vs. Mainz (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Barcelona W vs. Athletic Bilbao W (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Bologna vs. Udinese (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Duisburg vs. Hansa Rostock (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Dun Streda vs. Komarno (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| FC Arges vs. FCSB (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Gent U23 vs. Francs Borains (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Gijon vs. Las Palmas (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Hull City vs. Brighton & Hove Albion (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Kagera Sugar vs. TRA United (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Liverpool vs. Manchester United (Soccer) | 2/2 | 2/2 | 0/1 | 2 | KINGDOME, STRMGATE | doms9 | **DEFICIT** |
| Lommel SK vs. Standard Liege (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Lorient vs. Rennes (Soccer) | 1/2 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Milan vs. Frosinone (Soccer) | 1/1 | 1/2 | 0/1 | 1 | KINGDOME | doms9 | **DEFICIT** |
| Málaga vs. Osasuna (Soccer) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Nordsjaelland vs. FC Copenhagen (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Olympiacos vs. Iraklis 1908 (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Osasuna vs. Malaga (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA, KINGDOME | doms9 | **DEFICIT** |
| Osasuna vs. Málaga CF (Soccer) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Panetolikos vs. Volos (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Paris vs. Angers SCO (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Racing Santander vs. Real Sociedad (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| RSC Anderlecht vs. Leuven (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Sarpsborg vs. Lillestrom (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Sassuolo vs. Genoa (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| SV Werder Bremen vs. Hamburger SV (Soccer) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Werder Bremen vs. Hamburger SV (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Eyupspor vs. Trabzonspor (TUR 1) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |

## Deficits

- **TBD vs. NFL RedZone** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **American Univ. vs. Towson** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Canisius vs. Western Illinois** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Dayton vs. NW Wildcats** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Marquette vs. Chicago State** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Nebraska vs. Butler** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Texas Longhorns vs. Ohio State Buckeyes** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Apollon vs. Omonia 29th May** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Augsburg vs. Mainz** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Barcelona W vs. Athletic Bilbao W** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Bologna vs. Udinese** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Duisburg vs. Hansa Rostock** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Dun Streda vs. Komarno** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **FC Arges vs. FCSB** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Gent U23 vs. Francs Borains** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Gijon vs. Las Palmas** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Hull City vs. Brighton & Hove Albion** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Kagera Sugar vs. TRA United** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Liverpool vs. Manchester United** — needs 1 more confirmed dedicated backup feed(s).
- **Lommel SK vs. Standard Liege** — needs 1 more confirmed dedicated backup feed(s).
- **Lorient vs. Rennes** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Milan vs. Frosinone** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Málaga vs. Osasuna** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Nordsjaelland vs. FC Copenhagen** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Olympiacos vs. Iraklis 1908** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Osasuna vs. Malaga** — needs 1 more confirmed dedicated backup feed(s).
- **Osasuna vs. Málaga CF** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Panetolikos vs. Volos** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Paris vs. Angers SCO** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Racing Santander vs. Real Sociedad** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **RSC Anderlecht vs. Leuven** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Sarpsborg vs. Lillestrom** — needs 1 more confirmed dedicated backup feed(s).
- **Sassuolo vs. Genoa** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **SV Werder Bremen vs. Hamburger SV** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Werder Bremen vs. Hamburger SV** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Eyupspor vs. Trabzonspor** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
