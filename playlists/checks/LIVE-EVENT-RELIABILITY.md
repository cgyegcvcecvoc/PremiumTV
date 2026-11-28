# Live-event reliability audit

- **Scrape snapshot:** 2026-11-28T00:53:04Z
- **Scrape run:** `20261128T004518Z-3125` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 1/45
- **Fixtures with a redundancy deficit:** 44

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Atlanta Hawks vs. Boston Celtics (Basketball) | 2/2 | 2/2 | 0/1 | 1 | SPRTSBITE | doms9, doms9-events | **DEFICIT** |
| Brooklyn Nets vs. Toronto Raptors (Basketball) | 3/3 | 2/2 | 1/1 | 1 | SPRTSBITE | doms9, doms9-events | **DEFICIT** |
| Miami Heat vs. New York Knicks (Basketball) | 3/3 | 2/2 | 1/1 | 1 | SPRTSBITE | doms9, doms9-events | **DEFICIT** |
| Milwaukee Bucks vs. Detroit Pistons (Basketball) | 3/3 | 2/2 | 1/1 | 1 | SPRTSBITE | doms9, doms9-events | **DEFICIT** |
| Philadelphia 76ers vs. Indiana Pacers (Basketball) | 3/3 | 2/2 | 1/1 | 1 | SPRTSBITE | doms9, doms9-events | **DEFICIT** |
| Brazil vs. USA (Basketball World Cup) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9, doms9-events | **DEFICIT** |
| Akron vs. Buffalo (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| East Tennessee vs. Charleston Southern (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Georgia Bulldogs vs. UCF (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Illinois vs. W. Kentucky (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Indiana vs. Bowling Green (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Iowa vs. Nebraska (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Memphis vs. Temple (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| New Mexico vs. Air Force (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| North Carolina vs. West Virginia (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Ohio vs. Toledo (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Pennsylvania vs. Towson (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| St Mary's vs. Texas (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| New Zealand vs. India (Cricket) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Brazil vs. USA (FIBA World Cup Qualification, Americas) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Atlanta Hawks vs. Boston Celtics (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Brooklyn Nets vs. Toronto Raptors (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Miami Heat vs. New York Knicks (NBA Basketball) | 2/2 | 2/2 | 0/1 | 2 | ISTRMEAST, STRMGATE | doms9, doms9-events | **DEFICIT** |
| Milwaukee Bucks vs. Detroit Pistons (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Philadelphia 76ers vs. Indiana Pacers (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Anaheim Ducks vs. Los Angeles Kings (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9, doms9-events | **DEFICIT** |
| Boston Bruins vs. Toronto Maple Leafs (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Chicago Blackhawks vs. New York Rangers (NHL Hockey) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, STRMGATE | doms9, doms9-events | **PASS** |
| Colorado Avalanche vs. Minnesota Wild (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9, doms9-events | **DEFICIT** |
| Columbus Blue Jackets vs. Detroit Red Wings (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Nashville Predators vs. Utah Mammoth (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| New Jersey Devils vs. Calgary Flames (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Philadelphia Flyers vs. Vancouver Canucks (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Pittsburgh Penguins vs. Buffalo Sabres (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| San Jose Sharks vs. Vegas Golden Knights (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9, doms9-events | **DEFICIT** |
| Seattle Kraken vs. Edmonton Oilers (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Tampa Bay Lightning vs. Ottawa Senators (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Washington Capitals vs. Florida Panthers (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Winnipeg Jets vs. New York Islanders (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Sp Luqueno vs. Olimpia Asuncion (Paraguay Copa de Primera) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Columbus Crew vs. Inter Miami CF (Soccer) | 1/1 | 1/2 | 0/1 | 1 | SPRTSBITE | doms9, doms9-events | **DEFICIT** |
| Dep Cali vs. Bucaramanga (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Fluminense vs. Cruzeiro (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9, doms9-events | **DEFICIT** |
| Independiente vs. Real Oruro (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| USA vs. El Salvador (Soccer) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |

## Deficits

- **Atlanta Hawks vs. Boston Celtics** — needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Brooklyn Nets vs. Toronto Raptors** — needs 1 more independent origin family/families.
- **Miami Heat vs. New York Knicks** — needs 1 more independent origin family/families.
- **Milwaukee Bucks vs. Detroit Pistons** — needs 1 more independent origin family/families.
- **Philadelphia 76ers vs. Indiana Pacers** — needs 1 more independent origin family/families.
- **Brazil vs. USA** — needs 1 more confirmed dedicated backup feed(s).
- **Akron vs. Buffalo** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **East Tennessee vs. Charleston Southern** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Georgia Bulldogs vs. UCF** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Illinois vs. W. Kentucky** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Indiana vs. Bowling Green** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Iowa vs. Nebraska** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Memphis vs. Temple** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Mexico vs. Air Force** — needs 1 more confirmed dedicated backup feed(s).
- **North Carolina vs. West Virginia** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ohio vs. Toledo** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Pennsylvania vs. Towson** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **St Mary's vs. Texas** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Zealand vs. India** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Brazil vs. USA** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Atlanta Hawks vs. Boston Celtics** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Brooklyn Nets vs. Toronto Raptors** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Miami Heat vs. New York Knicks** — needs 1 more confirmed dedicated backup feed(s).
- **Milwaukee Bucks vs. Detroit Pistons** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Philadelphia 76ers vs. Indiana Pacers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Anaheim Ducks vs. Los Angeles Kings** — needs 1 more confirmed dedicated backup feed(s).
- **Boston Bruins vs. Toronto Maple Leafs** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Colorado Avalanche vs. Minnesota Wild** — needs 1 more confirmed dedicated backup feed(s).
- **Columbus Blue Jackets vs. Detroit Red Wings** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Nashville Predators vs. Utah Mammoth** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Jersey Devils vs. Calgary Flames** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Philadelphia Flyers vs. Vancouver Canucks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Pittsburgh Penguins vs. Buffalo Sabres** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **San Jose Sharks vs. Vegas Golden Knights** — needs 1 more confirmed dedicated backup feed(s).
- **Seattle Kraken vs. Edmonton Oilers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Tampa Bay Lightning vs. Ottawa Senators** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Washington Capitals vs. Florida Panthers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Winnipeg Jets vs. New York Islanders** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Sp Luqueno vs. Olimpia Asuncion** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Columbus Crew vs. Inter Miami CF** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Dep Cali vs. Bucaramanga** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Fluminense vs. Cruzeiro** — needs 1 more confirmed dedicated backup feed(s).
- **Independiente vs. Real Oruro** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **USA vs. El Salvador** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
