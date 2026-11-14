# Scraper status

- **Last run:** 2026-11-13 08:47 PM EST (2026-11-14 01:47 UTC)
- **Run:** _4:41 PM final check_ (`final_check`; ID `20261114T014404Z-2939`)
- **Scheduled for:** 2026-11-13T21:41:00Z — started late by +4h 03m
- **Outcome:** **WARNING**
- **Confirmed working:** 11882 / 17016 unique links
- **Dead:** 2419  |  **Unverified:** 2715
- **Retained (unverified, within grace):** 239 previously published links kept so their channels do not vanish after one unverifiable run
- **Unique links found:** 17016 from 21522 source entries
- **Changes vs. PremiumTV_all.m3u:** +293 added / -271 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (173 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (70 confirmed working / 77 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 733 |
| 2 | Lifestyle | 525 |
| 3 | Fox Channels | 21 |
| 4 | CBS | 38 |
| 5 | NBC | 59 |
| 6 | NBC Sports Channels | 8 |
| 7 | Cartoons | 200 |
| 8 | PBS | 20 |
| 9 | Game Shows | 18 |
| 10 | News | 1036 |
| 11 | Movies | 965 |
| 12 | Music | 869 |
| 13 | International | 834 |
| 14 | Entertainment | 830 |
| 15 | Europe | 763 |
| 16 | Religious | 638 |
| 17 | Series | 525 |
| 18 | South America | 486 |
| 19 | Asia | 483 |
| 20 | Documentary | 401 |
| 21 | United States | 401 |
| 22 | Kids | 380 |
| 23 | North America | 288 |
| 24 | Comedy | 178 |
| 25 | Education | 144 |
| 26 | Culture | 122 |
| 27 | Legislative | 117 |
| 28 | India | 88 |
| 29 | Classic TV | 70 |
| 30 | Africa | 69 |
| 31 | Business | 68 |
| 32 | A&E Networks | 47 |
| 33 | UK | 35 |
| 34 | Family | 33 |
| 35 | Canada | 26 |
| 36 | Auto | 21 |
| 37 | Weather | 17 |
| 38 | Online TV | 16 |
| 39 | DLTV | 15 |
| 40 | Animals & Nature | 13 |
| 41 | Australia | 13 |
| 42 | Public TV | 13 |
| 43 | Tv Reality | 13 |
| 44 | Global TV | 12 |
| 45 | Tv Paranormal | 11 |
| 46 | Tv Celebrities | 9 |
| 47 | Eurovision Song Contest Asia on Aria (November 14th) | 8 |
| 48 | Aria Web Channels | 6 |
| 49 | Tv Shows | 6 |
| 50 | Oceania | 5 |
| 51 | Relax | 3 |
| 52 | IPTV | 1 |
| 53 | MeTV | 1 |
| 54 | Shopping | 1 |
| 55 | TEST | 1 |
| 56 | United Kingdom | 1 |
| 57 | USA Channels | 1 |
| 58 | Other | 416 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 4 | 4 | 3 | 2 | 2 | 0 |
| priority-channels | ok | 13 | 13 | 10 | 13 | 0 | 0 |
| ae-networks | ok | 53 | 53 | 13 | 47 | 0 | 6 |
| aria | ok | 244 | 233 | 87 | 166 | 18 | 49 |
| doms9 | ok | 437 | 435 | 90 | 267 | 39 | 129 |
| xtemus | ok | 317 | 317 | 0 | 31 | 224 | 62 |
| iptv-org | ok | 11472 | 11472 | 3750 | 8073 | 1454 | 1945 |
| free-tv | ok | 2203 | 2179 | 934 | 1270 | 444 | 465 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| VIP-m3u-playlist 🌱 | ok | 201 | 201 | 95 | 180 | 20 | 1 |
| israel-tv-plus 🌱 | ok | 307 | 278 | 73 | 114 | 85 | 79 |
| m3u 🌱 | ok | 843 | 839 | 174 | 666 | 86 | 86 |
| openstream 🌱 | ok | 5428 | 5428 | 3130 | 4877 | 506 | 45 |

🌱 = source added automatically by the monthly discovery engine: VIP-m3u-playlist, israel-tv-plus, m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **12121** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 733 | 6.0% |
| Lifestyle | 525 | 4.3% |
| Fox Channels | 21 | 0.2% |
| CBS | 38 | 0.3% |
| NBC | 59 | 0.5% |
| NBC Sports Channels | 8 | 0.1% |
| Cartoons | 200 | 1.7% |
| PBS | 20 | 0.2% |
| Game Shows | 18 | 0.1% |
| News | 1036 | 8.5% |
| Movies | 965 | 8.0% |
| Music | 869 | 7.2% |
| International | 834 | 6.9% |
| Entertainment | 830 | 6.8% |
| Europe | 763 | 6.3% |
| Religious | 638 | 5.3% |
| Series | 525 | 4.3% |
| South America | 486 | 4.0% |
| Asia | 483 | 4.0% |
| Documentary | 401 | 3.3% |
| United States | 401 | 3.3% |
| Kids | 380 | 3.1% |
| North America | 288 | 2.4% |
| Comedy | 178 | 1.5% |
| Education | 144 | 1.2% |
| Culture | 122 | 1.0% |
| Legislative | 117 | 1.0% |
| India | 88 | 0.7% |
| Classic TV | 70 | 0.6% |
| Africa | 69 | 0.6% |
| Business | 68 | 0.6% |
| A&E Networks | 47 | 0.4% |
| UK | 35 | 0.3% |
| Family | 33 | 0.3% |
| Canada | 26 | 0.2% |
| Auto | 21 | 0.2% |
| Weather | 17 | 0.1% |
| Online TV | 16 | 0.1% |
| DLTV | 15 | 0.1% |
| Animals & Nature | 13 | 0.1% |
| Australia | 13 | 0.1% |
| Public TV | 13 | 0.1% |
| Tv Reality | 13 | 0.1% |
| Global TV | 12 | 0.1% |
| Tv Paranormal | 11 | 0.1% |
| Tv Celebrities | 9 | 0.1% |
| Eurovision Song Contest Asia on Aria (November 14th) | 8 | 0.1% |
| Aria Web Channels | 6 | 0.0% |
| Tv Shows | 6 | 0.0% |
| Oceania | 5 | 0.0% |
| Relax | 3 | 0.0% |
| IPTV | 1 | 0.0% |
| MeTV | 1 | 0.0% |
| Shopping | 1 | 0.0% |
| TEST | 1 | 0.0% |
| United Kingdom | 1 | 0.0% |
| USA Channels | 1 | 0.0% |
| Other | 416 | 3.4% |

## Country playlists (`playlists/countries/` — 173 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 2888 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1067 | [`countries/International.m3u`](countries/International.m3u) |
| India | 793 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 538 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 425 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Germany | 386 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| Sweden | 376 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| UK | 258 | [`countries/UK.m3u`](countries/UK.m3u) |
| France | 243 | [`countries/France.m3u`](countries/France.m3u) |
| Spain | 210 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| Dominican Republic | 201 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Chile | 189 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Brazil | 184 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Poland | 179 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Ukraine | 169 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Argentina | 165 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Romania | 164 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Hungary | 160 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| Canada | 149 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Netherlands | 148 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Peru | 141 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Turkey | 137 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Mexico | 122 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Colombia | 108 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| Indonesia | 106 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| _…and 148 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 70 / 77 unique links (dead: 0, unverified: 7)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | reachable | - | 0 | no_static_playlist | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. (repository is archived) |
| dlive.sx | failed | - | 0 | not_imported | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. — GET https://dlive.sx/24-7-channels.php failed: <urlopen error [Errno -2] Name or service not known> |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 403 | 0 | 1116 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 404 | 1112 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| TimeoutError | 0 | 803 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| gaierror | 0 | 411 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 376 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| ConnectionRefusedError | 0 | 147 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-09T16:14:00Z) | 145 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-09T16:14:00Z) | 145 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-09T16:14:00Z) | 112 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 400 | 66 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 401 | 0 | 58 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 502 | 0 | 28 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-09T16:14:00Z) | 27 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-13T14:37:07Z) | 26 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 504 | 0 | 25 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| SSLError | 0 | 22 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-11T14:17:46Z) | 22 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 503 | 0 | 21 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-10T14:54:44Z) | 20 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 1x, last 2026-11-09T16:14:00Z) | 19 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| RemoteDisconnected | 0 | 17 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-08T13:22:59Z) | 17 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-09T16:14:00Z) | 17 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-12T15:12:00Z) | 16 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 500 | 0 | 15 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| empty response | 14 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| OSError | 0 | 13 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme rtmp | 0 | 13 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-11T14:17:46Z) | 13 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 1x, last 2026-11-09T16:14:00Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 1x, last 2026-11-09T16:14:00Z) | 11 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-07T13:02:15Z) | 10 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 1x, last 2026-11-11T14:17:46Z) | 10 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-09T16:14:00Z) | 9 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-09T16:14:00Z) | 9 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-10T14:54:44Z) | 9 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-13T14:37:07Z) | 8 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-12T15:12:00Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 451 | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-10T14:54:44Z) | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-12T15:12:00Z) | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-13T14:37:07Z) | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-11T14:17:46Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-12T15:12:00Z) | 6 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 530 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-07T13:02:15Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-11-13T14:37:07Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-12T15:12:00Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-11-12T15:12:00Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-10T14:54:44Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| invalid URL | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-10T14:54:44Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 1x, last 2026-11-10T14:54:44Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 1x, last 2026-11-13T14:37:07Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-10T14:54:44Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-08T13:22:59Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-12T15:12:00Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-07T13:02:15Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-11T14:17:46Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLEOFError | 0 | 3 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-08T13:22:59Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-11T14:17:46Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-10T14:54:44Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-13T14:37:07Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-13T14:37:07Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 1x, last 2026-11-09T16:14:00Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 2 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 523 | 0 | 2 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme mmsh | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| not probed: unsupported scheme rtsp | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-07T13:02:15Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-08T13:22:59Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: html page, not a stream (failed the deep check 1x, last 2026-11-09T16:14:00Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 1x, last 2026-11-10T14:54:44Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-11-09T16:14:00Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-08T13:22:59Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 1x, last 2026-11-09T16:14:00Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-11-11T14:17:46Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-13T14:37:07Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-09T16:14:00Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-10T14:54:44Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-13T14:37:07Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 302 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 406 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 409 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 422 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 400 (failed the deep check 1x, last 2026-11-10T14:54:44Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 400 (failed the deep check 1x, last 2026-11-11T14:17:46Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 2x, last 2026-11-09T16:14:00Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: connection refused (failed the deep check 2x, last 2026-11-11T14:17:46Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: dash manifest has no representations (failed the deep check 2x, last 2026-11-12T15:12:00Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-07T13:02:15Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-11-08T13:22:59Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-11-09T16:14:00Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-11-10T14:54:44Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist lists no segments (failed the deep check 1x, last 2026-11-08T13:22:59Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist lists no segments (failed the deep check 1x, last 2026-11-11T14:17:46Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 2x, last 2026-11-09T16:14:00Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 401 (failed the deep check 1x, last 2026-11-09T16:14:00Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 401 (failed the deep check 1x, last 2026-11-12T15:12:00Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-13T14:37:07Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-11-07T13:02:15Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-11-11T14:17:46Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-11-12T15:12:00Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-09T16:14:00Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-10T14:54:44Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-11T14:17:46Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 1x, last 2026-11-09T16:14:00Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 1x, last 2026-11-12T15:12:00Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 1x, last 2026-11-13T14:37:07Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-11-07T13:02:15Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-11-09T16:14:00Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-11-11T14:17:46Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, segment too small (214 bytes) (failed the deep check 1x, last 2026-11-10T14:54:44Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 1x, last 2026-11-11T14:17:46Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 1x, last 2026-11-12T15:12:00Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-07T13:02:15Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-08T13:22:59Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-07T13:02:15Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-08T13:22:59Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-11T14:17:46Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 410 (failed the deep check 1x, last 2026-11-09T16:14:00Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |

### Run/source issues

- Reference check 'dlive.sx' failed: GET https://dlive.sx/24-7-channels.php failed: <urlopen error [Errno -2] Name or service not known>
- 2715 links could not be confirmed after retries (see unverified details).
- 2419 links returned a confirmed failure (see dead details).
- This run started +4h 03m after its scheduled time (2026-11-13T21:41:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
