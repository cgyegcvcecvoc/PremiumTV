# Live-event reliability audit

- **Scrape snapshot:** 2026-11-20T00:01:22Z
- **Scrape run:** `20261119T235748Z-2955` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 0/36
- **Fixtures with a redundancy deficit:** 36

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Indianapolis Colts vs. Houston Texans (American Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Bayern Munchen vs. Baskonia (Basketball Euroleague) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Olimpia Milano vs. Fenerbahce (Basketball Euroleague) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Paris vs. Hapoel Tel Aviv (Basketball Euroleague) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Valencia vs. Virtus Bologna (Basketball Euroleague) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Zalgiris Kaunas vs. Panathinaikos (Basketball Euroleague) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Florida Gators vs. Florida Atlantic Owls (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| NC State vs. Murray St. (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| North Carolina Tar Heels vs. Texas Tech Red Raiders (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Notre Dame vs. Auburn (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Notre Dame vs. Auburn Tigers (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Rice Owls vs. Temple Owls (College Football) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Virginia Cavaliers vs. James Madison Dukes (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| New Zealand vs. India (Cricket) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| ZED vs. Smouha (Egypt Cup) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Grenoble FC vs. Provence Rugby (France Rugby Pro D2) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Golden State Warriors vs. Memphis Grizzlies (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Los Angeles Clippers vs. San Antonio Spurs (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| New York Knicks vs. Minnesota Timberwolves (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Portland Trail Blazers vs. Milwaukee Bucks (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | GSPORTS | doms9 | **DEFICIT** |
| Buffalo Sabres vs. Washington Capitals (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Los Angeles Kings vs. Toronto Maple Leafs (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Montreal Canadiens vs. Carolina Hurricanes (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Philadelphia Flyers vs. Ottawa Senators (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| St. Louis Blues vs. Pittsburgh Penguins (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Arsenal W vs. OL Lyonnes W (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Ind Valle del Cauca vs. Envigado (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| U Magdalena vs. Boca Juniors (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Vasco vs. Internacional (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Vitoria vs. Bragantino (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Brynas vs. Lulea (Sweden Hockey SHL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Djurgarden vs. Skelleftea (Sweden Hockey SHL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Farjestad vs. Frolunda (Sweden Hockey SHL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Linkoping vs. HV (Sweden Hockey SHL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Malmo vs. Rogle (Sweden Hockey SHL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Vaxjo vs. IF Bjorkloven (Sweden Hockey SHL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **Indianapolis Colts vs. Houston Texans** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Bayern Munchen vs. Baskonia** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Olimpia Milano vs. Fenerbahce** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Paris vs. Hapoel Tel Aviv** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Valencia vs. Virtus Bologna** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Zalgiris Kaunas vs. Panathinaikos** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Florida Gators vs. Florida Atlantic Owls** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **NC State vs. Murray St.** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **North Carolina Tar Heels vs. Texas Tech Red Raiders** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Notre Dame vs. Auburn** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Notre Dame vs. Auburn Tigers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Rice Owls vs. Temple Owls** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Virginia Cavaliers vs. James Madison Dukes** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Zealand vs. India** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **ZED vs. Smouha** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Grenoble FC vs. Provence Rugby** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Golden State Warriors vs. Memphis Grizzlies** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Los Angeles Clippers vs. San Antonio Spurs** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New York Knicks vs. Minnesota Timberwolves** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Portland Trail Blazers vs. Milwaukee Bucks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Buffalo Sabres vs. Washington Capitals** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Los Angeles Kings vs. Toronto Maple Leafs** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Montreal Canadiens vs. Carolina Hurricanes** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Philadelphia Flyers vs. Ottawa Senators** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **St. Louis Blues vs. Pittsburgh Penguins** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Arsenal W vs. OL Lyonnes W** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ind Valle del Cauca vs. Envigado** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **U Magdalena vs. Boca Juniors** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Vasco vs. Internacional** — needs 1 more confirmed dedicated backup feed(s).
- **Vitoria vs. Bragantino** — needs 1 more confirmed dedicated backup feed(s).
- **Brynas vs. Lulea** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Djurgarden vs. Skelleftea** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Farjestad vs. Frolunda** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Linkoping vs. HV** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Malmo vs. Rogle** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Vaxjo vs. IF Bjorkloven** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
