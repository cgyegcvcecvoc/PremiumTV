# Local-market reference data

`scripts/build_local_channels.py` answers one question offline: *which of the
published local stations belong to the viewer's market?* It needs three things
that an M3U playlist cannot carry — which market each callsign serves, where
that market is, and which ZIP codes and place names belong to it. Those live
here as small CSV tables so the answer never depends on a network call, a
geocoder or a viewer's IP address.

| File | Rows | Shape | Used for |
|---|---|---|---|
| `us-tv-markets.csv` | 2,333 | `callsign,city,state,market_code` | WGAL → Lancaster PA / `USLNS` |
| `us-markets.csv` | 856 | `market_code,city,state,latitude,longitude` | the market's own city and position |
| `us-zip3.csv` | 912 | `prefix,state,latitude,longitude` | ZIP code → state + a point to measure from |
| `us-places.csv` | 29,542 | `state,place,latitude,longitude` | a typed city name → a point |

Nothing here is a channel list. These are geography and station-identity
tables; the stations themselves still come from `playlists/live/USA.m3u`, so a
feed that stops working drops out of the local directory on the next run just
like it drops out of every other published playlist.

## Provenance

Both upstream sources are public domain, and the tables above are derived
copies rather than mirrors:

- **Station identity** — the callsign → market mapping is derived from
  [`iptv-org/database`](https://github.com/iptv-org/database) (`feeds.csv`
  `broadcast_area`, whose `ct/US…` codes are the market codes, plus
  `cities.csv` for the market city and state). That repository is released
  into the public domain (Unlicense). Only the derived three-column table is
  stored here; the upstream files are not vendored.
- **ZIP codes and place positions** — derived from the geonames.org US postal
  code set as packaged by
  [`zauberware/postal-codes-json-xml-csv`](https://github.com/zauberware/postal-codes-json-xml-csv),
  which is licensed CC BY 4.0 (© geonames.org). The derived tables here keep
  that attribution, and `us-places.csv` is a name → centroid summary, not a
  copy of the postal-code database.

## Budget

The four tables total about 1 MB, and `playlists/local-channels.json` (the only
file the apps ship) stays around 215 KB because it holds just the 89 markets
PremiumTV actually publishes stations for. `us-places.csv` is the largest file
and is read only at build time — no app downloads it.

## Regenerating

Neither upstream source is fetched at build time: these tables are versioned
data, changed deliberately, so a scraped playlist can never silently move a
station to a different market. To refresh one, rebuild it from the upstream
source named above with the same columns and run:

```bash
python scripts/build_local_channels.py
python -m unittest tests.test_local_channels
```

`python scripts/build_local_channels.py --check` fails CI when the committed
`playlists/local-channels.json` no longer matches the tables and the playlist.

## Known gaps

- A ZIP prefix is filed under a market only when that market is within 120 km
  of the prefix's area (`NEAREST_MARKET_MAX_KM`, shared with the apps). Beyond
  that the prefix has no market and the apps say so, instead of naming the
  state's nearest market (1.1.21: Wilkes-Barre was reading as Philadelphia).
  A Lancaster ZIP still reads as Philadelphia (~95 km) until a Lancaster
  station (WGAL) has a working feed in `playlists/sources/local-channels.m3u`.
- Only stations PremiumTV actually publishes get a market, so a state with no
  carried affiliate (for example Wyoming or Vermont today) answers honestly
  with "no local stations yet" instead of borrowing a neighbouring market.
- A handful of stations broadcast in two markets (107 of the 2,336 callsigns in
  the upstream database). The table keeps the larger market, which is the
  station's primary licence in every case checked.
- `us-places.csv` keeps well-known English spellings ("St. Paul"), not
  alternative names; `scripts/build_local_channels.py` normalises typed
  spellings (Saint/St, Fort/Ft, Mount/Mt, punctuation) so both forms match.
