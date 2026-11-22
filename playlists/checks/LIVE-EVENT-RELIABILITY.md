# Live-event reliability audit

- **Scrape snapshot:** 2026-11-22T20:54:53Z
- **Scrape run:** `20261122T204949Z-2992` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 8/49
- **Fixtures with a redundancy deficit:** 41

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Arizona Cardinals vs. Kansas City Chiefs (American Football) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, KINGDOME, STRMGATE | doms9 | **PASS** |
| Baltimore Ravens vs. Carolina Panthers (American Football) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, KINGDOME, STRMGATE | doms9 | **PASS** |
| Buffalo Bills vs. Miami Dolphins (American Football) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, KINGDOME, STRMGATE | doms9 | **PASS** |
| Chicago Bears vs. New Orleans Saints (American Football) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, KINGDOME, STRMGATE | doms9 | **PASS** |
| Dallas Cowboys vs. Tennessee Titans (American Football) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, KINGDOME, STRMGATE | doms9 | **PASS** |
| Denver Broncos vs. Las Vegas Raiders (American Football) | 1/1 | 1/2 | 0/1 | 1 | KINGDOME | doms9 | **DEFICIT** |
| Detroit Lions vs. Tampa Bay Buccaneers (American Football) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, KINGDOME, STRMGATE | doms9 | **PASS** |
| Los Angeles Chargers vs. New York Jets (American Football) | 1/1 | 1/2 | 0/1 | 1 | KINGDOME | doms9 | **DEFICIT** |
| New York Giants vs. Jacksonville Jaguars (American Football) | 1/1 | 1/2 | 0/1 | 1 | KINGDOME | doms9 | **DEFICIT** |
| Philadelphia Eagles vs. Pittsburgh Steelers (American Football) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, KINGDOME, STRMGATE | doms9 | **PASS** |
| San Francisco 49ers vs. Minnesota Vikings (American Football) | 1/1 | 1/2 | 0/1 | 1 | KINGDOME | doms9 | **DEFICIT** |
| Cincinnati vs. UMass Lowell (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Creighton Bluejays vs. Nebraska Cornhuskers (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| G. Washington vs. W. Kentucky (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Memphis vs. Evansville (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Texas vs. USI (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Youngstown St. vs. William & Mary (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Atlanta Hawks vs. Detroit Pistons (NBA Basketball) | 5/5 | 2/2 | 3/1 | 5 | FAWA, KINGDOME, MP66, STRMGATE | doms9 | **PASS** |
| Miami Heat vs. Oklahoma City Thunder (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | KINGDOME | doms9 | **DEFICIT** |
| Utah Jazz vs. Dallas Mavericks (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | KINGDOME | doms9 | **DEFICIT** |
| Washington Wizards vs. Orlando Magic (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | KINGDOME | doms9 | **DEFICIT** |
| Carolina Hurricanes vs. New York Rangers (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Atalanta vs. Inter (Soccer) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Atalanta vs. Inter Milan (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Atalanta vs. Internazionale (Soccer) | 2/2 | 2/2 | 0/1 | 2 | KINGDOME, STRMGATE | doms9 | **DEFICIT** |
| Athletico-PR vs. Remo (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Atlético Madrid vs. Getafe (Soccer) | 2/2 | 2/2 | 0/1 | 2 | ISTRMEAST, STRMGATE | doms9 | **DEFICIT** |
| Bologna vs. Udinese (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Burgos CF vs. Albacete (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Getafe vs. Atletico Madrid (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Gijon vs. Las Palmas (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Hull City vs. Brighton & Hove Albion (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| KFUM Oslo vs. Brann (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Lazio W vs. Juventus W (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Liverpool vs. Manchester United (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Lorient vs. Rennes (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Marseille vs. Le Mans (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Milan vs. Frosinone (Soccer) | 1/1 | 1/2 | 0/1 | 1 | KINGDOME | doms9 | **DEFICIT** |
| Olympique Marseille vs. Le Mans (Soccer) | 1/1 | 1/2 | 0/1 | 1 | KINGDOME | doms9 | **DEFICIT** |
| Orense vs. Mushuc Runa (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Osasuna vs. Malaga (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Paris vs. Angers SCO (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Racing Santander vs. Real Sociedad (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Real Potosi vs. Bolivar (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Rosario Central vs. Gimnasia Mendoza (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Sassuolo vs. Genoa (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Sport Huancayo vs. U de Deportes (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Sporting Cristal vs. Cienciano (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Torreense vs. Benfica (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **Denver Broncos vs. Las Vegas Raiders** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Los Angeles Chargers vs. New York Jets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New York Giants vs. Jacksonville Jaguars** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **San Francisco 49ers vs. Minnesota Vikings** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Cincinnati vs. UMass Lowell** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Creighton Bluejays vs. Nebraska Cornhuskers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **G. Washington vs. W. Kentucky** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Memphis vs. Evansville** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Texas vs. USI** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Youngstown St. vs. William & Mary** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Miami Heat vs. Oklahoma City Thunder** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Utah Jazz vs. Dallas Mavericks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Washington Wizards vs. Orlando Magic** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Carolina Hurricanes vs. New York Rangers** — needs 1 more confirmed dedicated backup feed(s).
- **Atalanta vs. Inter** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Atalanta vs. Inter Milan** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Atalanta vs. Internazionale** — needs 1 more confirmed dedicated backup feed(s).
- **Athletico-PR vs. Remo** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Atlético Madrid vs. Getafe** — needs 1 more confirmed dedicated backup feed(s).
- **Bologna vs. Udinese** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Burgos CF vs. Albacete** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Getafe vs. Atletico Madrid** — needs 1 more confirmed dedicated backup feed(s).
- **Gijon vs. Las Palmas** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Hull City vs. Brighton & Hove Albion** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **KFUM Oslo vs. Brann** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Lazio W vs. Juventus W** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Liverpool vs. Manchester United** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Lorient vs. Rennes** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Marseille vs. Le Mans** — needs 1 more confirmed dedicated backup feed(s).
- **Milan vs. Frosinone** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Olympique Marseille vs. Le Mans** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Orense vs. Mushuc Runa** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Osasuna vs. Malaga** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Paris vs. Angers SCO** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Racing Santander vs. Real Sociedad** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Real Potosi vs. Bolivar** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Rosario Central vs. Gimnasia Mendoza** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Sassuolo vs. Genoa** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Sport Huancayo vs. U de Deportes** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Sporting Cristal vs. Cienciano** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Torreense vs. Benfica** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
