# Live-event reliability audit

- **Scrape snapshot:** 2026-11-16T21:11:27Z
- **Scrape run:** `20261116T210729Z-3433` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 5/16
- **Fixtures with a redundancy deficit:** 11

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| UTEP vs. Florida A&M (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Albacete vs. Celta Vigo B (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Andorra vs. Azerbaijan (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Cajamarca vs. Los Chankas (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Cusco vs. AD Tarma (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| England U21 vs. France U21 (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Germany vs. Netherlands (Soccer) | 6/6 | 2/2 | 4/1 | 5 | DAMITV, FAWA, ISTRMEAST, STRMGATE, XYZ | doms9 | **PASS** |
| Gibraltar vs. Malta (Soccer) | 6/6 | 2/2 | 4/1 | 6 | DAMITV, FAWA, ISTRMEAST, STRMGATE, XYZ | doms9 | **PASS** |
| Greece U21 vs. Iceland U21 (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Greece vs. Serbia (Soccer) | 5/5 | 2/2 | 3/1 | 5 | DAMITV, FAWA, ISTRMEAST, STRMGATE, XYZ | doms9 | **PASS** |
| Guyana vs. Puerto Rico (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Hungary U21 vs. Cyprus U21 (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Moquegua vs. Grau (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| North Macedonia vs. Slovenia (Soccer) | 5/5 | 2/2 | 3/1 | 5 | DAMITV, FAWA, ISTRMEAST, STRMGATE, XYZ | doms9 | **PASS** |
| Switzerland vs. Scotland (Soccer) | 6/6 | 2/2 | 4/1 | 5 | DAMITV, FAWA, ISTRMEAST, STRMGATE, XYZ | doms9 | **PASS** |
| Ostersund vs. Visby Roma (Sweden HockeyAllsvenskan) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **UTEP vs. Florida A&M** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Albacete vs. Celta Vigo B** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Andorra vs. Azerbaijan** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Cajamarca vs. Los Chankas** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Cusco vs. AD Tarma** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **England U21 vs. France U21** — needs 1 more confirmed dedicated backup feed(s).
- **Greece U21 vs. Iceland U21** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Guyana vs. Puerto Rico** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Hungary U21 vs. Cyprus U21** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Moquegua vs. Grau** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ostersund vs. Visby Roma** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
