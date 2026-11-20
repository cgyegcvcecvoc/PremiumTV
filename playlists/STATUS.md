# Scraper status

- **Last run:** 2026-11-20 02:14 PM EST (2026-11-20 19:14 UTC)
- **Run:** _6:23 AM recheck_ (`recheck`; ID `20261120T191043Z-3101`)
- **Scheduled for:** 2026-11-20T11:23:00Z — started late by +7h 48m
- **Outcome:** **WARNING**
- **Confirmed working:** 11985 / 17398 unique links
- **Dead:** 2842  |  **Unverified:** 2571
- **Retained (unverified, within grace):** 434 previously published links kept so their channels do not vanish after one unverifiable run
- **Unique links found:** 17398 from 21834 source entries
- **Changes vs. PremiumTV_all.m3u:** +402 added / -297 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (176 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (115 confirmed working / 123 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 694 |
| 2 | Lifestyle | 526 |
| 3 | Fox Channels | 35 |
| 4 | CBS | 51 |
| 5 | NBC | 64 |
| 6 | NBC Sports Channels | 6 |
| 7 | Cartoons | 205 |
| 8 | PBS | 21 |
| 9 | Game Shows | 19 |
| 10 | News | 1036 |
| 11 | Movies | 990 |
| 12 | Music | 895 |
| 13 | Entertainment | 851 |
| 14 | International | 822 |
| 15 | Europe | 799 |
| 16 | Religious | 661 |
| 17 | Series | 525 |
| 18 | Asia | 503 |
| 19 | South America | 491 |
| 20 | United States | 423 |
| 21 | Kids | 398 |
| 22 | Documentary | 395 |
| 23 | North America | 292 |
| 24 | Comedy | 183 |
| 25 | Education | 147 |
| 26 | Culture | 133 |
| 27 | Legislative | 114 |
| 28 | A&E Networks | 97 |
| 29 | India | 90 |
| 30 | Classic TV | 78 |
| 31 | Business | 73 |
| 32 | Africa | 69 |
| 33 | UK | 34 |
| 34 | Family | 33 |
| 35 | Online TV | 30 |
| 36 | Auto | 26 |
| 37 | Canada | 23 |
| 38 | Weather | 21 |
| 39 | DLTV | 15 |
| 40 | Animals & Nature | 13 |
| 41 | Australia | 13 |
| 42 | Global TV | 12 |
| 43 | Public TV | 11 |
| 44 | Tv Reality | 11 |
| 45 | Tv Paranormal | 10 |
| 46 | Tv Celebrities | 9 |
| 47 | Aria Web Channels | 6 |
| 48 | Tv Shows | 6 |
| 49 | Oceania | 5 |
| 50 | Relax | 5 |
| 51 | IPTV | 1 |
| 52 | Shopping | 1 |
| 53 | TEST | 1 |
| 54 | United Kingdom | 1 |
| 55 | USA Channels | 1 |
| 56 | Other | 445 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 2 | 2 | 2 | 1 | 1 | 0 |
| priority-channels | ok | 13 | 13 | 11 | 13 | 0 | 0 |
| ae-networks | ok | 50 | 50 | 11 | 47 | 0 | 3 |
| aria | ok | 233 | 222 | 84 | 153 | 17 | 52 |
| doms9 | ok | 613 | 610 | 71 | 220 | 41 | 349 |
| xtemus | ok | 317 | 317 | 0 | 31 | 251 | 35 |
| iptv-org | ok | 11681 | 11681 | 3705 | 8158 | 1754 | 1769 |
| free-tv | ok | 2203 | 2179 | 927 | 1246 | 582 | 351 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| VIP-m3u-playlist 🌱 | ok | 163 | 163 | 94 | 158 | 5 | 0 |
| israel-tv-plus 🌱 | ok | 288 | 284 | 81 | 176 | 10 | 98 |
| m3u 🌱 | ok | 843 | 839 | 174 | 671 | 130 | 37 |
| openstream 🌱 | ok | 5428 | 5428 | 3112 | 4902 | 482 | 44 |

🌱 = source added automatically by the monthly discovery engine: VIP-m3u-playlist, israel-tv-plus, m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **12419** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 694 | 5.6% |
| Lifestyle | 526 | 4.2% |
| Fox Channels | 35 | 0.3% |
| CBS | 51 | 0.4% |
| NBC | 64 | 0.5% |
| NBC Sports Channels | 6 | 0.0% |
| Cartoons | 205 | 1.7% |
| PBS | 21 | 0.2% |
| Game Shows | 19 | 0.2% |
| News | 1036 | 8.3% |
| Movies | 990 | 8.0% |
| Music | 895 | 7.2% |
| Entertainment | 851 | 6.9% |
| International | 822 | 6.6% |
| Europe | 799 | 6.4% |
| Religious | 661 | 5.3% |
| Series | 525 | 4.2% |
| Asia | 503 | 4.1% |
| South America | 491 | 4.0% |
| United States | 423 | 3.4% |
| Kids | 398 | 3.2% |
| Documentary | 395 | 3.2% |
| North America | 292 | 2.4% |
| Comedy | 183 | 1.5% |
| Education | 147 | 1.2% |
| Culture | 133 | 1.1% |
| Legislative | 114 | 0.9% |
| A&E Networks | 97 | 0.8% |
| India | 90 | 0.7% |
| Classic TV | 78 | 0.6% |
| Business | 73 | 0.6% |
| Africa | 69 | 0.6% |
| UK | 34 | 0.3% |
| Family | 33 | 0.3% |
| Online TV | 30 | 0.2% |
| Auto | 26 | 0.2% |
| Canada | 23 | 0.2% |
| Weather | 21 | 0.2% |
| DLTV | 15 | 0.1% |
| Animals & Nature | 13 | 0.1% |
| Australia | 13 | 0.1% |
| Global TV | 12 | 0.1% |
| Public TV | 11 | 0.1% |
| Tv Reality | 11 | 0.1% |
| Tv Paranormal | 10 | 0.1% |
| Tv Celebrities | 9 | 0.1% |
| Aria Web Channels | 6 | 0.0% |
| Tv Shows | 6 | 0.0% |
| Oceania | 5 | 0.0% |
| Relax | 5 | 0.0% |
| IPTV | 1 | 0.0% |
| Shopping | 1 | 0.0% |
| TEST | 1 | 0.0% |
| United Kingdom | 1 | 0.0% |
| USA Channels | 1 | 0.0% |
| Other | 445 | 3.6% |

## Country playlists (`playlists/countries/` — 176 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 3018 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1092 | [`countries/International.m3u`](countries/International.m3u) |
| India | 832 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 533 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 442 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Germany | 383 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| Sweden | 376 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| France | 285 | [`countries/France.m3u`](countries/France.m3u) |
| UK | 253 | [`countries/UK.m3u`](countries/UK.m3u) |
| Dominican Republic | 202 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Spain | 189 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| Poland | 184 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Chile | 179 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Brazil | 175 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Ukraine | 174 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Argentina | 169 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Romania | 167 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Hungary | 158 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| Canada | 151 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Netherlands | 149 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Turkey | 141 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Peru | 139 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Mexico | 121 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Colombia | 106 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| Indonesia | 104 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| _…and 151 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 115 / 123 unique links (dead: 4, unverified: 4)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | reachable | - | 0 | no_static_playlist | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. (repository is archived) |
| dlive.sx | failed | - | 0 | not_imported | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. — GET https://dlive.sx/24-7-channels.php failed: <urlopen error [Errno -2] Name or service not known> |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 403 | 0 | 1488 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 404 | 1068 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| TimeoutError | 0 | 769 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 382 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-15T19:20:25Z) | 351 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-15T19:20:25Z) | 135 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-15T19:20:25Z) | 129 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 89 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 82 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 400 | 72 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 62 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 59 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 401 | 0 | 56 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| gaierror | 0 | 49 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: connection refused (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 48 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 403 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 39 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 502 | 0 | 36 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 503 | 0 | 33 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 504 | 0 | 22 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| SSLError | 0 | 22 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: HTTP 404 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 20 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 19 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 18 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 18 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionRefusedError | 0 | 17 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 17 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 500 | 0 | 15 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| RemoteDisconnected | 0 | 15 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| empty response | 14 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| not probed: unsupported scheme rtmp | 0 | 13 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 13 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 13 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| OSError | 0 | 12 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 11 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 11 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 5x, last 2026-11-15T19:20:25Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 7 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 451 | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 530 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionResetError | 0 | 4 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| invalid URL | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-15T19:20:25Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, dns lookup failed (failed the deep check 5x, last 2026-11-15T19:20:25Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 521 | 0 | 3 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 6x, last 2026-11-15T19:20:25Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 401 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 2 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 523 | 0 | 2 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme rtsp | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 404 (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: connection refused (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: dns lookup failed (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 302 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 406 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 409 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 512 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 400 (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 7x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 8x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 422 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 6x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist lists no segments (failed the deep check 5x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 5x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 5x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 6x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 5x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 6x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 451 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, segment too small (214 bytes) (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 5x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 6x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 410 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |

### Run/source issues

- Reference check 'dlive.sx' failed: GET https://dlive.sx/24-7-channels.php failed: <urlopen error [Errno -2] Name or service not known>
- 2571 links could not be confirmed after retries (see unverified details).
- 2842 links returned a confirmed failure (see dead details).
- This run started +7h 48m after its scheduled time (2026-11-20T11:23:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
