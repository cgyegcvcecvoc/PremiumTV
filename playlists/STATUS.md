# Scraper status

- **Last run:** 2026-11-23 10:09 AM EST (2026-11-23 15:09 UTC)
- **Run:** _11:29 PM overnight recheck_ (`recheck`; ID `20261123T150445Z-3105`)
- **Scheduled for:** 2026-11-23T04:29:00Z — started late by +10h 36m
- **Outcome:** **WARNING**
- **Confirmed working:** 12876 / 19043 unique links
- **Dead:** 1930  |  **Unverified:** 4237
- **Retained (unverified, within grace):** 495 previously published links kept so their channels do not vanish after one unverifiable run
- **Unique links found:** 19043 from 23892 source entries
- **Changes vs. PremiumTV_all.m3u:** +246 added / -388 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (179 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (130 confirmed working / 151 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 691 |
| 2 | Lifestyle | 531 |
| 3 | Fox Channels | 37 |
| 4 | CBS | 73 |
| 5 | NBC | 71 |
| 6 | NBC Sports Channels | 6 |
| 7 | Cartoons | 204 |
| 8 | PBS | 23 |
| 9 | Game Shows | 20 |
| 10 | International | 1146 |
| 11 | News | 1120 |
| 12 | Movies | 1015 |
| 13 | Music | 928 |
| 14 | Entertainment | 887 |
| 15 | Europe | 787 |
| 16 | Religious | 693 |
| 17 | Series | 535 |
| 18 | Asia | 531 |
| 19 | South America | 512 |
| 20 | Kids | 424 |
| 21 | United States | 418 |
| 22 | Documentary | 399 |
| 23 | North America | 301 |
| 24 | Comedy | 202 |
| 25 | Education | 149 |
| 26 | Culture | 137 |
| 27 | Legislative | 130 |
| 28 | A&E Networks | 98 |
| 29 | India | 88 |
| 30 | Classic TV | 82 |
| 31 | Business | 76 |
| 32 | Africa | 73 |
| 33 | Canada | 62 |
| 34 | Reality | 55 |
| 35 | En Español | 44 |
| 36 | Family | 37 |
| 37 | Drama | 33 |
| 38 | Home + Food | 30 |
| 39 | Daytime + Game Shows | 29 |
| 40 | UK | 28 |
| 41 | Auto | 26 |
| 42 | Australia | 23 |
| 43 | Weather | 21 |
| 44 | True Crime | 20 |
| 45 | Sci-Fi | 19 |
| 46 | Online TV | 16 |
| 47 | Public TV | 16 |
| 48 | Anime | 15 |
| 49 | DLTV | 15 |
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
| 67 | Other | 363 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 2 | 2 | 2 | 1 | 1 | 0 |
| priority-channels | ok | 16 | 15 | 11 | 13 | 2 | 0 |
| ae-networks | ok | 50 | 50 | 12 | 46 | 0 | 4 |
| aria | ok | 237 | 226 | 226 | 164 | 10 | 52 |
| aria-plus | ok | 2039 | 1983 | 336 | 484 | 214 | 1285 |
| doms9 | ok | 370 | 367 | 60 | 147 | 15 | 205 |
| xtemus | ok | 317 | 317 | 0 | 32 | 233 | 52 |
| iptv-org | ok | 11505 | 11505 | 3750 | 8276 | 1042 | 2187 |
| free-tv | ok | 2203 | 2179 | 942 | 1346 | 338 | 495 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| pluto-us | ok | 458 | 458 | 0 | 457 | 0 | 1 |
| VIP-m3u-playlist 🌱 | ok | 219 | 214 | 145 | 207 | 7 | 0 |
| israel-tv-plus 🌱 | ok | 195 | 192 | 72 | 108 | 5 | 79 |
| m3u 🌱 | ok | 853 | 848 | 172 | 695 | 71 | 81 |
| openstream 🌱 | ok | 5428 | 5428 | 3114 | 5137 | 231 | 60 |

🌱 = source added automatically by the monthly discovery engine: VIP-m3u-playlist, israel-tv-plus, m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **13371** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 691 | 5.2% |
| Lifestyle | 531 | 4.0% |
| Fox Channels | 37 | 0.3% |
| CBS | 73 | 0.5% |
| NBC | 71 | 0.5% |
| NBC Sports Channels | 6 | 0.0% |
| Cartoons | 204 | 1.5% |
| PBS | 23 | 0.2% |
| Game Shows | 20 | 0.1% |
| International | 1146 | 8.6% |
| News | 1120 | 8.4% |
| Movies | 1015 | 7.6% |
| Music | 928 | 6.9% |
| Entertainment | 887 | 6.6% |
| Europe | 787 | 5.9% |
| Religious | 693 | 5.2% |
| Series | 535 | 4.0% |
| Asia | 531 | 4.0% |
| South America | 512 | 3.8% |
| Kids | 424 | 3.2% |
| United States | 418 | 3.1% |
| Documentary | 399 | 3.0% |
| North America | 301 | 2.3% |
| Comedy | 202 | 1.5% |
| Education | 149 | 1.1% |
| Culture | 137 | 1.0% |
| Legislative | 130 | 1.0% |
| A&E Networks | 98 | 0.7% |
| India | 88 | 0.7% |
| Classic TV | 82 | 0.6% |
| Business | 76 | 0.6% |
| Africa | 73 | 0.5% |
| Canada | 62 | 0.5% |
| Reality | 55 | 0.4% |
| En Español | 44 | 0.3% |
| Family | 37 | 0.3% |
| Drama | 33 | 0.2% |
| Home + Food | 30 | 0.2% |
| Daytime + Game Shows | 29 | 0.2% |
| UK | 28 | 0.2% |
| Auto | 26 | 0.2% |
| Australia | 23 | 0.2% |
| Weather | 21 | 0.2% |
| True Crime | 20 | 0.1% |
| Sci-Fi | 19 | 0.1% |
| Online TV | 16 | 0.1% |
| Public TV | 16 | 0.1% |
| Anime | 15 | 0.1% |
| DLTV | 15 | 0.1% |
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
| Other | 363 | 2.7% |

## Country playlists (`playlists/countries/` — 179 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 3265 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1293 | [`countries/International.m3u`](countries/International.m3u) |
| India | 837 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 557 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 471 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Germany | 386 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| UK | 278 | [`countries/UK.m3u`](countries/UK.m3u) |
| France | 277 | [`countries/France.m3u`](countries/France.m3u) |
| Sweden | 277 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| Dominican Republic | 222 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Spain | 221 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| Canada | 202 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Poland | 202 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Chile | 194 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Brazil | 182 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Ukraine | 175 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Netherlands | 173 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Romania | 170 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Hungary | 167 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| Argentina | 166 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Turkey | 165 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Peru | 154 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Mexico | 135 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Indonesia | 122 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| Iran | 121 | [`countries/Iran.m3u`](countries/Iran.m3u) |
| _…and 154 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 130 / 151 unique links (dead: 3, unverified: 18)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | failed | - | 0 | not_imported | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. — GET https://api.github.com/repos/gookie-dev/StepDaddyLiveHD failed: HTTP Error 404: Not Found |
| dlive.sx | failed | - | 0 | not_imported | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. — GET https://dlive.sx/24-7-channels.php failed: <urlopen error [Errno -2] Name or service not known> |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| TimeoutError | 0 | 1522 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 403 | 0 | 1446 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 404 | 1183 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| gaierror | 0 | 480 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 406 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| ConnectionRefusedError | 0 | 275 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 401 | 0 | 228 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 400 | 109 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLError | 0 | 68 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 503 | 0 | 51 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 32 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 429 | 0 | 26 | The host rate-limited the check; this scraper now limits parallel requests per host and retries with Retry-After/backoff. |
| RemoteDisconnected | 0 | 24 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 504 | 0 | 22 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 502 | 0 | 20 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 18 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 500 | 0 | 17 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| empty response | 15 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| not probed: unsupported scheme rtmp | 0 | 13 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 13 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| OSError | 0 | 12 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 10 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 451 | 9 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 511 | 0 | 7 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| invalid URL | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 444 | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 530 | 0 | 6 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 521 | 0 | 3 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 2 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 523 | 0 | 2 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
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
| HTTP 408 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 422 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 458 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
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
- 4237 links could not be confirmed after retries (see unverified details).
- 1930 links returned a confirmed failure (see dead details).
- This run started +10h 36m after its scheduled time (2026-11-23T04:29:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
