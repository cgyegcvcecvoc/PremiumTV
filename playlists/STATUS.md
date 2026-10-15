# Scraper status

- **Last run:** 2026-10-15 06:27 PM EDT (2026-10-15 22:27 UTC)
- **Run:** _manual re-scrape (run-scrape.txt)_ (`manual`; ID `20261015T222335Z-2913`)
- **Outcome:** **WARNING**
- **Confirmed working:** 11705 / 16753 unique links
- **Dead:** 2060  |  **Unverified:** 2988
- **Unique links found:** 16753 from 20987 source entries
- **Changes vs. PremiumTV_all.m3u:** +192 added / -285 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (177 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (67 confirmed working / 71 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 624 |
| 2 | Lifestyle | 492 |
| 3 | Fox Channels | 24 |
| 4 | CBS | 43 |
| 5 | NBC | 63 |
| 6 | NBC Sports Channels | 9 |
| 7 | Cartoons | 192 |
| 8 | PBS | 18 |
| 9 | Game Shows | 19 |
| 10 | News | 967 |
| 11 | Movies | 963 |
| 12 | Music | 869 |
| 13 | International | 782 |
| 14 | Europe | 771 |
| 15 | Entertainment | 755 |
| 16 | Religious | 641 |
| 17 | Series | 516 |
| 18 | South America | 498 |
| 19 | Asia | 465 |
| 20 | Documentary | 402 |
| 21 | United States | 368 |
| 22 | Kids | 351 |
| 23 | North America | 290 |
| 24 | Comedy | 172 |
| 25 | Education | 131 |
| 26 | Culture | 124 |
| 27 | Legislative | 107 |
| 28 | India | 91 |
| 29 | Classic TV | 74 |
| 30 | Africa | 67 |
| 31 | Business | 67 |
| 32 | A&E Networks | 50 |
| 33 | UK | 37 |
| 34 | Family | 32 |
| 35 | Canada | 26 |
| 36 | Auto | 23 |
| 37 | Australia | 17 |
| 38 | Weather | 16 |
| 39 | DLTV | 15 |
| 40 | Animals & Nature | 13 |
| 41 | Tv Reality | 13 |
| 42 | Public TV | 11 |
| 43 | Global TV | 10 |
| 44 | Tv Paranormal | 10 |
| 45 | Tv Celebrities | 7 |
| 46 | Tv Shows | 7 |
| 47 | Online TV | 6 |
| 48 | Aria Web Channels | 5 |
| 49 | Oceania | 5 |
| 50 | Relax | 5 |
| 51 | Shopping | 2 |
| 52 | 3-Radio#Chicago | 1 |
| 53 | MeTV | 1 |
| 54 | TEST | 1 |
| 55 | United Kingdom | 1 |
| 56 | USA Channels | 1 |
| 57 | Other | 435 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 4 | 4 | 3 | 2 | 2 | 0 |
| priority-channels | ok | 18 | 18 | 10 | 18 | 0 | 0 |
| ae-networks | ok | 53 | 53 | 17 | 50 | 0 | 3 |
| aria | ok | 320 | 316 | 94 | 229 | 14 | 73 |
| doms9 | ok | 661 | 656 | 76 | 240 | 109 | 307 |
| xtemus | ok | 317 | 317 | 0 | 24 | 219 | 74 |
| iptv-org | ok | 11340 | 11340 | 3624 | 7988 | 1237 | 2115 |
| free-tv | ok | 2023 | 1998 | 810 | 1146 | 424 | 428 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| m3u 🌱 | ok | 831 | 827 | 177 | 630 | 94 | 103 |
| openstream 🌱 | ok | 5420 | 5420 | 3163 | 5166 | 233 | 21 |

🌱 = source added automatically by the monthly discovery engine: m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **11705** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 624 | 5.3% |
| Lifestyle | 492 | 4.2% |
| Fox Channels | 24 | 0.2% |
| CBS | 43 | 0.4% |
| NBC | 63 | 0.5% |
| NBC Sports Channels | 9 | 0.1% |
| Cartoons | 192 | 1.6% |
| PBS | 18 | 0.2% |
| Game Shows | 19 | 0.2% |
| News | 967 | 8.3% |
| Movies | 963 | 8.2% |
| Music | 869 | 7.4% |
| International | 782 | 6.7% |
| Europe | 771 | 6.6% |
| Entertainment | 755 | 6.5% |
| Religious | 641 | 5.5% |
| Series | 516 | 4.4% |
| South America | 498 | 4.3% |
| Asia | 465 | 4.0% |
| Documentary | 402 | 3.4% |
| United States | 368 | 3.1% |
| Kids | 351 | 3.0% |
| North America | 290 | 2.5% |
| Comedy | 172 | 1.5% |
| Education | 131 | 1.1% |
| Culture | 124 | 1.1% |
| Legislative | 107 | 0.9% |
| India | 91 | 0.8% |
| Classic TV | 74 | 0.6% |
| Africa | 67 | 0.6% |
| Business | 67 | 0.6% |
| A&E Networks | 50 | 0.4% |
| UK | 37 | 0.3% |
| Family | 32 | 0.3% |
| Canada | 26 | 0.2% |
| Auto | 23 | 0.2% |
| Australia | 17 | 0.1% |
| Weather | 16 | 0.1% |
| DLTV | 15 | 0.1% |
| Animals & Nature | 13 | 0.1% |
| Tv Reality | 13 | 0.1% |
| Public TV | 11 | 0.1% |
| Global TV | 10 | 0.1% |
| Tv Paranormal | 10 | 0.1% |
| Tv Celebrities | 7 | 0.1% |
| Tv Shows | 7 | 0.1% |
| Online TV | 6 | 0.1% |
| Aria Web Channels | 5 | 0.0% |
| Oceania | 5 | 0.0% |
| Relax | 5 | 0.0% |
| Shopping | 2 | 0.0% |
| 3-Radio#Chicago | 1 | 0.0% |
| MeTV | 1 | 0.0% |
| TEST | 1 | 0.0% |
| United Kingdom | 1 | 0.0% |
| USA Channels | 1 | 0.0% |
| Other | 435 | 3.7% |

## Country playlists (`playlists/countries/` — 177 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 2753 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1161 | [`countries/International.m3u`](countries/International.m3u) |
| India | 715 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 488 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 412 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Germany | 393 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| Sweden | 379 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| UK | 247 | [`countries/UK.m3u`](countries/UK.m3u) |
| Poland | 210 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| France | 204 | [`countries/France.m3u`](countries/France.m3u) |
| Chile | 200 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Spain | 193 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| Dominican Republic | 191 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Brazil | 178 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Ukraine | 174 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Argentina | 162 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Canada | 148 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Peru | 147 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Netherlands | 145 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Turkey | 137 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Romania | 136 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Mexico | 124 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Indonesia | 110 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| Colombia | 108 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| Greece | 83 | [`countries/Greece.m3u`](countries/Greece.m3u) |
| _…and 152 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 67 / 71 unique links (dead: 0, unverified: 4)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | reachable | - | 0 | no_static_playlist | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. (repository is archived) |
| dlive.sx | reachable | 899 | 0 | player_pages_only | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 403 | 0 | 1273 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 404 | 1091 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| TimeoutError | 0 | 804 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| gaierror | 0 | 423 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 371 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| HTTP 503 | 0 | 166 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| ConnectionRefusedError | 0 | 111 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 87 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-10-10T23:28:01Z) | 65 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 54 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 400 | 49 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 401 | 0 | 48 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 31 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-10-10T23:28:01Z) | 29 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 504 | 0 | 23 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-12T13:10:53Z) | 23 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLEOFError | 0 | 21 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-14T10:10:14Z) | 21 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLError | 0 | 20 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 20 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 502 | 0 | 16 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 500 | 0 | 15 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| OSError | 0 | 15 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-13T12:42:59Z) | 15 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| RemoteDisconnected | 0 | 14 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| empty response | 13 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 13 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 2x, last 2026-10-15T15:47:48Z) | 13 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 2x, last 2026-10-14T10:10:14Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-15T09:52:34Z) | 10 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-15T15:47:48Z) | 9 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 451 | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme rtmp | 0 | 8 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| HTTP 530 | 0 | 6 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-12T13:10:53Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-14T10:10:14Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 523 | 0 | 4 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| invalid URL | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, dns lookup failed (failed the deep check 1x, last 2026-10-10T23:28:01Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 456 | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| deep check: offline (playlist only, timeout) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| deep check: offline (variant HTTP TimeoutError) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: dns lookup failed (failed the deep check 2x, last 2026-10-15T09:52:34Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist lists no segments (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-13T12:42:59Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-15T09:52:34Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 409 | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 429 | 0 | 2 | The host rate-limited the check; this scraper now limits parallel requests per host and retries with Retry-After/backoff. |
| HTTP 521 | 0 | 2 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| deep check: offline (variant HTTP 404) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme mmsh | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: connection refused (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: connection refused (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: connection refused (failed the deep check 2x, last 2026-10-12T13:10:53Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: empty response (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-14T10:10:14Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-15T09:52:34Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-15T15:47:48Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 302 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 406 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 408 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 410 | 1 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 477 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 511 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| deep check: offline (playlist only, SSLEOFError) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| deep check: offline (playlist only, TimeoutError) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| deep check: offline (variant HTTP 400) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| deep check: offline (variant HTTP 502) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| deep check: offline (variant HTTP RemoteDisconnected) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme rtsp | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-13T12:42:59Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: dash manifest has no representations (failed the deep check 2x, last 2026-10-12T13:10:53Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dash manifest has no representations (failed the deep check 2x, last 2026-10-14T10:10:14Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist lists no segments (failed the deep check 2x, last 2026-10-14T10:10:14Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 304 (failed the deep check 2x, last 2026-10-15T15:47:48Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 401 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-13T12:42:59Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, OSError (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, dns lookup failed (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-10-15T15:47:48Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, segment too small (214 bytes) (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, segment too small (94 bytes) (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |

### Run/source issues

- 2988 links could not be confirmed after retries (see unverified details).
- 2060 links returned a confirmed failure (see dead details).
