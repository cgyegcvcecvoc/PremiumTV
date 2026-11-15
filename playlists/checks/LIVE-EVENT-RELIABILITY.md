# Live-event reliability audit

- **Scrape snapshot:** 2026-11-15T20:00:24Z
- **Scrape run:** `20261115T195644Z-2950` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 6/46
- **Fixtures with a redundancy deficit:** 40

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Atlanta Falcons vs. Kansas City Chiefs (American Football) | 3/3 | 2/2 | 1/1 | 3 | GSPORTS, ISTRMEAST, STRMGATE | doms9 | **PASS** |
| Buffalo Bills vs. New York Jets (American Football) | 2/2 | 2/2 | 0/1 | 2 | ISTRMEAST, STRMGATE | doms9 | **DEFICIT** |
| Carolina Panthers vs. New Orleans Saints (American Football) | 2/3 | 1/2 | 1/1 | 2 | ISTRMEAST, STRMGATE | doms9 | **DEFICIT** |
| Cleveland Browns vs. Houston Texans (American Football) | 3/3 | 2/2 | 1/1 | 3 | GSPORTS, ISTRMEAST, STRMGATE | doms9 | **PASS** |
| Green Bay Packers vs. Minnesota Vikings (American Football) | 3/3 | 2/2 | 1/1 | 3 | GSPORTS, ISTRMEAST, STRMGATE | doms9 | **PASS** |
| Indianapolis Colts vs. Miami Dolphins (American Football) | 3/3 | 2/2 | 1/1 | 3 | GSPORTS, ISTRMEAST, STRMGATE | doms9 | **PASS** |
| Jacksonville Jaguars vs. Tennessee Titans (American Football) | 3/3 | 2/2 | 1/1 | 3 | GSPORTS, ISTRMEAST, STRMGATE | doms9 | **PASS** |
| TBD vs. NFL RedZone (American Football) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Iowa Hawkeyes vs. Vanderbilt Commodores (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Iowa State vs. Niagara (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Maryland Terrapins vs. Columbia Lions (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Memphis Tigers vs. Louisville Cardinals (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Memphis vs. Louisville (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Michigan vs. William & Mary (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Nebraska Cornhuskers vs. Boise State Broncos (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Nebraska vs. Boise State (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Oklahoma Sooners vs. Ole Miss Rebels (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Oklahoma vs. Ole Miss (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| South Carolina Gamecocks vs. USC Trojans (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| South Dakota State Jackrabbits vs. Oklahoma State Cowgirls (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Texas Longhorns vs. Baylor Bears (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Philadelphia 76ers vs. Indiana Pacers (National Basketball Association) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Atlanta Falcons vs. Kansas City Chiefs (National Football League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Cleveland Browns vs. Houston Texans (National Football League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Green Bay Packers vs. Minnesota Vikings (National Football League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Indianapolis Colts vs. Miami Dolphins (National Football League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| New Orleans Saints vs. Carolina Panthers (National Football League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| New York Jets vs. Buffalo Bills (National Football League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Tennessee Titans vs. Jacksonville Jaguars (National Football League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Philadelphia 76ers vs. Indiana Pacers (NBA Basketball) | 5/5 | 2/2 | 3/1 | 5 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Always Ready vs. Independiente (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Belarus vs. Albania (Soccer) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Boca Juniors vs. Ind Valle del Cauca (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Buffalo Bills vs. New York Jets (Soccer) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Comerciantes Unidos vs. Sport Boys (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Czechia vs. Croatia (Soccer) | 2/2 | 2/2 | 0/1 | 2 | DAMITV, STRMGATE | doms9 | **DEFICIT** |
| Danubio vs. Liverpool M (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| England vs. Spain (Soccer) | 2/2 | 2/2 | 0/1 | 2 | DAMITV, STRMGATE | doms9 | **DEFICIT** |
| France vs. Türkiye (Soccer) | 2/2 | 2/2 | 0/1 | 2 | DAMITV, STRMGATE | doms9 | **DEFICIT** |
| Gotham W vs. Kansas City Current W (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Houston Texans vs. Cleveland Browns (Soccer) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Italy vs. Belgium (Soccer) | 2/2 | 2/2 | 0/1 | 2 | DAMITV, STRMGATE | doms9 | **DEFICIT** |
| Kansas City Chiefs vs. Atlanta Falcons (Soccer) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Miami Dolphins vs. Indianapolis Colts (Soccer) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Minnesota Vikings vs. Green Bay Packers (Soccer) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Canada vs. Sweden (World Championship Women) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |

## Deficits

- **Buffalo Bills vs. New York Jets** — needs 1 more confirmed dedicated backup feed(s).
- **Carolina Panthers vs. New Orleans Saints** — needs 1 more confirmed primary feed(s).
- **TBD vs. NFL RedZone** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Iowa Hawkeyes vs. Vanderbilt Commodores** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Iowa State vs. Niagara** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Maryland Terrapins vs. Columbia Lions** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Memphis Tigers vs. Louisville Cardinals** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Memphis vs. Louisville** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Michigan vs. William & Mary** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Nebraska Cornhuskers vs. Boise State Broncos** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Nebraska vs. Boise State** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Oklahoma Sooners vs. Ole Miss Rebels** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Oklahoma vs. Ole Miss** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **South Carolina Gamecocks vs. USC Trojans** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **South Dakota State Jackrabbits vs. Oklahoma State Cowgirls** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Texas Longhorns vs. Baylor Bears** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Philadelphia 76ers vs. Indiana Pacers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Atlanta Falcons vs. Kansas City Chiefs** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Cleveland Browns vs. Houston Texans** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Green Bay Packers vs. Minnesota Vikings** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Indianapolis Colts vs. Miami Dolphins** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Orleans Saints vs. Carolina Panthers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New York Jets vs. Buffalo Bills** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Tennessee Titans vs. Jacksonville Jaguars** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Always Ready vs. Independiente** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Belarus vs. Albania** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Boca Juniors vs. Ind Valle del Cauca** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Buffalo Bills vs. New York Jets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Comerciantes Unidos vs. Sport Boys** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Czechia vs. Croatia** — needs 1 more confirmed dedicated backup feed(s).
- **Danubio vs. Liverpool M** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **England vs. Spain** — needs 1 more confirmed dedicated backup feed(s).
- **France vs. Türkiye** — needs 1 more confirmed dedicated backup feed(s).
- **Gotham W vs. Kansas City Current W** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Houston Texans vs. Cleveland Browns** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Italy vs. Belgium** — needs 1 more confirmed dedicated backup feed(s).
- **Kansas City Chiefs vs. Atlanta Falcons** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Miami Dolphins vs. Indianapolis Colts** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Minnesota Vikings vs. Green Bay Packers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Canada vs. Sweden** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
