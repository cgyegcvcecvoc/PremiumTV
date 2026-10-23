# Scraper status

- **Last run:** 2026-10-23 07:31 PM EDT (2026-10-23 23:31 UTC)
- **Run:** _4:41 PM final check_ (`final_check`; ID `20261023T232757Z-2936`)
- **Scheduled for:** 2026-10-23T20:41:00Z — started late by +2h 47m
- **Outcome:** **WARNING**
- **Confirmed working:** 11792 / 16779 unique links
- **Dead:** 2463  |  **Unverified:** 2524
- **Retained (unverified, within grace):** 1738 previously published links kept so their channels do not vanish after one unverifiable run
- **Unique links found:** 16779 from 21849 source entries
- **Changes vs. PremiumTV_all.m3u:** +495 added / -483 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (180 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (68 confirmed working / 73 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 759 |
| 2 | Lifestyle | 538 |
| 3 | Fox Channels | 26 |
| 4 | CBS | 41 |
| 5 | NBC | 67 |
| 6 | NBC Sports Channels | 7 |
| 7 | Cartoons | 208 |
| 8 | PBS | 18 |
| 9 | Game Shows | 18 |
| 10 | News | 1141 |
| 11 | Movies | 1025 |
| 12 | International | 1003 |
| 13 | Music | 962 |
| 14 | Europe | 935 |
| 15 | Entertainment | 854 |
| 16 | Religious | 692 |
| 17 | Asia | 654 |
| 18 | South America | 575 |
| 19 | Series | 522 |
| 20 | United States | 430 |
| 21 | Documentary | 410 |
| 22 | Kids | 398 |
| 23 | North America | 339 |
| 24 | Comedy | 189 |
| 25 | Education | 172 |
| 26 | Culture | 155 |
| 27 | Legislative | 150 |
| 28 | Africa | 100 |
| 29 | India | 91 |
| 30 | Business | 78 |
| 31 | Classic TV | 76 |
| 32 | UK | 70 |
| 33 | A&E Networks | 50 |
| 34 | Canada | 49 |
| 35 | Family | 35 |
| 36 | Australia | 27 |
| 37 | Animals & Nature | 23 |
| 38 | Auto | 23 |
| 39 | Global TV | 22 |
| 40 | Weather | 19 |
| 41 | Tv Paranormal | 18 |
| 42 | Tv Reality | 17 |
| 43 | DLTV | 16 |
| 44 | Digital TV | 15 |
| 45 | Online TV | 15 |
| 46 | Public TV | 12 |
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
| 57 | Tv Pets | 1 |
| 58 | United Kingdom | 1 |
| 59 | USA Channels | 1 |
| 60 | Other | 446 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 4 | 4 | 3 | 2 | 2 | 0 |
| priority-channels | ok | 18 | 18 | 8 | 18 | 0 | 0 |
| ae-networks | ok | 53 | 53 | 16 | 50 | 2 | 1 |
| aria | ok | 312 | 308 | 91 | 216 | 15 | 77 |
| doms9 | ok | 687 | 684 | 82 | 267 | 45 | 372 |
| xtemus | ok | 317 | 317 | 0 | 31 | 251 | 35 |
| iptv-org | ok | 11302 | 11302 | 3631 | 7957 | 1592 | 1753 |
| free-tv | ok | 2052 | 2028 | 811 | 1211 | 481 | 336 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| m3u 🌱 | ok | 1674 | 832 | 174 | 666 | 116 | 49 |
| openstream 🌱 | ok | 5430 | 5430 | 3159 | 5197 | 198 | 35 |

🌱 = source added automatically by the monthly discovery engine: m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **13530** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 759 | 5.6% |
| Lifestyle | 538 | 4.0% |
| Fox Channels | 26 | 0.2% |
| CBS | 41 | 0.3% |
| NBC | 67 | 0.5% |
| NBC Sports Channels | 7 | 0.1% |
| Cartoons | 208 | 1.5% |
| PBS | 18 | 0.1% |
| Game Shows | 18 | 0.1% |
| News | 1141 | 8.4% |
| Movies | 1025 | 7.6% |
| International | 1003 | 7.4% |
| Music | 962 | 7.1% |
| Europe | 935 | 6.9% |
| Entertainment | 854 | 6.3% |
| Religious | 692 | 5.1% |
| Asia | 654 | 4.8% |
| South America | 575 | 4.2% |
| Series | 522 | 3.9% |
| United States | 430 | 3.2% |
| Documentary | 410 | 3.0% |
| Kids | 398 | 2.9% |
| North America | 339 | 2.5% |
| Comedy | 189 | 1.4% |
| Education | 172 | 1.3% |
| Culture | 155 | 1.1% |
| Legislative | 150 | 1.1% |
| Africa | 100 | 0.7% |
| India | 91 | 0.7% |
| Business | 78 | 0.6% |
| Classic TV | 76 | 0.6% |
| UK | 70 | 0.5% |
| A&E Networks | 50 | 0.4% |
| Canada | 49 | 0.4% |
| Family | 35 | 0.3% |
| Australia | 27 | 0.2% |
| Animals & Nature | 23 | 0.2% |
| Auto | 23 | 0.2% |
| Global TV | 22 | 0.2% |
| Weather | 19 | 0.1% |
| Tv Paranormal | 18 | 0.1% |
| Tv Reality | 17 | 0.1% |
| DLTV | 16 | 0.1% |
| Digital TV | 15 | 0.1% |
| Online TV | 15 | 0.1% |
| Public TV | 12 | 0.1% |
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
| Tv Pets | 1 | 0.0% |
| United Kingdom | 1 | 0.0% |
| USA Channels | 1 | 0.0% |
| Other | 446 | 3.3% |

## Country playlists (`playlists/countries/` — 180 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 2998 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1237 | [`countries/International.m3u`](countries/International.m3u) |
| India | 762 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 582 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 509 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Germany | 423 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| Sweden | 385 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| UK | 341 | [`countries/UK.m3u`](countries/UK.m3u) |
| Spain | 255 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| Brazil | 249 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| France | 249 | [`countries/France.m3u`](countries/France.m3u) |
| Chile | 224 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Dominican Republic | 207 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Ukraine | 193 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Canada | 189 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Poland | 187 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Argentina | 172 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| China | 164 | [`countries/China.m3u`](countries/China.m3u) |
| Mexico | 163 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Netherlands | 159 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Peru | 158 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Turkey | 153 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Romania | 137 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Indonesia | 127 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| Colombia | 126 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| _…and 155 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 68 / 73 unique links (dead: 4, unverified: 1)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | reachable | - | 0 | no_static_playlist | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. (repository is archived) |
| dlive.sx | reachable | 899 | 0 | player_pages_only | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 403 | 0 | 1309 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 404 | 1153 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| TimeoutError | 0 | 836 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 379 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-10-20T10:13:37Z) | 309 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 106 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-10-20T10:13:37Z) | 99 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| gaierror | 0 | 95 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 400 | 75 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 401 | 0 | 46 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 503 | 0 | 41 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 37 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| OSError | 0 | 33 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 504 | 0 | 23 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-19T10:50:27Z) | 22 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-10-22T10:19:47Z) | 22 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| ConnectionRefusedError | 0 | 20 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| SSLEOFError | 0 | 20 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| SSLError | 0 | 19 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-17T09:20:11Z) | 19 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| RemoteDisconnected | 0 | 18 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 502 | 0 | 16 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-20T10:13:37Z) | 15 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-22T10:19:47Z) | 14 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-10-21T10:17:30Z) | 14 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| empty response | 13 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| HTTP 500 | 0 | 12 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-21T10:17:30Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-10-19T10:50:27Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 451 | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 530 | 0 | 8 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme rtmp | 0 | 8 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-10-19T10:50:27Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-19T10:50:27Z) | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-20T10:13:37Z) | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-10-19T10:50:27Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-22T10:19:47Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-17T09:20:11Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-17T09:20:11Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| invalid URL | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-18T09:38:18Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-10-21T10:17:30Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 400 (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-10-20T10:13:37Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, dns lookup failed (failed the deep check 1x, last 2026-10-20T10:13:37Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-21T10:17:30Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 458 | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-21T10:17:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 2x, last 2026-10-20T10:13:37Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-10-21T10:17:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-10-21T10:17:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-21T10:17:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 2 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 429 | 0 | 2 | The host rate-limited the check; this scraper now limits parallel requests per host and retries with Retry-After/backoff. |
| HTTP 456 | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 523 | 0 | 2 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme mmsh | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-10-22T10:19:47Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 2x, last 2026-10-17T09:20:11Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
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
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 511 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme rtsp | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-17T09:20:11Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 422 (failed the deep check 1x, last 2026-10-19T10:50:27Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist lists no segments (failed the deep check 1x, last 2026-10-18T09:38:18Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 2x, last 2026-10-17T09:20:11Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
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

- 2524 links could not be confirmed after retries (see unverified details).
- 2463 links returned a confirmed failure (see dead details).
- This run started +2h 47m after its scheduled time (2026-10-23T20:41:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
