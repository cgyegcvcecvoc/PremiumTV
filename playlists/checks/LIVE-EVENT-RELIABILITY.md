# Live-event reliability audit

- **Generated:** 2026-11-12T19:03:28Z
- **Scrape run:** `20261112T190011Z-2983` — health check completed
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 2/21
- **Fixtures with a redundancy deficit:** 19

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Seattle Kraken vs. Carolina Hurricanes (National Hockey League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Türkiye vs. Belgium (Nations League) | 1/1 | 1/2 | 0/1 | 1 | DAMITV | doms9 | **DEFICIT** |
| Carolina Hurricanes vs. Seattle Kraken (NHL Hockey) | 4/4 | 2/2 | 2/1 | 4 | FAWA, ISTRMEAST, MP66, STRMGATE | doms9 | **PASS** |
| Arsenal vs. Barcelona (Soccer) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Barcelona W vs. Arsenal W (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Belgium vs. Türkiye (Soccer) | 2/2 | 2/2 | 0/1 | 2 | ISTRMEAST, STRMGATE | doms9 | **DEFICIT** |
| Cyprus vs. Armenia (Soccer) | 3/3 | 2/2 | 1/1 | 3 | DAMITV, ISTRMEAST, STRMGATE | doms9 | **PASS** |
| Guinea vs. Eritrea (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Lithuania vs. Suriname (Soccer) | 2/2 | 2/2 | 0/1 | 2 | DAMITV, FAWA | doms9 | **DEFICIT** |
| Malta vs. Eswatini (Soccer) | 2/2 | 2/2 | 0/1 | 2 | DAMITV, FAWA | doms9 | **DEFICIT** |
| Navalcarnero vs. Real Betis (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Puertollano vs. Albacete (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Tarancon vs. Levante (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Torreense W vs. Sparta Prague W (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Brynas vs. Skelleftea (Sweden Hockey SHL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Farjestad vs. Djurgarden (Sweden Hockey SHL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Frolunda vs. Malmo (Sweden Hockey SHL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| HV vs. Lulea (Sweden Hockey SHL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| IF Bjorkloven vs. Orebro (Sweden Hockey SHL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Linkoping vs. Rogle (Sweden Hockey SHL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Vaxjo vs. Timra (Sweden Hockey SHL) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **Seattle Kraken vs. Carolina Hurricanes** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Türkiye vs. Belgium** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Arsenal vs. Barcelona** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Barcelona W vs. Arsenal W** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Belgium vs. Türkiye** — needs 1 more confirmed dedicated backup feed(s).
- **Guinea vs. Eritrea** — needs 1 more confirmed dedicated backup feed(s).
- **Lithuania vs. Suriname** — needs 1 more confirmed dedicated backup feed(s).
- **Malta vs. Eswatini** — needs 1 more confirmed dedicated backup feed(s).
- **Navalcarnero vs. Real Betis** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Puertollano vs. Albacete** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Tarancon vs. Levante** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Torreense W vs. Sparta Prague W** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Brynas vs. Skelleftea** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Farjestad vs. Djurgarden** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Frolunda vs. Malmo** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **HV vs. Lulea** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **IF Bjorkloven vs. Orebro** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Linkoping vs. Rogle** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Vaxjo vs. Timra** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` means the latest checked scrape received stream-shaped data; it is a point-in-time result.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
