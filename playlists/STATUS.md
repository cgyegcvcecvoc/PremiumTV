# Scraper status

- **Last run:** 2026-10-30 06:11 PM EDT (2026-10-30 22:11 UTC)
- **Run:** _manual re-scrape (run-scrape.txt)_ (`manual`; ID `20261030T220753Z-2883`)
- **Outcome:** **WARNING**
- **Confirmed working:** 12168 / 16781 unique links
- **Dead:** 1746  |  **Unverified:** 2867
- **Retained (unverified, within grace):** 241 previously published links kept so their channels do not vanish after one unverifiable run
- **Unique links found:** 16781 from 20990 source entries
- **Changes vs. PremiumTV_all.m3u:** +884 added / -1396 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (177 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (70 confirmed working / 74 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 633 |
| 2 | Sports Backups | 3 |
| 3 | Lifestyle | 533 |
| 4 | Fox Channels | 24 |
| 5 | CBS | 39 |
| 6 | NBC | 62 |
| 7 | NBC Sports Channels | 6 |
| 8 | Cartoons | 191 |
| 9 | PBS | 19 |
| 10 | Game Shows | 19 |
| 11 | News | 1036 |
| 12 | Movies | 965 |
| 13 | Music | 924 |
| 14 | International | 867 |
| 15 | Europe | 825 |
| 16 | Entertainment | 824 |
| 17 | Religious | 678 |
| 18 | Series | 526 |
| 19 | Asia | 521 |
| 20 | South America | 519 |
| 21 | Documentary | 413 |
| 22 | United States | 411 |
| 23 | Kids | 370 |
| 24 | North America | 310 |
| 25 | Comedy | 180 |
| 26 | Education | 151 |
| 27 | Culture | 139 |
| 28 | Legislative | 131 |
| 29 | India | 103 |
| 30 | Classic TV | 79 |
| 31 | Africa | 76 |
| 32 | Business | 70 |
| 33 | A&E Networks | 50 |
| 34 | UK | 43 |
| 35 | Family | 37 |
| 36 | Canada | 25 |
| 37 | Auto | 24 |
| 38 | Australia | 23 |
| 39 | Public TV | 20 |
| 40 | Weather | 17 |
| 41 | DLTV | 15 |
| 42 | Animals & Nature | 13 |
| 43 | Global TV | 13 |
| 44 | Tv Reality | 13 |
| 45 | Tv Paranormal | 11 |
| 46 | Online TV | 10 |
| 47 | Tv Celebrities | 9 |
| 48 | Aria Web Channels | 6 |
| 49 | Tv Shows | 6 |
| 50 | Oceania | 5 |
| 51 | Relax | 5 |
| 52 | Shopping | 2 |
| 53 | United Kingdom | 2 |
| 54 | 3-Radio#Chicago | 1 |
| 55 | MeTV | 1 |
| 56 | TEST | 1 |
| 57 | USA Channels | 1 |
| 58 | Other | 409 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 4 | 4 | 3 | 2 | 2 | 0 |
| priority-channels | ok | 17 | 17 | 10 | 17 | 0 | 0 |
| ae-networks | ok | 53 | 53 | 16 | 50 | 0 | 3 |
| aria | ok | 302 | 298 | 87 | 224 | 9 | 65 |
| doms9 | ok | 595 | 592 | 82 | 191 | 80 | 321 |
| xtemus | ok | 317 | 317 | 0 | 32 | 233 | 52 |
| iptv-org | ok | 11379 | 11379 | 3597 | 8412 | 968 | 1999 |
| free-tv | ok | 2053 | 2029 | 803 | 1233 | 349 | 447 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| m3u 🌱 | ok | 842 | 837 | 174 | 665 | 81 | 90 |
| openstream 🌱 | ok | 5428 | 5428 | 3147 | 5228 | 182 | 18 |

🌱 = source added automatically by the monthly discovery engine: m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **12409** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 633 | 5.1% |
| Sports Backups | 3 | 0.0% |
| Lifestyle | 533 | 4.3% |
| Fox Channels | 24 | 0.2% |
| CBS | 39 | 0.3% |
| NBC | 62 | 0.5% |
| NBC Sports Channels | 6 | 0.0% |
| Cartoons | 191 | 1.5% |
| PBS | 19 | 0.2% |
| Game Shows | 19 | 0.2% |
| News | 1036 | 8.3% |
| Movies | 965 | 7.8% |
| Music | 924 | 7.4% |
| International | 867 | 7.0% |
| Europe | 825 | 6.6% |
| Entertainment | 824 | 6.6% |
| Religious | 678 | 5.5% |
| Series | 526 | 4.2% |
| Asia | 521 | 4.2% |
| South America | 519 | 4.2% |
| Documentary | 413 | 3.3% |
| United States | 411 | 3.3% |
| Kids | 370 | 3.0% |
| North America | 310 | 2.5% |
| Comedy | 180 | 1.5% |
| Education | 151 | 1.2% |
| Culture | 139 | 1.1% |
| Legislative | 131 | 1.1% |
| India | 103 | 0.8% |
| Classic TV | 79 | 0.6% |
| Africa | 76 | 0.6% |
| Business | 70 | 0.6% |
| A&E Networks | 50 | 0.4% |
| UK | 43 | 0.3% |
| Family | 37 | 0.3% |
| Canada | 25 | 0.2% |
| Auto | 24 | 0.2% |
| Australia | 23 | 0.2% |
| Public TV | 20 | 0.2% |
| Weather | 17 | 0.1% |
| DLTV | 15 | 0.1% |
| Animals & Nature | 13 | 0.1% |
| Global TV | 13 | 0.1% |
| Tv Reality | 13 | 0.1% |
| Tv Paranormal | 11 | 0.1% |
| Online TV | 10 | 0.1% |
| Tv Celebrities | 9 | 0.1% |
| Aria Web Channels | 6 | 0.0% |
| Tv Shows | 6 | 0.0% |
| Oceania | 5 | 0.0% |
| Relax | 5 | 0.0% |
| Shopping | 2 | 0.0% |
| United Kingdom | 2 | 0.0% |
| 3-Radio#Chicago | 1 | 0.0% |
| MeTV | 1 | 0.0% |
| TEST | 1 | 0.0% |
| USA Channels | 1 | 0.0% |
| Other | 409 | 3.3% |

## Country playlists (`playlists/countries/` — 177 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 2833 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1172 | [`countries/International.m3u`](countries/International.m3u) |
| India | 796 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 530 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 439 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Sweden | 376 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| Germany | 374 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| UK | 259 | [`countries/UK.m3u`](countries/UK.m3u) |
| France | 230 | [`countries/France.m3u`](countries/France.m3u) |
| Spain | 227 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| Dominican Republic | 216 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Chile | 206 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Brazil | 193 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Ukraine | 177 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Poland | 170 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Argentina | 166 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Netherlands | 160 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Hungary | 153 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| Peru | 151 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Turkey | 143 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Canada | 142 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Romania | 132 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Mexico | 125 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Colombia | 124 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| Indonesia | 114 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| _…and 152 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 70 / 74 unique links (dead: 0, unverified: 4)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | reachable | - | 0 | no_static_playlist | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. (repository is archived) |
| dlive.sx | reachable | 899 | 0 | player_pages_only | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 403 | 0 | 1291 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 404 | 1062 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| TimeoutError | 0 | 824 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| gaierror | 0 | 414 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 378 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-10-24T12:31:30Z) | 138 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionRefusedError | 0 | 105 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 400 | 68 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 401 | 0 | 38 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 503 | 0 | 35 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 504 | 0 | 23 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| SSLError | 0 | 20 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| RemoteDisconnected | 0 | 19 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLEOFError | 0 | 19 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 502 | 0 | 17 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: playlist only, HTTP 400 (failed the deep check 1x, last 2026-10-24T12:31:30Z) | 16 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 500 | 0 | 14 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| empty response | 14 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| OSError | 0 | 13 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 1x, last 2026-10-24T12:31:30Z) | 11 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 1x, last 2026-10-24T12:31:30Z) | 10 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme rtmp | 0 | 8 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| HTTP 451 | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 530 | 0 | 6 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-24T12:31:30Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-24T12:31:30Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 521 | 0 | 4 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| invalid URL | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-10-24T12:31:30Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-10-24T12:31:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 1x, last 2026-10-24T12:31:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-24T12:31:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 2 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 523 | 0 | 2 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme mmsh | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-10-24T12:31:30Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 302 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 406 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 409 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme rtsp | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: connection refused (failed the deep check 1x, last 2026-10-24T12:31:30Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-10-24T12:31:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-24T12:31:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 3x, last 2026-10-24T12:31:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 410 (failed the deep check 1x, last 2026-10-24T12:31:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |

### Run/source issues

- 2867 links could not be confirmed after retries (see unverified details).
- 1746 links returned a confirmed failure (see dead details).
