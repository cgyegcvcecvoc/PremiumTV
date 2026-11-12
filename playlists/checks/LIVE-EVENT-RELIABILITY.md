# Live-event reliability audit

- **Generated:** 2026-11-12T21:38:45Z
- **Scrape run:** `20261112T213505Z-2947` — health check completed
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 6/17
- **Fixtures with a redundancy deficit:** 11

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Maccabi Tel Aviv vs. Hapoel Tel Aviv (Basketball Euroleague) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Olimpia Milano vs. Zalgiris Kaunas (Basketball Euroleague) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Olympiacos vs. Dubai (Basketball Euroleague) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Real Madrid vs. Crvena Zvezda (Basketball Euroleague) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Valencia vs. Bayern Munchen (Basketball Euroleague) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Brown Bears vs. Holy Cross Crusaders (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Czechia vs. Spain (Nations League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Seattle Kraken vs. Carolina Hurricanes (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Croatia vs. England (Soccer) | 5/5 | 2/2 | 3/1 | 4 | DAMITV, FAWA, ISTRMEAST, STRMGATE | doms9 | **PASS** |
| Czech Republic vs. Spain (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Czechia vs. Spain (Soccer) | 3/3 | 2/2 | 1/1 | 2 | ISTRMEAST, STRMGATE | doms9 | **PASS** |
| Dep Pasto vs. Junior (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Finland vs. Albania (Soccer) | 5/5 | 2/2 | 3/1 | 5 | DAMITV, FAWA, ISTRMEAST, STRMGATE | doms9 | **PASS** |
| France vs. Italy (Soccer) | 6/6 | 2/2 | 4/1 | 4 | DAMITV, FAWA, ISTRMEAST, STRMGATE | doms9 | **PASS** |
| Latvia vs. Montenegro (Soccer) | 5/5 | 2/2 | 3/1 | 5 | DAMITV, FAWA, ISTRMEAST, STRMGATE | doms9 | **PASS** |
| San Marino vs. Belarus (Soccer) | 4/4 | 2/2 | 2/1 | 4 | DAMITV, FAWA, ISTRMEAST | doms9 | **PASS** |
| SL Benfica W vs. Austria Vienna W (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **Maccabi Tel Aviv vs. Hapoel Tel Aviv** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Olimpia Milano vs. Zalgiris Kaunas** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Olympiacos vs. Dubai** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Real Madrid vs. Crvena Zvezda** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Valencia vs. Bayern Munchen** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Brown Bears vs. Holy Cross Crusaders** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Czechia vs. Spain** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Seattle Kraken vs. Carolina Hurricanes** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Czech Republic vs. Spain** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Dep Pasto vs. Junior** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **SL Benfica W vs. Austria Vienna W** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` means the latest checked scrape received stream-shaped data; it is a point-in-time result.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
