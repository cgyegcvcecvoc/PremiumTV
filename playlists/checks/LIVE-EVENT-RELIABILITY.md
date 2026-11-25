# Live-event reliability audit

- **Scrape snapshot:** 2026-11-25T20:39:56Z
- **Scrape run:** `20261125T203220Z-2990` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 4/40
- **Fixtures with a redundancy deficit:** 36

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Baskonia vs. Anadolu Efes (Basketball Euroleague) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Olympiacos vs. Hapoel Tel Aviv (Basketball Euroleague) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Real Madrid vs. Zalgiris Kaunas (Basketball Euroleague) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Appalachian State vs. Akron (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| LSU vs. Arizona State (College Football) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| NJIT vs. Manhattan (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Oklahoma State vs. Jackson State (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Ole Miss vs. Arizona (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Texas A&M vs. Xavier (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Virginia vs. Marquette (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Atlético Madrid vs. Viking FK (Soccer) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, SPRTSBITE, STRMGATE | doms9 | **PASS** |
| Bolton vs. West Bromwich (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Boreham Wood vs. Aldershot (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Burnley vs. Birmingham City (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Club Brugge KV vs. Liverpool FC (Soccer) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Club Brugge vs. Liverpool (Soccer) | 2/2 | 2/2 | 0/1 | 2 | SPRTSBITE, STRMGATE | doms9 | **DEFICIT** |
| Fleetwood vs. Leeds U21 (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Harrogate vs. Kidderminster (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Hartlepool vs. Solihull Moors (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Inter Milan vs. VfB Stuttgart (Soccer) | 1/1 | 1/2 | 0/1 | 1 | SPRTSBITE | doms9 | **DEFICIT** |
| Inter vs. VfB Stuttgart (Soccer) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Lille vs. Bayern Munich (Soccer) | 2/2 | 2/2 | 0/1 | 2 | SPRTSBITE, STRMGATE | doms9 | **DEFICIT** |
| LOSC Lille vs. FC Bayern München (Soccer) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Mantova vs. Arezzo (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Padova vs. Sampdoria (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Paris Saint-Germain vs. AS Roma (Soccer) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, SPRTSBITE, STRMGATE | doms9 | **PASS** |
| Pisa vs. Modena (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Sabah FK vs. Barcelona (Soccer) | 0/3 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Shakhtar Donetsk vs. Fenerbahce (Soccer) | 4/4 | 2/2 | 2/1 | 3 | FAWA, SPRTSBITE, STRMGATE | doms9 | **PASS** |
| Shakhtar Donetsk vs. Fenerbahçe (Soccer) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Slavia Prague vs. Villarreal (Soccer) | 0/2 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Sporting CP vs. Manchester United (Soccer) | 3/3 | 2/2 | 1/1 | 3 | ISTRMEAST, SPRTSBITE, STRMGATE | doms9 | **PASS** |
| Stoke City vs. Millwall (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| VfB Stuttgart vs. Internazionale (Soccer) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Watford vs. Blackburn Rovers (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Almtuna vs. Visby Roma (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Kalmar vs. AIK (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Mora vs. Ostersund (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Nybro vs. Vasteras (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Sodertalje vs. Modo (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **Baskonia vs. Anadolu Efes** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Olympiacos vs. Hapoel Tel Aviv** — needs 1 more confirmed dedicated backup feed(s).
- **Real Madrid vs. Zalgiris Kaunas** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Appalachian State vs. Akron** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **LSU vs. Arizona State** — needs 1 more confirmed dedicated backup feed(s).
- **NJIT vs. Manhattan** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Oklahoma State vs. Jackson State** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ole Miss vs. Arizona** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Texas A&M vs. Xavier** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Virginia vs. Marquette** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Bolton vs. West Bromwich** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Boreham Wood vs. Aldershot** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Burnley vs. Birmingham City** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Club Brugge KV vs. Liverpool FC** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Club Brugge vs. Liverpool** — needs 1 more confirmed dedicated backup feed(s).
- **Fleetwood vs. Leeds U21** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Harrogate vs. Kidderminster** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Hartlepool vs. Solihull Moors** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Inter Milan vs. VfB Stuttgart** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Inter vs. VfB Stuttgart** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Lille vs. Bayern Munich** — needs 1 more confirmed dedicated backup feed(s).
- **LOSC Lille vs. FC Bayern München** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Mantova vs. Arezzo** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Padova vs. Sampdoria** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Pisa vs. Modena** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Sabah FK vs. Barcelona** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Shakhtar Donetsk vs. Fenerbahçe** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Slavia Prague vs. Villarreal** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Stoke City vs. Millwall** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **VfB Stuttgart vs. Internazionale** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Watford vs. Blackburn Rovers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Almtuna vs. Visby Roma** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Kalmar vs. AIK** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Mora vs. Ostersund** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Nybro vs. Vasteras** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Sodertalje vs. Modo** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
