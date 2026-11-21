# Live-event reliability audit

- **Scrape snapshot:** 2026-11-21T02:52:38Z
- **Scrape run:** `20261121T024900Z-3085` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 7/36
- **Fixtures with a redundancy deficit:** 29

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Amari Jones vs. DeAundre Pettus (Boxing) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| BKFC Fight Night: Richardson vs. Oxendine (Boxing) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Air Force vs. UTEP (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| Arkansas vs. Mississippi Valley (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Bowling Green Falcons vs. Toledo Rockets (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Clemson Tigers vs. Duke Blue Devils (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Connecticut Huskies vs. Seton Hall Pirates (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Duke vs. Clemson (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| Georgia Tech vs. Georgia Bulldogs (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Illinois vs. Eastern Illinois (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Indiana vs. Kentucky (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Michigan State vs. Oregon (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| Missouri vs. Le Moyne (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| New Mexico Lobos vs. Wyoming Cowboys (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| North Carolina vs. Marshall (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Oregon Ducks vs. Michigan State Spartans (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| South. Methodist vs. South Alabama (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Toledo vs. Bowling Green (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| UCF vs. Iowa State (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| UTEP Miners vs. Air Force Falcons (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Vanderbilt vs. UCF (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Wyoming vs. New Mexico (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| New Zealand vs. India (Cricket) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Brooklyn Nets vs. Orlando Magic (NBA Basketball) | 6/6 | 2/2 | 4/1 | 6 | FAWA, GSPORTS, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Charlotte Hornets vs. Atlanta Hawks (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Chicago Bulls vs. Washington Wizards (NBA Basketball) | 6/6 | 2/2 | 4/1 | 6 | FAWA, GSPORTS, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Cleveland Cavaliers vs. Indiana Pacers (NBA Basketball) | 5/5 | 2/2 | 3/1 | 5 | FAWA, GSPORTS, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Denver Nuggets vs. Houston Rockets (NBA Basketball) | 2/2 | 2/2 | 0/1 | 2 | FAWA, GSPORTS | doms9 | **DEFICIT** |
| Detroit Pistons vs. Toronto Raptors (NBA Basketball) | 6/6 | 2/2 | 4/1 | 6 | FAWA, GSPORTS, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Los Angeles Lakers vs. Sacramento Kings (NBA Basketball) | 3/3 | 2/2 | 1/1 | 3 | FAWA, GSPORTS, STRMGATE | doms9 | **PASS** |
| Oklahoma City Thunder vs. New Orleans Pelicans (NBA Basketball) | 6/6 | 2/2 | 4/1 | 6 | FAWA, GSPORTS, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Utah Jazz vs. Phoenix Suns (NBA Basketball) | 5/5 | 2/2 | 3/1 | 5 | FAWA, GSPORTS, MP66, STRMGATE | doms9 | **PASS** |
| Bucaramanga vs. America De Cali (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Palestino vs. Union La Calera (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Puebla vs. Atl San Luis (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Velez Sarsfield vs. Belgrano (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **Amari Jones vs. DeAundre Pettus** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **BKFC Fight Night: Richardson vs. Oxendine** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Air Force vs. UTEP** — needs 1 more confirmed dedicated backup feed(s).
- **Arkansas vs. Mississippi Valley** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Bowling Green Falcons vs. Toledo Rockets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Clemson Tigers vs. Duke Blue Devils** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Connecticut Huskies vs. Seton Hall Pirates** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Duke vs. Clemson** — needs 1 more confirmed dedicated backup feed(s).
- **Georgia Tech vs. Georgia Bulldogs** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Illinois vs. Eastern Illinois** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Indiana vs. Kentucky** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Michigan State vs. Oregon** — needs 1 more confirmed dedicated backup feed(s).
- **Missouri vs. Le Moyne** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Mexico Lobos vs. Wyoming Cowboys** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **North Carolina vs. Marshall** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Oregon Ducks vs. Michigan State Spartans** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **South. Methodist vs. South Alabama** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Toledo vs. Bowling Green** — needs 1 more confirmed dedicated backup feed(s).
- **UCF vs. Iowa State** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **UTEP Miners vs. Air Force Falcons** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Vanderbilt vs. UCF** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Wyoming vs. New Mexico** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Zealand vs. India** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Charlotte Hornets vs. Atlanta Hawks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Denver Nuggets vs. Houston Rockets** — needs 1 more confirmed dedicated backup feed(s).
- **Bucaramanga vs. America De Cali** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Palestino vs. Union La Calera** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Puebla vs. Atl San Luis** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Velez Sarsfield vs. Belgrano** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
