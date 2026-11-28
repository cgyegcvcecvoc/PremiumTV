# Live-event reliability audit

- **Scrape snapshot:** 2026-11-28T09:04:50Z
- **Scrape run:** `20261128T085620Z-2993` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 0/16
- **Fixtures with a redundancy deficit:** 16

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Sydney W vs. Townsville W (Basketball WNBL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| New Zealand vs. India (Cricket) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Melbourne Renegades W vs. Sydney Sixers W (Cricket WBBL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Anaheim Ducks vs. Los Angeles Kings (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Buffalo Sabres vs. Pittsburgh Penguins (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Chicago Blackhawks vs. New York Rangers (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Columbus Blue Jackets vs. Detroit Red Wings (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Edmonton Oilers vs. Seattle Kraken (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Minnesota Wild vs. Colorado Avalanche (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| New York Islanders vs. Winnipeg Jets (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Philadelphia Flyers vs. Vancouver Canucks (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| San Jose Sharks vs. Vegas Golden Knights (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Tampa Bay Lightning vs. Ottawa Senators (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Washington Capitals vs. Florida Panthers (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Bucheon FC 1995 vs. Gimcheon Sangmu (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |
| Pohang vs. Gwangju FC (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9, doms9-events | **DEFICIT** |

## Deficits

- **Sydney W vs. Townsville W** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New Zealand vs. India** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Melbourne Renegades W vs. Sydney Sixers W** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Anaheim Ducks vs. Los Angeles Kings** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Buffalo Sabres vs. Pittsburgh Penguins** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Chicago Blackhawks vs. New York Rangers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Columbus Blue Jackets vs. Detroit Red Wings** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Edmonton Oilers vs. Seattle Kraken** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Minnesota Wild vs. Colorado Avalanche** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New York Islanders vs. Winnipeg Jets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Philadelphia Flyers vs. Vancouver Canucks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **San Jose Sharks vs. Vegas Golden Knights** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Tampa Bay Lightning vs. Ottawa Senators** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Washington Capitals vs. Florida Panthers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Bucheon FC 1995 vs. Gimcheon Sangmu** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Pohang vs. Gwangju FC** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
