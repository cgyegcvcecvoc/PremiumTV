# Live-event reliability audit

- **Scrape snapshot:** 2026-11-25T01:45:54Z
- **Scrape run:** `20261125T014115Z-3190` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 3/35
- **Fixtures with a redundancy deficit:** 32

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Air Force vs. Army (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Arkansas Little Rock vs. Arkansas Baptist Buffaloes (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Auburn vs. Lipscomb (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Chattanooga vs. Delaware State (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Clemson vs. Washington (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Coastal Carolina vs. Campbell (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| Connecticut Huskies vs. South Carolina Gamecocks (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Eastern Michigan vs. Kent State (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| Georgia Tech vs. Samford (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| Indiana vs. Jacksonville (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| James Madison vs. Charleston Southern (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Lehigh Mountain vs. Binghamton (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Louisiana Tech vs. Alcorn St. (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| North Alabama Lions vs. Alabama A&M (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Notre Dame vs. Central Michigan (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Ohio State vs. Vanderbilt (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Old Dominion vs. Hampton (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| Pennsylvania vs. Drexel (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Santa Clara vs. Nevada (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| SE Missouri St vs. IPFW (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Seton Hall vs. New Hampshire (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| South Alabama vs. Florida A&M (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| South Florida vs. Stetson (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| Tennessee Tech vs. West Georgia Wolves (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Texas Tech vs. Louisville (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| ULM vs. Houston Baptist (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Villanova vs. Coppin St. (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Western Michigan vs. Miami OH (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Western Michigan vs. Miami Ohio (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Orlando Magic vs. Detroit Pistons (NBA Basketball) | 5/5 | 2/2 | 3/1 | 5 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Washington Wizards vs. Boston Celtics (NBA Basketball) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Edmonton Oilers vs. Vegas Golden Knights (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Chapecoense-SC vs. Palmeiras (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Coquimbo vs. Union La Calera (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Millonarios vs. Bucaramanga (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **Air Force vs. Army** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Arkansas Little Rock vs. Arkansas Baptist Buffaloes** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Auburn vs. Lipscomb** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Chattanooga vs. Delaware State** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Clemson vs. Washington** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Coastal Carolina vs. Campbell** — needs 1 more confirmed dedicated backup feed(s).
- **Connecticut Huskies vs. South Carolina Gamecocks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Eastern Michigan vs. Kent State** — needs 1 more confirmed dedicated backup feed(s).
- **Georgia Tech vs. Samford** — needs 1 more confirmed dedicated backup feed(s).
- **Indiana vs. Jacksonville** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **James Madison vs. Charleston Southern** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Lehigh Mountain vs. Binghamton** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Louisiana Tech vs. Alcorn St.** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **North Alabama Lions vs. Alabama A&M** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Notre Dame vs. Central Michigan** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ohio State vs. Vanderbilt** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Old Dominion vs. Hampton** — needs 1 more confirmed dedicated backup feed(s).
- **Pennsylvania vs. Drexel** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Santa Clara vs. Nevada** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **SE Missouri St vs. IPFW** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Seton Hall vs. New Hampshire** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **South Alabama vs. Florida A&M** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **South Florida vs. Stetson** — needs 1 more confirmed dedicated backup feed(s).
- **Tennessee Tech vs. West Georgia Wolves** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Texas Tech vs. Louisville** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **ULM vs. Houston Baptist** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Villanova vs. Coppin St.** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Western Michigan vs. Miami OH** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Western Michigan vs. Miami Ohio** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Chapecoense-SC vs. Palmeiras** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Coquimbo vs. Union La Calera** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Millonarios vs. Bucaramanga** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
