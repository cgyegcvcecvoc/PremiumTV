# Scraper status

- **Last run:** 2026-11-15 03:00 PM EST (2026-11-15 20:00 UTC)
- **Run:** _9:41 AM recheck_ (`recheck`; ID `20261115T195644Z-2950`)
- **Scheduled for:** 2026-11-15T14:41:00Z — started late by +5h 16m
- **Outcome:** **WARNING**
- **Confirmed working:** 12089 / 17201 unique links
- **Dead:** 2789  |  **Unverified:** 2323
- **Retained (unverified, within grace):** 264 previously published links kept so their channels do not vanish after one unverifiable run
- **Unique links found:** 17201 from 21709 source entries
- **Changes vs. PremiumTV_all.m3u:** +331 added / -330 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (176 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (111 confirmed working / 121 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 747 |
| 2 | Lifestyle | 524 |
| 3 | Fox Channels | 23 |
| 4 | CBS | 39 |
| 5 | NBC | 62 |
| 6 | NBC Sports Channels | 9 |
| 7 | Cartoons | 201 |
| 8 | PBS | 20 |
| 9 | Game Shows | 19 |
| 10 | News | 1049 |
| 11 | Movies | 984 |
| 12 | Music | 898 |
| 13 | Entertainment | 858 |
| 14 | International | 830 |
| 15 | Europe | 777 |
| 16 | Religious | 673 |
| 17 | Series | 523 |
| 18 | Asia | 494 |
| 19 | South America | 488 |
| 20 | United States | 403 |
| 21 | Kids | 390 |
| 22 | Documentary | 379 |
| 23 | North America | 305 |
| 24 | Comedy | 180 |
| 25 | Education | 144 |
| 26 | Culture | 127 |
| 27 | Legislative | 116 |
| 28 | A&E Networks | 97 |
| 29 | India | 90 |
| 30 | Classic TV | 78 |
| 31 | Africa | 72 |
| 32 | Business | 69 |
| 33 | UK | 34 |
| 34 | Family | 33 |
| 35 | Canada | 24 |
| 36 | Auto | 22 |
| 37 | Weather | 17 |
| 38 | Online TV | 16 |
| 39 | DLTV | 15 |
| 40 | Animals & Nature | 13 |
| 41 | Australia | 13 |
| 42 | Global TV | 12 |
| 43 | Public TV | 11 |
| 44 | Tv Reality | 11 |
| 45 | Tv Paranormal | 10 |
| 46 | Tv Celebrities | 9 |
| 47 | Aria Web Channels | 6 |
| 48 | Eurovision Song Contest Asia On Aria November 14Th | 6 |
| 49 | Tv Shows | 6 |
| 50 | Oceania | 5 |
| 51 | Relax | 4 |
| 52 | IPTV | 1 |
| 53 | Shopping | 1 |
| 54 | TEST | 1 |
| 55 | United Kingdom | 1 |
| 56 | USA Channels | 1 |
| 57 | Other | 413 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 2 | 2 | 2 | 2 | 0 | 0 |
| priority-channels | ok | 16 | 16 | 14 | 16 | 0 | 0 |
| ae-networks | ok | 50 | 50 | 12 | 47 | 0 | 3 |
| aria | ok | 249 | 232 | 87 | 161 | 21 | 50 |
| doms9 | ok | 590 | 589 | 93 | 265 | 55 | 269 |
| xtemus | ok | 317 | 317 | 0 | 31 | 251 | 35 |
| iptv-org | ok | 11502 | 11502 | 3742 | 8256 | 1630 | 1616 |
| free-tv | ok | 2203 | 2179 | 934 | 1285 | 560 | 334 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| VIP-m3u-playlist 🌱 | ok | 202 | 202 | 94 | 190 | 10 | 2 |
| israel-tv-plus 🌱 | ok | 307 | 278 | 73 | 111 | 86 | 81 |
| m3u 🌱 | ok | 843 | 839 | 174 | 673 | 129 | 36 |
| openstream 🌱 | ok | 5428 | 5428 | 3129 | 5013 | 378 | 37 |

🌱 = source added automatically by the monthly discovery engine: VIP-m3u-playlist, israel-tv-plus, m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **12353** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 747 | 6.0% |
| Lifestyle | 524 | 4.2% |
| Fox Channels | 23 | 0.2% |
| CBS | 39 | 0.3% |
| NBC | 62 | 0.5% |
| NBC Sports Channels | 9 | 0.1% |
| Cartoons | 201 | 1.6% |
| PBS | 20 | 0.2% |
| Game Shows | 19 | 0.2% |
| News | 1049 | 8.5% |
| Movies | 984 | 8.0% |
| Music | 898 | 7.3% |
| Entertainment | 858 | 6.9% |
| International | 830 | 6.7% |
| Europe | 777 | 6.3% |
| Religious | 673 | 5.4% |
| Series | 523 | 4.2% |
| Asia | 494 | 4.0% |
| South America | 488 | 4.0% |
| United States | 403 | 3.3% |
| Kids | 390 | 3.2% |
| Documentary | 379 | 3.1% |
| North America | 305 | 2.5% |
| Comedy | 180 | 1.5% |
| Education | 144 | 1.2% |
| Culture | 127 | 1.0% |
| Legislative | 116 | 0.9% |
| A&E Networks | 97 | 0.8% |
| India | 90 | 0.7% |
| Classic TV | 78 | 0.6% |
| Africa | 72 | 0.6% |
| Business | 69 | 0.6% |
| UK | 34 | 0.3% |
| Family | 33 | 0.3% |
| Canada | 24 | 0.2% |
| Auto | 22 | 0.2% |
| Weather | 17 | 0.1% |
| Online TV | 16 | 0.1% |
| DLTV | 15 | 0.1% |
| Animals & Nature | 13 | 0.1% |
| Australia | 13 | 0.1% |
| Global TV | 12 | 0.1% |
| Public TV | 11 | 0.1% |
| Tv Reality | 11 | 0.1% |
| Tv Paranormal | 10 | 0.1% |
| Tv Celebrities | 9 | 0.1% |
| Aria Web Channels | 6 | 0.0% |
| Eurovision Song Contest Asia On Aria November 14Th | 6 | 0.0% |
| Tv Shows | 6 | 0.0% |
| Oceania | 5 | 0.0% |
| Relax | 4 | 0.0% |
| IPTV | 1 | 0.0% |
| Shopping | 1 | 0.0% |
| TEST | 1 | 0.0% |
| United Kingdom | 1 | 0.0% |
| USA Channels | 1 | 0.0% |
| Other | 413 | 3.3% |

## Country playlists (`playlists/countries/` — 176 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 2978 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1075 | [`countries/International.m3u`](countries/International.m3u) |
| India | 806 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 540 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 420 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Germany | 389 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| Sweden | 376 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| France | 263 | [`countries/France.m3u`](countries/France.m3u) |
| UK | 254 | [`countries/UK.m3u`](countries/UK.m3u) |
| Spain | 214 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| Dominican Republic | 208 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Chile | 182 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Poland | 182 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Brazil | 181 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Ukraine | 173 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Argentina | 172 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Romania | 167 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Hungary | 162 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| Canada | 154 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Peru | 152 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Netherlands | 150 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Turkey | 146 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Mexico | 126 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Colombia | 110 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| Indonesia | 107 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| _…and 151 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 111 / 121 unique links (dead: 5, unverified: 5)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | reachable | - | 0 | no_static_playlist | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. (repository is archived) |
| dlive.sx | failed | - | 0 | not_imported | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. — GET https://dlive.sx/24-7-channels.php failed: <urlopen error [Errno -2] Name or service not known> |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 403 | 0 | 1276 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 404 | 1196 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| TimeoutError | 0 | 769 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-15T19:20:25Z) | 393 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| html page, not a stream | 383 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-15T19:20:25Z) | 133 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 91 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 84 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 400 | 67 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 60 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 401 | 0 | 58 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 502 | 0 | 53 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: connection refused (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 50 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 403 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 45 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-15T19:20:25Z) | 43 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 504 | 0 | 28 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 503 | 0 | 24 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 500 | 0 | 22 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| SSLError | 0 | 21 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: dns lookup failed (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 20 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 19 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| RemoteDisconnected | 0 | 17 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 17 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 17 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| empty response | 15 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| OSError | 0 | 13 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme rtmp | 0 | 13 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 11 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 5x, last 2026-11-15T19:20:25Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 8 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 451 | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 530 | 0 | 6 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: playlist only, HTTP 400 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| deep check: offline (HTTP 404) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| invalid URL | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-15T19:20:25Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, dns lookup failed (failed the deep check 5x, last 2026-11-15T19:20:25Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 1x, last 2026-11-15T19:20:25Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 401 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 2 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 422 | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 523 | 0 | 2 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| SSLEOFError | 0 | 2 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| not probed: unsupported scheme mmsh | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| not probed: unsupported scheme rtsp | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 404 (failed the deep check 7x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: dns lookup failed (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 5x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 3x, last 2026-11-15T19:20:25Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionRefusedError | 0 | 1 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 302 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 406 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 409 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 429 | 0 | 1 | The host rate-limited the check; this scraper now limits parallel requests per host and retries with Retry-After/backoff. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| deep check: offline (connection refused) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| deep check: offline (playlist only, HTTP 404) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| deep check: offline (playlist only, empty segment) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| gaierror | 0 | 1 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 400 (failed the deep check 1x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 8x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 6x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
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
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 6x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 410 (failed the deep check 2x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 4x, last 2026-11-15T19:20:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |

### Run/source issues

- Reference check 'dlive.sx' failed: GET https://dlive.sx/24-7-channels.php failed: <urlopen error [Errno -2] Name or service not known>
- 2323 links could not be confirmed after retries (see unverified details).
- 2789 links returned a confirmed failure (see dead details).
- This run started +5h 16m after its scheduled time (2026-11-15T14:41:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
