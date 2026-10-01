# Scraper status

- **Last run:** 2026-10-01 10:28 AM EDT (2026-10-01 14:28 UTC)
- **Run:** _3:07 AM daily scrape_ (`regular_check`; ID `20261001T142531Z-2396`)
- **Scheduled for:** 2026-10-01T07:07:00Z — started late by +7h 18m
- **Outcome:** **WARNING**
- **Confirmed working:** 9480 / 13515 unique links
- **Dead:** 1343  |  **Unverified:** 2692
- **Unique links found:** 13515 from 14439 source entries
- **Changes vs. PremiumTV_all.m3u:** +446 added / -235 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (175 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (54 confirmed working / 56 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| ae-networks | ok | 53 | 53 | 14 | 51 | 0 | 2 |
| aria | ok | 401 | 395 | 121 | 318 | 7 | 70 |
| doms9 | ok | 459 | 458 | 62 | 219 | 29 | 210 |
| xtemus | ok | 317 | 317 | 0 | 33 | 231 | 53 |
| iptv-org | ok | 11129 | 11129 | 842 | 8304 | 806 | 2019 |
| free-tv | ok | 2080 | 2054 | 709 | 1298 | 302 | 454 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |

## Country playlists (`playlists/countries/` — 175 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 1883 | [`countries/USA.m3u`](countries/USA.m3u) |
| India | 729 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 517 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 391 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Germany | 384 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| Sweden | 378 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| Spain | 218 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| Dominican Republic | 201 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Chile | 187 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| UK | 181 | [`countries/UK.m3u`](countries/UK.m3u) |
| Brazil | 174 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Ukraine | 165 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Netherlands | 157 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Argentina | 146 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| France | 142 | [`countries/France.m3u`](countries/France.m3u) |
| Peru | 139 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Turkey | 136 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Canada | 121 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Romania | 120 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Iran | 118 | [`countries/Iran.m3u`](countries/Iran.m3u) |
| Mexico | 118 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Indonesia | 117 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| Hungary | 112 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| Colombia | 98 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| Poland | 96 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| _…and 150 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 54 / 56 unique links (dead: 0, unverified: 2)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | reachable | - | 0 | no_static_playlist | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. (repository is archived) |
| dlive.sx | reachable | 899 | 0 | player_pages_only | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 403 | 0 | 1183 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| TimeoutError | 0 | 857 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 404 | 847 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| html page, not a stream | 415 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| gaierror | 0 | 298 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| ConnectionRefusedError | 0 | 104 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 503 | 0 | 62 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 400 | 47 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 401 | 0 | 35 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| RemoteDisconnected | 0 | 24 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLError | 0 | 23 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 502 | 0 | 18 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 504 | 0 | 17 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| empty response | 13 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| OSError | 0 | 12 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLEOFError | 0 | 12 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 500 | 0 | 9 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme rtmp | 0 | 8 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| HTTP 451 | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 530 | 0 | 7 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 406 | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 521 | 0 | 3 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 523 | 0 | 3 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 477 | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 520 | 0 | 2 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| invalid URL | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
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

- 2692 links could not be confirmed after retries (see unverified details).
- 1343 links returned a confirmed failure (see dead details).
- This run started +7h 18m after its scheduled time (2026-10-01T07:07:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
