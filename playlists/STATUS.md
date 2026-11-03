# Scraper status

- **Last run:** 2026-11-02 07:10 PM EST (2026-11-03 00:10 UTC)
- **Run:** _12:53 PM recheck_ (`recheck`; ID `20261103T000623Z-2881`)
- **Scheduled for:** 2026-11-02T17:53:00Z — started late by +6h 13m
- **Outcome:** **WARNING**
- **Confirmed working:** 12101 / 16982 unique links
- **Dead:** 1959  |  **Unverified:** 2922
- **Retained (unverified, within grace):** 183 previously published links kept so their channels do not vanish after one unverifiable run
- **Unique links found:** 16982 from 21384 source entries
- **Changes vs. PremiumTV_all.m3u:** +227 added / -305 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (171 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (70 confirmed working / 75 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 669 |
| 2 | Sports Backups | 2 |
| 3 | Lifestyle | 532 |
| 4 | Fox Channels | 21 |
| 5 | CBS | 38 |
| 6 | NBC | 60 |
| 7 | NBC Sports Channels | 8 |
| 8 | Cartoons | 194 |
| 9 | PBS | 20 |
| 10 | Game Shows | 19 |
| 11 | News | 1025 |
| 12 | Movies | 997 |
| 13 | Music | 907 |
| 14 | Entertainment | 874 |
| 15 | International | 832 |
| 16 | Europe | 817 |
| 17 | Religious | 675 |
| 18 | Series | 523 |
| 19 | South America | 505 |
| 20 | Asia | 500 |
| 21 | Documentary | 416 |
| 22 | Kids | 386 |
| 23 | United States | 370 |
| 24 | North America | 294 |
| 25 | Comedy | 180 |
| 26 | Education | 136 |
| 27 | Culture | 130 |
| 28 | Legislative | 104 |
| 29 | India | 86 |
| 30 | Classic TV | 78 |
| 31 | Business | 69 |
| 32 | Africa | 68 |
| 33 | A&E Networks | 49 |
| 34 | Family | 36 |
| 35 | UK | 31 |
| 36 | Auto | 24 |
| 37 | Canada | 24 |
| 38 | Weather | 17 |
| 39 | DLTV | 15 |
| 40 | Online TV | 15 |
| 41 | Animals & Nature | 13 |
| 42 | Australia | 13 |
| 43 | Tv Reality | 13 |
| 44 | Global TV | 12 |
| 45 | Public TV | 12 |
| 46 | Tv Paranormal | 11 |
| 47 | Tv Celebrities | 9 |
| 48 | Aria Web Channels | 6 |
| 49 | Tv Shows | 6 |
| 50 | Oceania | 5 |
| 51 | Relax | 5 |
| 52 | Shopping | 2 |
| 53 | 3-Radio#Chicago | 1 |
| 54 | IPTV | 1 |
| 55 | Live TV | 1 |
| 56 | MeTV | 1 |
| 57 | TEST | 1 |
| 58 | United Kingdom | 1 |
| 59 | USA Channels | 1 |
| 60 | Other | 424 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 4 | 4 | 3 | 2 | 2 | 0 |
| priority-channels | ok | 19 | 19 | 12 | 19 | 0 | 0 |
| ae-networks | ok | 53 | 53 | 16 | 49 | 1 | 3 |
| aria | ok | 290 | 286 | 86 | 212 | 18 | 56 |
| doms9 | ok | 462 | 456 | 88 | 233 | 71 | 152 |
| xtemus | ok | 317 | 317 | 0 | 31 | 111 | 175 |
| iptv-org | ok | 11399 | 11399 | 3690 | 8207 | 1155 | 2037 |
| free-tv | ok | 2065 | 2041 | 811 | 1197 | 402 | 442 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| VIP-m3u-playlist 🌱 | ok | 211 | 210 | 100 | 204 | 3 | 3 |
| israel-tv-plus 🌱 | ok | 297 | 274 | 59 | 115 | 79 | 80 |
| m3u 🌱 | ok | 839 | 835 | 174 | 667 | 83 | 84 |
| openstream 🌱 | ok | 5428 | 5428 | 3160 | 5088 | 315 | 25 |

🌱 = source added automatically by the monthly discovery engine: VIP-m3u-playlist, israel-tv-plus, m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **12284** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 669 | 5.4% |
| Sports Backups | 2 | 0.0% |
| Lifestyle | 532 | 4.3% |
| Fox Channels | 21 | 0.2% |
| CBS | 38 | 0.3% |
| NBC | 60 | 0.5% |
| NBC Sports Channels | 8 | 0.1% |
| Cartoons | 194 | 1.6% |
| PBS | 20 | 0.2% |
| Game Shows | 19 | 0.2% |
| News | 1025 | 8.3% |
| Movies | 997 | 8.1% |
| Music | 907 | 7.4% |
| Entertainment | 874 | 7.1% |
| International | 832 | 6.8% |
| Europe | 817 | 6.7% |
| Religious | 675 | 5.5% |
| Series | 523 | 4.3% |
| South America | 505 | 4.1% |
| Asia | 500 | 4.1% |
| Documentary | 416 | 3.4% |
| Kids | 386 | 3.1% |
| United States | 370 | 3.0% |
| North America | 294 | 2.4% |
| Comedy | 180 | 1.5% |
| Education | 136 | 1.1% |
| Culture | 130 | 1.1% |
| Legislative | 104 | 0.8% |
| India | 86 | 0.7% |
| Classic TV | 78 | 0.6% |
| Business | 69 | 0.6% |
| Africa | 68 | 0.6% |
| A&E Networks | 49 | 0.4% |
| Family | 36 | 0.3% |
| UK | 31 | 0.3% |
| Auto | 24 | 0.2% |
| Canada | 24 | 0.2% |
| Weather | 17 | 0.1% |
| DLTV | 15 | 0.1% |
| Online TV | 15 | 0.1% |
| Animals & Nature | 13 | 0.1% |
| Australia | 13 | 0.1% |
| Tv Reality | 13 | 0.1% |
| Global TV | 12 | 0.1% |
| Public TV | 12 | 0.1% |
| Tv Paranormal | 11 | 0.1% |
| Tv Celebrities | 9 | 0.1% |
| Aria Web Channels | 6 | 0.0% |
| Tv Shows | 6 | 0.0% |
| Oceania | 5 | 0.0% |
| Relax | 5 | 0.0% |
| Shopping | 2 | 0.0% |
| 3-Radio#Chicago | 1 | 0.0% |
| IPTV | 1 | 0.0% |
| Live TV | 1 | 0.0% |
| MeTV | 1 | 0.0% |
| TEST | 1 | 0.0% |
| United Kingdom | 1 | 0.0% |
| USA Channels | 1 | 0.0% |
| Other | 424 | 3.5% |

## Country playlists (`playlists/countries/` — 171 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 2790 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1308 | [`countries/International.m3u`](countries/International.m3u) |
| India | 790 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 527 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 429 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Sweden | 376 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| Germany | 368 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| UK | 248 | [`countries/UK.m3u`](countries/UK.m3u) |
| France | 216 | [`countries/France.m3u`](countries/France.m3u) |
| Dominican Republic | 206 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Spain | 196 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| Chile | 194 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Brazil | 180 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Ukraine | 178 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Poland | 170 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Argentina | 164 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Hungary | 163 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| Netherlands | 151 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Peru | 151 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Romania | 143 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Turkey | 138 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Canada | 137 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Mexico | 123 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Colombia | 119 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| Indonesia | 114 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| _…and 146 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 70 / 75 unique links (dead: 1, unverified: 4)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | reachable | - | 0 | no_static_playlist | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. (repository is archived) |
| dlive.sx | reachable | 899 | 0 | player_pages_only | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 403 | 0 | 1226 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 404 | 1051 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| TimeoutError | 0 | 808 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| gaierror | 0 | 414 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 243 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 146 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 429 | 0 | 136 | The host rate-limited the check; this scraper now limits parallel requests per host and retries with Retry-After/backoff. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 117 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionRefusedError | 0 | 97 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist lists no segments (failed the deep check 2x, last 2026-11-02T15:49:00Z) | 78 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 400 | 69 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 503 | 0 | 43 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 401 | 0 | 39 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 39 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 32 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-02T15:49:00Z) | 26 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 504 | 0 | 22 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| SSLError | 0 | 21 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| SSLEOFError | 0 | 20 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 400 (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 19 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| RemoteDisconnected | 0 | 17 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 502 | 0 | 15 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| OSError | 0 | 15 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| empty response | 15 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| HTTP 500 | 0 | 13 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme rtmp | 0 | 13 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: variant HTTP 403 (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 13 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 11 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-02T15:49:00Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 451 | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-01T11:56:39Z) | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 6 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-02T15:49:00Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 530 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-02T15:49:00Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-01T11:56:39Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-01T11:56:39Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| invalid URL | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-02T15:49:00Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-02T15:49:00Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-11-01T11:56:39Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 2 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 523 | 0 | 2 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| deep check: offline (HTTP 404) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme mmsh | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-02T15:49:00Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: html page, not a stream (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 302 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 406 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 409 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 521 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| deep check: offline (variant HTTP 403) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme rtsp | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: dns lookup failed (failed the deep check 2x, last 2026-11-02T15:49:00Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 2x, last 2026-11-01T11:56:39Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist lists no segments (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 1x, last 2026-11-02T15:49:00Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 401 (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-11-01T11:56:39Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 1x, last 2026-11-02T15:49:00Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, segment too small (214 bytes) (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 1x, last 2026-11-02T15:49:00Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-02T15:49:00Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 410 (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |

### Run/source issues

- 2922 links could not be confirmed after retries (see unverified details).
- 1959 links returned a confirmed failure (see dead details).
- This run started +6h 13m after its scheduled time (2026-11-02T17:53:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
