# Scraper status

- **Last run:** 2026-10-01 04:22 PM EDT (2026-10-01 20:22 UTC)
- **Run:** _manual error-log re-scrape_ (`manual`; ID `20261001T201905Z-2395`)
- **Outcome:** **WARNING**
- **Confirmed working:** 12306 / 16582 unique links
- **Dead:** 1501  |  **Unverified:** 2775
- **Unique links found:** 16582 from 20920 source entries
- **Changes vs. PremiumTV_all.m3u:** +366 added / -292 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (176 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (68 confirmed working / 71 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| ae-networks | ok | 53 | 53 | 17 | 51 | 0 | 2 |
| aria | ok | 401 | 395 | 125 | 318 | 10 | 67 |
| doms9 | ok | 561 | 559 | 68 | 284 | 38 | 237 |
| xtemus | ok | 317 | 317 | 0 | 32 | 232 | 53 |
| iptv-org | ok | 11129 | 11129 | 3708 | 8298 | 818 | 2013 |
| free-tv | ok | 2080 | 2054 | 831 | 1295 | 307 | 452 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| m3u 🌱 | ok | 831 | 827 | 174 | 642 | 125 | 60 |
| openstream 🌱 | ok | 5548 | 5548 | 3243 | 5490 | 38 | 20 |

🌱 = source added automatically by the monthly discovery engine: m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Country playlists (`playlists/countries/` — 176 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 2810 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1202 | [`countries/International.m3u`](countries/International.m3u) |
| India | 798 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 531 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 442 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Germany | 407 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| Sweden | 378 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| Spain | 239 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| UK | 237 | [`countries/UK.m3u`](countries/UK.m3u) |
| Chile | 204 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Dominican Republic | 204 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| France | 199 | [`countries/France.m3u`](countries/France.m3u) |
| Brazil | 190 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Ukraine | 178 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Netherlands | 172 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Argentina | 157 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Peru | 154 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Turkey | 151 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Canada | 147 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Mexico | 128 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Romania | 124 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Iran | 119 | [`countries/Iran.m3u`](countries/Iran.m3u) |
| Poland | 118 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Indonesia | 114 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| Hungary | 113 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| _…and 151 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 68 / 71 unique links (dead: 0, unverified: 3)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | reachable | - | 0 | no_static_playlist | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. (repository is archived) |
| dlive.sx | reachable | 899 | 0 | player_pages_only | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 403 | 0 | 1203 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 404 | 913 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| TimeoutError | 0 | 861 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 417 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| gaierror | 0 | 331 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| ConnectionRefusedError | 0 | 100 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| invalid URL | 79 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 503 | 0 | 68 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 400 | 60 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 401 | 0 | 46 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| SSLError | 0 | 24 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| RemoteDisconnected | 0 | 22 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 502 | 0 | 21 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 504 | 0 | 21 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| empty response | 13 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| OSError | 0 | 12 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLEOFError | 0 | 12 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 500 | 0 | 11 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme rtmp | 0 | 8 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| HTTP 429 | 0 | 7 | The host rate-limited the check; this scraper now limits parallel requests per host and retries with Retry-After/backoff. |
| HTTP 451 | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 530 | 0 | 6 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 406 | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 521 | 0 | 3 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 477 | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 520 | 0 | 2 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 523 | 0 | 2 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme mmsh | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| HTTP 302 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 409 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 1 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 458 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme rtsp | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |

### Run/source issues

- 2775 links could not be confirmed after retries (see unverified details).
- 1501 links returned a confirmed failure (see dead details).
