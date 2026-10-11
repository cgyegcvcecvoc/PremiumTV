# Scraper status

- **Last run:** 2026-10-11 04:42 PM EDT (2026-10-11 20:42 UTC)
- **Run:** _12:53 PM recheck_ (`recheck`; ID `20261011T203851Z-2648`)
- **Scheduled for:** 2026-10-11T16:53:00Z — started late by +3h 46m
- **Outcome:** **WARNING**
- **Confirmed working:** 9960 / 16940 unique links
- **Dead:** 2842  |  **Unverified:** 4138
- **Unique links found:** 16940 from 21235 source entries
- **Changes vs. PremiumTV_all.m3u:** +741 added / -731 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (172 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (59 confirmed working / 71 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 590 |
| 2 | Lifestyle | 407 |
| 3 | Fox Channels | 25 |
| 4 | CBS | 41 |
| 5 | NBC | 63 |
| 6 | NBC Sports Channels | 7 |
| 7 | Cartoons | 92 |
| 8 | PBS | 17 |
| 9 | Game Shows | 19 |
| 10 | News | 884 |
| 11 | Music | 808 |
| 12 | International | 761 |
| 13 | Europe | 723 |
| 14 | Movies | 697 |
| 15 | Religious | 615 |
| 16 | Entertainment | 556 |
| 17 | South America | 473 |
| 18 | Asia | 440 |
| 19 | United States | 357 |
| 20 | Documentary | 298 |
| 21 | North America | 293 |
| 22 | Kids | 259 |
| 23 | Series | 237 |
| 24 | Education | 123 |
| 25 | Culture | 119 |
| 26 | Legislative | 98 |
| 27 | India | 87 |
| 28 | Comedy | 77 |
| 29 | Business | 63 |
| 30 | Africa | 61 |
| 31 | A&E Networks | 42 |
| 32 | Classic TV | 33 |
| 33 | UK | 33 |
| 34 | Family | 30 |
| 35 | Canada | 20 |
| 36 | Weather | 14 |
| 37 | Tv Reality | 13 |
| 38 | Auto | 11 |
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
| 54 | Other | 412 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 4 | 4 | 3 | 2 | 0 | 2 |
| priority-channels | ok | 13 | 13 | 6 | 13 | 0 | 0 |
| ae-networks | ok | 53 | 53 | 17 | 42 | 3 | 8 |
| aria | ok | 347 | 342 | 113 | 250 | 21 | 71 |
| doms9 | ok | 967 | 950 | 74 | 276 | 113 | 561 |
| xtemus | ok | 317 | 317 | 0 | 2 | 261 | 54 |
| iptv-org | ok | 11181 | 11181 | 3650 | 6538 | 1731 | 2912 |
| free-tv | ok | 2080 | 2054 | 831 | 1069 | 520 | 465 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| m3u 🌱 | ok | 831 | 827 | 178 | 332 | 199 | 296 |
| openstream 🌱 | ok | 5442 | 5442 | 3178 | 5003 | 425 | 14 |

🌱 = source added automatically by the monthly discovery engine: m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **9960** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 590 | 5.9% |
| Lifestyle | 407 | 4.1% |
| Fox Channels | 25 | 0.3% |
| CBS | 41 | 0.4% |
| NBC | 63 | 0.6% |
| NBC Sports Channels | 7 | 0.1% |
| Cartoons | 92 | 0.9% |
| PBS | 17 | 0.2% |
| Game Shows | 19 | 0.2% |
| News | 884 | 8.9% |
| Music | 808 | 8.1% |
| International | 761 | 7.6% |
| Europe | 723 | 7.3% |
| Movies | 697 | 7.0% |
| Religious | 615 | 6.2% |
| Entertainment | 556 | 5.6% |
| South America | 473 | 4.7% |
| Asia | 440 | 4.4% |
| United States | 357 | 3.6% |
| Documentary | 298 | 3.0% |
| North America | 293 | 2.9% |
| Kids | 259 | 2.6% |
| Series | 237 | 2.4% |
| Education | 123 | 1.2% |
| Culture | 119 | 1.2% |
| Legislative | 98 | 1.0% |
| India | 87 | 0.9% |
| Comedy | 77 | 0.8% |
| Business | 63 | 0.6% |
| Africa | 61 | 0.6% |
| A&E Networks | 42 | 0.4% |
| Classic TV | 33 | 0.3% |
| UK | 33 | 0.3% |
| Family | 30 | 0.3% |
| Canada | 20 | 0.2% |
| Weather | 14 | 0.1% |
| Tv Reality | 13 | 0.1% |
| Auto | 11 | 0.1% |
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
| Other | 412 | 4.1% |

## Country playlists (`playlists/countries/` — 172 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 2194 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 972 | [`countries/International.m3u`](countries/International.m3u) |
| India | 682 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 470 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 355 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| UK | 223 | [`countries/UK.m3u`](countries/UK.m3u) |
| France | 204 | [`countries/France.m3u`](countries/France.m3u) |
| Dominican Republic | 199 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Chile | 189 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Spain | 182 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| Brazil | 181 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Germany | 169 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| Argentina | 152 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Netherlands | 148 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Poland | 146 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Ukraine | 143 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Peru | 134 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Canada | 133 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Romania | 129 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Turkey | 126 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Mexico | 119 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Indonesia | 111 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| Hungary | 107 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| Colombia | 103 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| Greece | 86 | [`countries/Greece.m3u`](countries/Greece.m3u) |
| _…and 147 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 59 / 71 unique links (dead: 3, unverified: 9)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | reachable | - | 0 | no_static_playlist | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. (repository is archived) |
| dlive.sx | reachable | 899 | 0 | player_pages_only | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 403 | 0 | 2528 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 404 | 1093 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| TimeoutError | 0 | 797 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 415 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| gaierror | 0 | 388 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 386 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| ConnectionRefusedError | 0 | 111 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 88 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 503 | 0 | 81 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-10-10T23:28:01Z) | 69 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-10-10T23:28:01Z) | 65 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 55 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 400 | 54 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 401 | 0 | 48 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 502 | 0 | 43 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-10-10T23:28:01Z) | 29 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 26 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP timeout (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 26 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 24 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 504 | 0 | 23 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| RemoteDisconnected | 0 | 22 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-06T12:02:47Z) | 20 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 20 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLEOFError | 0 | 19 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 18 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 16 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLError | 0 | 15 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 15 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| OSError | 0 | 14 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| empty response | 14 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 14 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 12 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 500 | 0 | 11 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 11 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 11 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP timeout (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 10 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 9 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 9 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 302 (failed the deep check 1x, last 2026-10-10T23:28:01Z) | 9 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-06T12:02:47Z) | 9 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 451 | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme rtmp | 0 | 8 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 8 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 400 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 8 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP timeout (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 8 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP timeout (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 8 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 530 | 0 | 7 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 302 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: connection refused (failed the deep check 2x, last 2026-10-06T12:02:47Z) | 5 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 5 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-06T12:02:47Z) | 5 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 504 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 5 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 1x, last 2026-10-10T23:28:01Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 523 | 0 | 4 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| invalid URL | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist lists no segments (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 503 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-06T12:02:47Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, dns lookup failed (failed the deep check 1x, last 2026-10-10T23:28:01Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 456 | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-06T12:02:47Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, RemoteDisconnected (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 3x, last 2026-10-10T23:28:01Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 502 (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 503 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP RemoteDisconnected (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP RemoteDisconnected (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-06T12:02:47Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
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
| quarantined: dns lookup failed (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 502 (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 403 (failed the deep check 1x, last 2026-10-10T23:28:01Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 502 (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP RemoteDisconnected (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP timeout (failed the deep check 2x, last 2026-10-06T12:02:47Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP timeout (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 302 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 406 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 1 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 429 | 0 | 1 | The host rate-limited the check; this scraper now limits parallel requests per host and retries with Retry-After/backoff. |
| HTTP 477 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 511 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme rtsp | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-05T12:17:17Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-08T12:02:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: empty response (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 401 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-06T12:02:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 500 (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 502 (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 502 (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 502 (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 503 (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, OSError (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, TimeoutError (failed the deep check 1x, last 2026-10-10T23:28:01Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, dns lookup failed (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, segment too small (214 bytes) (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, segment too small (94 bytes) (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-10-09T11:54:37Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 410 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 502 (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 502 (failed the deep check 2x, last 2026-10-10T23:28:01Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 503 (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 503 (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP ConnectionResetError (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP ConnectionResetError (failed the deep check 2x, last 2026-10-11T11:25:41Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP OSError (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP RemoteDisconnected (failed the deep check 2x, last 2026-10-06T12:02:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP RemoteDisconnected (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP SSLEOFError (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-10T11:11:41Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-10T23:38:59Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP timeout (failed the deep check 2x, last 2026-10-09T11:54:37Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |

### Run/source issues

- 4138 links could not be confirmed after retries (see unverified details).
- 2842 links returned a confirmed failure (see dead details).
- This run started +3h 46m after its scheduled time (2026-10-11T16:53:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
