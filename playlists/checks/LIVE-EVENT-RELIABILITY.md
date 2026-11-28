# Live-event reliability audit

- **Scrape snapshot:** 2026-11-28T03:38:46Z
- **Scrape run:** `20261128T033109Z-3222` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 8/40
- **Fixtures with a redundancy deficit:** 32

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Denver Nuggets vs. Utah Jazz (Basketball) | 1/1 | 1/2 | 0/1 | 1 | SPRTSBITE | doms9, doms9-events | **DEFICIT** |
| Los Angeles Lakers vs. San Antonio Spurs (Basketball) | 2/2 | 2/2 | 0/1 | 1 | SPRTSBITE | doms9, doms9-events | **DEFICIT** |
| Memphis Grizzlies vs. Minnesota Timberwolves (Basketball) | 2/2 | 2/2 | 0/1 | 1 | SPRTSBITE | doms9, doms9-events | **DEFICIT** |
| New Orleans Pelicans vs. LA Clippers (Basketball) | 1/1 | 1/2 | 0/1 | 1 | SPRTSBITE | doms9, doms9-events | **DEFICIT** |
| Kentucky vs. Wichita State (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Miami vs. Alabama (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| New Mexico vs. Air Force (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| San Jose State vs. North Dakota State (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Tennessee vs. Louisville (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Texas A&M vs. Texas (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Utah vs. West Virginia (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Wisconsin vs. Minnesota (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| USA W vs. El Salvador W (CONCACAF Championship Women) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| New Zealand vs. India (Cricket) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Atlanta Hawks vs. Boston Celtics (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Brooklyn Nets vs. Toronto Raptors (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Los Angeles Clippers vs. New Orleans Pelicans (NBA Basketball) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9, doms9-events | **DEFICIT** |
| Miami Heat vs. New York Knicks (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Milwaukee Bucks vs. Detroit Pistons (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Minnesota Timberwolves vs. Memphis Grizzlies (NBA Basketball) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, STRMGATE | doms9, doms9-events | **PASS** |
| New Orleans Pelicans vs. LA Clippers (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Philadelphia 76ers vs. Indiana Pacers (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9, doms9-events | **DEFICIT** |
| Phoenix Suns vs. Dallas Mavericks (NBA Basketball) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, STRMGATE | doms9, doms9-events | **PASS** |
| Portland Trail Blazers vs. Golden State Warriors (NBA Basketball) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, STRMGATE | doms9, doms9-events | **PASS** |
| San Antonio Spurs vs. Los Angeles Lakers (NBA Basketball) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, STRMGATE | doms9, doms9-events | **PASS** |
| Utah Jazz vs. Denver Nuggets (NBA Basketball) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, STRMGATE | doms9, doms9-events | **PASS** |
| Anaheim Ducks vs. Los Angeles Kings (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Buffalo Sabres vs. Pittsburgh Penguins (NHL Hockey) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, STRMGATE | doms9, doms9-events | **PASS** |
| Chicago Blackhawks vs. New York Rangers (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Columbus Blue Jackets vs. Detroit Red Wings (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Edmonton Oilers vs. Seattle Kraken (NHL Hockey) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, STRMGATE | doms9, doms9-events | **PASS** |
| Minnesota Wild vs. Colorado Avalanche (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| New York Islanders vs. Winnipeg Jets (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9, doms9-events | **DEFICIT** |
| Philadelphia Flyers vs. Vancouver Canucks (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| San Jose Sharks vs. Vegas Golden Knights (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Tampa Bay Lightning vs. Ottawa Senators (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Washington Capitals vs. Florida Panthers (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Sp Luqueno vs. Olimpia Asuncion (Paraguay Copa de Primera) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Dep Cali vs. Bucaramanga (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Real Salt Lake vs. Vancouver Whitecaps (Soccer) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, SPRTSBITE | doms9, doms9-events | **PASS** |

## Deficits

- **Denver Nuggets vs. Utah Jazz** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Los Angeles Lakers vs. San Antonio Spurs** — needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Memphis Grizzlies vs. Minnesota Timberwolves** — needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Orleans Pelicans vs. LA Clippers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Kentucky vs. Wichita State** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Miami vs. Alabama** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Mexico vs. Air Force** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **San Jose State vs. North Dakota State** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Tennessee vs. Louisville** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Texas A&M vs. Texas** — needs 1 more confirmed dedicated backup feed(s).
- **Utah vs. West Virginia** — needs 1 more confirmed dedicated backup feed(s).
- **Wisconsin vs. Minnesota** — needs 1 more confirmed dedicated backup feed(s).
- **USA W vs. El Salvador W** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Zealand vs. India** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Atlanta Hawks vs. Boston Celtics** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Brooklyn Nets vs. Toronto Raptors** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Los Angeles Clippers vs. New Orleans Pelicans** — needs 1 more confirmed dedicated backup feed(s).
- **Miami Heat vs. New York Knicks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Milwaukee Bucks vs. Detroit Pistons** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Orleans Pelicans vs. LA Clippers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Philadelphia 76ers vs. Indiana Pacers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Anaheim Ducks vs. Los Angeles Kings** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Chicago Blackhawks vs. New York Rangers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Columbus Blue Jackets vs. Detroit Red Wings** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Minnesota Wild vs. Colorado Avalanche** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New York Islanders vs. Winnipeg Jets** — needs 1 more confirmed dedicated backup feed(s).
- **Philadelphia Flyers vs. Vancouver Canucks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **San Jose Sharks vs. Vegas Golden Knights** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Tampa Bay Lightning vs. Ottawa Senators** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Washington Capitals vs. Florida Panthers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Sp Luqueno vs. Olimpia Asuncion** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Dep Cali vs. Bucaramanga** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
