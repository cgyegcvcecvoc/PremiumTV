# Live-event reliability audit

- **Generated:** 2026-11-13T02:11:06Z
- **Scrape run:** `20261113T020723Z-2932` — health check completed
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 11/46
- **Fixtures with a redundancy deficit:** 35

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| New York Giants vs. Washington Commanders (American Football) | 2/2 | 2/2 | 0/1 | 2 | ISTRMEAST, STRMGATE | doms9 | **DEFICIT** |
| Estudiantes LP vs. Ind Rivadavia (Argentina Super Copa) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Charlotte Hornets vs. Phoenix Suns (Basketball) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Dallas Mavericks vs. Minnesota Timberwolves (Basketball) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Arkansas Razorbacks vs. Arkansas-Pine Bluff Golden Lions (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Ball State Cardinals vs. Louisville Cardinals (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| BYU Cougars vs. Montana State Bobcats (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Clemson Tigers vs. South Carolina Gamecocks (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Georgia Tech Yellow Jackets vs. Maryland Eastern Shore Hawks (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Iowa Hawkeyes vs. Northern Iowa Panthers (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Louisiana-Monroe vs. Louisiana-Lafayette (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Minnesota vs. Southern Univ. (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| South Florida vs. Memphis (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| Texas A&M vs. Oklahoma State (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Minnesota Timberwolves vs. Dallas Mavericks (National Basketball Association) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Philadelphia 76ers vs. Toronto Raptors (National Basketball Association) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Phoenix Suns vs. Charlotte Hornets (National Basketball Association) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Washington Wizards vs. Detroit Pistons (National Basketball Association) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| New York Giants vs. Washington Commanders (National Football League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Boston Bruins vs. Montreal Canadiens (National Hockey League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Chicago Blackhawks vs. Buffalo Sabres (National Hockey League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Columbus Blue Jackets vs. Tampa Bay Lightning (National Hockey League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Dallas Stars vs. Winnipeg Jets (National Hockey League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Florida Panthers vs. Detroit Red Wings (National Hockey League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| New Jersey Devils vs. Washington Capitals (National Hockey League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Ottawa Senators vs. Colorado Avalanche (National Hockey League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Toronto Maple Leafs vs. Minnesota Wild (National Hockey League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Utah Mammoth vs. St. Louis Blues (National Hockey League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Minnesota Timberwolves vs. Dallas Mavericks (NBA Basketball) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Philadelphia 76ers vs. Toronto Raptors (NBA Basketball) | 5/5 | 2/2 | 3/1 | 5 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Phoenix Suns vs. Charlotte Hornets (NBA Basketball) | 3/3 | 2/2 | 1/1 | 3 | FAWA, MP66, STRMGATE | doms9 | **PASS** |
| Washington Wizards vs. Detroit Pistons (NBA Basketball) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Boston Bruins vs. Montreal Canadiens (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Boston Bruins vs. Montréal Canadiens (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | ISTRMEAST, MP66 | doms9 | **DEFICIT** |
| Buffalo Sabres vs. Chicago Blackhawks (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Colorado Avalanche vs. Ottawa Senators (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Columbus Blue Jackets vs. Tampa Bay Lightning (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Dallas Stars vs. Winnipeg Jets (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Detroit Red Wings vs. Florida Panthers (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Los Angeles Kings vs. New York Islanders (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| New Jersey Devils vs. Washington Capitals (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Toronto Maple Leafs vs. Minnesota Wild (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Utah Mammoth vs. St Louis Blues (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Curacao vs. Panama (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Dep Pasto vs. Junior (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Washington Commanders vs. New York Giants (Soccer) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |

## Deficits

- **New York Giants vs. Washington Commanders** — needs 1 more confirmed dedicated backup feed(s).
- **Estudiantes LP vs. Ind Rivadavia** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Charlotte Hornets vs. Phoenix Suns** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Dallas Mavericks vs. Minnesota Timberwolves** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Arkansas Razorbacks vs. Arkansas-Pine Bluff Golden Lions** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ball State Cardinals vs. Louisville Cardinals** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **BYU Cougars vs. Montana State Bobcats** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Clemson Tigers vs. South Carolina Gamecocks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Georgia Tech Yellow Jackets vs. Maryland Eastern Shore Hawks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Iowa Hawkeyes vs. Northern Iowa Panthers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Louisiana-Monroe vs. Louisiana-Lafayette** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Minnesota vs. Southern Univ.** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **South Florida vs. Memphis** — needs 1 more confirmed dedicated backup feed(s).
- **Texas A&M vs. Oklahoma State** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Minnesota Timberwolves vs. Dallas Mavericks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Philadelphia 76ers vs. Toronto Raptors** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Phoenix Suns vs. Charlotte Hornets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Washington Wizards vs. Detroit Pistons** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New York Giants vs. Washington Commanders** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Boston Bruins vs. Montreal Canadiens** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Chicago Blackhawks vs. Buffalo Sabres** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Columbus Blue Jackets vs. Tampa Bay Lightning** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Dallas Stars vs. Winnipeg Jets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Florida Panthers vs. Detroit Red Wings** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Jersey Devils vs. Washington Capitals** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ottawa Senators vs. Colorado Avalanche** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Toronto Maple Leafs vs. Minnesota Wild** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Utah Mammoth vs. St. Louis Blues** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Boston Bruins vs. Montreal Canadiens** — needs 1 more confirmed dedicated backup feed(s).
- **Boston Bruins vs. Montréal Canadiens** — needs 1 more confirmed dedicated backup feed(s).
- **Los Angeles Kings vs. New York Islanders** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Utah Mammoth vs. St Louis Blues** — needs 1 more confirmed dedicated backup feed(s).
- **Curacao vs. Panama** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Dep Pasto vs. Junior** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Washington Commanders vs. New York Giants** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` means the latest checked scrape received stream-shaped data; it is a point-in-time result.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
