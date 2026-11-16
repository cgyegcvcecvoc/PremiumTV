# Scraper status

- **Last run:** 2026-11-16 06:33 PM EST (2026-11-16 23:33 UTC)
- **Run:** _9:41 AM recheck_ (`recheck`; ID `20261116T232957Z-2986`)
- **Scheduled for:** 2026-11-16T14:41:00Z — started late by +8h 49m
- **Outcome:** **WARNING**
- **Confirmed working:** 12047 / 17041 unique links
- **Dead:** 2689  |  **Unverified:** 2305
- **Retained (unverified, within grace):** 195 previously published links kept so their channels do not vanish after one unverifiable run
- **Unique links found:** 17041 from 21512 source entries
- **Changes vs. PremiumTV_all.m3u:** +116 added / -136 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (176 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (112 confirmed working / 121 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 676 |
| 2 | Lifestyle | 523 |
| 3 | Fox Channels | 23 |
| 4 | CBS | 39 |
| 5 | NBC | 62 |
| 6 | NBC Sports Channels | 9 |
| 7 | Cartoons | 201 |
| 8 | PBS | 20 |
| 9 | Game Shows | 19 |
| 10 | News | 1050 |
| 11 | Movies | 986 |
| 12 | Music | 891 |
| 13 | Entertainment | 852 |
| 14 | International | 825 |
| 15 | Europe | 778 |
| 16 | Religious | 670 |
| 17 | Series | 523 |
| 18 | Asia | 497 |
| 19 | South America | 475 |
| 20 | United States | 402 |
| 21 | Kids | 392 |
| 22 | Documentary | 380 |
| 23 | North America | 303 |
| 24 | Comedy | 181 |
| 25 | Education | 144 |
| 26 | Culture | 125 |
| 27 | Legislative | 116 |
| 28 | A&E Networks | 97 |
| 29 | India | 90 |
| 30 | Classic TV | 78 |
| 31 | Africa | 70 |
| 32 | Business | 70 |
| 33 | Family | 34 |
| 34 | UK | 33 |
| 35 | Canada | 24 |
| 36 | Auto | 22 |
| 37 | Weather | 17 |
| 38 | DLTV | 15 |
| 39 | Online TV | 15 |
| 40 | Animals & Nature | 13 |
| 41 | Australia | 12 |
| 42 | Global TV | 12 |
| 43 | Public TV | 11 |
| 44 | Tv Reality | 11 |
| 45 | Tv Paranormal | 10 |
| 46 | Tv Celebrities | 9 |
| 47 | Aria Web Channels | 6 |
| 48 | Tv Shows | 6 |
| 49 | Oceania | 5 |
| 50 | Relax | 4 |
| 51 | IPTV | 1 |
| 52 | Shopping | 1 |
| 53 | TEST | 1 |
| 54 | United Kingdom | 1 |
| 55 | USA Channels | 1 |
| 56 | Other | 411 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 2 | 2 | 2 | 2 | 0 | 0 |
| priority-channels | ok | 16 | 16 | 12 | 12 | 1 | 3 |
| ae-networks | ok | 50 | 50 | 12 | 47 | 0 | 3 |
| aria | ok | 233 | 222 | 83 | 156 | 17 | 49 |
| doms9 | ok | 433 | 433 | 91 | 183 | 31 | 219 |
| xtemus | ok | 317 | 317 | 0 | 30 | 129 | 158 |
| iptv-org | ok | 11502 | 11502 | 3739 | 8290 | 1682 | 1530 |
| free-tv | ok | 2203 | 2179 | 934 | 1289 | 554 | 336 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| VIP-m3u-playlist 🌱 | ok | 201 | 201 | 94 | 191 | 10 | 0 |
| israel-tv-plus 🌱 | ok | 284 | 279 | 73 | 112 | 87 | 80 |
| m3u 🌱 | ok | 843 | 839 | 174 | 673 | 129 | 36 |
| openstream 🌱 | ok | 5428 | 5428 | 3129 | 4988 | 398 | 42 |

🌱 = source added automatically by the monthly discovery engine: VIP-m3u-playlist, israel-tv-plus, m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **12242** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 676 | 5.5% |
| Lifestyle | 523 | 4.3% |
| Fox Channels | 23 | 0.2% |
| CBS | 39 | 0.3% |
| NBC | 62 | 0.5% |
| NBC Sports Channels | 9 | 0.1% |
| Cartoons | 201 | 1.6% |
| PBS | 20 | 0.2% |
| Game Shows | 19 | 0.2% |
| News | 1050 | 8.6% |
| Movies | 986 | 8.1% |
| Music | 891 | 7.3% |
| Entertainment | 852 | 7.0% |
| International | 825 | 6.7% |
| Europe | 778 | 6.4% |
| Religious | 670 | 5.5% |
| Series | 523 | 4.3% |
| Asia | 497 | 4.1% |
| South America | 475 | 3.9% |
| United States | 402 | 3.3% |
| Kids | 392 | 3.2% |
| Documentary | 380 | 3.1% |
| North America | 303 | 2.5% |
| Comedy | 181 | 1.5% |
| Education | 144 | 1.2% |
| Culture | 125 | 1.0% |
| Legislative | 116 | 0.9% |
| A&E Networks | 97 | 0.8% |
| India | 90 | 0.7% |
| Classic TV | 78 | 0.6% |
| Africa | 70 | 0.6% |
| Business | 70 | 0.6% |
| Family | 34 | 0.3% |
| UK | 33 | 0.3% |
| Canada | 24 | 0.2% |
| Auto | 22 | 0.2% |
| Weather | 17 | 0.1% |
| DLTV | 15 | 0.1% |
| Online TV | 15 | 0.1% |
| Animals & Nature | 13 | 0.1% |
| Australia | 12 | 0.1% |
| Global TV | 12 | 0.1% |
| Public TV | 11 | 0.1% |
| Tv Reality | 11 | 0.1% |
| Tv Paranormal | 10 | 0.1% |
| Tv Celebrities | 9 | 0.1% |
| Aria Web Channels | 6 | 0.0% |
| Tv Shows | 6 | 0.0% |
| Oceania | 5 | 0.0% |
| Relax | 4 | 0.0% |
| IPTV | 1 | 0.0% |
| Shopping | 1 | 0.0% |
| TEST | 1 | 0.0% |
| United Kingdom | 1 | 0.0% |
| USA Channels | 1 | 0.0% |
| Other | 411 | 3.4% |

## Country playlists (`playlists/countries/` — 176 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 2912 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1069 | [`countries/International.m3u`](countries/International.m3u) |
| India | 804 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 535 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 438 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Germany | 390 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| Sweden | 376 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| France | 260 | [`countries/France.m3u`](countries/France.m3u) |
| UK | 253 | [`countries/UK.m3u`](countries/UK.m3u) |
| Spain | 211 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| Dominican Republic | 206 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Chile | 182 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Poland | 182 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Brazil | 178 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Ukraine | 175 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Argentina | 169 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Romania | 164 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Hungary | 162 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| Canada | 154 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Netherlands | 149 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Peru | 145 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Turkey | 144 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Mexico | 124 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Colombia | 104 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| Indonesia | 102 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| _…and 151 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 112 / 121 unique links (dead: 5, unverified: 4)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | failed | - | 0 | not_imported | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. — GET https://api.github.com/repos/gookie-dev/StepDaddyLiveHD failed: HTTP Error 403: rate limit exceeded |
| dlive.sx | failed | - | 0 | not_imported | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. — GET https://dlive.sx/24-7-channels.php failed: <urlopen error [Errno -2] Name or service not known> |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 404 | 1130 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 403 | 0 | 1113 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| TimeoutError | 0 | 726 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-15T19:20:25Z) | 393 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| html page, not a stream | 246 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| HTTP 429 | 0 | 136 | The host rate-limited the check; this scraper now limits parallel requests per host and retries with Retry-After/backoff. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-15T19:20:25Z) | 134 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-15T19:20:25Z) | 104 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 91 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 84 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 400 | 68 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| OSError | 0 | 65 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 58 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 401 | 0 | 57 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| quarantined: connection refused (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 50 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 502 | 0 | 47 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 46 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 45 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| RemoteDisconnected | 0 | 30 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 503 | 0 | 28 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 504 | 0 | 26 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| SSLError | 0 | 21 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: HTTP 404 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 21 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 20 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 19 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 17 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 500 | 0 | 16 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| empty response | 15 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| not probed: unsupported scheme rtmp | 0 | 13 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 11 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 5x, last 2026-11-15T19:20:25Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 8 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 451 | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 530 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| deep check: offline (HTTP 404) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| invalid URL | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-15T19:20:25Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, dns lookup failed (failed the deep check 5x, last 2026-11-15T19:20:25Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| gaierror | 0 | 3 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: HTTP 404 (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 401 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 2 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 523 | 0 | 2 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme mmsh | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| not probed: unsupported scheme rtsp | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 404 (failed the deep check 6x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: dns lookup failed (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 5x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 302 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 406 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 408 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 409 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 458 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| deep check: offline (connection refused) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| deep check: offline (playlist only, HTTP 404) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| deep check: offline (playlist only, empty segment) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 404 (failed the deep check 7x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 422 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 6x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 1x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist lists no segments (failed the deep check 5x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 5x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 6x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 5x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 6x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 451 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 5x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 6x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 410 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |

### Run/source issues

- Reference check 'StepDaddyLiveHD' failed: GET https://api.github.com/repos/gookie-dev/StepDaddyLiveHD failed: HTTP Error 403: rate limit exceeded
- Reference check 'dlive.sx' failed: GET https://dlive.sx/24-7-channels.php failed: <urlopen error [Errno -2] Name or service not known>
- 2305 links could not be confirmed after retries (see unverified details).
- 2689 links returned a confirmed failure (see dead details).
- This run started +8h 49m after its scheduled time (2026-11-16T14:41:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
