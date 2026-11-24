# Live-event reliability audit

- **Scrape snapshot:** 2026-11-24T21:28:52Z
- **Scrape run:** `20261124T212355Z-3039` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 1/39
- **Fixtures with a redundancy deficit:** 38

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| Barcelona vs. Fenerbahce (Basketball Euroleague) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Lyon-Villeurbanne vs. Olimpia Milano (Basketball Euroleague) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Valencia vs. Panathinaikos (Basketball Euroleague) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Detroit vs. North Dakota (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Long Beach vs. Arkansas St. (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Miami vs. TCU (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Ole Miss vs. BYU (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Tennessee vs. Maryland (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Yale vs. Appalachian State (College Football) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Derby County vs. Wolverhampton Wanderers (ENG 2) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| West Ham United vs. Portsmouth (ENG 2) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Wrexham vs. Bristol City (ENG 2) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Barnet vs. Crawley Town (ENG 4) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| AEK Athens vs. Como (Soccer) | 2/2 | 2/2 | 0/1 | 2 | ISTRMEAST, STRMGATE | doms9 | **DEFICIT** |
| Arsenal vs. Borussia Dortmund (Soccer) | 2/2 | 2/2 | 0/1 | 2 | ISTRMEAST, STRMGATE | doms9 | **DEFICIT** |
| Bodo Glimt vs. LASK (Soccer) | 0/1 | 0/2 | 0/1 | 0 | unknown | doms9 | **DEFICIT** |
| Bristol City vs. Wrexham (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Bromley vs. Wycombe (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Cardiff City vs. Preston (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Charlton vs. Lincoln (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| FC Porto vs. Feyenoord Rotterdam (Soccer) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Feyenoord vs. FC Porto (Soccer) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Hibernian vs. Dundee FC (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Lens vs. RB Leipzig (Soccer) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Manchester City vs. SSC Napoli (Soccer) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Middlesbrough vs. Swansea City (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Napoli vs. Manchester City (Soccer) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Norwich City vs. QPR (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Portsmouth vs. West Ham (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Portsmouth vs. West Ham United (Soccer) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| PSV Eindhoven vs. Real Madrid (Soccer) | 2/2 | 2/2 | 0/1 | 2 | ISTRMEAST, STRMGATE | doms9 | **DEFICIT** |
| Rangers vs. Aberdeen (Soccer) | 3/3 | 2/2 | 1/1 | 3 | FAWA, ISTRMEAST | doms9 | **PASS** |
| RB Leipzig vs. RC Lens (Soccer) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Real Betis vs. Slovan Bratislava (Soccer) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Sheffield United vs. Southampton (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Stevenage vs. Sheffield Wednesday (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Wolverhampton vs. Derby County (Soccer) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Wolves vs. Derby County (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| ŠK Slovan Bratislava vs. Real Betis (Soccer) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |

## Deficits

- **Barcelona vs. Fenerbahce** — needs 1 more confirmed dedicated backup feed(s).
- **Lyon-Villeurbanne vs. Olimpia Milano** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Valencia vs. Panathinaikos** — needs 1 more confirmed dedicated backup feed(s).
- **Detroit vs. North Dakota** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Long Beach vs. Arkansas St.** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Miami vs. TCU** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Ole Miss vs. BYU** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Tennessee vs. Maryland** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Yale vs. Appalachian State** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Derby County vs. Wolverhampton Wanderers** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **West Ham United vs. Portsmouth** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Wrexham vs. Bristol City** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Barnet vs. Crawley Town** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **AEK Athens vs. Como** — needs 1 more confirmed dedicated backup feed(s).
- **Arsenal vs. Borussia Dortmund** — needs 1 more confirmed dedicated backup feed(s).
- **Bodo Glimt vs. LASK** — needs 2 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 2 more independent origin family/families.
- **Bristol City vs. Wrexham** — needs 1 more confirmed dedicated backup feed(s).
- **Bromley vs. Wycombe** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Cardiff City vs. Preston** — needs 1 more confirmed dedicated backup feed(s).
- **Charlton vs. Lincoln** — needs 1 more confirmed dedicated backup feed(s).
- **FC Porto vs. Feyenoord Rotterdam** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Feyenoord vs. FC Porto** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Hibernian vs. Dundee FC** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Lens vs. RB Leipzig** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Manchester City vs. SSC Napoli** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Middlesbrough vs. Swansea City** — needs 1 more confirmed dedicated backup feed(s).
- **Napoli vs. Manchester City** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Norwich City vs. QPR** — needs 1 more confirmed dedicated backup feed(s).
- **Portsmouth vs. West Ham** — needs 1 more confirmed dedicated backup feed(s).
- **Portsmouth vs. West Ham United** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **PSV Eindhoven vs. Real Madrid** — needs 1 more confirmed dedicated backup feed(s).
- **RB Leipzig vs. RC Lens** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Real Betis vs. Slovan Bratislava** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Sheffield United vs. Southampton** — needs 1 more confirmed dedicated backup feed(s).
- **Stevenage vs. Sheffield Wednesday** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Wolverhampton vs. Derby County** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Wolves vs. Derby County** — needs 1 more confirmed dedicated backup feed(s).
- **ŠK Slovan Bratislava vs. Real Betis** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
