# Live-event reliability audit

- **Scrape snapshot:** 2026-11-26T09:41:58Z
- **Scrape run:** `20261126T093407Z-2986` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 0/24
- **Fixtures with a redundancy deficit:** 24

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Phoenix Suns vs. Houston Rockets (Basketball) | 0/3 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Sacramento Kings vs. Golden State Warriors (Basketball) | 0/2 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| San Antonio Spurs vs. Portland Trail Blazers (Basketball) | 0/2 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Melbourne Renegades W vs. Sydney Sixers W (Cricket WBBL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Chicago Blackhawks vs. Seattle Kraken (Ice Hockey) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Montreal Canadiens vs. Colorado Avalanche (Ice Hockey) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| San Jose Sharks vs. Anaheim Ducks (Ice Hockey) | 0/2 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Vancouver Canucks vs. Detroit Red Wings (Ice Hockey) | 0/2 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Winnipeg Jets vs. Boston Bruins (Ice Hockey) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| San Antonio Spurs vs. Portland Trail Blazers (NBA Basketball) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Anaheim Ducks vs. San Jose Sharks (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Boston Bruins vs. Winnipeg Jets (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Buffalo Sabres vs. New York Rangers (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Colorado Avalanche vs. Montreal Canadiens (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Dallas Stars vs. Nashville Predators (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Detroit Red Wings vs. Vancouver Canucks (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Florida Panthers vs. Ottawa Senators (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Minnesota Wild vs. Utah Mammoth (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Montréal Canadiens vs. Colorado Avalanche (NHL Hockey) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| New York Islanders vs. St Louis Blues (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Pittsburgh Penguins vs. Calgary Flames (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Seattle Kraken vs. Chicago Blackhawks (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Tampa Bay Lightning vs. Carolina Hurricanes (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Washington Capitals vs. Philadelphia Flyers (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **Phoenix Suns vs. Houston Rockets** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Sacramento Kings vs. Golden State Warriors** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **San Antonio Spurs vs. Portland Trail Blazers** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Melbourne Renegades W vs. Sydney Sixers W** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Chicago Blackhawks vs. Seattle Kraken** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Montreal Canadiens vs. Colorado Avalanche** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **San Jose Sharks vs. Anaheim Ducks** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Vancouver Canucks vs. Detroit Red Wings** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Winnipeg Jets vs. Boston Bruins** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **San Antonio Spurs vs. Portland Trail Blazers** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Anaheim Ducks vs. San Jose Sharks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Boston Bruins vs. Winnipeg Jets** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Buffalo Sabres vs. New York Rangers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Colorado Avalanche vs. Montreal Canadiens** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Dallas Stars vs. Nashville Predators** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Detroit Red Wings vs. Vancouver Canucks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Florida Panthers vs. Ottawa Senators** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Minnesota Wild vs. Utah Mammoth** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Montréal Canadiens vs. Colorado Avalanche** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **New York Islanders vs. St Louis Blues** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Pittsburgh Penguins vs. Calgary Flames** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Seattle Kraken vs. Chicago Blackhawks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Tampa Bay Lightning vs. Carolina Hurricanes** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Washington Capitals vs. Philadelphia Flyers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
