# Scraper status

- **Last run:** 2026-10-13 05:39 PM EDT (2026-10-13 21:39 UTC)
- **Run:** _12:53 PM recheck_ (`recheck`; ID `20261013T213550Z-2913`)
- **Scheduled for:** 2026-10-13T16:53:00Z — started late by +4h 43m
- **Outcome:** **WARNING**
- **Confirmed working:** 9818 / 16749 unique links
- **Dead:** 3979  |  **Unverified:** 2952
- **Unique links found:** 16749 from 21033 source entries
- **Changes vs. PremiumTV_all.m3u:** +614 added / -400 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (173 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (58 confirmed working / 71 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 553 |
| 2 | Lifestyle | 418 |
| 3 | Fox Channels | 24 |
| 4 | CBS | 40 |
| 5 | NBC | 63 |
| 6 | NBC Sports Channels | 6 |
| 7 | Cartoons | 99 |
| 8 | PBS | 17 |
| 9 | Game Shows | 18 |
| 10 | News | 886 |
| 11 | Music | 794 |
| 12 | International | 742 |
| 13 | Europe | 707 |
| 14 | Movies | 676 |
| 15 | Religious | 609 |
| 16 | Entertainment | 535 |
| 17 | South America | 489 |
| 18 | Asia | 445 |
| 19 | United States | 353 |
| 20 | Documentary | 288 |
| 21 | North America | 278 |
| 22 | Series | 239 |
| 23 | Kids | 237 |
| 24 | Education | 118 |
| 25 | Culture | 115 |
| 26 | Legislative | 101 |
| 27 | India | 89 |
| 28 | Comedy | 76 |
| 29 | Business | 65 |
| 30 | Africa | 62 |
| 31 | A&E Networks | 41 |
| 32 | UK | 36 |
| 33 | Classic TV | 34 |
| 34 | Family | 29 |
| 35 | Canada | 22 |
| 36 | Weather | 14 |
| 37 | Tv Reality | 13 |
| 38 | Auto | 12 |
| 39 | Public TV | 11 |
| 40 | Animals & Nature | 8 |
| 41 | Global TV | 6 |
| 42 | Aria Web Channels | 5 |
| 43 | Relax | 5 |
| 44 | Tv Paranormal | 5 |
| 45 | Australia | 4 |
| 46 | Online TV | 4 |
| 47 | Oceania | 3 |
| 48 | Tv Celebrities | 3 |
| 49 | Tv Shows | 3 |
| 50 | Shopping | 2 |
| 51 | MeTV | 1 |
| 52 | TEST | 1 |
| 53 | United Kingdom | 1 |
| 54 | USA Channels | 1 |
| 55 | Other | 412 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 4 | 4 | 3 | 2 | 2 | 0 |
| priority-channels | ok | 16 | 16 | 6 | 15 | 1 | 0 |
| ae-networks | ok | 53 | 53 | 17 | 41 | 9 | 3 |
| aria | ok | 332 | 327 | 95 | 237 | 22 | 68 |
| doms9 | ok | 708 | 700 | 74 | 226 | 131 | 343 |
| xtemus | ok | 317 | 317 | 0 | 2 | 241 | 74 |
| iptv-org | ok | 11221 | 11221 | 3657 | 6431 | 2758 | 2032 |
| free-tv | ok | 2080 | 2054 | 839 | 1055 | 529 | 470 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| m3u 🌱 | ok | 831 | 827 | 177 | 331 | 395 | 101 |
| openstream 🌱 | ok | 5471 | 5471 | 3186 | 5013 | 438 | 20 |

🌱 = source added automatically by the monthly discovery engine: m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **9818** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 553 | 5.6% |
| Lifestyle | 418 | 4.3% |
| Fox Channels | 24 | 0.2% |
| CBS | 40 | 0.4% |
| NBC | 63 | 0.6% |
| NBC Sports Channels | 6 | 0.1% |
| Cartoons | 99 | 1.0% |
| PBS | 17 | 0.2% |
| Game Shows | 18 | 0.2% |
| News | 886 | 9.0% |
| Music | 794 | 8.1% |
| International | 742 | 7.6% |
| Europe | 707 | 7.2% |
| Movies | 676 | 6.9% |
| Religious | 609 | 6.2% |
| Entertainment | 535 | 5.4% |
| South America | 489 | 5.0% |
| Asia | 445 | 4.5% |
| United States | 353 | 3.6% |
| Documentary | 288 | 2.9% |
| North America | 278 | 2.8% |
| Series | 239 | 2.4% |
| Kids | 237 | 2.4% |
| Education | 118 | 1.2% |
| Culture | 115 | 1.2% |
| Legislative | 101 | 1.0% |
| India | 89 | 0.9% |
| Comedy | 76 | 0.8% |
| Business | 65 | 0.7% |
| Africa | 62 | 0.6% |
| A&E Networks | 41 | 0.4% |
| UK | 36 | 0.4% |
| Classic TV | 34 | 0.3% |
| Family | 29 | 0.3% |
| Canada | 22 | 0.2% |
| Weather | 14 | 0.1% |
| Tv Reality | 13 | 0.1% |
| Auto | 12 | 0.1% |
| Public TV | 11 | 0.1% |
| Animals & Nature | 8 | 0.1% |
| Global TV | 6 | 0.1% |
| Aria Web Channels | 5 | 0.1% |
| Relax | 5 | 0.1% |
| Tv Paranormal | 5 | 0.1% |
| Australia | 4 | 0.0% |
| Online TV | 4 | 0.0% |
| Oceania | 3 | 0.0% |
| Tv Celebrities | 3 | 0.0% |
| Tv Shows | 3 | 0.0% |
| Shopping | 2 | 0.0% |
| MeTV | 1 | 0.0% |
| TEST | 1 | 0.0% |
| United Kingdom | 1 | 0.0% |
| USA Channels | 1 | 0.0% |
| Other | 412 | 4.2% |

## Country playlists (`playlists/countries/` — 173 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 2120 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 971 | [`countries/International.m3u`](countries/International.m3u) |
| India | 689 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 458 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 355 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| UK | 225 | [`countries/UK.m3u`](countries/UK.m3u) |
| France | 193 | [`countries/France.m3u`](countries/France.m3u) |
| Dominican Republic | 182 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Brazil | 180 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Chile | 176 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Germany | 176 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| Spain | 176 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| Argentina | 157 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Netherlands | 154 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Ukraine | 144 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Peru | 142 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Poland | 140 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Canada | 136 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Romania | 135 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Turkey | 131 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Mexico | 123 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Indonesia | 114 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| Colombia | 106 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| Greece | 84 | [`countries/Greece.m3u`](countries/Greece.m3u) |
| Mongolia | 76 | [`countries/Mongolia.m3u`](countries/Mongolia.m3u) |
| _…and 148 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 58 / 71 unique links (dead: 9, unverified: 4)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | reachable | - | 0 | no_static_playlist | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. (repository is archived) |
| dlive.sx | reachable | 899 | 0 | player_pages_only | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 403 | 0 | 1235 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 404 | 1138 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| TimeoutError | 0 | 779 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 414 (failed the deep check 2x, last 2026-10-13T12:42:59Z) | 582 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 414 (failed the deep check 1x, last 2026-10-13T12:42:59Z) | 516 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 414 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| gaierror | 0 | 391 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 373 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| HTTP 503 | 0 | 198 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| ConnectionRefusedError | 0 | 113 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 87 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-10-10T23:28:01Z) | 65 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-10-10T23:28:01Z) | 65 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 400 | 59 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 55 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 401 | 0 | 48 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 502 | 0 | 42 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 30 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-10-10T23:28:01Z) | 29 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP timeout (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 26 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 24 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 504 | 0 | 22 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| SSLError | 0 | 20 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| RemoteDisconnected | 0 | 19 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLEOFError | 0 | 19 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 18 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 17 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-12T13:10:53Z) | 16 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 16 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| OSError | 0 | 15 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 14 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| empty response | 13 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-12T13:10:53Z) | 13 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-13T12:42:59Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 12 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 500 | 0 | 11 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 11 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 9 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 9 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 302 (failed the deep check 1x, last 2026-10-10T23:28:01Z) | 9 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-13T12:42:59Z) | 9 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP timeout (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 9 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 451 | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme rtmp | 0 | 8 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-12T13:10:53Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 8 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP timeout (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 8 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 530 | 0 | 6 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-12T13:10:53Z) | 6 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 302 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 414 (failed the deep check 3x, last 2026-10-13T12:42:59Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP timeout (failed the deep check 2x, last 2026-10-13T12:42:59Z) | 6 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 5 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-12T13:10:53Z) | 5 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 504 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 5 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 1x, last 2026-10-10T23:28:01Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 429 | 0 | 4 | The host rate-limited the check; this scraper now limits parallel requests per host and retries with Retry-After/backoff. |
| HTTP 523 | 0 | 4 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| invalid URL | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist lists no segments (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 503 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, dns lookup failed (failed the deep check 1x, last 2026-10-10T23:28:01Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 500 (failed the deep check 2x, last 2026-10-12T13:10:53Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-13T12:42:59Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 456 | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-13T12:42:59Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, RemoteDisconnected (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-13T12:42:59Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 3x, last 2026-10-10T23:28:01Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 502 (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 503 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP RemoteDisconnected (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP RemoteDisconnected (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP timeout (failed the deep check 1x, last 2026-10-10T23:28:01Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 409 | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 521 | 0 | 2 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme mmsh | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: connection refused (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: connection refused (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: connection refused (failed the deep check 2x, last 2026-10-12T13:10:53Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: dns lookup failed (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-13T12:42:59Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 403 (failed the deep check 1x, last 2026-10-10T23:28:01Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP RemoteDisconnected (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP RemoteDisconnected (failed the deep check 2x, last 2026-10-12T13:10:53Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP timeout (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 406 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 1 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 477 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 511 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme rtsp | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-08T12:02:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-13T12:42:59Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: connection refused (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: dash manifest has no representations (failed the deep check 2x, last 2026-10-12T13:10:53Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 401 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-13T12:42:59Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 500 (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 500 (failed the deep check 2x, last 2026-10-13T12:42:59Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 502 (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 503 (failed the deep check 2x, last 2026-10-12T13:10:53Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, OSError (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, OSError (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, TimeoutError (failed the deep check 1x, last 2026-10-10T23:28:01Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, dns lookup failed (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, segment too small (214 bytes) (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, segment too small (94 bytes) (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-10-09T11:54:37Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 410 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 502 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 502 (failed the deep check 2x, last 2026-10-12T13:10:53Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 503 (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 503 (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP ConnectionResetError (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP ConnectionResetError (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP OSError (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP RemoteDisconnected (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP SSLEOFError (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-12T13:10:53Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP timeout (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP timeout (failed the deep check 2x, last 2026-10-12T13:10:53Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |

### Run/source issues

- 2952 links could not be confirmed after retries (see unverified details).
- 3979 links returned a confirmed failure (see dead details).
- This run started +4h 43m after its scheduled time (2026-10-13T16:53:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
