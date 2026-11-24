# Live-event reliability audit

- **Scrape snapshot:** 2026-11-24T11:04:11Z
- **Scrape run:** `20261124T105912Z-2993` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 0/11
- **Fixtures with a redundancy deficit:** 11

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Sacramento Kings vs. San Antonio Spurs (Basketball) | 2/2 | 2/2 | 0/1 | 1 | SPRTSBITE | doms9 | **DEFICIT** |
| Minnesota Wild vs. San Jose Sharks (Hockey) | 1/1 | 1/2 | 0/1 | 1 | SPRTSBITE | doms9 | **DEFICIT** |
| San Antonio Spurs vs. Sacramento Kings (NBA Basketball) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Utah Jazz vs. Los Angeles Lakers (NBA Basketball) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Montreal Canadiens vs. Los Angeles Kings (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| New Jersey Devils vs. Columbus Blue Jackets (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| New York Islanders vs. Toronto Maple Leafs (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Ottawa Senators vs. Calgary Flames (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| San Jose Sharks vs. Minnesota Wild (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Seattle Kraken vs. Anaheim Ducks (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Winnipeg Jets vs. Utah Mammoth (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **Sacramento Kings vs. San Antonio Spurs** — needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Minnesota Wild vs. San Jose Sharks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **San Antonio Spurs vs. Sacramento Kings** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Utah Jazz vs. Los Angeles Lakers** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Montreal Canadiens vs. Los Angeles Kings** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Jersey Devils vs. Columbus Blue Jackets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New York Islanders vs. Toronto Maple Leafs** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ottawa Senators vs. Calgary Flames** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **San Jose Sharks vs. Minnesota Wild** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Seattle Kraken vs. Anaheim Ducks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Winnipeg Jets vs. Utah Mammoth** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
