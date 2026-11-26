# Live-event reliability audit

- **Scrape snapshot:** 2026-11-26T03:55:06Z
- **Scrape run:** `20261126T034605Z-3000` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 7/38
- **Fixtures with a redundancy deficit:** 31

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Green Bay Packers vs. Los Angeles Rams (American Football) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Phoenix Suns vs. Houston Rockets (Basketball) | 3/3 | 2/2 | 1/1 | 1 | SPRTSBITE | doms9 | **DEFICIT** |
| Sacramento Kings vs. Golden State Warriors (Basketball) | 2/2 | 2/2 | 0/1 | 1 | SPRTSBITE | doms9 | **DEFICIT** |
| San Antonio Spurs vs. Portland Trail Blazers (Basketball) | 2/2 | 2/2 | 0/1 | 1 | SPRTSBITE | doms9 | **DEFICIT** |
| Colorado vs. Gr. Canyon (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Mississippi State vs. Wake Forest (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| New Mexico vs. Mississippi Valley (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Washington vs. VCU (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Chicago Blackhawks vs. Seattle Kraken (Ice Hockey) | 1/1 | 1/2 | 0/1 | 1 | SPRTSBITE | doms9 | **DEFICIT** |
| Montreal Canadiens vs. Colorado Avalanche (Ice Hockey) | 1/1 | 1/2 | 0/1 | 1 | SPRTSBITE | doms9 | **DEFICIT** |
| San Jose Sharks vs. Anaheim Ducks (Ice Hockey) | 2/2 | 2/2 | 0/1 | 1 | SPRTSBITE | doms9 | **DEFICIT** |
| Vancouver Canucks vs. Detroit Red Wings (Ice Hockey) | 0/2 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Winnipeg Jets vs. Boston Bruins (Ice Hockey) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Brooklyn Nets vs. Milwaukee Bucks (NBA Basketball) | 2/2 | 2/2 | 0/1 | 2 | MP66, STRMGATE | doms9 | **DEFICIT** |
| Chicago Bulls vs. Charlotte Hornets (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Cleveland Cavaliers vs. New York Knicks (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Golden State Warriors vs. Sacramento Kings (NBA Basketball) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, STRMGATE | doms9 | **PASS** |
| Houston Rockets vs. Phoenix Suns (NBA Basketball) | 5/5 | 2/2 | 3/1 | 5 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| LA Clippers vs. Memphis Grizzlies (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Los Angeles Clippers vs. Memphis Grizzlies (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | MP66 | doms9 | **DEFICIT** |
| Minnesota Timberwolves vs. Oklahoma City Thunder (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Portland Trail Blazers vs. San Antonio Spurs (NBA Basketball) | 5/5 | 2/2 | 3/1 | 5 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Anaheim Ducks vs. San Jose Sharks (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Boston Bruins vs. Winnipeg Jets (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Buffalo Sabres vs. New York Rangers (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Calgary Flames vs. Pittsburgh Penguins (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Carolina Hurricanes vs. Tampa Bay Lightning (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Chicago Blackhawks vs. Seattle Kraken (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Colorado Avalanche vs. Montreal Canadiens (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Colorado Avalanche vs. Montréal Canadiens (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | ISTRMEAST, MP66 | doms9 | **DEFICIT** |
| Dallas Stars vs. Nashville Predators (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Detroit Red Wings vs. Vancouver Canucks (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Florida Panthers vs. Ottawa Senators (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Minnesota Wild vs. Utah Mammoth (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| New Jersey Devils vs. Columbus Blue Jackets (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| New York Islanders vs. St Louis Blues (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Washington Capitals vs. Philadelphia Flyers (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Monterrey vs. Club America (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **Phoenix Suns vs. Houston Rockets** — needs 1 more independent origin family/families.
- **Sacramento Kings vs. Golden State Warriors** — needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **San Antonio Spurs vs. Portland Trail Blazers** — needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Colorado vs. Gr. Canyon** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Mississippi State vs. Wake Forest** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Mexico vs. Mississippi Valley** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Washington vs. VCU** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Chicago Blackhawks vs. Seattle Kraken** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Montreal Canadiens vs. Colorado Avalanche** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **San Jose Sharks vs. Anaheim Ducks** — needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Vancouver Canucks vs. Detroit Red Wings** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Winnipeg Jets vs. Boston Bruins** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Brooklyn Nets vs. Milwaukee Bucks** — needs 1 more confirmed dedicated backup feed(s).
- **Chicago Bulls vs. Charlotte Hornets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Cleveland Cavaliers vs. New York Knicks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **LA Clippers vs. Memphis Grizzlies** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Los Angeles Clippers vs. Memphis Grizzlies** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Minnesota Timberwolves vs. Oklahoma City Thunder** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Boston Bruins vs. Winnipeg Jets** — needs 1 more confirmed dedicated backup feed(s).
- **Buffalo Sabres vs. New York Rangers** — needs 1 more confirmed dedicated backup feed(s).
- **Calgary Flames vs. Pittsburgh Penguins** — needs 1 more confirmed dedicated backup feed(s).
- **Carolina Hurricanes vs. Tampa Bay Lightning** — needs 1 more confirmed dedicated backup feed(s).
- **Colorado Avalanche vs. Montreal Canadiens** — needs 1 more confirmed dedicated backup feed(s).
- **Colorado Avalanche vs. Montréal Canadiens** — needs 1 more confirmed dedicated backup feed(s).
- **Dallas Stars vs. Nashville Predators** — needs 1 more confirmed dedicated backup feed(s).
- **Detroit Red Wings vs. Vancouver Canucks** — needs 1 more confirmed dedicated backup feed(s).
- **Florida Panthers vs. Ottawa Senators** — needs 1 more confirmed dedicated backup feed(s).
- **New Jersey Devils vs. Columbus Blue Jackets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New York Islanders vs. St Louis Blues** — needs 1 more confirmed dedicated backup feed(s).
- **Washington Capitals vs. Philadelphia Flyers** — needs 1 more confirmed dedicated backup feed(s).
- **Monterrey vs. Club America** — needs 1 more confirmed dedicated backup feed(s).

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
