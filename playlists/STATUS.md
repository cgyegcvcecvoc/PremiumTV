# Scraper status

- **Last run:** 2026-10-25 01:17 PM EDT (2026-10-25 17:17 UTC)
- **Run:** _9:41 AM recheck_ (`recheck`; ID `20261025T171359Z-2702`)
- **Scheduled for:** 2026-10-25T13:41:00Z — started late by +3h 33m
- **Outcome:** **WARNING**
- **Confirmed working:** 11785 / 17293 unique links
- **Dead:** 2632  |  **Unverified:** 2876
- **Retained (unverified, within grace):** 1766 previously published links kept so their channels do not vanish after one unverifiable run
- **Unique links found:** 17293 from 21515 source entries
- **Changes vs. PremiumTV_all.m3u:** +1112 added / -660 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (178 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (69 confirmed working / 74 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 771 |
| 2 | Sports Backups | 3 |
| 3 | Lifestyle | 543 |
| 4 | Fox Channels | 27 |
| 5 | CBS | 41 |
| 6 | NBC | 64 |
| 7 | NBC Sports Channels | 6 |
| 8 | Cartoons | 206 |
| 9 | PBS | 18 |
| 10 | Game Shows | 20 |
| 11 | News | 1126 |
| 12 | Movies | 1027 |
| 13 | International | 1016 |
| 14 | Music | 973 |
| 15 | Europe | 938 |
| 16 | Entertainment | 865 |
| 17 | Religious | 701 |
| 18 | Asia | 650 |
| 19 | South America | 573 |
| 20 | Series | 535 |
| 21 | United States | 424 |
| 22 | Documentary | 415 |
| 23 | Kids | 400 |
| 24 | North America | 330 |
| 25 | Comedy | 187 |
| 26 | Education | 173 |
| 27 | Legislative | 153 |
| 28 | Culture | 152 |
| 29 | Africa | 104 |
| 30 | India | 98 |
| 31 | Classic TV | 80 |
| 32 | Business | 75 |
| 33 | UK | 68 |
| 34 | A&E Networks | 50 |
| 35 | Canada | 49 |
| 36 | Family | 39 |
| 37 | Australia | 32 |
| 38 | Auto | 23 |
| 39 | Global TV | 23 |
| 40 | Weather | 19 |
| 41 | Public TV | 17 |
| 42 | DLTV | 16 |
| 43 | Digital TV | 15 |
| 44 | Online TV | 15 |
| 45 | Animals & Nature | 14 |
| 46 | Tv Reality | 13 |
| 47 | Tv Paranormal | 11 |
| 48 | Tv Celebrities | 9 |
| 49 | Tv Shows | 6 |
| 50 | Aria Web Channels | 5 |
| 51 | Oceania | 5 |
| 52 | Relax | 4 |
| 53 | Anime | 2 |
| 54 | Shopping | 2 |
| 55 | United Kingdom | 2 |
| 56 | 3-Radio#Chicago | 1 |
| 57 | MeTV | 1 |
| 58 | TEST | 1 |
| 59 | USA Channels | 1 |
| 60 | Other | 414 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 4 | 4 | 3 | 2 | 2 | 0 |
| priority-channels | ok | 17 | 17 | 10 | 17 | 0 | 0 |
| ae-networks | ok | 53 | 53 | 16 | 50 | 2 | 1 |
| aria | ok | 304 | 300 | 88 | 222 | 10 | 68 |
| doms9 | ok | 1168 | 1166 | 82 | 263 | 203 | 700 |
| xtemus | ok | 317 | 317 | 0 | 32 | 250 | 35 |
| iptv-org | ok | 11333 | 11333 | 3621 | 7986 | 1591 | 1756 |
| free-tv | ok | 2052 | 2028 | 807 | 1211 | 453 | 364 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| m3u 🌱 | ok | 842 | 837 | 174 | 672 | 114 | 50 |
| openstream 🌱 | ok | 5425 | 5425 | 3157 | 5179 | 225 | 21 |

🌱 = source added automatically by the monthly discovery engine: m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **13551** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 771 | 5.7% |
| Sports Backups | 3 | 0.0% |
| Lifestyle | 543 | 4.0% |
| Fox Channels | 27 | 0.2% |
| CBS | 41 | 0.3% |
| NBC | 64 | 0.5% |
| NBC Sports Channels | 6 | 0.0% |
| Cartoons | 206 | 1.5% |
| PBS | 18 | 0.1% |
| Game Shows | 20 | 0.1% |
| News | 1126 | 8.3% |
| Movies | 1027 | 7.6% |
| International | 1016 | 7.5% |
| Music | 973 | 7.2% |
| Europe | 938 | 6.9% |
| Entertainment | 865 | 6.4% |
| Religious | 701 | 5.2% |
| Asia | 650 | 4.8% |
| South America | 573 | 4.2% |
| Series | 535 | 3.9% |
| United States | 424 | 3.1% |
| Documentary | 415 | 3.1% |
| Kids | 400 | 3.0% |
| North America | 330 | 2.4% |
| Comedy | 187 | 1.4% |
| Education | 173 | 1.3% |
| Legislative | 153 | 1.1% |
| Culture | 152 | 1.1% |
| Africa | 104 | 0.8% |
| India | 98 | 0.7% |
| Classic TV | 80 | 0.6% |
| Business | 75 | 0.6% |
| UK | 68 | 0.5% |
| A&E Networks | 50 | 0.4% |
| Canada | 49 | 0.4% |
| Family | 39 | 0.3% |
| Australia | 32 | 0.2% |
| Auto | 23 | 0.2% |
| Global TV | 23 | 0.2% |
| Weather | 19 | 0.1% |
| Public TV | 17 | 0.1% |
| DLTV | 16 | 0.1% |
| Digital TV | 15 | 0.1% |
| Online TV | 15 | 0.1% |
| Animals & Nature | 14 | 0.1% |
| Tv Reality | 13 | 0.1% |
| Tv Paranormal | 11 | 0.1% |
| Tv Celebrities | 9 | 0.1% |
| Tv Shows | 6 | 0.0% |
| Aria Web Channels | 5 | 0.0% |
| Oceania | 5 | 0.0% |
| Relax | 4 | 0.0% |
| Anime | 2 | 0.0% |
| Shopping | 2 | 0.0% |
| United Kingdom | 2 | 0.0% |
| 3-Radio#Chicago | 1 | 0.0% |
| MeTV | 1 | 0.0% |
| TEST | 1 | 0.0% |
| USA Channels | 1 | 0.0% |
| Other | 414 | 3.1% |

## Country playlists (`playlists/countries/` — 178 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 2970 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1216 | [`countries/International.m3u`](countries/International.m3u) |
| India | 795 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 585 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 523 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Germany | 413 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| Sweden | 385 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| UK | 345 | [`countries/UK.m3u`](countries/UK.m3u) |
| Spain | 264 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| France | 255 | [`countries/France.m3u`](countries/France.m3u) |
| Brazil | 250 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Chile | 218 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Dominican Republic | 204 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Ukraine | 197 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Canada | 189 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Poland | 188 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Netherlands | 173 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Argentina | 170 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| China | 159 | [`countries/China.m3u`](countries/China.m3u) |
| Turkey | 156 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Mexico | 155 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Peru | 152 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Romania | 145 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Colombia | 125 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| Indonesia | 125 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| _…and 153 more countries_ | | [Full country index](countries/README.md) |

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
| HTTP 403 | 0 | 1655 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 404 | 1338 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| TimeoutError | 0 | 862 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 379 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-10-20T10:13:37Z) | 309 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-10-24T12:31:30Z) | 140 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-10-20T10:13:37Z) | 99 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| gaierror | 0 | 94 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 400 | 74 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 401 | 0 | 49 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 503 | 0 | 38 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 504 | 0 | 23 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: connection refused (failed the deep check 1x, last 2026-10-22T10:19:47Z) | 23 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| ConnectionRefusedError | 0 | 20 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| SSLError | 0 | 20 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-19T10:50:27Z) | 20 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLEOFError | 0 | 19 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| OSError | 0 | 18 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| RemoteDisconnected | 0 | 16 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-20T10:13:37Z) | 16 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 1x, last 2026-10-24T12:31:30Z) | 16 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 502 | 0 | 15 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-22T10:19:47Z) | 14 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-10-21T10:17:30Z) | 14 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 500 | 0 | 13 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| empty response | 13 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 1x, last 2026-10-24T12:31:30Z) | 11 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-21T10:17:30Z) | 10 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 1x, last 2026-10-24T12:31:30Z) | 10 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 530 | 0 | 8 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme rtmp | 0 | 8 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-10-19T10:50:27Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-10-19T10:50:27Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 451 | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-19T10:50:27Z) | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-24T12:31:30Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-20T10:13:37Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-10-19T10:50:27Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-22T10:19:47Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-24T12:31:30Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-10-24T12:31:30Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| invalid URL | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-10-21T10:17:30Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-10-20T10:13:37Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, dns lookup failed (failed the deep check 1x, last 2026-10-20T10:13:37Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-21T10:17:30Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 523 | 0 | 3 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-21T10:17:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 2x, last 2026-10-20T10:13:37Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-10-21T10:17:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-10-21T10:17:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-10-24T12:31:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-21T10:17:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 1x, last 2026-10-24T12:31:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-10-21T10:17:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-24T12:31:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 2 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| deep check: offline (variant HTTP 404) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme mmsh | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-10-22T10:19:47Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-19T10:50:27Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-10-24T12:31:30Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-10-19T10:50:27Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-19T10:50:27Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 302 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 406 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 409 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 422 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 456 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| deep check: offline (variant HTTP 403) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme rtsp | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: connection refused (failed the deep check 2x, last 2026-10-19T10:50:27Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-10-20T10:13:37Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-10-22T10:19:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-21T10:17:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-10-22T10:19:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-22T10:19:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-24T12:31:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 3x, last 2026-10-24T12:31:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-10-20T10:13:37Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 1x, last 2026-10-22T10:19:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-10-21T10:17:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, segment too small (214 bytes) (failed the deep check 1x, last 2026-10-20T10:13:37Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-10-19T10:50:27Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-10-22T10:19:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 410 (failed the deep check 1x, last 2026-10-24T12:31:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |

### Run/source issues

- 2876 links could not be confirmed after retries (see unverified details).
- 2632 links returned a confirmed failure (see dead details).
- This run started +3h 33m after its scheduled time (2026-10-25T13:41:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
