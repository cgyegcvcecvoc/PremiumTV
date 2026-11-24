# Scraper status

- **Last run:** 2026-11-24 06:04 AM EST (2026-11-24 11:04 UTC)
- **Run:** _8:17 PM recheck_ (`recheck`; ID `20261124T105912Z-2993`)
- **Scheduled for:** 2026-11-24T01:17:00Z — started late by +9h 42m
- **Outcome:** **WARNING**
- **Confirmed working:** 12441 / 19423 unique links
- **Dead:** 2296  |  **Unverified:** 4686
- **Retained (unverified, within grace):** 843 previously published links kept so their channels do not vanish after one unverifiable run
- **Unique links found:** 19423 from 24332 source entries
- **Changes vs. PremiumTV_all.m3u:** +63 added / -57 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (175 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (115 confirmed working / 151 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 698 |
| 2 | Lifestyle | 528 |
| 3 | Fox Channels | 36 |
| 4 | CBS | 71 |
| 5 | NBC | 68 |
| 6 | NBC Sports Channels | 6 |
| 7 | Cartoons | 203 |
| 8 | PBS | 24 |
| 9 | Game Shows | 20 |
| 10 | News | 1087 |
| 11 | International | 1071 |
| 12 | Movies | 997 |
| 13 | Music | 924 |
| 14 | Entertainment | 853 |
| 15 | Europe | 764 |
| 16 | Religious | 669 |
| 17 | Series | 531 |
| 18 | Asia | 523 |
| 19 | South America | 474 |
| 20 | Kids | 422 |
| 21 | United States | 411 |
| 22 | Documentary | 392 |
| 23 | North America | 286 |
| 24 | Comedy | 201 |
| 25 | Education | 145 |
| 26 | Culture | 130 |
| 27 | Legislative | 116 |
| 28 | A&E Networks | 99 |
| 29 | Classic TV | 82 |
| 30 | India | 80 |
| 31 | Business | 78 |
| 32 | Africa | 67 |
| 33 | Canada | 58 |
| 34 | Reality | 55 |
| 35 | En Español | 44 |
| 36 | Family | 35 |
| 37 | Drama | 33 |
| 38 | Home + Food | 30 |
| 39 | Daytime + Game Shows | 29 |
| 40 | UK | 28 |
| 41 | Auto | 27 |
| 42 | Weather | 21 |
| 43 | True Crime | 20 |
| 44 | Sci-Fi | 19 |
| 45 | Australia | 16 |
| 46 | Online TV | 16 |
| 47 | Anime | 15 |
| 48 | DLTV | 15 |
| 49 | Aria Web Channels | 14 |
| 50 | Westerns | 14 |
| 51 | Animals & Nature | 13 |
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
| 67 | Other | 624 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 2 | 2 | 2 | 1 | 1 | 0 |
| priority-channels | ok | 13 | 13 | 11 | 13 | 0 | 0 |
| ae-networks | ok | 50 | 50 | 12 | 47 | 0 | 3 |
| aria | ok | 234 | 223 | 223 | 154 | 17 | 52 |
| aria-plus | ok | 2039 | 1983 | 334 | 469 | 258 | 1256 |
| doms9 | ok | 456 | 456 | 88 | 174 | 70 | 212 |
| xtemus | ok | 317 | 317 | 0 | 31 | 114 | 172 |
| iptv-org | ok | 11473 | 11473 | 3776 | 8166 | 1274 | 2033 |
| free-tv | ok | 2203 | 2179 | 939 | 1246 | 447 | 486 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| pluto-us | ok | 458 | 458 | 0 | 0 | 0 | 458 |
| aria-overseas | ok | 42 | 42 | 20 | 40 | 1 | 1 |
| vbskycn-iptv | ok | 345 | 343 | 13 | 319 | 0 | 24 |
| VIP-m3u-playlist 🌱 | ok | 224 | 219 | 150 | 206 | 13 | 0 |
| israel-tv-plus 🌱 | ok | 195 | 192 | 72 | 106 | 5 | 81 |
| m3u 🌱 | ok | 853 | 848 | 173 | 689 | 77 | 81 |
| openstream 🌱 | ok | 5428 | 5428 | 3123 | 4908 | 456 | 64 |

🌱 = source added automatically by the monthly discovery engine: VIP-m3u-playlist, israel-tv-plus, m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **13284** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 698 | 5.3% |
| Lifestyle | 528 | 4.0% |
| Fox Channels | 36 | 0.3% |
| CBS | 71 | 0.5% |
| NBC | 68 | 0.5% |
| NBC Sports Channels | 6 | 0.0% |
| Cartoons | 203 | 1.5% |
| PBS | 24 | 0.2% |
| Game Shows | 20 | 0.2% |
| News | 1087 | 8.2% |
| International | 1071 | 8.1% |
| Movies | 997 | 7.5% |
| Music | 924 | 7.0% |
| Entertainment | 853 | 6.4% |
| Europe | 764 | 5.8% |
| Religious | 669 | 5.0% |
| Series | 531 | 4.0% |
| Asia | 523 | 3.9% |
| South America | 474 | 3.6% |
| Kids | 422 | 3.2% |
| United States | 411 | 3.1% |
| Documentary | 392 | 3.0% |
| North America | 286 | 2.2% |
| Comedy | 201 | 1.5% |
| Education | 145 | 1.1% |
| Culture | 130 | 1.0% |
| Legislative | 116 | 0.9% |
| A&E Networks | 99 | 0.7% |
| Classic TV | 82 | 0.6% |
| India | 80 | 0.6% |
| Business | 78 | 0.6% |
| Africa | 67 | 0.5% |
| Canada | 58 | 0.4% |
| Reality | 55 | 0.4% |
| En Español | 44 | 0.3% |
| Family | 35 | 0.3% |
| Drama | 33 | 0.2% |
| Home + Food | 30 | 0.2% |
| Daytime + Game Shows | 29 | 0.2% |
| UK | 28 | 0.2% |
| Auto | 27 | 0.2% |
| Weather | 21 | 0.2% |
| True Crime | 20 | 0.2% |
| Sci-Fi | 19 | 0.1% |
| Australia | 16 | 0.1% |
| Online TV | 16 | 0.1% |
| Anime | 15 | 0.1% |
| DLTV | 15 | 0.1% |
| Aria Web Channels | 14 | 0.1% |
| Westerns | 14 | 0.1% |
| Animals & Nature | 13 | 0.1% |
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
| Other | 624 | 4.7% |

## Country playlists (`playlists/countries/` — 175 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 3225 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1550 | [`countries/International.m3u`](countries/International.m3u) |
| India | 823 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 540 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 468 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Germany | 369 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| Sweden | 277 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| France | 274 | [`countries/France.m3u`](countries/France.m3u) |
| UK | 271 | [`countries/UK.m3u`](countries/UK.m3u) |
| Dominican Republic | 214 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Spain | 207 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| Canada | 200 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Poland | 197 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Chile | 185 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Brazil | 178 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Ukraine | 172 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Romania | 170 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Argentina | 166 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Netherlands | 161 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Turkey | 161 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Hungary | 157 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| Peru | 145 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Mexico | 122 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Indonesia | 119 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| Colombia | 117 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| _…and 150 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 115 / 151 unique links (dead: 5, unverified: 31)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | failed | - | 0 | not_imported | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. — GET https://api.github.com/repos/gookie-dev/StepDaddyLiveHD failed: HTTP Error 403: rate limit exceeded |
| dlive.sx | failed | - | 0 | not_imported | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. — GET https://dlive.sx/24-7-channels.php failed: <urlopen error [Errno -2] Name or service not known> |
| xyzstreams | reachable | - | 0 | not_imported | Live-event index (soccer, NFL, NBA and more) whose schedules the site renders in the viewer's own time zone and whose streams are resolved by JavaScript inside its player pages, so it publishes no static playlist. Checked for reachability only and never imported as channels; its backup index is https://xyzstreams.space/alt.html. Configure XYZSTREAMS_M3U_URL only if you have an authorized direct playlist. |
| ppv.st | reachable | - | 0 | not_imported | Live-event directory (NFL, college football, basketball, soccer, PPV cards) that lists its fixtures and countdowns but serves no static M3U; the page itself now points readers to https://mirrors.st/ for its current address. Checked for reachability only, never imported. Configure PPVST_M3U_URL only if you have an authorized direct playlist. |
| Easy-Web-TV-M3u8 | failed | - | 0 | not_imported | zhangboheng's all-in-one web TV catalogue. Its country pages are generated in the browser from the iptv-org public API (which this repository already reads through the iptv-org source), and the repository tree publishes no .m3u file at all, so there is nothing to import. This check counts the playlists it carries so a future static export is noticed. — GET https://api.github.com/repos/zhangboheng/Easy-Web-TV-M3u8 failed: HTTP Error 403: rate limit exceeded |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 403 | 0 | 1363 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| TimeoutError | 0 | 1302 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 404 | 1278 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 401 | 0 | 686 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| gaierror | 0 | 494 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| ConnectionRefusedError | 0 | 264 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 257 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| HTTP 429 | 0 | 157 | The host rate-limited the check; this scraper now limits parallel requests per host and retries with Retry-After/backoff. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 145 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| OSError | 0 | 132 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 400 | 110 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 109 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLError | 0 | 67 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 503 | 0 | 53 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| RemoteDisconnected | 0 | 44 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 38 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 502 | 0 | 35 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 33 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 31 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 24 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 504 | 0 | 22 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: playlist only, HTTP 400 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 19 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 18 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 500 | 0 | 16 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| empty response | 14 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| quarantined: variant HTTP 403 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 14 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme rtmp | 0 | 13 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 13 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 530 | 0 | 12 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 11 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 11 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 10 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 451 | 9 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 407 | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 511 | 0 | 7 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| invalid URL | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 444 | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-17T16:02:34Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-23T18:06:21Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, dns lookup failed (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 521 | 0 | 3 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-23T18:06:21Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme rtsp | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: connection refused (failed the deep check 2x, last 2026-11-17T16:02:34Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
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
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-11-23T18:06:21Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
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

- Reference check 'StepDaddyLiveHD' failed: GET https://api.github.com/repos/gookie-dev/StepDaddyLiveHD failed: HTTP Error 403: rate limit exceeded
- Reference check 'dlive.sx' failed: GET https://dlive.sx/24-7-channels.php failed: <urlopen error [Errno -2] Name or service not known>
- Reference check 'Easy-Web-TV-M3u8' failed: GET https://api.github.com/repos/zhangboheng/Easy-Web-TV-M3u8 failed: HTTP Error 403: rate limit exceeded
- 4686 links could not be confirmed after retries (see unverified details).
- 2296 links returned a confirmed failure (see dead details).
- This run started +9h 42m after its scheduled time (2026-11-24T01:17:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
