# Live-event reliability audit

- **Scrape snapshot:** 2026-11-16T23:33:30Z
- **Scrape run:** `20261116T232957Z-2986` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 0/16
- **Fixtures with a redundancy deficit:** 16

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Los Angeles Chargers vs. Baltimore Ravens (American Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Texas A&M Aggies vs. Lamar Cardinals (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Chicago Bulls vs. Cleveland Cavaliers (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Golden State Warriors vs. New Orleans Pelicans (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Houston Rockets vs. Miami Heat (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Memphis Grizzlies vs. Washington Wizards (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Orlando Magic vs. Boston Celtics (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Philadelphia 76ers vs. Brooklyn Nets (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Phoenix Suns vs. Denver Nuggets (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Portland Trail Blazers vs. Minnesota Timberwolves (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| New York Rangers vs. Montreal Canadiens (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Utah Mammoth vs. Vancouver Canucks (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Canada vs. Guatemala (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Martinique vs. Aruba (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Trinidad and Tobago vs. Antigua and Barbuda (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Wanderers vs. Juventud (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **Los Angeles Chargers vs. Baltimore Ravens** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Texas A&M Aggies vs. Lamar Cardinals** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Chicago Bulls vs. Cleveland Cavaliers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Golden State Warriors vs. New Orleans Pelicans** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Houston Rockets vs. Miami Heat** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Memphis Grizzlies vs. Washington Wizards** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Orlando Magic vs. Boston Celtics** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Philadelphia 76ers vs. Brooklyn Nets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Phoenix Suns vs. Denver Nuggets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Portland Trail Blazers vs. Minnesota Timberwolves** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New York Rangers vs. Montreal Canadiens** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Utah Mammoth vs. Vancouver Canucks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Canada vs. Guatemala** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Martinique vs. Aruba** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Trinidad and Tobago vs. Antigua and Barbuda** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Wanderers vs. Juventud** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
