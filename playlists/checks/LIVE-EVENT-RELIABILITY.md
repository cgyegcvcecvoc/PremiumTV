# Live-event reliability audit

- **Scrape snapshot:** 2026-11-22T16:17:05Z
- **Scrape run:** `20261122T161230Z-2975` — health check completed
- **Exact-URL evidence:** available
- **Policy:** 3 confirmed, distinct feeds per fixture (two primaries + one dedicated backup), across at least 2 origin families
- **Fixtures meeting policy:** 2/37
- **Fixtures with a redundancy deficit:** 35

> Duplicate URLs count once. Provider labels, origin families, and ingest source files are reported separately; a mirror of the same feed is never padded into another backup.

| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |
|---|---:|---|---|---:|---|---|---|
| West Ham United vs. Arsenal (ENG W 1) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Fortuna Sittard vs. Go Ahead Eagles (NED 1) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Angers vs. Paris FC (Soccer) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Arsenal W vs. West Ham W (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Augsburg vs. Mainz (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Beerschot VA vs. Genk U23 (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Bologna vs. Udinese (Soccer) | 2/2 | 2/2 | 0/1 | 2 | KINGDOME, STRMGATE | doms9 | **DEFICIT** |
| Brommapojkarna vs. Halmstad (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| FC Augsburg vs. 1. FSV Mainz (Soccer) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| FC Basel vs. Luzern (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| GA Eagles vs. Fortuna Sittard (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Gijon vs. Las Palmas (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Hull City vs. Brighton & Hove Albion (Soccer) | 4/4 | 2/2 | 2/1 | 3 | KINGDOME, SPRTSBITE, STRMGATE | doms9 | **PASS** |
| Kagera Sugar vs. TRA United (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Karmiotissa vs. AEL Limassol (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Kortrijk vs. Royale Union SG (Soccer) | 2/2 | 2/2 | 0/1 | 2 | FAWA | doms9 | **DEFICIT** |
| Kosice vs. Skalica (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Lausanne vs. Vaduz (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Liverpool vs. Manchester United (Soccer) | 2/2 | 2/2 | 0/1 | 2 | KINGDOME, STRMGATE | doms9 | **DEFICIT** |
| Lorient vs. Rennes (Soccer) | 2/2 | 2/2 | 0/1 | 2 | KINGDOME, STRMGATE | doms9 | **DEFICIT** |
| Milan vs. Frosinone (Soccer) | 1/1 | 1/2 | 0/1 | 1 | KINGDOME | doms9 | **DEFICIT** |
| Nyiregyhaza vs. Debrecen (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Panathinaikos vs. OFI Crete (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Panetolikos vs. Volos (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Paris vs. Angers SCO (Soccer) | 1/1 | 1/2 | 0/1 | 1 | KINGDOME | doms9 | **DEFICIT** |
| Racing Santander vs. Real Sociedad (Soccer) | 4/4 | 2/2 | 2/1 | 4 | FAWA, KINGDOME, STRMGATE | doms9 | **PASS** |
| RB Leipzig W vs. Wolfsburg W (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Real Racing Club vs. Real Sociedad (Soccer) | 1/1 | 1/2 | 0/1 | 1 | ISTRMEAST | doms9 | **DEFICIT** |
| Saarbrucken vs. Wehen (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Sassuolo vs. Genoa (Soccer) | 1/1 | 1/2 | 0/1 | 1 | KINGDOME | doms9 | **DEFICIT** |
| Sonderjyske vs. Odense (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| UTA Arad vs. Univ Craiova (Soccer) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Eyupspor vs. Trabzonspor (TUR 1) | 1/1 | 1/2 | 0/1 | 1 | STRMGATE | doms9 | **DEFICIT** |
| Argentina U17 vs. Mozambique U17 (World Cup U17) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Qatar U17 vs. Egypt U17 (World Cup U17) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| South Korea U17 vs. New Caledonia U17 (World Cup U17) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |
| Uruguay U17 vs. Haiti U17 (World Cup U17) | 1/1 | 1/2 | 0/1 | 1 | FAWA | doms9 | **DEFICIT** |

## Deficits

- **West Ham United vs. Arsenal** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Fortuna Sittard vs. Go Ahead Eagles** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Angers vs. Paris FC** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Arsenal W vs. West Ham W** — needs 1 more confirmed dedicated backup feed(s).
- **Augsburg vs. Mainz** — needs 1 more confirmed dedicated backup feed(s).
- **Beerschot VA vs. Genk U23** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Bologna vs. Udinese** — needs 1 more confirmed dedicated backup feed(s).
- **Brommapojkarna vs. Halmstad** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **FC Augsburg vs. 1. FSV Mainz** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **FC Basel vs. Luzern** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **GA Eagles vs. Fortuna Sittard** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Gijon vs. Las Palmas** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Kagera Sugar vs. TRA United** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Karmiotissa vs. AEL Limassol** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Kortrijk vs. Royale Union SG** — needs 1 more confirmed dedicated backup feed(s).
- **Kosice vs. Skalica** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Lausanne vs. Vaduz** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Liverpool vs. Manchester United** — needs 1 more confirmed dedicated backup feed(s).
- **Lorient vs. Rennes** — needs 1 more confirmed dedicated backup feed(s).
- **Milan vs. Frosinone** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Nyiregyhaza vs. Debrecen** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Panathinaikos vs. OFI Crete** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Panetolikos vs. Volos** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Paris vs. Angers SCO** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **RB Leipzig W vs. Wolfsburg W** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Real Racing Club vs. Real Sociedad** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Saarbrucken vs. Wehen** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Sassuolo vs. Genoa** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Sonderjyske vs. Odense** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **UTA Arad vs. Univ Craiova** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Eyupspor vs. Trabzonspor** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Argentina U17 vs. Mozambique U17** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Qatar U17 vs. Egypt U17** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **South Korea U17 vs. New Caledonia U17** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.
- **Uruguay U17 vs. Haiti U17** — needs 1 more confirmed primary feed(s); needs 1 more confirmed dedicated backup feed(s); needs 1 more independent origin family/families.

## Interpretation

- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.
- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.
- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.
- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.
