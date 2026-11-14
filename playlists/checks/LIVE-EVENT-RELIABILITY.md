# Live-event reliability audit

- **Scrape snapshot:** 2026-11-14T01:47:45Z
- **Scrape run:** `20261114T014404Z-2939` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 8/61
- **Fixtures with a redundancy deficit:** 53

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Atlanta Hawks vs. Chicago Bulls (Basketball) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Cleveland Cavaliers vs. Miami Heat (Basketball) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Memphis Grizzlies vs. New Orleans Pelicans (Basketball) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Utah Jazz vs. Houston Rockets (Basketball) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Peterson vs. Hernandez (Boxing) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Alabama Crimson Tide vs. Seton Hall Pirates (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Arkansas Razorbacks vs. Central Arkansas Bears (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Arkansas vs. Central Arkansas (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Auburn Tigers vs. Arizona Wildcats (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Bucknell vs. Columbia (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Butler vs. Pittsburgh (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Colorado Buffaloes vs. Houston (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Duke Blue Devils vs. SIU Edwardsville Cougars (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Duke vs. SIU Edwardsville (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Florida Gators vs. Merrimack Warriors (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Florida vs. Merrimack (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Grand Canyon Antelopes vs. Gonzaga Bulldogs (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Illinois vs. Sam Houston St. (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Indiana Hoosiers vs. Samford Bulldogs (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Kentucky vs. Northern Arizona (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Kentucky Wildcats vs. Northern Arizona Lumberjacks (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Maryland Terrapins vs. Virginia Cavaliers (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Maryland vs. Virginia (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Michigan State Spartans vs. Northern Iowa Panthers (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Michigan State vs. Northern Iowa (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| NC State vs. Troy (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| North Carolina vs. Georgia Bulldogs (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Oklahoma vs. Fairleigh Dickinson (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Pittsburgh vs. Florida State (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Purdue vs. Ohio (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Tennessee Volunteers vs. Tennessee State Tigers (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Tennessee vs. Tennessee Tigers (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| UCF vs. Georgia Southern (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| UCLA Bruins vs. Illinois Fighting Illini (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| UCLA vs. Illinois (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| UConn Huskies vs. Ohio State Buckeyes (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| UConn vs. Ohio State (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Vanderbilt Commodores vs. Prairie View A&M Panthers (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Vanderbilt vs. Prairie View A&M (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Virginia Tech vs. Mount St Mary's (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Chicago Bulls vs. Atlanta Hawks (National Basketball Association) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Houston Rockets vs. Utah Jazz (National Basketball Association) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Indiana Pacers vs. New York Knicks (National Basketball Association) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Orlando Magic vs. Milwaukee Bucks (National Basketball Association) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Vancouver Canucks vs. New York Rangers (National Hockey League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Atlanta Hawks vs. Chicago Bulls (NBA Basketball) | 5/5 | 2/2 | 3/1 | 5 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Houston Rockets vs. Utah Jazz (NBA Basketball) | 4/4 | 2/2 | 2/1 | 4 | FAWA, MP66, STRMGATE | doms9 | **PASS** |
| Indiana Pacers vs. New York Knicks (NBA Basketball) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, STRMGATE | doms9 | **PASS** |
| Los Angeles Clippers vs. Oklahoma City Thunder (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Miami Heat vs. Cleveland Cavaliers (NBA Basketball) | 5/5 | 2/2 | 3/1 | 5 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| New Orleans Pelicans vs. Memphis Grizzlies (NBA Basketball) | 5/5 | 2/2 | 3/1 | 5 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Orlando Magic vs. Milwaukee Bucks (NBA Basketball) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, STRMGATE | doms9 | **PASS** |
| Vancouver Canucks vs. New York Rangers (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Vegas Golden Knights vs. Nashville Predators (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Bolivia vs. Peru (Soccer) | 3/3 | 2/2 | 1/1 | 3 | FAWA, STRMGATE | doms9 | **PASS** |
| Chile vs. Colombia (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Costa Rica vs. Ecuador (Soccer) | 3/3 | 2/2 | 1/1 | 3 | FAWA, STRMGATE | doms9 | **PASS** |
| Guatemala vs. Canada (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Montserrat vs. Nicaragua (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Saint Martin vs. El Salvador (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Uruguay vs. Argentina (Soccer) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |

## Deficits

- **Atlanta Hawks vs. Chicago Bulls** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Cleveland Cavaliers vs. Miami Heat** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Memphis Grizzlies vs. New Orleans Pelicans** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Utah Jazz vs. Houston Rockets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Peterson vs. Hernandez** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Alabama Crimson Tide vs. Seton Hall Pirates** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Arkansas Razorbacks vs. Central Arkansas Bears** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Arkansas vs. Central Arkansas** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Auburn Tigers vs. Arizona Wildcats** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Bucknell vs. Columbia** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Butler vs. Pittsburgh** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Colorado Buffaloes vs. Houston** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Duke Blue Devils vs. SIU Edwardsville Cougars** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Duke vs. SIU Edwardsville** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Florida Gators vs. Merrimack Warriors** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Florida vs. Merrimack** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Grand Canyon Antelopes vs. Gonzaga Bulldogs** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Illinois vs. Sam Houston St.** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Indiana Hoosiers vs. Samford Bulldogs** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Kentucky vs. Northern Arizona** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Kentucky Wildcats vs. Northern Arizona Lumberjacks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Maryland Terrapins vs. Virginia Cavaliers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Maryland vs. Virginia** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Michigan State Spartans vs. Northern Iowa Panthers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Michigan State vs. Northern Iowa** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **NC State vs. Troy** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **North Carolina vs. Georgia Bulldogs** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Oklahoma vs. Fairleigh Dickinson** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Pittsburgh vs. Florida State** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Purdue vs. Ohio** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Tennessee Volunteers vs. Tennessee State Tigers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Tennessee vs. Tennessee Tigers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **UCF vs. Georgia Southern** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **UCLA Bruins vs. Illinois Fighting Illini** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **UCLA vs. Illinois** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **UConn Huskies vs. Ohio State Buckeyes** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **UConn vs. Ohio State** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Vanderbilt Commodores vs. Prairie View A&M Panthers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Vanderbilt vs. Prairie View A&M** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Virginia Tech vs. Mount St Mary's** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Chicago Bulls vs. Atlanta Hawks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Houston Rockets vs. Utah Jazz** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Indiana Pacers vs. New York Knicks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Orlando Magic vs. Milwaukee Bucks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Vancouver Canucks vs. New York Rangers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Los Angeles Clippers vs. Oklahoma City Thunder** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Vancouver Canucks vs. New York Rangers** — needs 1 more confirmed dedicated backup feed(s).
- **Vegas Golden Knights vs. Nashville Predators** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Chile vs. Colombia** — needs 1 more confirmed dedicated backup feed(s).
- **Guatemala vs. Canada** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Montserrat vs. Nicaragua** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Saint Martin vs. El Salvador** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Uruguay vs. Argentina** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
