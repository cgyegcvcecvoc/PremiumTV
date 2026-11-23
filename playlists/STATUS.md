# Scraper status

- **Last run:** 2026-11-23 04:13 AM EST (2026-11-23 09:13 UTC)
- **Run:** _8:17 PM recheck_ (`recheck`; ID `20261123T090919Z-3036`)
- **Scheduled for:** 2026-11-23T01:17:00Z — started late by +7h 52m
- **Outcome:** **WARNING**
- **Confirmed working:** 12932 / 19185 unique links
- **Dead:** 1959  |  **Unverified:** 4294
- **Retained (unverified, within grace):** 436 previously published links kept so their channels do not vanish after one unverifiable run
- **Unique links found:** 19185 from 24034 source entries
- **Changes vs. PremiumTV_all.m3u:** +551 added / -564 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (177 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (129 confirmed working / 151 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 692 |
| 2 | Lifestyle | 529 |
| 3 | Fox Channels | 37 |
| 4 | CBS | 73 |
| 5 | NBC | 71 |
| 6 | NBC Sports Channels | 6 |
| 7 | Cartoons | 204 |
| 8 | PBS | 23 |
| 9 | Game Shows | 20 |
| 10 | International | 1143 |
| 11 | News | 1129 |
| 12 | Movies | 1025 |
| 13 | Music | 921 |
| 14 | Entertainment | 880 |
| 15 | Europe | 793 |
| 16 | Religious | 695 |
| 17 | Asia | 549 |
| 18 | Series | 535 |
| 19 | South America | 485 |
| 20 | Kids | 425 |
| 21 | United States | 418 |
| 22 | Documentary | 404 |
| 23 | North America | 292 |
| 24 | Comedy | 202 |
| 25 | Education | 148 |
| 26 | Culture | 135 |
| 27 | Legislative | 130 |
| 28 | A&E Networks | 98 |
| 29 | India | 89 |
| 30 | Classic TV | 82 |
| 31 | Business | 75 |
| 32 | Africa | 70 |
| 33 | Canada | 61 |
| 34 | Reality | 55 |
| 35 | En Español | 44 |
| 36 | Family | 36 |
| 37 | Drama | 33 |
| 38 | Home + Food | 30 |
| 39 | Daytime + Game Shows | 29 |
| 40 | UK | 29 |
| 41 | Auto | 26 |
| 42 | Australia | 23 |
| 43 | Weather | 21 |
| 44 | True Crime | 20 |
| 45 | Sci-Fi | 19 |
| 46 | Public TV | 16 |
| 47 | Anime | 15 |
| 48 | DLTV | 15 |
| 49 | Online TV | 14 |
| 50 | Westerns | 14 |
| 51 | Animals & Nature | 13 |
| 52 | Aria Web Channels | 13 |
| 53 | Global TV | 12 |
| 54 | Animals + Nature | 11 |
| 55 | Competition Reality | 10 |
| 56 | Tv Celebrities | 10 |
| 57 | Tv Paranormal | 10 |
| 58 | United Kingdom | 8 |
| 59 | Tv Reality | 7 |
| 60 | Relax | 6 |
| 61 | Season's Greetings | 6 |
| 62 | Tv Shows | 6 |
| 63 | Oceania | 3 |
| 64 | Halloween Hits | 1 |
| 65 | Local TV | 1 |
| 66 | Shopping | 1 |
| 67 | Other | 372 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 2 | 2 | 2 | 1 | 1 | 0 |
| priority-channels | ok | 16 | 15 | 12 | 13 | 2 | 0 |
| ae-networks | ok | 50 | 50 | 12 | 46 | 0 | 4 |
| aria | ok | 237 | 226 | 226 | 164 | 10 | 52 |
| aria-plus | ok | 2039 | 1983 | 336 | 481 | 235 | 1267 |
| doms9 | ok | 512 | 510 | 61 | 144 | 33 | 333 |
| xtemus | ok | 317 | 317 | 0 | 31 | 231 | 55 |
| iptv-org | ok | 11505 | 11505 | 3749 | 8303 | 1060 | 2142 |
| free-tv | ok | 2203 | 2179 | 942 | 1364 | 341 | 474 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| pluto-us | ok | 458 | 458 | 0 | 458 | 0 | 0 |
| VIP-m3u-playlist 🌱 | ok | 219 | 214 | 145 | 209 | 5 | 0 |
| israel-tv-plus 🌱 | ok | 195 | 192 | 72 | 108 | 5 | 79 |
| m3u 🌱 | ok | 853 | 848 | 172 | 697 | 68 | 82 |
| openstream 🌱 | ok | 5428 | 5428 | 3114 | 5138 | 220 | 70 |

🌱 = source added automatically by the monthly discovery engine: VIP-m3u-playlist, israel-tv-plus, m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **13368** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 692 | 5.2% |
| Lifestyle | 529 | 4.0% |
| Fox Channels | 37 | 0.3% |
| CBS | 73 | 0.5% |
| NBC | 71 | 0.5% |
| NBC Sports Channels | 6 | 0.0% |
| Cartoons | 204 | 1.5% |
| PBS | 23 | 0.2% |
| Game Shows | 20 | 0.1% |
| International | 1143 | 8.6% |
| News | 1129 | 8.4% |
| Movies | 1025 | 7.7% |
| Music | 921 | 6.9% |
| Entertainment | 880 | 6.6% |
| Europe | 793 | 5.9% |
| Religious | 695 | 5.2% |
| Asia | 549 | 4.1% |
| Series | 535 | 4.0% |
| South America | 485 | 3.6% |
| Kids | 425 | 3.2% |
| United States | 418 | 3.1% |
| Documentary | 404 | 3.0% |
| North America | 292 | 2.2% |
| Comedy | 202 | 1.5% |
| Education | 148 | 1.1% |
| Culture | 135 | 1.0% |
| Legislative | 130 | 1.0% |
| A&E Networks | 98 | 0.7% |
| India | 89 | 0.7% |
| Classic TV | 82 | 0.6% |
| Business | 75 | 0.6% |
| Africa | 70 | 0.5% |
| Canada | 61 | 0.5% |
| Reality | 55 | 0.4% |
| En Español | 44 | 0.3% |
| Family | 36 | 0.3% |
| Drama | 33 | 0.2% |
| Home + Food | 30 | 0.2% |
| Daytime + Game Shows | 29 | 0.2% |
| UK | 29 | 0.2% |
| Auto | 26 | 0.2% |
| Australia | 23 | 0.2% |
| Weather | 21 | 0.2% |
| True Crime | 20 | 0.1% |
| Sci-Fi | 19 | 0.1% |
| Public TV | 16 | 0.1% |
| Anime | 15 | 0.1% |
| DLTV | 15 | 0.1% |
| Online TV | 14 | 0.1% |
| Westerns | 14 | 0.1% |
| Animals & Nature | 13 | 0.1% |
| Aria Web Channels | 13 | 0.1% |
| Global TV | 12 | 0.1% |
| Animals + Nature | 11 | 0.1% |
| Competition Reality | 10 | 0.1% |
| Tv Celebrities | 10 | 0.1% |
| Tv Paranormal | 10 | 0.1% |
| United Kingdom | 8 | 0.1% |
| Tv Reality | 7 | 0.1% |
| Relax | 6 | 0.0% |
| Season's Greetings | 6 | 0.0% |
| Tv Shows | 6 | 0.0% |
| Oceania | 3 | 0.0% |
| Halloween Hits | 1 | 0.0% |
| Local TV | 1 | 0.0% |
| Shopping | 1 | 0.0% |
| Other | 372 | 2.8% |

## Country playlists (`playlists/countries/` — 177 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 3272 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1316 | [`countries/International.m3u`](countries/International.m3u) |
| India | 843 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 558 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 473 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Germany | 386 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| UK | 278 | [`countries/UK.m3u`](countries/UK.m3u) |
| France | 277 | [`countries/France.m3u`](countries/France.m3u) |
| Sweden | 277 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| Spain | 228 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| Dominican Republic | 218 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Canada | 202 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Poland | 201 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Chile | 187 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Brazil | 178 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Romania | 174 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Ukraine | 174 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Netherlands | 173 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Argentina | 169 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Hungary | 167 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| Turkey | 167 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Mexico | 134 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Peru | 134 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Indonesia | 125 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| Iran | 121 | [`countries/Iran.m3u`](countries/Iran.m3u) |
| _…and 152 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 129 / 151 unique links (dead: 4, unverified: 18)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | failed | - | 0 | not_imported | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. — GET https://api.github.com/repos/gookie-dev/StepDaddyLiveHD failed: HTTP Error 403: rate limit exceeded |
| dlive.sx | failed | - | 0 | not_imported | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. — GET https://dlive.sx/24-7-channels.php failed: <urlopen error [Errno -2] Name or service not known> |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 403 | 0 | 1480 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| TimeoutError | 0 | 1343 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 404 | 1211 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| gaierror | 0 | 479 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 397 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| ConnectionRefusedError | 0 | 277 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 401 | 0 | 233 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| OSError | 0 | 184 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 400 | 108 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLError | 0 | 68 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 503 | 0 | 53 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| RemoteDisconnected | 0 | 46 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 34 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 502 | 0 | 32 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 504 | 0 | 22 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 500 | 0 | 20 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 19 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| empty response | 14 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| not probed: unsupported scheme rtmp | 0 | 13 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 13 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 530 | 0 | 12 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 11 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 10 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 451 | 9 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 511 | 0 | 8 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| invalid URL | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 429 | 0 | 6 | The host rate-limited the check; this scraper now limits parallel requests per host and retries with Retry-After/backoff. |
| HTTP 444 | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 407 | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 521 | 0 | 3 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
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
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 458 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
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

- Reference check 'StepDaddyLiveHD' failed: GET https://api.github.com/repos/gookie-dev/StepDaddyLiveHD failed: HTTP Error 403: rate limit exceeded
- Reference check 'dlive.sx' failed: GET https://dlive.sx/24-7-channels.php failed: <urlopen error [Errno -2] Name or service not known>
- 4294 links could not be confirmed after retries (see unverified details).
- 1959 links returned a confirmed failure (see dead details).
- This run started +7h 52m after its scheduled time (2026-11-23T01:17:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
