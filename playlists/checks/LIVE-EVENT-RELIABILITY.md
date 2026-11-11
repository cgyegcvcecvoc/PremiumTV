# Live-event reliability audit

- **Generated:** 2026-11-11T23:49:37Z
- **Scrape run:** `20261111T234559Z-2953` — health check completed
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 0/24
- **Fixtures with a redundancy deficit:** 24

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Boston Celtics vs. Toronto Raptors (Basketball) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Cleveland Cavaliers vs. New York Knicks (Basketball) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Washington Wizards vs. Indiana Pacers (Basketball) | 1/1 | 1/2 | 0/1 | 1 | XYZ | doms9 | **DEFICIT** |
| Ball State vs. Buffalo (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Boston College Eagles vs. Massachusetts Lowell River Hawks (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Central Michigan vs. CS Sacramento (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Florida State Seminoles vs. West Florida Argonauts (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Michigan vs. Marquette (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Navy vs. Pennsylvania (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| St John vs. Colgate (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Syracuse Orange vs. Siena Saints (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Toledo vs. Massachusetts (College Football) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Indiana Pacers vs. Washington Wizards (NBA Basketball) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| New York Knicks vs. Cleveland Cavaliers (NBA Basketball) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Toronto Raptors vs. Boston Celtics (NBA Basketball) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Anaheim Ducks vs. Nashville Predators (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Buffalo Sabres vs. Tampa Bay Lightning (NHL Hockey) | 2/2 | 2/2 | 0/1 | 2 | FAWA, STRMGATE | doms9 | **DEFICIT** |
| Calgary Flames vs. New York Rangers (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Edmonton Oilers vs. Philadelphia Flyers (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| San Jose Sharks vs. Pittsburgh Penguins (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Vegas Golden Knights vs. Utah Mammoth (NHL Hockey) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Independiente vs. Always Ready (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Londrina vs. Nautico (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Quindio vs. Tigres (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **Boston Celtics vs. Toronto Raptors** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Cleveland Cavaliers vs. New York Knicks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Washington Wizards vs. Indiana Pacers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ball State vs. Buffalo** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Boston College Eagles vs. Massachusetts Lowell River Hawks** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Central Michigan vs. CS Sacramento** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Florida State Seminoles vs. West Florida Argonauts** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Michigan vs. Marquette** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Navy vs. Pennsylvania** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **St John vs. Colgate** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Syracuse Orange vs. Siena Saints** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Toledo vs. Massachusetts** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Indiana Pacers vs. Washington Wizards** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **New York Knicks vs. Cleveland Cavaliers** — needs 1 more confirmed dedicated backup feed(s).
- **Toronto Raptors vs. Boston Celtics** — needs 1 more confirmed dedicated backup feed(s).
- **Anaheim Ducks vs. Nashville Predators** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Buffalo Sabres vs. Tampa Bay Lightning** — needs 1 more confirmed dedicated backup feed(s).
- **Calgary Flames vs. New York Rangers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Edmonton Oilers vs. Philadelphia Flyers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **San Jose Sharks vs. Pittsburgh Penguins** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Vegas Golden Knights vs. Utah Mammoth** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Independiente vs. Always Ready** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Londrina vs. Nautico** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Quindio vs. Tigres** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` means the latest checked scrape received stream-shaped data; it is a point-in-time result.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
