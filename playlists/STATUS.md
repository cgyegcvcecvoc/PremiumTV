# Scraper status

- **Last run:** 2026-11-23 05:50 PM EST (2026-11-23 22:50 UTC)
- **Run:** _6:23 AM recheck_ (`recheck`; ID `20261123T224554Z-2992`)
- **Scheduled for:** 2026-11-23T11:23:00Z — started late by +11h 23m
- **Outcome:** **WARNING**
- **Confirmed working:** 12591 / 19069 unique links
- **Dead:** 2255  |  **Unverified:** 4223
- **Retained (unverified, within grace):** 385 previously published links kept so their channels do not vanish after one unverifiable run
- **Unique links found:** 19069 from 23951 source entries
- **Changes vs. PremiumTV_all.m3u:** +126 added / -134 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (176 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (131 confirmed working / 151 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 697 |
| 2 | Lifestyle | 526 |
| 3 | Fox Channels | 36 |
| 4 | CBS | 71 |
| 5 | NBC | 71 |
| 6 | NBC Sports Channels | 6 |
| 7 | Cartoons | 203 |
| 8 | PBS | 23 |
| 9 | Game Shows | 20 |
| 10 | News | 1070 |
| 11 | International | 1057 |
| 12 | Movies | 999 |
| 13 | Music | 916 |
| 14 | Entertainment | 857 |
| 15 | Europe | 759 |
| 16 | Religious | 675 |
| 17 | Series | 531 |
| 18 | Asia | 508 |
| 19 | South America | 499 |
| 20 | Kids | 418 |
| 21 | United States | 413 |
| 22 | Documentary | 394 |
| 23 | North America | 296 |
| 24 | Comedy | 201 |
| 25 | Education | 145 |
| 26 | Culture | 132 |
| 27 | Legislative | 115 |
| 28 | A&E Networks | 98 |
| 29 | India | 85 |
| 30 | Classic TV | 82 |
| 31 | Business | 76 |
| 32 | Africa | 70 |
| 33 | Reality | 55 |
| 34 | Canada | 54 |
| 35 | En Español | 44 |
| 36 | Family | 35 |
| 37 | Drama | 33 |
| 38 | Home + Food | 30 |
| 39 | Daytime + Game Shows | 29 |
| 40 | Auto | 27 |
| 41 | UK | 27 |
| 42 | Weather | 21 |
| 43 | True Crime | 20 |
| 44 | Sci-Fi | 19 |
| 45 | Australia | 16 |
| 46 | Anime | 15 |
| 47 | DLTV | 15 |
| 48 | Westerns | 14 |
| 49 | Animals & Nature | 13 |
| 50 | Aria Web Channels | 13 |
| 51 | Online TV | 13 |
| 52 | Public TV | 13 |
| 53 | Animals + Nature | 11 |
| 54 | Global TV | 11 |
| 55 | Competition Reality | 10 |
| 56 | Tv Celebrities | 10 |
| 57 | Tv Paranormal | 10 |
| 58 | Tv Reality | 7 |
| 59 | United Kingdom | 7 |
| 60 | Relax | 6 |
| 61 | Season's Greetings | 6 |
| 62 | Tv Shows | 5 |
| 63 | Oceania | 3 |
| 64 | Halloween Hits | 1 |
| 65 | Local TV | 1 |
| 66 | Shopping | 1 |
| 67 | Other | 332 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 2 | 2 | 2 | 1 | 1 | 0 |
| priority-channels | ok | 13 | 13 | 11 | 13 | 0 | 0 |
| ae-networks | ok | 50 | 50 | 12 | 47 | 0 | 3 |
| aria | ok | 243 | 232 | 232 | 155 | 25 | 52 |
| aria-plus | ok | 2039 | 1983 | 341 | 450 | 295 | 1238 |
| doms9 | ok | 426 | 426 | 89 | 192 | 36 | 198 |
| xtemus | ok | 317 | 317 | 0 | 31 | 109 | 177 |
| iptv-org | ok | 11505 | 11505 | 3772 | 8175 | 1252 | 2078 |
| free-tv | ok | 2203 | 2179 | 942 | 1267 | 430 | 482 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| pluto-us | ok | 458 | 458 | 0 | 457 | 0 | 1 |
| VIP-m3u-playlist 🌱 | ok | 219 | 214 | 145 | 201 | 13 | 0 |
| israel-tv-plus 🌱 | ok | 195 | 192 | 72 | 103 | 8 | 81 |
| m3u 🌱 | ok | 853 | 848 | 172 | 689 | 77 | 81 |
| openstream 🌱 | ok | 5428 | 5428 | 3114 | 4918 | 440 | 70 |

🌱 = source added automatically by the monthly discovery engine: VIP-m3u-playlist, israel-tv-plus, m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **12976** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 697 | 5.4% |
| Lifestyle | 526 | 4.1% |
| Fox Channels | 36 | 0.3% |
| CBS | 71 | 0.5% |
| NBC | 71 | 0.5% |
| NBC Sports Channels | 6 | 0.0% |
| Cartoons | 203 | 1.6% |
| PBS | 23 | 0.2% |
| Game Shows | 20 | 0.2% |
| News | 1070 | 8.2% |
| International | 1057 | 8.1% |
| Movies | 999 | 7.7% |
| Music | 916 | 7.1% |
| Entertainment | 857 | 6.6% |
| Europe | 759 | 5.8% |
| Religious | 675 | 5.2% |
| Series | 531 | 4.1% |
| Asia | 508 | 3.9% |
| South America | 499 | 3.8% |
| Kids | 418 | 3.2% |
| United States | 413 | 3.2% |
| Documentary | 394 | 3.0% |
| North America | 296 | 2.3% |
| Comedy | 201 | 1.5% |
| Education | 145 | 1.1% |
| Culture | 132 | 1.0% |
| Legislative | 115 | 0.9% |
| A&E Networks | 98 | 0.8% |
| India | 85 | 0.7% |
| Classic TV | 82 | 0.6% |
| Business | 76 | 0.6% |
| Africa | 70 | 0.5% |
| Reality | 55 | 0.4% |
| Canada | 54 | 0.4% |
| En Español | 44 | 0.3% |
| Family | 35 | 0.3% |
| Drama | 33 | 0.3% |
| Home + Food | 30 | 0.2% |
| Daytime + Game Shows | 29 | 0.2% |
| Auto | 27 | 0.2% |
| UK | 27 | 0.2% |
| Weather | 21 | 0.2% |
| True Crime | 20 | 0.2% |
| Sci-Fi | 19 | 0.1% |
| Australia | 16 | 0.1% |
| Anime | 15 | 0.1% |
| DLTV | 15 | 0.1% |
| Westerns | 14 | 0.1% |
| Animals & Nature | 13 | 0.1% |
| Aria Web Channels | 13 | 0.1% |
| Online TV | 13 | 0.1% |
| Public TV | 13 | 0.1% |
| Animals + Nature | 11 | 0.1% |
| Global TV | 11 | 0.1% |
| Competition Reality | 10 | 0.1% |
| Tv Celebrities | 10 | 0.1% |
| Tv Paranormal | 10 | 0.1% |
| Tv Reality | 7 | 0.1% |
| United Kingdom | 7 | 0.1% |
| Relax | 6 | 0.0% |
| Season's Greetings | 6 | 0.0% |
| Tv Shows | 5 | 0.0% |
| Oceania | 3 | 0.0% |
| Halloween Hits | 1 | 0.0% |
| Local TV | 1 | 0.0% |
| Shopping | 1 | 0.0% |
| Other | 332 | 2.6% |

## Country playlists (`playlists/countries/` — 176 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 3235 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1250 | [`countries/International.m3u`](countries/International.m3u) |
| India | 819 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 541 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 459 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Germany | 367 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| Sweden | 277 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| France | 273 | [`countries/France.m3u`](countries/France.m3u) |
| UK | 270 | [`countries/UK.m3u`](countries/UK.m3u) |
| Dominican Republic | 217 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Poland | 200 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Spain | 200 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| Canada | 191 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Chile | 188 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Brazil | 179 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Ukraine | 172 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Romania | 171 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Argentina | 166 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Hungary | 165 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| Netherlands | 162 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Turkey | 158 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Peru | 151 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Mexico | 126 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Colombia | 117 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| Indonesia | 113 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| _…and 151 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 131 / 151 unique links (dead: 5, unverified: 15)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | failed | - | 0 | not_imported | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. — GET https://api.github.com/repos/gookie-dev/StepDaddyLiveHD failed: HTTP Error 404: Not Found |
| dlive.sx | failed | - | 0 | not_imported | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. — GET https://dlive.sx/24-7-channels.php failed: <urlopen error [Errno -2] Name or service not known> |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 403 | 0 | 1370 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| TimeoutError | 0 | 1313 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 404 | 1228 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| gaierror | 0 | 477 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| ConnectionRefusedError | 0 | 264 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 260 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| HTTP 401 | 0 | 226 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 429 | 0 | 162 | The host rate-limited the check; this scraper now limits parallel requests per host and retries with Retry-After/backoff. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 148 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| OSError | 0 | 130 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 111 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 400 | 109 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLError | 0 | 68 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 503 | 0 | 51 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| RemoteDisconnected | 0 | 41 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 39 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 458 | 36 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 32 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 502 | 0 | 31 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 25 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 504 | 0 | 22 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 500 | 0 | 20 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: playlist only, HTTP 400 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 19 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 17 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| empty response | 15 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| quarantined: variant HTTP 403 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 14 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme rtmp | 0 | 13 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 13 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 11 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 11 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 451 | 9 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionResetError | 0 | 7 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 511 | 0 | 7 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| invalid URL | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 444 | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 530 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-23T18:06:21Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, dns lookup failed (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 521 | 0 | 3 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 2 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| SSLEOFError | 0 | 2 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| not probed: unsupported scheme rtsp | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-23T18:06:21Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: html page, not a stream (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 401 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-11-23T18:06:21Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 302 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 406 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 408 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 523 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 400 (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 400 (failed the deep check 2x, last 2026-11-23T18:06:21Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: connection refused (failed the deep check 2x, last 2026-11-23T18:06:21Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: dash manifest has no representations (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, segment too small (214 bytes) (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-11-23T18:06:21Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 410 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |

### Run/source issues

- Reference check 'StepDaddyLiveHD' failed: GET https://api.github.com/repos/gookie-dev/StepDaddyLiveHD failed: HTTP Error 404: Not Found
- Reference check 'dlive.sx' failed: GET https://dlive.sx/24-7-channels.php failed: <urlopen error [Errno -2] Name or service not known>
- 4223 links could not be confirmed after retries (see unverified details).
- 2255 links returned a confirmed failure (see dead details).
- This run started +11h 23m after its scheduled time (2026-11-23T11:23:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
