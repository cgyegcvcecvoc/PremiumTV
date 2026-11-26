# Live-event reliability audit

- **Scrape snapshot:** 2026-11-26T01:21:56Z
- **Scrape run:** `20261126T011416Z-3107` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 17/43
- **Fixtures with a redundancy deficit:** 26

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Green Bay Packers vs. Los Angeles Rams (American Football) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Chicago Bulls vs. Charlotte Hornets (Basketball) | 2/2 | 2/2 | 0/1 | 1 | SPRTSBITE | doms9 | **DEFICIT** |
| Cleveland Cavaliers vs. New York Knicks (Basketball) | 3/3 | 2/2 | 1/1 | 1 | SPRTSBITE | doms9 | **DEFICIT** |
| Miami Heat vs. Philadelphia 76ers (Basketball) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Minnesota Timberwolves vs. Oklahoma City Thunder (Basketball) | 2/2 | 2/2 | 0/1 | 1 | SPRTSBITE | doms9 | **DEFICIT** |
| George Mason vs. Longwood (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| NC State vs. Norfolk St. (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Penn State vs. Memphis (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Pepperdine vs. CS Bakersfield (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| SIU Edwardsville vs. Northern Illinois (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Texas Longhorns vs. Southeastern Louisiana Lions (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| UConn vs. Duke (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Utah State vs. South. Methodist (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Wisconsin vs. Northeastern (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Vancouver Canucks vs. Detroit Red Wings (Hockey) | 2/2 | 2/2 | 0/1 | 1 | SPRTSBITE | doms9 | **DEFICIT** |
| Winnipeg Jets vs. Boston Bruins (Hockey) | 1/1 | 1/2 | 0/1 | 1 | SPRTSBITE | doms9 | **DEFICIT** |
| Charlotte Hornets vs. Chicago Bulls (NBA Basketball) | 5/5 | 2/2 | 3/1 | 5 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| LA Clippers vs. Memphis Grizzlies (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Memphis Grizzlies vs. Los Angeles Clippers (NBA Basketball) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, MP66 | doms9 | **PASS** |
| Miami Heat vs. Philadelphia 76ers (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Milwaukee Bucks vs. Brooklyn Nets (NBA Basketball) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| New York Knicks vs. Cleveland Cavaliers (NBA Basketball) | 5/5 | 2/2 | 3/1 | 5 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Oklahoma City Thunder vs. Minnesota Timberwolves (NBA Basketball) | 5/5 | 2/2 | 3/1 | 5 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Phoenix Suns vs. Houston Rockets (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Anaheim Ducks vs. San Jose Sharks (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Boston Bruins vs. Winnipeg Jets (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Buffalo Sabres vs. New York Rangers (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Calgary Flames vs. Pittsburgh Penguins (NHL Hockey) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Carolina Hurricanes vs. Tampa Bay Lightning (NHL Hockey) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, STRMGATE | doms9 | **PASS** |
| Colorado Avalanche vs. Montreal Canadiens (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Columbus Blue Jackets vs. New Jersey Devils (NHL Hockey) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Dallas Stars vs. Nashville Predators (NHL Hockey) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, STRMGATE | doms9 | **PASS** |
| Detroit Red Wings vs. Vancouver Canucks (NHL Hockey) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, STRMGATE | doms9 | **PASS** |
| Florida Panthers vs. Ottawa Senators (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Minnesota Wild vs. Utah Mammoth (NHL Hockey) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, STRMGATE | doms9 | **PASS** |
| New York Islanders vs. St Louis Blues (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Seattle Kraken vs. Chicago Blackhawks (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Washington Capitals vs. Philadelphia Flyers (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Atl Nacional vs. Ind Medellin (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Atletico-MG vs. Corinthians (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Barcelona SC vs. Ind del Valle (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Boca Juniors vs. Ind Rivadavia (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Monterrey vs. Club America (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **Chicago Bulls vs. Charlotte Hornets** — needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Cleveland Cavaliers vs. New York Knicks** — needs 1 more independent origin family/families.
- **Miami Heat vs. Philadelphia 76ers** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Minnesota Timberwolves vs. Oklahoma City Thunder** — needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **George Mason vs. Longwood** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **NC State vs. Norfolk St.** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Penn State vs. Memphis** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Pepperdine vs. CS Bakersfield** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **SIU Edwardsville vs. Northern Illinois** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Texas Longhorns vs. Southeastern Louisiana Lions** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **UConn vs. Duke** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Utah State vs. South. Methodist** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Wisconsin vs. Northeastern** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Vancouver Canucks vs. Detroit Red Wings** — needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Winnipeg Jets vs. Boston Bruins** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **LA Clippers vs. Memphis Grizzlies** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Miami Heat vs. Philadelphia 76ers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Phoenix Suns vs. Houston Rockets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Anaheim Ducks vs. San Jose Sharks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Colorado Avalanche vs. Montreal Canadiens** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Seattle Kraken vs. Chicago Blackhawks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Atl Nacional vs. Ind Medellin** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Atletico-MG vs. Corinthians** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Barcelona SC vs. Ind del Valle** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Boca Juniors vs. Ind Rivadavia** — needs 1 more confirmed dedicated backup feed(s).
- **Monterrey vs. Club America** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
