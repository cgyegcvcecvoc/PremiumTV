# Scraper status

- **Last run:** 2026-11-22 03:54 PM EST (2026-11-22 20:54 UTC)
- **Run:** _9:41 AM recheck_ (`recheck`; ID `20261122T204949Z-2992`)
- **Scheduled for:** 2026-11-22T14:41:00Z — started late by +6h 09m
- **Outcome:** **WARNING**
- **Confirmed working:** 12471 / 19598 unique links
- **Dead:** 1914  |  **Unverified:** 5213
- **Retained (unverified, within grace):** 493 previously published links kept so their channels do not vanish after one unverifiable run
- **Unique links found:** 19598 from 24453 source entries
- **Changes vs. PremiumTV_all.m3u:** +132 added / -150 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (178 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (112 confirmed working / 144 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 759 |
| 2 | Lifestyle | 532 |
| 3 | Fox Channels | 34 |
| 4 | CBS | 55 |
| 5 | NBC | 68 |
| 6 | NBC Sports Channels | 6 |
| 7 | Cartoons | 203 |
| 8 | PBS | 23 |
| 9 | Game Shows | 20 |
| 10 | International | 1130 |
| 11 | News | 1107 |
| 12 | Movies | 1002 |
| 13 | Music | 901 |
| 14 | Entertainment | 861 |
| 15 | Europe | 794 |
| 16 | Religious | 689 |
| 17 | Series | 535 |
| 18 | Asia | 529 |
| 19 | South America | 502 |
| 20 | United States | 419 |
| 21 | Documentary | 401 |
| 22 | Kids | 401 |
| 23 | North America | 291 |
| 24 | Comedy | 176 |
| 25 | Education | 148 |
| 26 | Culture | 136 |
| 27 | Legislative | 130 |
| 28 | A&E Networks | 96 |
| 29 | India | 90 |
| 30 | Business | 75 |
| 31 | Africa | 70 |
| 32 | Canada | 61 |
| 33 | Classic TV | 58 |
| 34 | Family | 35 |
| 35 | UK | 30 |
| 36 | Auto | 26 |
| 37 | Australia | 23 |
| 38 | Weather | 21 |
| 39 | Online TV | 16 |
| 40 | Public TV | 16 |
| 41 | DLTV | 15 |
| 42 | Reality | 14 |
| 43 | Animals & Nature | 13 |
| 44 | Aria Web Channels | 13 |
| 45 | Global TV | 12 |
| 46 | Tv Celebrities | 10 |
| 47 | Tv Paranormal | 10 |
| 48 | United Kingdom | 9 |
| 49 | Tv Reality | 7 |
| 50 | Daytime + Game Shows | 6 |
| 51 | En Español | 6 |
| 52 | Relax | 6 |
| 53 | Tv Shows | 6 |
| 54 | Home + Food | 4 |
| 55 | Westerns | 4 |
| 56 | Animals + Nature | 3 |
| 57 | Drama | 3 |
| 58 | Oceania | 3 |
| 59 | Sci-Fi | 3 |
| 60 | Anime | 2 |
| 61 | Shopping | 1 |
| 62 | True Crime | 1 |
| 63 | Other | 344 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 2 | 2 | 2 | 1 | 1 | 0 |
| priority-channels | ok | 16 | 15 | 12 | 14 | 0 | 1 |
| ae-networks | ok | 50 | 50 | 12 | 46 | 0 | 4 |
| aria | ok | 237 | 226 | 226 | 163 | 10 | 53 |
| aria-plus | ok | 2039 | 1983 | 334 | 476 | 234 | 1273 |
| doms9 | ok | 923 | 923 | 61 | 206 | 138 | 579 |
| xtemus | ok | 317 | 317 | 0 | 32 | 108 | 177 |
| iptv-org | ok | 11512 | 11512 | 3757 | 8293 | 1048 | 2171 |
| free-tv | ok | 2203 | 2179 | 944 | 1361 | 327 | 491 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| pluto-us | ok | 458 | 458 | 0 | 0 | 0 | 458 |
| VIP-m3u-playlist 🌱 | ok | 220 | 215 | 146 | 208 | 7 | 0 |
| israel-tv-plus 🌱 | ok | 195 | 192 | 73 | 104 | 5 | 83 |
| m3u 🌱 | ok | 853 | 848 | 172 | 697 | 68 | 82 |
| openstream 🌱 | ok | 5428 | 5428 | 3117 | 5108 | 212 | 108 |

🌱 = source added automatically by the monthly discovery engine: VIP-m3u-playlist, israel-tv-plus, m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **12964** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 759 | 5.9% |
| Lifestyle | 532 | 4.1% |
| Fox Channels | 34 | 0.3% |
| CBS | 55 | 0.4% |
| NBC | 68 | 0.5% |
| NBC Sports Channels | 6 | 0.0% |
| Cartoons | 203 | 1.6% |
| PBS | 23 | 0.2% |
| Game Shows | 20 | 0.2% |
| International | 1130 | 8.7% |
| News | 1107 | 8.5% |
| Movies | 1002 | 7.7% |
| Music | 901 | 7.0% |
| Entertainment | 861 | 6.6% |
| Europe | 794 | 6.1% |
| Religious | 689 | 5.3% |
| Series | 535 | 4.1% |
| Asia | 529 | 4.1% |
| South America | 502 | 3.9% |
| United States | 419 | 3.2% |
| Documentary | 401 | 3.1% |
| Kids | 401 | 3.1% |
| North America | 291 | 2.2% |
| Comedy | 176 | 1.4% |
| Education | 148 | 1.1% |
| Culture | 136 | 1.0% |
| Legislative | 130 | 1.0% |
| A&E Networks | 96 | 0.7% |
| India | 90 | 0.7% |
| Business | 75 | 0.6% |
| Africa | 70 | 0.5% |
| Canada | 61 | 0.5% |
| Classic TV | 58 | 0.4% |
| Family | 35 | 0.3% |
| UK | 30 | 0.2% |
| Auto | 26 | 0.2% |
| Australia | 23 | 0.2% |
| Weather | 21 | 0.2% |
| Online TV | 16 | 0.1% |
| Public TV | 16 | 0.1% |
| DLTV | 15 | 0.1% |
| Reality | 14 | 0.1% |
| Animals & Nature | 13 | 0.1% |
| Aria Web Channels | 13 | 0.1% |
| Global TV | 12 | 0.1% |
| Tv Celebrities | 10 | 0.1% |
| Tv Paranormal | 10 | 0.1% |
| United Kingdom | 9 | 0.1% |
| Tv Reality | 7 | 0.1% |
| Daytime + Game Shows | 6 | 0.0% |
| En Español | 6 | 0.0% |
| Relax | 6 | 0.0% |
| Tv Shows | 6 | 0.0% |
| Home + Food | 4 | 0.0% |
| Westerns | 4 | 0.0% |
| Animals + Nature | 3 | 0.0% |
| Drama | 3 | 0.0% |
| Oceania | 3 | 0.0% |
| Sci-Fi | 3 | 0.0% |
| Anime | 2 | 0.0% |
| Shopping | 1 | 0.0% |
| True Crime | 1 | 0.0% |
| Other | 344 | 2.7% |

## Country playlists (`playlists/countries/` — 178 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 3129 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1061 | [`countries/International.m3u`](countries/International.m3u) |
| India | 878 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 555 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 464 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Germany | 386 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| UK | 281 | [`countries/UK.m3u`](countries/UK.m3u) |
| Sweden | 277 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| France | 274 | [`countries/France.m3u`](countries/France.m3u) |
| Spain | 231 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| Dominican Republic | 215 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Poland | 200 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Canada | 196 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Chile | 187 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Brazil | 177 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Romania | 174 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Argentina | 170 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Ukraine | 170 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Hungary | 167 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| Netherlands | 166 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Turkey | 166 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Peru | 151 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Mexico | 133 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Iran | 119 | [`countries/Iran.m3u`](countries/Iran.m3u) |
| Colombia | 113 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| _…and 153 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 112 / 144 unique links (dead: 4, unverified: 28)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | failed | - | 0 | not_imported | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. — GET https://api.github.com/repos/gookie-dev/StepDaddyLiveHD failed: HTTP Error 404: Not Found |
| dlive.sx | failed | - | 0 | not_imported | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. — GET https://dlive.sx/24-7-channels.php failed: <urlopen error [Errno -2] Name or service not known> |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 403 | 0 | 1670 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| TimeoutError | 0 | 1411 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 404 | 1315 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 401 | 0 | 687 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| gaierror | 0 | 480 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| ConnectionRefusedError | 0 | 278 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 263 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| OSError | 0 | 236 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 429 | 0 | 154 | The host rate-limited the check; this scraper now limits parallel requests per host and retries with Retry-After/backoff. |
| HTTP 400 | 109 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLError | 0 | 69 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| RemoteDisconnected | 0 | 50 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 503 | 0 | 48 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 502 | 0 | 43 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 29 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 504 | 0 | 22 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 500 | 0 | 20 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 19 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| empty response | 15 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| not probed: unsupported scheme rtmp | 0 | 13 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 13 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 13 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 11 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 451 | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 511 | 0 | 8 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| invalid URL | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 444 | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 530 | 0 | 6 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 521 | 0 | 3 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 2 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| not probed: unsupported scheme rtsp | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: connection refused (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 302 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 406 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 407 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 523 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 400 (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dash manifest has no representations (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, segment too small (214 bytes) (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |

### Run/source issues

- Reference check 'StepDaddyLiveHD' failed: GET https://api.github.com/repos/gookie-dev/StepDaddyLiveHD failed: HTTP Error 404: Not Found
- Reference check 'dlive.sx' failed: GET https://dlive.sx/24-7-channels.php failed: <urlopen error [Errno -2] Name or service not known>
- 5213 links could not be confirmed after retries (see unverified details).
- 1914 links returned a confirmed failure (see dead details).
- This run started +6h 09m after its scheduled time (2026-11-22T14:41:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
