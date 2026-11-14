# Live-event reliability audit

- **Scrape snapshot:** 2026-11-14T19:31:21Z
- **Scrape run:** `20261114T192742Z-2950` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 1/65
- **Fixtures with a redundancy deficit:** 64

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Carlos Adames vs. Gerome Warburton (Boxing) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Army vs. Saint Thomas Tommies (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Charlotte vs. East Carolina (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| Clemson Tigers vs. Georgia Tech Yellow Jackets (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Clemson vs. Georgia Tech (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| Coastal Carolina vs. Arkansas State (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| Colorado St. vs. Loyola Chicago (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Connecticut vs. James Madison (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Iowa State vs. Cincinnati (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Iowa State vs. Cincinnati Bearcats (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Maryland vs. Wisconsin (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| Miami FL vs. Duke (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Miami Hurricanes vs. Duke (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Miami Hurricanes vs. Duke Blue Devils (College Football) | 2/2 | 2/2 | 0/1 | 2 | DAMITV, GSPORTS | doms9 | **DEFICIT** |
| Missouri Tigers vs. Georgia Bulldogs (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| NC State vs. Syracuse (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| North Carolina State vs. Syracuse (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Notre Dame Fighting Irish vs. DePaul Blue Demons (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Ohio State Buckeyes vs. Northwestern Wildcats (College Football) | 2/2 | 2/2 | 0/1 | 2 | DAMITV, GSPORTS | doms9 | **DEFICIT** |
| Ohio State vs. Northwestern (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| Ole Miss Rebels vs. Oklahoma Sooners (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Oregon State Beavers vs. Boise State Broncos (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Rutgers vs. Nebraska (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| Sam Houston State vs. Kennesaw State (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| SMU Mustangs vs. Wake Forest Demon Deacons (College Football) | 2/2 | 2/2 | 0/1 | 2 | DAMITV, GSPORTS | doms9 | **DEFICIT** |
| SMU vs. Wake Forest (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Southern Methodist vs. Wake Forest (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| TCU vs. Kansas State (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Temple vs. UAB (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| Tennessee Volunteers vs. Texas A&M Aggies (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Texas Tech Red Raiders vs. Stonehill Skyhawks (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Utah Utes vs. Arizona Wildcats (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Vanderbilt Commodores vs. Alabama Crimson Tide (College Football) | 2/2 | 2/2 | 0/1 | 2 | DAMITV, GSPORTS | doms9 | **DEFICIT** |
| Vanderbilt vs. Alabama (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| Carolina Hurricanes vs. Seattle Kraken (National Hockey League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Carolina Hurricanes vs. Seattle Kraken (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| RAF Abu Dhabi Chimaev vs. Weidman (Other) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| PFL Dubai: Nemkov vs. Bilostenniy (PFL) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| RAF Abu Dhabi Chimaev vs. Weidman (RAF Wrestling) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| England vs. Japan (Rugby Nations Championship) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Algeria vs. Togo (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Almere City vs. Helmond (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Almeria vs. Andorra (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Angola vs. South Sudan (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Atletico GO vs. Cuiaba (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| CRB vs. Ceara (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Criciuma vs. Novorizontino (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| De Graafschap vs. Top Oss (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Dordrecht vs. Heracles (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Fleetwood vs. Tranmere (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Georgia vs. Hungary (Soccer) | 2/2 | 2/2 | 0/1 | 2 | DAMITV, XYZ | doms9 | **DEFICIT** |
| Juventude vs. Botafogo SP (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Maldonado vs. CA Cerro (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Mallorca vs. Cordoba (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Norway vs. Wales (Soccer) | 2/2 | 2/2 | 0/1 | 2 | DAMITV, XYZ | doms9 | **DEFICIT** |
| Roda vs. FC Volendam (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Sint Maarten vs. French Guiana (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Venlo vs. Eindhoven FC (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Waalwijk vs. FC Den Bosch (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| IF Bjorkloven vs. Brynas (Sweden Hockey SHL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Lulea vs. Farjestad (Sweden Hockey SHL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Orebro vs. Djurgarden (Sweden Hockey SHL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Skelleftea vs. Linkoping (Sweden Hockey SHL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Almtuna vs. BIK Karlskoga (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| PFL Dubai: Vadim Nemkov vs. Sergei Bilostenniy (UFC / MMA) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |

## Deficits

- **Carlos Adames vs. Gerome Warburton** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Army vs. Saint Thomas Tommies** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Charlotte vs. East Carolina** — needs 1 more confirmed dedicated backup feed(s).
- **Clemson Tigers vs. Georgia Tech Yellow Jackets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Clemson vs. Georgia Tech** — needs 1 more confirmed dedicated backup feed(s).
- **Coastal Carolina vs. Arkansas State** — needs 1 more confirmed dedicated backup feed(s).
- **Colorado St. vs. Loyola Chicago** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Connecticut vs. James Madison** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Iowa State vs. Cincinnati** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Iowa State vs. Cincinnati Bearcats** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Maryland vs. Wisconsin** — needs 1 more confirmed dedicated backup feed(s).
- **Miami FL vs. Duke** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Miami Hurricanes vs. Duke** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Miami Hurricanes vs. Duke Blue Devils** — needs 1 more confirmed dedicated backup feed(s).
- **Missouri Tigers vs. Georgia Bulldogs** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **NC State vs. Syracuse** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **North Carolina State vs. Syracuse** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Notre Dame Fighting Irish vs. DePaul Blue Demons** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ohio State Buckeyes vs. Northwestern Wildcats** — needs 1 more confirmed dedicated backup feed(s).
- **Ohio State vs. Northwestern** — needs 1 more confirmed dedicated backup feed(s).
- **Ole Miss Rebels vs. Oklahoma Sooners** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Oregon State Beavers vs. Boise State Broncos** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Rutgers vs. Nebraska** — needs 1 more confirmed dedicated backup feed(s).
- **Sam Houston State vs. Kennesaw State** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **SMU Mustangs vs. Wake Forest Demon Deacons** — needs 1 more confirmed dedicated backup feed(s).
- **SMU vs. Wake Forest** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Southern Methodist vs. Wake Forest** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **TCU vs. Kansas State** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Temple vs. UAB** — needs 1 more confirmed dedicated backup feed(s).
- **Tennessee Volunteers vs. Texas A&M Aggies** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Texas Tech Red Raiders vs. Stonehill Skyhawks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Utah Utes vs. Arizona Wildcats** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Vanderbilt Commodores vs. Alabama Crimson Tide** — needs 1 more confirmed dedicated backup feed(s).
- **Vanderbilt vs. Alabama** — needs 1 more confirmed dedicated backup feed(s).
- **Carolina Hurricanes vs. Seattle Kraken** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **RAF Abu Dhabi Chimaev vs. Weidman** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **PFL Dubai: Nemkov vs. Bilostenniy** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **RAF Abu Dhabi Chimaev vs. Weidman** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **England vs. Japan** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Algeria vs. Togo** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Almere City vs. Helmond** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Almeria vs. Andorra** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Angola vs. South Sudan** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Atletico GO vs. Cuiaba** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **CRB vs. Ceara** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Criciuma vs. Novorizontino** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **De Graafschap vs. Top Oss** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Dordrecht vs. Heracles** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Fleetwood vs. Tranmere** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Georgia vs. Hungary** — needs 1 more confirmed dedicated backup feed(s).
- **Juventude vs. Botafogo SP** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Maldonado vs. CA Cerro** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Mallorca vs. Cordoba** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Norway vs. Wales** — needs 1 more confirmed dedicated backup feed(s).
- **Roda vs. FC Volendam** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Sint Maarten vs. French Guiana** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Venlo vs. Eindhoven FC** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Waalwijk vs. FC Den Bosch** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **IF Bjorkloven vs. Brynas** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Lulea vs. Farjestad** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Orebro vs. Djurgarden** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Skelleftea vs. Linkoping** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Almtuna vs. BIK Karlskoga** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **PFL Dubai: Vadim Nemkov vs. Sergei Bilostenniy** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
