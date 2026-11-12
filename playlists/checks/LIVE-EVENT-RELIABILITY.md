# Live-event reliability audit

- **Scrape snapshot:** 2026-11-12T16:49:35Z
- **Scrape run:** `20261112T164557Z-3170` — health check completed
- **Exact-URL evidence:** unavailable (legacy or incomplete scrape)
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 0/9
- **Fixtures with a redundancy deficit:** 9

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| DR Congo vs. Sierra Leone (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Equatorial Guinea vs. Zimbabwe (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| France U20 vs. Denmark U20 (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Ghana vs. Somalia (Soccer) | 0/2 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Guinea vs. Eritrea (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Italy U20 vs. Portugal U20 (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Madagascar vs. Guinea Bissau (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Turkey vs. Belgium (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Uzbekistan vs. Russia (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |

## Deficits

- **DR Congo vs. Sierra Leone** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Equatorial Guinea vs. Zimbabwe** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **France U20 vs. Denmark U20** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Ghana vs. Somalia** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Guinea vs. Eritrea** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Italy U20 vs. Portugal U20** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Madagascar vs. Guinea Bissau** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Turkey vs. Belgium** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Uzbekistan vs. Russia** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
