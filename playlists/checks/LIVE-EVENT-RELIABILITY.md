# Live-event reliability audit

- **Scrape snapshot:** 2026-11-17T22:41:42Z
- **Scrape run:** `20261117T223820Z-2968` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 0/23
- **Fixtures with a redundancy deficit:** 23

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Barcelona vs. Paris (Basketball Euroleague) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Baskonia vs. Hapoel Tel Aviv (Basketball Euroleague) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Olimpia Milano vs. Crvena Zvezda (Basketball Euroleague) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Partizan vs. Valencia (Basketball Euroleague) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Virtus Bologna vs. Panathinaikos (Basketball Euroleague) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Ball State Cardinals vs. Ohio Bobcats (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Eastern Michigan Eagles vs. Western Michigan Broncos (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Florida Gators vs. Notre Dame Fighting Irish (College Football) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Florida vs. Notre Dame (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Miami (Ohio) RedHawks vs. Kent State Golden Flashes (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Charlotte Hornets vs. Los Angeles Lakers (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Detroit Pistons vs. San Antonio Spurs (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| New York Knicks vs. Toronto Raptors (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Portland Trail Blazers vs. Minnesota Timberwolves (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Utah Jazz vs. Los Angeles Clippers (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Austria vs. Israel (Soccer) | 2/2 | 2/2 | 0/1 | 2 | DAMITV, STRMGATE | doms9 | **DEFICIT** |
| Bosnia-Herzegovina vs. Romania (Soccer) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Denmark vs. Norway (Soccer) | 2/2 | 2/2 | 0/1 | 2 | DAMITV, STRMGATE | doms9 | **DEFICIT** |
| Hungary vs. Northern Ireland (Soccer) | 2/2 | 2/2 | 0/1 | 2 | DAMITV, STRMGATE | doms9 | **DEFICIT** |
| Poland vs. Sweden (Soccer) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Republic of Ireland vs. Kosovo (Soccer) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Ukraine vs. Georgia (Soccer) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Wales vs. Portugal (Soccer) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |

## Deficits

- **Barcelona vs. Paris** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Baskonia vs. Hapoel Tel Aviv** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Olimpia Milano vs. Crvena Zvezda** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Partizan vs. Valencia** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Virtus Bologna vs. Panathinaikos** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ball State Cardinals vs. Ohio Bobcats** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Eastern Michigan Eagles vs. Western Michigan Broncos** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Florida Gators vs. Notre Dame Fighting Irish** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Florida vs. Notre Dame** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Miami (Ohio) RedHawks vs. Kent State Golden Flashes** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Charlotte Hornets vs. Los Angeles Lakers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Detroit Pistons vs. San Antonio Spurs** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New York Knicks vs. Toronto Raptors** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Portland Trail Blazers vs. Minnesota Timberwolves** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Utah Jazz vs. Los Angeles Clippers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Austria vs. Israel** — needs 1 more confirmed dedicated backup feed(s).
- **Bosnia-Herzegovina vs. Romania** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Denmark vs. Norway** — needs 1 more confirmed dedicated backup feed(s).
- **Hungary vs. Northern Ireland** — needs 1 more confirmed dedicated backup feed(s).
- **Poland vs. Sweden** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Republic of Ireland vs. Kosovo** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ukraine vs. Georgia** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Wales vs. Portugal** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
