# Live-event reliability audit

- **Scrape snapshot:** 2026-11-27T23:02:10Z
- **Scrape run:** `20261127T225510Z-3046` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 3/38
- **Fixtures with a redundancy deficit:** 35

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Denver Broncos vs. Pittsburgh Steelers (American Football) | 2/2 | 2/2 | 0/1 | 2 | ISTRMEAST, STRMGATE | doms9, doms9-events | **DEFICIT** |
| Akron vs. Buffalo (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Boston College vs. Cincinnati (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Florida State vs. Florida (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Iowa vs. Nebraska (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Kansas vs. Villanova (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| La Salle vs. Bucknell (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Lafayette vs. Niagara (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Marquette vs. Texas A&M (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Maryland vs. Oregon (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Memphis vs. Temple (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Michigan vs. Kansas St (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Missouri vs. Arkansas-Pine (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| New Mexico vs. Air Force (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Ohio vs. Toledo (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Ole Miss vs. Mississippi St (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| San Jose St. vs. North Dakota State Bison (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| South Alabama vs. Appalachian St. (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| St Mary's vs. Texas (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| UTSA vs. Tulsa (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Villanova Wildcats vs. LSU Tigers (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Virginia Tech vs. Old Dominion (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Jamaica W vs. Costa Rica W (CONCACAF Championship Women) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| New Zealand vs. India (Cricket) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Anaheim Ducks vs. Los Angeles Kings (NHL Hockey) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, STRMGATE | doms9, doms9-events | **PASS** |
| Boston Bruins vs. Toronto Maple Leafs (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Chicago Blackhawks vs. New York Rangers (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9, doms9-events | **DEFICIT** |
| Colorado Avalanche vs. Minnesota Wild (NHL Hockey) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, STRMGATE | doms9, doms9-events | **PASS** |
| Dallas Stars vs. St. Louis Blues (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9, doms9-events | **DEFICIT** |
| Detroit Red Wings vs. Columbus Blue Jackets (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Florida Panthers vs. Washington Capitals (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Nashville Predators vs. Utah Mammoth (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| New Jersey Devils vs. Calgary Flames (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Ottawa Senators vs. Tampa Bay Lightning (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| San Jose Sharks vs. Vegas Golden Knights (NHL Hockey) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, STRMGATE | doms9, doms9-events | **PASS** |
| Vancouver Canucks vs. Philadelphia Flyers (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Jamaica vs. Costa Rica (Soccer) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| USA vs. El Salvador (Soccer) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |

## Deficits

- **Denver Broncos vs. Pittsburgh Steelers** — needs 1 more confirmed dedicated backup feed(s).
- **Akron vs. Buffalo** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Boston College vs. Cincinnati** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Florida State vs. Florida** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Iowa vs. Nebraska** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Kansas vs. Villanova** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **La Salle vs. Bucknell** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Lafayette vs. Niagara** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Marquette vs. Texas A&M** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Maryland vs. Oregon** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Memphis vs. Temple** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Michigan vs. Kansas St** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Missouri vs. Arkansas-Pine** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Mexico vs. Air Force** — needs 1 more confirmed dedicated backup feed(s).
- **Ohio vs. Toledo** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ole Miss vs. Mississippi St** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **San Jose St. vs. North Dakota State Bison** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **South Alabama vs. Appalachian St.** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **St Mary's vs. Texas** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **UTSA vs. Tulsa** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Villanova Wildcats vs. LSU Tigers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Virginia Tech vs. Old Dominion** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Jamaica W vs. Costa Rica W** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Zealand vs. India** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Boston Bruins vs. Toronto Maple Leafs** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Chicago Blackhawks vs. New York Rangers** — needs 1 more confirmed dedicated backup feed(s).
- **Dallas Stars vs. St. Louis Blues** — needs 1 more confirmed dedicated backup feed(s).
- **Detroit Red Wings vs. Columbus Blue Jackets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Florida Panthers vs. Washington Capitals** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Nashville Predators vs. Utah Mammoth** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Jersey Devils vs. Calgary Flames** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ottawa Senators vs. Tampa Bay Lightning** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Vancouver Canucks vs. Philadelphia Flyers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Jamaica vs. Costa Rica** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **USA vs. El Salvador** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
