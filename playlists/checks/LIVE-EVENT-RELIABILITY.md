# Live-event reliability audit

- **Scrape snapshot:** 2026-11-25T14:27:54Z
- **Scrape run:** `20261125T141902Z-2970` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 0/11
- **Fixtures with a redundancy deficit:** 11

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| South Africa vs. Bangladesh (Cricket) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Club Brugge U19 vs. Liverpool U19 (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Kashima Antlers vs. Jeonbuk (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Nasaf Qarshi vs. Al Khalidiyah (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Persib Bandung vs. Seoul (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Sporting CP U19 vs. Manchester Utd U19 (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Ecuador U17 vs. South Korea U17 (World Cup U17) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Greece U17 vs. Qatar U17 (World Cup U17) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Haiti U17 vs. Saudi Arabia U17 (World Cup U17) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Panama U17 vs. Egypt U17 (World Cup U17) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Uganda U17 vs. New Caledonia U17 (World Cup U17) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **South Africa vs. Bangladesh** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Club Brugge U19 vs. Liverpool U19** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Kashima Antlers vs. Jeonbuk** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Nasaf Qarshi vs. Al Khalidiyah** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Persib Bandung vs. Seoul** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Sporting CP U19 vs. Manchester Utd U19** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ecuador U17 vs. South Korea U17** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Greece U17 vs. Qatar U17** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Haiti U17 vs. Saudi Arabia U17** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Panama U17 vs. Egypt U17** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Uganda U17 vs. New Caledonia U17** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
