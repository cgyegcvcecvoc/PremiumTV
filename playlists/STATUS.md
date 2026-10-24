# Scraper status

- **Last run:** 2026-10-24 08:02 AM EDT (2026-10-24 12:02 UTC)
- **Run:** _3:07 AM daily scrape_ (`regular_check`; ID `20261024T115816Z-3191`)
- **Scheduled for:** 2026-10-24T07:07:00Z — started late by +4h 51m
- **Outcome:** **WARNING**
- **Confirmed working:** 11701 / 16841 unique links
- **Dead:** 2544  |  **Unverified:** 2596
- **Retained (unverified, within grace):** 1761 previously published links kept so their channels do not vanish after one unverifiable run
- **Unique links found:** 16841 from 21080 source entries
- **Changes vs. PremiumTV_all.m3u:** +406 added / -344 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (180 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (69 confirmed working / 74 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 673 |
| 2 | Lifestyle | 537 |
| 3 | Fox Channels | 26 |
| 4 | CBS | 40 |
| 5 | NBC | 64 |
| 6 | NBC Sports Channels | 6 |
| 7 | Cartoons | 207 |
| 8 | PBS | 18 |
| 9 | Game Shows | 18 |
| 10 | News | 1158 |
| 11 | Movies | 1029 |
| 12 | International | 1010 |
| 13 | Music | 967 |
| 14 | Europe | 941 |
| 15 | Entertainment | 857 |
| 16 | Religious | 705 |
| 17 | Asia | 657 |
| 18 | South America | 558 |
| 19 | Series | 530 |
| 20 | United States | 430 |
| 21 | Documentary | 415 |
| 22 | Kids | 400 |
| 23 | North America | 332 |
| 24 | Comedy | 188 |
| 25 | Education | 170 |
| 26 | Culture | 155 |
| 27 | Legislative | 150 |
| 28 | Africa | 101 |
| 29 | India | 98 |
| 30 | Classic TV | 79 |
| 31 | Business | 77 |
| 32 | UK | 69 |
| 33 | A&E Networks | 50 |
| 34 | Canada | 49 |
| 35 | Family | 36 |
| 36 | Australia | 27 |
| 37 | Auto | 23 |
| 38 | Global TV | 22 |
| 39 | Weather | 19 |
| 40 | DLTV | 16 |
| 41 | Digital TV | 15 |
| 42 | Online TV | 15 |
| 43 | Animals & Nature | 14 |
| 44 | Tv Reality | 13 |
| 45 | Public TV | 12 |
| 46 | Tv Paranormal | 11 |
| 47 | Tv Celebrities | 9 |
| 48 | Tv Shows | 7 |
| 49 | Aria Web Channels | 5 |
| 50 | Oceania | 5 |
| 51 | Relax | 4 |
| 52 | Anime | 2 |
| 53 | Shopping | 2 |
| 54 | 3-Radio#Chicago | 1 |
| 55 | MeTV | 1 |
| 56 | TEST | 1 |
| 57 | United Kingdom | 1 |
| 58 | USA Channels | 1 |
| 59 | Other | 436 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 4 | 4 | 3 | 2 | 2 | 0 |
| priority-channels | ok | 18 | 18 | 8 | 16 | 0 | 2 |
| ae-networks | ok | 53 | 53 | 16 | 50 | 2 | 1 |
| aria | ok | 305 | 301 | 88 | 218 | 15 | 68 |
| doms9 | ok | 736 | 724 | 82 | 148 | 149 | 427 |
| xtemus | ok | 317 | 317 | 0 | 31 | 251 | 35 |
| iptv-org | ok | 11323 | 11323 | 3631 | 7984 | 1583 | 1756 |
| free-tv | ok | 2052 | 2028 | 810 | 1205 | 462 | 361 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| m3u 🌱 | ok | 842 | 837 | 174 | 671 | 116 | 49 |
| openstream 🌱 | ok | 5430 | 5430 | 3160 | 5226 | 189 | 15 |

🌱 = source added automatically by the monthly discovery engine: m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **13462** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 673 | 5.0% |
| Lifestyle | 537 | 4.0% |
| Fox Channels | 26 | 0.2% |
| CBS | 40 | 0.3% |
| NBC | 64 | 0.5% |
| NBC Sports Channels | 6 | 0.0% |
| Cartoons | 207 | 1.5% |
| PBS | 18 | 0.1% |
| Game Shows | 18 | 0.1% |
| News | 1158 | 8.6% |
| Movies | 1029 | 7.6% |
| International | 1010 | 7.5% |
| Music | 967 | 7.2% |
| Europe | 941 | 7.0% |
| Entertainment | 857 | 6.4% |
| Religious | 705 | 5.2% |
| Asia | 657 | 4.9% |
| South America | 558 | 4.1% |
| Series | 530 | 3.9% |
| United States | 430 | 3.2% |
| Documentary | 415 | 3.1% |
| Kids | 400 | 3.0% |
| North America | 332 | 2.5% |
| Comedy | 188 | 1.4% |
| Education | 170 | 1.3% |
| Culture | 155 | 1.2% |
| Legislative | 150 | 1.1% |
| Africa | 101 | 0.8% |
| India | 98 | 0.7% |
| Classic TV | 79 | 0.6% |
| Business | 77 | 0.6% |
| UK | 69 | 0.5% |
| A&E Networks | 50 | 0.4% |
| Canada | 49 | 0.4% |
| Family | 36 | 0.3% |
| Australia | 27 | 0.2% |
| Auto | 23 | 0.2% |
| Global TV | 22 | 0.2% |
| Weather | 19 | 0.1% |
| DLTV | 16 | 0.1% |
| Digital TV | 15 | 0.1% |
| Online TV | 15 | 0.1% |
| Animals & Nature | 14 | 0.1% |
| Tv Reality | 13 | 0.1% |
| Public TV | 12 | 0.1% |
| Tv Paranormal | 11 | 0.1% |
| Tv Celebrities | 9 | 0.1% |
| Tv Shows | 7 | 0.1% |
| Aria Web Channels | 5 | 0.0% |
| Oceania | 5 | 0.0% |
| Relax | 4 | 0.0% |
| Anime | 2 | 0.0% |
| Shopping | 2 | 0.0% |
| 3-Radio#Chicago | 1 | 0.0% |
| MeTV | 1 | 0.0% |
| TEST | 1 | 0.0% |
| United Kingdom | 1 | 0.0% |
| USA Channels | 1 | 0.0% |
| Other | 436 | 3.2% |

## Country playlists (`playlists/countries/` — 180 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 2900 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1237 | [`countries/International.m3u`](countries/International.m3u) |
| India | 805 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 584 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 508 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Germany | 423 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| Sweden | 385 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| UK | 334 | [`countries/UK.m3u`](countries/UK.m3u) |
| Spain | 256 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| France | 249 | [`countries/France.m3u`](countries/France.m3u) |
| Brazil | 246 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Chile | 223 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Dominican Republic | 207 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Ukraine | 198 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Canada | 186 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Poland | 186 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Argentina | 167 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| China | 164 | [`countries/China.m3u`](countries/China.m3u) |
| Netherlands | 160 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Mexico | 159 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Peru | 154 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Turkey | 154 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Romania | 141 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Indonesia | 129 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| Colombia | 120 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| _…and 155 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 69 / 74 unique links (dead: 4, unverified: 1)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | reachable | - | 0 | no_static_playlist | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. (repository is archived) |
| dlive.sx | reachable | 899 | 0 | player_pages_only | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 403 | 0 | 1375 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 404 | 1230 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| TimeoutError | 0 | 875 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 378 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-10-20T10:13:37Z) | 309 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 106 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-10-20T10:13:37Z) | 99 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| gaierror | 0 | 95 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 400 | 76 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 401 | 0 | 47 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 410 | 45 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 37 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 503 | 0 | 27 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: connection refused (failed the deep check 1x, last 2026-10-22T10:19:47Z) | 23 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 504 | 0 | 22 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-19T10:50:27Z) | 21 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionRefusedError | 0 | 20 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| SSLEOFError | 0 | 20 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| SSLError | 0 | 20 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 502 | 0 | 17 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| RemoteDisconnected | 0 | 16 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-22T10:19:47Z) | 16 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| OSError | 0 | 14 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-10-21T10:17:30Z) | 14 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| empty response | 13 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| HTTP 500 | 0 | 12 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-20T10:13:37Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-10-19T10:50:27Z) | 10 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-21T10:17:30Z) | 9 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 451 | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 530 | 0 | 8 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme rtmp | 0 | 8 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-20T10:13:37Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-10-19T10:50:27Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-19T10:50:27Z) | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-10-19T10:50:27Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-22T10:19:47Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| invalid URL | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-18T09:38:18Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-21T10:17:30Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-10-21T10:17:30Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 400 (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-10-20T10:13:37Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, dns lookup failed (failed the deep check 1x, last 2026-10-20T10:13:37Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-21T10:17:30Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 523 | 0 | 3 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: dns lookup failed (failed the deep check 2x, last 2026-10-20T10:13:37Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-10-21T10:17:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-10-21T10:17:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-21T10:17:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme mmsh | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-10-22T10:19:47Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-18T09:38:18Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-19T10:50:27Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-10-19T10:50:27Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-10-21T10:17:30Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-10-22T10:19:47Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-19T10:50:27Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 302 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 406 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 409 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 412 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 429 | 0 | 1 | The host rate-limited the check; this scraper now limits parallel requests per host and retries with Retry-After/backoff. |
| HTTP 456 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 511 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme rtsp | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 422 (failed the deep check 1x, last 2026-10-19T10:50:27Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 2x, last 2026-10-19T10:50:27Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist lists no segments (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 401 (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-10-20T10:13:37Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-10-22T10:19:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-21T10:17:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-10-22T10:19:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-22T10:19:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-10-18T09:38:18Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-10-20T10:13:37Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 1x, last 2026-10-22T10:19:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-10-18T09:38:18Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-10-21T10:17:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, segment too small (214 bytes) (failed the deep check 1x, last 2026-10-20T10:13:37Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, segment too small (94 bytes) (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-10-19T10:50:27Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |

### Run/source issues

- 2596 links could not be confirmed after retries (see unverified details).
- 2544 links returned a confirmed failure (see dead details).
- This run started +4h 51m after its scheduled time (2026-10-24T07:07:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
