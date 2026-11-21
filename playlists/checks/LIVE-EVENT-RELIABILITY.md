# Live-event reliability audit

- **Scrape snapshot:** 2026-11-21T16:09:41Z
- **Scrape run:** `20261121T160559Z-2973` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 7/105
- **Fixtures with a redundancy deficit:** 98

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Panathinaikos vs. Maroussi (Basketball Greece League) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| PAOK vs. Aris (Basketball Greece League) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Arizona Wildcats vs. Kansas State Wildcats (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| BYU Cougars vs. Kansas Jayhawks (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Chattanooga Mocs vs. Alabama Crimson Tide (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Georgia Bulldogs vs. South Carolina Gamecocks (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Houston Cougars vs. West Virginia Mountaineers (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Indiana Hoosiers vs. Washington Huskies (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Iowa Hawkeyes vs. Illinois Fighting Illini (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Kentucky Wildcats vs. Missouri Tigers (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Maryland Terrapins vs. USC Trojans (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Ohio State Buckeyes vs. Nebraska Cornhuskers (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Oklahoma State Cowboys vs. Arizona State Sun Devils (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| San Diego State Aztecs vs. Boise State Broncos (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| SMU Mustangs vs. Notre Dame Fighting Irish (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Texas Tech Red Raiders vs. Baylor Bears (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| UCLA Bruins vs. Michigan Wolverines (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Utah Utes vs. TCU Horned Frogs (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Virginia Tech Hokies vs. Miami Hurricanes (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Wake Forest Demon Deacons vs. Georgia Tech Yellow Jackets (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Wofford Terriers vs. Ole Miss Rebels (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Bristol City vs. Middlesbrough (ENG 2) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Charlton Athletic vs. Wolverhampton Wanderers (ENG 2) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Preston North End vs. West Ham United (ENG 2) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Wrexham vs. Lincoln City (ENG 2) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Boston Celtics vs. Sacramento Kings (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Los Angeles Clippers vs. Dallas Mavericks (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Memphis Grizzlies vs. Minnesota Timberwolves (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Milwaukee Bucks vs. Philadelphia 76ers (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| New Orleans Pelicans vs. San Antonio Spurs (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Portland Trail Blazers vs. New York Knicks (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| 1. FC Union Berlin vs. RB Leipzig (Soccer) | 2/2 | 2/2 | 0/1 | 2 | ISTRMEAST, STRMGATE | doms9 | **DEFICIT** |
| Accrington vs. Salford (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| AFC Bournemouth vs. Nottingham Forest (Soccer) | 2/2 | 2/2 | 0/1 | 2 | KINGDOME, STRMGATE | doms9 | **DEFICIT** |
| Alaves vs. Deportivo la Coruna (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Aston Villa vs. Sunderland (Soccer) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, KINGDOME, STRMGATE | doms9 | **PASS** |
| Barnet vs. Port Vale (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Bayer Leverkusen vs. Paderborn (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Bolton vs. Portsmouth (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Borussia Dortmund vs. Borussia Mönchengladbach (Soccer) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Borussia Mgladbach vs. Borussia Dortmund (Soccer) | 1/1 | 1/2 | 0/1 | 1 | KINGDOME | doms9 | **DEFICIT** |
| Bournemouth vs. Nottingham Forest (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| Bradford City vs. Doncaster (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Burton vs. Luton (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Cambridge Utd vs. Stockport County (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Celtic vs. St Mirren (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| CFR Cluj vs. Otelul (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Charleroi vs. STVV (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Chelsea vs. Leeds United (Soccer) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, KINGDOME, STRMGATE | doms9 | **PASS** |
| Cheltenham vs. Bristol Rovers (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Chesterfield vs. Shrewsbury (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Como vs. Cagliari (Soccer) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, KINGDOME, STRMGATE | doms9 | **PASS** |
| Coventry City vs. Crystal Palace (Soccer) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, KINGDOME, STRMGATE | doms9 | **PASS** |
| Crawley vs. Fleetwood (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Eintracht Frankfurt vs. Hoffenheim (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Eintracht Frankfurt vs. TSG Hoffenheim (Soccer) | 2/2 | 2/2 | 0/1 | 2 | ISTRMEAST, STRMGATE | doms9 | **DEFICIT** |
| Elversberg vs. Freiburg (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Falkirk vs. St Johnstone (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Grimsby vs. Rotherham (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Hibernian vs. Dundee Utd (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Huddersfield vs. Leicester (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Ipswich Town vs. Tottenham Hotspur (Soccer) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, KINGDOME, STRMGATE | doms9 | **PASS** |
| Kilmarnock vs. Aberdeen (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Kocaelispor vs. Fenerbahce (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| LASK vs. Hartberg (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Lazio vs. Lecce (Soccer) | 3/3 | 2/2 | 1/1 | 3 | FAWA, KINGDOME, STRMGATE | doms9 | **PASS** |
| Leyton Orient vs. AFC Wimbledon (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Lincoln vs. Wrexham (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Lunds vs. Norrby (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Mansfield vs. MK Dons (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Middlesbrough vs. Bristol City (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Monchengladbach vs. Borussia Dortmund (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| NEC Nijmegen vs. PSV (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Nice vs. PSG (Soccer) | 1/1 | 1/2 | 0/1 | 1 | KINGDOME | doms9 | **DEFICIT** |
| Northampton vs. Rochdale (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Notts County vs. Stevenage (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| OFK Beograd vs. Novi Pazar (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Oldham vs. Exeter (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Omonia Aradippou vs. Pafos (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Omonia vs. APOEL (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Oxford Utd vs. Wycombe (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Parma vs. Roma (Soccer) | 1/1 | 1/2 | 0/1 | 1 | KINGDOME | doms9 | **DEFICIT** |
| Plymouth vs. Peterborough (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Rayo Vallecano vs. Valencia (Soccer) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, KINGDOME, STRMGATE | doms9 | **PASS** |
| Real Sociedad B vs. Cadiz CF (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Rubin Kazan vs. Zenit (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| SC Freiburg vs. SV Elversberg (Soccer) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| SC Paderborn vs. Bayer Leverkusen (Soccer) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Sheffield United vs. Watford (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Stoke City vs. Birmingham City (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Swansea City vs. West Bromwich (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Tirol vs. Austria Lustenau (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Tottenham vs. Ipswich (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Tranmere vs. Colchester (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Union Berlin vs. RB Leipzig (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| West Ham United vs. Preston North End (Soccer) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| West Ham vs. Preston (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Wolves vs. Charlton (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| York City vs. Walsall (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Frolunda vs. Brynas (Sweden Hockey SHL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Rogle vs. Timra (Sweden Hockey SHL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Shoaib Yousaf vs. John Mitchell (UFC / MMA) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| UFC Fight Night: Jiri Prochazka vs. Navajo Stirling (UFC / MMA) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| UFC Fight Night: Prochazka vs. Stirling (UFC / MMA) | 1/1 | 1/2 | 0/1 | 1 | KINGDOME | doms9 | **DEFICIT** |
| UFC Fight Night: Procházka vs. Stirling (UFC / MMA) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |

## Deficits

- **Panathinaikos vs. Maroussi** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **PAOK vs. Aris** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Arizona Wildcats vs. Kansas State Wildcats** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **BYU Cougars vs. Kansas Jayhawks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Chattanooga Mocs vs. Alabama Crimson Tide** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Georgia Bulldogs vs. South Carolina Gamecocks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Houston Cougars vs. West Virginia Mountaineers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Indiana Hoosiers vs. Washington Huskies** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Iowa Hawkeyes vs. Illinois Fighting Illini** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Kentucky Wildcats vs. Missouri Tigers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Maryland Terrapins vs. USC Trojans** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ohio State Buckeyes vs. Nebraska Cornhuskers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Oklahoma State Cowboys vs. Arizona State Sun Devils** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **San Diego State Aztecs vs. Boise State Broncos** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **SMU Mustangs vs. Notre Dame Fighting Irish** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Texas Tech Red Raiders vs. Baylor Bears** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **UCLA Bruins vs. Michigan Wolverines** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Utah Utes vs. TCU Horned Frogs** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Virginia Tech Hokies vs. Miami Hurricanes** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Wake Forest Demon Deacons vs. Georgia Tech Yellow Jackets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Wofford Terriers vs. Ole Miss Rebels** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Bristol City vs. Middlesbrough** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Charlton Athletic vs. Wolverhampton Wanderers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Preston North End vs. West Ham United** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Wrexham vs. Lincoln City** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Boston Celtics vs. Sacramento Kings** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Los Angeles Clippers vs. Dallas Mavericks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Memphis Grizzlies vs. Minnesota Timberwolves** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Milwaukee Bucks vs. Philadelphia 76ers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Orleans Pelicans vs. San Antonio Spurs** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Portland Trail Blazers vs. New York Knicks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **1. FC Union Berlin vs. RB Leipzig** — needs 1 more confirmed dedicated backup feed(s).
- **Accrington vs. Salford** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **AFC Bournemouth vs. Nottingham Forest** — needs 1 more confirmed dedicated backup feed(s).
- **Alaves vs. Deportivo la Coruna** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Barnet vs. Port Vale** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Bayer Leverkusen vs. Paderborn** — needs 1 more confirmed dedicated backup feed(s).
- **Bolton vs. Portsmouth** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Borussia Dortmund vs. Borussia Mönchengladbach** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Borussia Mgladbach vs. Borussia Dortmund** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Bournemouth vs. Nottingham Forest** — needs 1 more confirmed dedicated backup feed(s).
- **Bradford City vs. Doncaster** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Burton vs. Luton** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Cambridge Utd vs. Stockport County** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Celtic vs. St Mirren** — needs 1 more confirmed dedicated backup feed(s).
- **CFR Cluj vs. Otelul** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Charleroi vs. STVV** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Cheltenham vs. Bristol Rovers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Chesterfield vs. Shrewsbury** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Crawley vs. Fleetwood** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Eintracht Frankfurt vs. Hoffenheim** — needs 1 more confirmed dedicated backup feed(s).
- **Eintracht Frankfurt vs. TSG Hoffenheim** — needs 1 more confirmed dedicated backup feed(s).
- **Elversberg vs. Freiburg** — needs 1 more confirmed dedicated backup feed(s).
- **Falkirk vs. St Johnstone** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Grimsby vs. Rotherham** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Hibernian vs. Dundee Utd** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Huddersfield vs. Leicester** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Kilmarnock vs. Aberdeen** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Kocaelispor vs. Fenerbahce** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **LASK vs. Hartberg** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Leyton Orient vs. AFC Wimbledon** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Lincoln vs. Wrexham** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Lunds vs. Norrby** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Mansfield vs. MK Dons** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Middlesbrough vs. Bristol City** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Monchengladbach vs. Borussia Dortmund** — needs 1 more confirmed dedicated backup feed(s).
- **NEC Nijmegen vs. PSV** — needs 1 more confirmed dedicated backup feed(s).
- **Nice vs. PSG** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Northampton vs. Rochdale** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Notts County vs. Stevenage** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **OFK Beograd vs. Novi Pazar** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Oldham vs. Exeter** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Omonia Aradippou vs. Pafos** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Omonia vs. APOEL** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Oxford Utd vs. Wycombe** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Parma vs. Roma** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Plymouth vs. Peterborough** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Real Sociedad B vs. Cadiz CF** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Rubin Kazan vs. Zenit** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **SC Freiburg vs. SV Elversberg** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **SC Paderborn vs. Bayer Leverkusen** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Sheffield United vs. Watford** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Stoke City vs. Birmingham City** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Swansea City vs. West Bromwich** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Tirol vs. Austria Lustenau** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Tottenham vs. Ipswich** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Tranmere vs. Colchester** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Union Berlin vs. RB Leipzig** — needs 1 more confirmed dedicated backup feed(s).
- **West Ham United vs. Preston North End** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **West Ham vs. Preston** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Wolves vs. Charlton** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **York City vs. Walsall** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Frolunda vs. Brynas** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Rogle vs. Timra** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Shoaib Yousaf vs. John Mitchell** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **UFC Fight Night: Jiri Prochazka vs. Navajo Stirling** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **UFC Fight Night: Prochazka vs. Stirling** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **UFC Fight Night: Procházka vs. Stirling** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
