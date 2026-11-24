# Live-event reliability audit

- **Scrape snapshot:** 2026-11-24T05:36:04Z
- **Scrape run:** `20261124T053018Z-2995` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 3/14
- **Fixtures with a redundancy deficit:** 11

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Sacramento Kings vs. San Antonio Spurs (Basketball) | 2/2 | 2/2 | 0/1 | 1 | SPRTSBITE | doms9 | **DEFICIT** |
| Minnesota Wild vs. San Jose Sharks (Hockey) | 1/1 | 1/2 | 0/1 | 1 | SPRTSBITE | doms9 | **DEFICIT** |
| LA Clippers vs. Houston Rockets (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Los Angeles Lakers vs. Utah Jazz (NBA Basketball) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66 | doms9 | **PASS** |
| Sacramento Kings vs. San Antonio Spurs (NBA Basketball) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, MP66 | doms9 | **PASS** |
| Montreal Canadiens vs. Los Angeles Kings (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| New Jersey Devils vs. Columbus Blue Jackets (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| New York Islanders vs. Toronto Maple Leafs (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Ottawa Senators vs. Calgary Flames (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| San Jose Sharks vs. Minnesota Wild (NHL Hockey) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST, MP66 | doms9 | **PASS** |
| Seattle Kraken vs. Anaheim Ducks (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, ISTRMEAST | doms9 | **DEFICIT** |
| Winnipeg Jets vs. Utah Mammoth (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Albion vs. Danubio (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| St Louis City vs. Los Angeles FCFC (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **Sacramento Kings vs. San Antonio Spurs** — needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Minnesota Wild vs. San Jose Sharks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **LA Clippers vs. Houston Rockets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Montreal Canadiens vs. Los Angeles Kings** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Jersey Devils vs. Columbus Blue Jackets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New York Islanders vs. Toronto Maple Leafs** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ottawa Senators vs. Calgary Flames** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Seattle Kraken vs. Anaheim Ducks** — needs 1 more confirmed dedicated backup feed(s).
- **Winnipeg Jets vs. Utah Mammoth** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Albion vs. Danubio** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **St Louis City vs. Los Angeles FCFC** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
