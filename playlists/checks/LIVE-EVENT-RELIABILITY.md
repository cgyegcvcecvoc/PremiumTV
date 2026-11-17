# Live-event reliability audit

- **Scrape snapshot:** 2026-11-17T01:14:44Z
- **Scrape run:** `20261117T011057Z-3164` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 7/43
- **Fixtures with a redundancy deficit:** 36

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Los Angeles Chargers vs. Baltimore Ravens (American Football) | 2/2 | 2/2 | 0/1 | 2 | GSPORTS, STRMGATE | doms9 | **DEFICIT** |
| Chicago Bulls vs. Cleveland Cavaliers (Basketball) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Golden State Warriors vs. New Orleans Pelicans (Basketball) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Houston Rockets vs. Miami Heat (Basketball) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Memphis Grizzlies vs. Washington Wizards (Basketball) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Orlando Magic vs. Boston Celtics (Basketball) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Philadelphia 76ers vs. Brooklyn Nets (Basketball) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Portland Trail Blazers vs. Minnesota Timberwolves (Basketball) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Clemson vs. Citadel (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Georgia Bulldogs vs. Jacksonville (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Kent St. vs. Eastern Kentucky (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Kentucky vs. Grambling St. (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Maryland vs. Alcorn St. (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Ohio State vs. Prairie View A&M (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Pennsylvania vs. Desales Bulldogs (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Rutgers Scarlet Knights vs. Albany Great Danes (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Tulsa vs. W. Kentucky (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Virginia Tech vs. Richmond (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Boston Celtics vs. Orlando Magic (National Basketball Association) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Brooklyn Nets vs. Philadelphia 76ers (National Basketball Association) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Cleveland Cavaliers vs. Chicago Bulls (National Basketball Association) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Miami Heat vs. Houston Rockets (National Basketball Association) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Minnesota Timberwolves vs. Portland Trail Blazers (National Basketball Association) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| New Orleans Pelicans vs. Golden State Warriors (National Basketball Association) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Washington Wizards vs. Memphis Grizzlies (National Basketball Association) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Baltimore Ravens vs. Los Angeles Chargers (National Football League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| New York Rangers vs. Montreal Canadiens (National Hockey League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Boston Celtics vs. Orlando Magic (NBA Basketball) | 6/6 | 2/2 | 4/1 | 6 | FAWA, GSPORTS, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Brooklyn Nets vs. Philadelphia 76ers (NBA Basketball) | 6/6 | 2/2 | 4/1 | 6 | FAWA, GSPORTS, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Cleveland Cavaliers vs. Chicago Bulls (NBA Basketball) | 6/6 | 2/2 | 4/1 | 6 | FAWA, GSPORTS, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Denver Nuggets vs. Phoenix Suns (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Miami Heat vs. Houston Rockets (NBA Basketball) | 6/6 | 2/2 | 4/1 | 6 | FAWA, GSPORTS, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Minnesota Timberwolves vs. Portland Trail Blazers (NBA Basketball) | 4/4 | 2/2 | 2/1 | 4 | FAWA, GSPORTS, MP66, STRMGATE | doms9 | **PASS** |
| New Orleans Pelicans vs. Golden State Warriors (NBA Basketball) | 5/5 | 2/2 | 3/1 | 5 | FAWA, GSPORTS, MP66, STRMGATE | doms9 | **PASS** |
| Washington Wizards vs. Memphis Grizzlies (NBA Basketball) | 6/6 | 2/2 | 4/1 | 6 | FAWA, GSPORTS, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Montréal Canadiens vs. New York Rangers (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | ISTRMEAST, MP66 | doms9 | **DEFICIT** |
| New York Rangers vs. Montreal Canadiens (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Utah Mammoth vs. Vancouver Canucks (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Canada vs. Guatemala (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Los Angeles Chargers vs. Baltimore Ravens (Soccer) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Martinique vs. Aruba (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Trinidad and Tobago vs. Antigua and Barbuda (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Wanderers vs. Juventud (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **Los Angeles Chargers vs. Baltimore Ravens** — needs 1 more confirmed dedicated backup feed(s).
- **Chicago Bulls vs. Cleveland Cavaliers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Golden State Warriors vs. New Orleans Pelicans** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Houston Rockets vs. Miami Heat** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Memphis Grizzlies vs. Washington Wizards** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Orlando Magic vs. Boston Celtics** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Philadelphia 76ers vs. Brooklyn Nets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Portland Trail Blazers vs. Minnesota Timberwolves** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Clemson vs. Citadel** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Georgia Bulldogs vs. Jacksonville** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Kent St. vs. Eastern Kentucky** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Kentucky vs. Grambling St.** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Maryland vs. Alcorn St.** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ohio State vs. Prairie View A&M** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Pennsylvania vs. Desales Bulldogs** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Rutgers Scarlet Knights vs. Albany Great Danes** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Tulsa vs. W. Kentucky** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Virginia Tech vs. Richmond** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Boston Celtics vs. Orlando Magic** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Brooklyn Nets vs. Philadelphia 76ers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Cleveland Cavaliers vs. Chicago Bulls** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Miami Heat vs. Houston Rockets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Minnesota Timberwolves vs. Portland Trail Blazers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Orleans Pelicans vs. Golden State Warriors** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Washington Wizards vs. Memphis Grizzlies** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Baltimore Ravens vs. Los Angeles Chargers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New York Rangers vs. Montreal Canadiens** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Denver Nuggets vs. Phoenix Suns** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Montréal Canadiens vs. New York Rangers** — needs 1 more confirmed dedicated backup feed(s).
- **New York Rangers vs. Montreal Canadiens** — needs 1 more confirmed dedicated backup feed(s).
- **Utah Mammoth vs. Vancouver Canucks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Canada vs. Guatemala** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Los Angeles Chargers vs. Baltimore Ravens** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Martinique vs. Aruba** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Trinidad and Tobago vs. Antigua and Barbuda** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Wanderers vs. Juventud** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
