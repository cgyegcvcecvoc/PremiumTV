# Live-event reliability audit

- **Scrape snapshot:** 2026-11-18T00:09:22Z
- **Scrape run:** `20261118T000534Z-2971` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 3/38
- **Fixtures with a redundancy deficit:** 35

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| New York Knicks vs. Toronto Raptors (Basketball) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Alabama vs. Kennesaw State (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Army vs. Marist (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Ball State Cardinals vs. Ohio Bobcats (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Duke vs. University of Illinois (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Eastern Michigan Eagles vs. Western Michigan Broncos (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Florida Gators vs. Notre Dame Fighting Irish (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Florida vs. Notre Dame (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Kent State vs. Miami OH (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Liberty vs. Southern Illinois (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Miami (Ohio) RedHawks vs. Kent State Golden Flashes (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Ohio vs. Ball State (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Purdue vs. Lipscomb (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Western Michigan vs. Eastern Michigan (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| Argentina vs. Costa Rica (International Friendly Games) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Charlotte Hornets vs. Los Angeles Lakers (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Detroit Pistons vs. San Antonio Spurs (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| New York Knicks vs. Toronto Raptors (NBA Basketball) | 2/2 | 2/2 | 0/1 | 2 | GSPORTS, STRMGATE | doms9 | **DEFICIT** |
| Portland Trail Blazers vs. Minnesota Timberwolves (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Utah Jazz vs. Los Angeles Clippers (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Boston Bruins vs. Los Angeles Kings (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Buffalo Sabres vs. Philadelphia Flyers (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Chicago Blackhawks vs. Toronto Maple Leafs (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Columbus Blue Jackets vs. New York Islanders (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Edmonton Oilers vs. Florida Panthers (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Minnesota Wild vs. Nashville Predators (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| San Jose Sharks vs. Calgary Flames (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| St Louis Blues vs. Anaheim Ducks (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Tampa Bay Lightning vs. Washington Capitals (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Vegas Golden Knights vs. Dallas Stars (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Winnipeg Jets vs. Ottawa Senators (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| America De Cali vs. Inter Bogota (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Bolivia vs. Ecuador (Soccer) | 3/3 | 2/2 | 1/1 | 3 | FAWA, STRMGATE | doms9 | **PASS** |
| Colombia vs. Chile (Soccer) | 3/3 | 2/2 | 1/1 | 3 | FAWA, STRMGATE | doms9 | **PASS** |
| Costa Rica vs. Argentina (Soccer) | 3/3 | 2/2 | 1/1 | 3 | FAWA, STRMGATE | doms9 | **PASS** |
| French Guiana vs. Saint Vincent and the Grenadines (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Uruguay vs. Dominican Republic (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| USA vs. Haiti (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **New York Knicks vs. Toronto Raptors** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Alabama vs. Kennesaw State** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Army vs. Marist** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ball State Cardinals vs. Ohio Bobcats** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Duke vs. University of Illinois** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Eastern Michigan Eagles vs. Western Michigan Broncos** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Florida Gators vs. Notre Dame Fighting Irish** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Florida vs. Notre Dame** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Kent State vs. Miami OH** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Liberty vs. Southern Illinois** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Miami (Ohio) RedHawks vs. Kent State Golden Flashes** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ohio vs. Ball State** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Purdue vs. Lipscomb** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Western Michigan vs. Eastern Michigan** — needs 1 more confirmed dedicated backup feed(s).
- **Argentina vs. Costa Rica** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Charlotte Hornets vs. Los Angeles Lakers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Detroit Pistons vs. San Antonio Spurs** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New York Knicks vs. Toronto Raptors** — needs 1 more confirmed dedicated backup feed(s).
- **Portland Trail Blazers vs. Minnesota Timberwolves** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Utah Jazz vs. Los Angeles Clippers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Boston Bruins vs. Los Angeles Kings** — needs 1 more confirmed dedicated backup feed(s).
- **Buffalo Sabres vs. Philadelphia Flyers** — needs 1 more confirmed dedicated backup feed(s).
- **Chicago Blackhawks vs. Toronto Maple Leafs** — needs 1 more confirmed dedicated backup feed(s).
- **Columbus Blue Jackets vs. New York Islanders** — needs 1 more confirmed dedicated backup feed(s).
- **Edmonton Oilers vs. Florida Panthers** — needs 1 more confirmed dedicated backup feed(s).
- **Minnesota Wild vs. Nashville Predators** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **San Jose Sharks vs. Calgary Flames** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **St Louis Blues vs. Anaheim Ducks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Tampa Bay Lightning vs. Washington Capitals** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Vegas Golden Knights vs. Dallas Stars** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Winnipeg Jets vs. Ottawa Senators** — needs 1 more confirmed dedicated backup feed(s).
- **America De Cali vs. Inter Bogota** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **French Guiana vs. Saint Vincent and the Grenadines** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Uruguay vs. Dominican Republic** — needs 1 more confirmed dedicated backup feed(s).
- **USA vs. Haiti** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
