# Live-event reliability audit

- **Scrape snapshot:** 2026-11-17T04:14:13Z
- **Scrape run:** `20261117T041041Z-3187` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 3/26
- **Fixtures with a redundancy deficit:** 23

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Baltimore Ravens vs. Los Angeles Chargers (American Football) | 4/4 | 2/2 | 2/1 | 4 | GSPORTS, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Phoenix Suns vs. Denver Nuggets (Basketball) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| St Mary's vs. Portland State (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| UC San Diego vs. TX Southern (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| UCLA Bruins vs. Long Beach State Beach (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| UCLA vs. Long Beach (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Afghanistan vs. Zimbabwe (Cricket) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Pakistan vs. Sri Lanka (Cricket) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| South Africa vs. Bangladesh (Cricket) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Denver Nuggets vs. Phoenix Suns (National Basketball Association) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Baltimore Ravens vs. Los Angeles Chargers (National Football League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Utah Mammoth vs. Vancouver Canucks (National Hockey League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Chicago Bulls vs. Cleveland Cavaliers (NBA Basketball) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Denver Nuggets vs. Phoenix Suns (NBA Basketball) | 6/6 | 2/2 | 4/1 | 6 | FAWA, GSPORTS, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Golden State Warriors vs. New Orleans Pelicans (NBA Basketball) | 1/2 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Houston Rockets vs. Miami Heat (NBA Basketball) | 1/2 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Memphis Grizzlies vs. Washington Wizards (NBA Basketball) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Orlando Magic vs. Boston Celtics (NBA Basketball) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Philadelphia 76ers vs. Brooklyn Nets (NBA Basketball) | 1/2 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Portland Trail Blazers vs. Minnesota Timberwolves (NBA Basketball) | 1/2 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| New York Rangers vs. Montreal Canadiens (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Utah Mammoth vs. Vancouver Canucks (NHL Hockey) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, STRMGATE | doms9 | **PASS** |
| Canada vs. Guatemala (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Los Angeles Chargers vs. Baltimore Ravens (Soccer) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Martinique vs. Aruba (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Trinidad and Tobago vs. Antigua and Barbuda (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **Phoenix Suns vs. Denver Nuggets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **St Mary's vs. Portland State** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **UC San Diego vs. TX Southern** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **UCLA Bruins vs. Long Beach State Beach** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **UCLA vs. Long Beach** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Afghanistan vs. Zimbabwe** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Pakistan vs. Sri Lanka** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **South Africa vs. Bangladesh** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Denver Nuggets vs. Phoenix Suns** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Baltimore Ravens vs. Los Angeles Chargers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Utah Mammoth vs. Vancouver Canucks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Chicago Bulls vs. Cleveland Cavaliers** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Golden State Warriors vs. New Orleans Pelicans** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Houston Rockets vs. Miami Heat** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Memphis Grizzlies vs. Washington Wizards** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Orlando Magic vs. Boston Celtics** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Philadelphia 76ers vs. Brooklyn Nets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Portland Trail Blazers vs. Minnesota Timberwolves** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New York Rangers vs. Montreal Canadiens** — needs 1 more confirmed dedicated backup feed(s).
- **Canada vs. Guatemala** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Los Angeles Chargers vs. Baltimore Ravens** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Martinique vs. Aruba** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Trinidad and Tobago vs. Antigua and Barbuda** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
