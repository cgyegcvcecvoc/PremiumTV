# Live-event reliability audit

- **Scrape snapshot:** 2026-11-15T07:57:47Z
- **Scrape run:** `20261115T075352Z-2962` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 0/41
- **Fixtures with a redundancy deficit:** 41

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Brisbane Bullets vs. Tasmania JackJumpers (Basketball NBL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Air Force vs. San Jose State (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Alabama Crimson Tide vs. Vanderbilt Commodores (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Arizona Wildcats vs. Utah Utes (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Baylor Bears vs. BYU Cougars (College Football) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Boise State vs. Oregon State (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Boston College Eagles vs. Notre Dame Fighting Irish (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Duke Blue Devils vs. Miami Hurricanes (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Hawaii vs. North Dakota State (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Michigan Wolverines vs. Oregon Ducks (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Missouri Tigers vs. Georgia Bulldogs (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Northwestern Wildcats vs. Ohio State Buckeyes (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Ole Miss Rebels vs. Oklahoma Sooners (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Oregon vs. Michigan (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| South Carolina Gamecocks vs. Arkansas Razorbacks (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Tennessee Volunteers vs. Texas A&M Aggies (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| UCF vs. Arizona State (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| USC Trojans vs. Indiana Hoosiers (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Wake Forest Demon Deacons vs. SMU Mustangs (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Australia vs. England (Cricket) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| New Zealand vs. India (Cricket) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Sydney Kings vs. New Zealand Breakers (National Basketball League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Brooklyn Nets vs. Memphis Grizzlies (NBA Basketball) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Chicago Bulls vs. Minnesota Timberwolves (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Dallas Mavericks vs. Cleveland Cavaliers (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Denver Nuggets vs. New Orleans Pelicans (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Detroit Pistons vs. Miami Heat (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Anaheim Ducks vs. New York Islanders (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Boston Bruins vs. Minnesota Wild (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Calgary Flames vs. Los Angeles Kings (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, MP66 | doms9 | **DEFICIT** |
| Columbus Blue Jackets vs. Philadelphia Flyers (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Dallas Stars vs. Buffalo Sabres (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Montreal Canadiens vs. Colorado Avalanche (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Pittsburgh Penguins vs. Ottawa Senators (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| St Louis Blues vs. Florida Panthers (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Tampa Bay Lightning vs. Detroit Red Wings (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Toronto Maple Leafs vs. Edmonton Oilers (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Utah Mammoth vs. San Jose Sharks (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Washington Capitals vs. New Jersey Devils (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| PFL Dubai: Vadim Nemkov vs. Sergei Bilostenniy (UFC / MMA) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| UFC 334 : Jared Gordon vs. Melquizael Costa (UFC Fight Night) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |

## Deficits

- **Brisbane Bullets vs. Tasmania JackJumpers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Air Force vs. San Jose State** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Alabama Crimson Tide vs. Vanderbilt Commodores** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Arizona Wildcats vs. Utah Utes** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Baylor Bears vs. BYU Cougars** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Boise State vs. Oregon State** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Boston College Eagles vs. Notre Dame Fighting Irish** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Duke Blue Devils vs. Miami Hurricanes** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Hawaii vs. North Dakota State** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Michigan Wolverines vs. Oregon Ducks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Missouri Tigers vs. Georgia Bulldogs** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Northwestern Wildcats vs. Ohio State Buckeyes** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ole Miss Rebels vs. Oklahoma Sooners** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Oregon vs. Michigan** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **South Carolina Gamecocks vs. Arkansas Razorbacks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Tennessee Volunteers vs. Texas A&M Aggies** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **UCF vs. Arizona State** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **USC Trojans vs. Indiana Hoosiers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Wake Forest Demon Deacons vs. SMU Mustangs** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Australia vs. England** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Zealand vs. India** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Sydney Kings vs. New Zealand Breakers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Brooklyn Nets vs. Memphis Grizzlies** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Chicago Bulls vs. Minnesota Timberwolves** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Dallas Mavericks vs. Cleveland Cavaliers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Denver Nuggets vs. New Orleans Pelicans** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Detroit Pistons vs. Miami Heat** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Anaheim Ducks vs. New York Islanders** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Boston Bruins vs. Minnesota Wild** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Calgary Flames vs. Los Angeles Kings** — needs 1 more confirmed dedicated backup feed(s).
- **Columbus Blue Jackets vs. Philadelphia Flyers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Dallas Stars vs. Buffalo Sabres** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Montreal Canadiens vs. Colorado Avalanche** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Pittsburgh Penguins vs. Ottawa Senators** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **St Louis Blues vs. Florida Panthers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Tampa Bay Lightning vs. Detroit Red Wings** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Toronto Maple Leafs vs. Edmonton Oilers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Utah Mammoth vs. San Jose Sharks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Washington Capitals vs. New Jersey Devils** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **PFL Dubai: Vadim Nemkov vs. Sergei Bilostenniy** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **UFC 334 : Jared Gordon vs. Melquizael Costa** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
