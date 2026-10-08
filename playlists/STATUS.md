# Scraper status

- **Last run:** 2026-10-08 03:30 PM EDT (2026-10-08 19:30 UTC)
- **Run:** _9:41 AM recheck_ (`recheck`; ID `20261008T192704Z-2633`)
- **Scheduled for:** 2026-10-08T13:41:00Z — started late by +5h 46m
- **Outcome:** **WARNING**
- **Confirmed working:** 9806 / 16417 unique links
- **Dead:** 3863  |  **Unverified:** 2748
- **Unique links found:** 16417 from 20720 source entries
- **Changes vs. PremiumTV_all.m3u:** +181 added / -182 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (173 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (59 confirmed working / 71 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 421 |
| 2 | Sports Backups | 70 |
| 3 | Lifestyle | 385 |
| 4 | Lifestyle Backups | 69 |
| 5 | Fox Channels | 32 |
| 6 | Fox Channels Backups | 1 |
| 7 | CBS | 31 |
| 8 | CBS Backups | 13 |
| 9 | NBC | 71 |
| 10 | NBC Backups | 9 |
| 11 | NBC Sports Channels | 7 |
| 12 | NBC Sports Channels Backups | 1 |
| 13 | Cartoons | 85 |
| 14 | Cartoons Backups | 19 |
| 15 | PBS | 34 |
| 16 | PBS Backups | 8 |
| 17 | Game Shows | 11 |
| 18 | Game Shows Backups | 11 |
| 19 | Music | 757 |
| 20 | Music Backups | 67 |
| 21 | News | 715 |
| 22 | News Backups | 146 |
| 23 | Europe | 684 |
| 24 | Europe Backups | 66 |
| 25 | Movies | 624 |
| 26 | Movies Backups | 68 |
| 27 | International | 622 |
| 28 | International Backups | 97 |
| 29 | Religious | 562 |
| 30 | Religious Backups | 36 |
| 31 | Entertainment | 493 |
| 32 | Entertainment Backups | 51 |
| 33 | South America | 448 |
| 34 | South America Backups | 21 |
| 35 | Asia | 417 |
| 36 | Asia Backups | 23 |
| 37 | United States | 308 |
| 38 | United States Backups | 47 |
| 39 | North America | 287 |
| 40 | North America Backups | 4 |
| 41 | Documentary | 259 |
| 42 | Documentary Backups | 52 |
| 43 | Kids | 216 |
| 44 | Kids Backups | 39 |
| 45 | Series | 144 |
| 46 | Series Backups | 68 |
| 47 | Education | 114 |
| 48 | Education Backups | 5 |
| 49 | Culture | 111 |
| 50 | Culture Backups | 7 |
| 51 | Legislative | 96 |
| 52 | Legislative Backups | 3 |
| 53 | India | 77 |
| 54 | India Backups | 5 |
| 55 | Africa | 64 |
| 56 | Business | 44 |
| 57 | Business Backups | 10 |
| 58 | Comedy | 39 |
| 59 | Comedy Backups | 23 |
| 60 | Classic TV | 31 |
| 61 | Classic TV Backups | 4 |
| 62 | Family | 24 |
| 63 | Family Backups | 2 |
| 64 | UK | 24 |
| 65 | UK Backups | 4 |
| 66 | A&E Networks | 23 |
| 67 | A&E Networks Backups | 2 |
| 68 | Canada | 21 |
| 69 | Weather | 9 |
| 70 | Weather Backups | 3 |
| 71 | Animals & Nature | 5 |
| 72 | Animals & Nature Backups | 2 |
| 73 | Aria Web Channels | 5 |
| 74 | Online TV | 4 |
| 75 | Online TV Backups | 1 |
| 76 | Tv Paranormal | 4 |
| 77 | Tv Paranormal Backups | 1 |
| 78 | Australia | 3 |
| 79 | Global TV | 3 |
| 80 | Global TV Backups | 2 |
| 81 | Tv Celebrities | 3 |
| 82 | Oceania | 2 |
| 83 | Oceania Backups | 1 |
| 84 | Relax | 2 |
| 85 | Relax Backups | 1 |
| 86 | Tv Shows | 2 |
| 87 | MeTV | 1 |
| 88 | United Kingdom | 1 |
| 89 | Other | 285 |
| 90 | Other Backups | 134 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 4 | 4 | 3 | 2 | 0 | 2 |
| priority-channels | ok | 15 | 15 | 6 | 15 | 0 | 0 |
| ae-networks | ok | 53 | 53 | 17 | 42 | 9 | 2 |
| aria | ok | 348 | 343 | 112 | 249 | 25 | 69 |
| doms9 | ok | 384 | 383 | 70 | 212 | 41 | 130 |
| xtemus | ok | 317 | 317 | 0 | 2 | 262 | 53 |
| iptv-org | ok | 11196 | 11196 | 3671 | 6435 | 2714 | 2047 |
| free-tv | ok | 2080 | 2054 | 832 | 1080 | 514 | 460 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| m3u 🌱 | ok | 831 | 827 | 178 | 327 | 399 | 101 |
| openstream 🌱 | ok | 5492 | 5492 | 3211 | 5002 | 472 | 18 |

🌱 = source added automatically by the monthly discovery engine: m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **9806** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 421 | 4.3% |
| Sports Backups | 70 | 0.7% |
| Lifestyle | 385 | 3.9% |
| Lifestyle Backups | 69 | 0.7% |
| Fox Channels | 32 | 0.3% |
| Fox Channels Backups | 1 | 0.0% |
| CBS | 31 | 0.3% |
| CBS Backups | 13 | 0.1% |
| NBC | 71 | 0.7% |
| NBC Backups | 9 | 0.1% |
| NBC Sports Channels | 7 | 0.1% |
| NBC Sports Channels Backups | 1 | 0.0% |
| Cartoons | 85 | 0.9% |
| Cartoons Backups | 19 | 0.2% |
| PBS | 34 | 0.3% |
| PBS Backups | 8 | 0.1% |
| Game Shows | 11 | 0.1% |
| Game Shows Backups | 11 | 0.1% |
| Music | 757 | 7.7% |
| Music Backups | 67 | 0.7% |
| News | 715 | 7.3% |
| News Backups | 146 | 1.5% |
| Europe | 684 | 7.0% |
| Europe Backups | 66 | 0.7% |
| Movies | 624 | 6.4% |
| Movies Backups | 68 | 0.7% |
| International | 622 | 6.3% |
| International Backups | 97 | 1.0% |
| Religious | 562 | 5.7% |
| Religious Backups | 36 | 0.4% |
| Entertainment | 493 | 5.0% |
| Entertainment Backups | 51 | 0.5% |
| South America | 448 | 4.6% |
| South America Backups | 21 | 0.2% |
| Asia | 417 | 4.3% |
| Asia Backups | 23 | 0.2% |
| United States | 308 | 3.1% |
| United States Backups | 47 | 0.5% |
| North America | 287 | 2.9% |
| North America Backups | 4 | 0.0% |
| Documentary | 259 | 2.6% |
| Documentary Backups | 52 | 0.5% |
| Kids | 216 | 2.2% |
| Kids Backups | 39 | 0.4% |
| Series | 144 | 1.5% |
| Series Backups | 68 | 0.7% |
| Education | 114 | 1.2% |
| Education Backups | 5 | 0.1% |
| Culture | 111 | 1.1% |
| Culture Backups | 7 | 0.1% |
| Legislative | 96 | 1.0% |
| Legislative Backups | 3 | 0.0% |
| India | 77 | 0.8% |
| India Backups | 5 | 0.1% |
| Africa | 64 | 0.7% |
| Business | 44 | 0.4% |
| Business Backups | 10 | 0.1% |
| Comedy | 39 | 0.4% |
| Comedy Backups | 23 | 0.2% |
| Classic TV | 31 | 0.3% |
| Classic TV Backups | 4 | 0.0% |
| Family | 24 | 0.2% |
| Family Backups | 2 | 0.0% |
| UK | 24 | 0.2% |
| UK Backups | 4 | 0.0% |
| A&E Networks | 23 | 0.2% |
| A&E Networks Backups | 2 | 0.0% |
| Canada | 21 | 0.2% |
| Weather | 9 | 0.1% |
| Weather Backups | 3 | 0.0% |
| Animals & Nature | 5 | 0.1% |
| Animals & Nature Backups | 2 | 0.0% |
| Aria Web Channels | 5 | 0.1% |
| Online TV | 4 | 0.0% |
| Online TV Backups | 1 | 0.0% |
| Tv Paranormal | 4 | 0.0% |
| Tv Paranormal Backups | 1 | 0.0% |
| Australia | 3 | 0.0% |
| Global TV | 3 | 0.0% |
| Global TV Backups | 2 | 0.0% |
| Tv Celebrities | 3 | 0.0% |
| Oceania | 2 | 0.0% |
| Oceania Backups | 1 | 0.0% |
| Relax | 2 | 0.0% |
| Relax Backups | 1 | 0.0% |
| Tv Shows | 2 | 0.0% |
| MeTV | 1 | 0.0% |
| United Kingdom | 1 | 0.0% |
| Other | 285 | 2.9% |
| Other Backups | 134 | 1.4% |

## Country playlists (`playlists/countries/` — 173 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 2084 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 979 | [`countries/International.m3u`](countries/International.m3u) |
| India | 634 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 475 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 397 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| UK | 224 | [`countries/UK.m3u`](countries/UK.m3u) |
| Brazil | 191 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| France | 190 | [`countries/France.m3u`](countries/France.m3u) |
| Dominican Republic | 188 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Spain | 187 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| Chile | 173 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Ukraine | 171 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Germany | 169 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| Argentina | 157 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Peru | 146 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Netherlands | 133 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Canada | 129 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Poland | 126 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Turkey | 126 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Mexico | 124 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Romania | 119 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Hungary | 107 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| Indonesia | 107 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| Colombia | 103 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| Greece | 79 | [`countries/Greece.m3u`](countries/Greece.m3u) |
| _…and 148 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 59 / 71 unique links (dead: 9, unverified: 3)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | reachable | - | 0 | no_static_playlist | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. (repository is archived) |
| dlive.sx | reachable | 899 | 0 | player_pages_only | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 403 | 0 | 1071 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 975 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 404 | 949 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| TimeoutError | 0 | 775 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-10-03T10:25:19Z) | 620 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| html page, not a stream | 406 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| gaierror | 0 | 389 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| ConnectionRefusedError | 0 | 222 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 97 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 503 | 0 | 82 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-10-03T10:25:19Z) | 65 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 400 | 54 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 52 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 401 | 0 | 46 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-10-03T10:25:19Z) | 29 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 504 | 0 | 23 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| RemoteDisconnected | 0 | 22 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-03T14:46:53Z) | 22 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-06T12:02:47Z) | 21 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLEOFError | 0 | 20 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| SSLError | 0 | 17 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-04T11:07:47Z) | 17 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 502 | 0 | 16 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| OSError | 0 | 15 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 15 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 14 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 14 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 14 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| empty response | 13 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 500 | 0 | 10 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 10 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 9 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 9 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-04T11:07:47Z) | 9 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-06T12:02:47Z) | 9 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 3x, last 2026-10-03T10:25:19Z) | 9 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 530 | 0 | 8 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme rtmp | 0 | 8 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-02T20:58:47Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-02T21:14:06Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-03T15:00:01Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 4x, last 2026-10-03T15:00:01Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 302 (failed the deep check 1x, last 2026-10-03T10:25:19Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP timeout (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 8 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-02T21:46:31Z) | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-03T15:10:12Z) | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-10-02T21:31:25Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 502 (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-03T15:00:01Z) | 6 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-03T15:10:12Z) | 6 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 404 (failed the deep check 4x, last 2026-10-03T15:00:01Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 504 (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP RemoteDisconnected (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 6 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: connection refused (failed the deep check 2x, last 2026-10-06T12:02:47Z) | 5 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 404 (failed the deep check 4x, last 2026-10-03T15:00:01Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, dns lookup failed (failed the deep check 1x, last 2026-10-03T10:25:19Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-10-02T20:58:47Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-02T20:58:47Z) | 5 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-06T12:02:47Z) | 5 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 302 (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 504 (failed the deep check 2x, last 2026-10-02T21:31:25Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 1x, last 2026-10-03T10:25:19Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 451 | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 523 | 0 | 4 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| invalid URL | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 503 (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-06T12:02:47Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-02T21:31:25Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-04T11:07:47Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-03T15:00:01Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP timeout (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 4 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 429 | 0 | 3 | The host rate-limited the check; this scraper now limits parallel requests per host and retries with Retry-After/backoff. |
| quarantined: connection refused (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: dns lookup failed (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist lists no segments (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-02T21:14:06Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-06T12:02:47Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-04T11:07:47Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-02T21:31:25Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 429 (failed the deep check 2x, last 2026-10-02T21:46:31Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 502 (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-06T12:02:47Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP TimeoutError (failed the deep check 4x, last 2026-10-03T15:00:01Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP timeout (failed the deep check 1x, last 2026-10-03T10:25:19Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 409 | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 477 | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 521 | 0 | 2 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme mmsh | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: connection refused (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: dns lookup failed (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 2x, last 2026-10-04T11:07:47Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-10-03T14:46:53Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist lists no segments (failed the deep check 2x, last 2026-10-04T11:07:47Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-02T20:58:47Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-02T21:46:31Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-04T11:07:47Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-10-02T21:46:31Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 502 (failed the deep check 2x, last 2026-10-02T20:58:47Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, SSLEOFError (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, TimeoutError (failed the deep check 4x, last 2026-10-03T15:00:01Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-10-04T11:07:47Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-03T14:46:53Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 403 (failed the deep check 1x, last 2026-10-03T10:25:19Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 502 (failed the deep check 2x, last 2026-10-03T14:46:53Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 502 (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP RemoteDisconnected (failed the deep check 2x, last 2026-10-03T14:46:53Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP RemoteDisconnected (failed the deep check 2x, last 2026-10-04T11:07:47Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP SSLEOFError (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP timeout (failed the deep check 2x, last 2026-10-06T12:02:47Z) | 2 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 302 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 406 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 1 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 458 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme rtsp | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-02T20:58:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-05T12:17:17Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-10-08T12:02:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 4x, last 2026-10-03T15:10:12Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 2x, last 2026-10-03T14:46:53Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: connection refused (failed the deep check 2x, last 2026-10-03T15:00:01Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: connection refused (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: dns lookup failed (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 2x, last 2026-10-03T15:10:12Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 4x, last 2026-10-03T15:00:01Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, ConnectionResetError (failed the deep check 2x, last 2026-10-02T20:58:47Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 302 (failed the deep check 1x, last 2026-10-03T10:25:19Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 302 (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 304 (failed the deep check 2x, last 2026-10-04T11:07:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 401 (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-03T15:00:01Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-04T11:07:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-06T12:02:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-10-02T21:46:31Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-03T15:00:01Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-10-03T15:10:12Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-10-03T15:10:12Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-10-04T11:07:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 429 (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 500 (failed the deep check 2x, last 2026-10-02T21:14:06Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 500 (failed the deep check 2x, last 2026-10-04T11:07:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 502 (failed the deep check 2x, last 2026-10-03T15:00:01Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 502 (failed the deep check 2x, last 2026-10-04T11:07:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 502 (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 502 (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 502 (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 503 (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, InvalidURL (failed the deep check 2x, last 2026-10-02T21:31:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, RemoteDisconnected (failed the deep check 2x, last 2026-10-03T15:10:12Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-02T20:58:47Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-03T14:46:53Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, TimeoutError (failed the deep check 2x, last 2026-10-03T15:00:01Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-10-02T21:31:25Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, segment too small (214 bytes) (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, segment too small (94 bytes) (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, timeout (failed the deep check 1x, last 2026-10-02T21:14:06Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, timeout (failed the deep check 1x, last 2026-10-02T21:46:31Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, timeout (failed the deep check 2x, last 2026-10-02T21:14:06Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, timeout (failed the deep check 4x, last 2026-10-03T15:00:01Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-10-03T15:00:01Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-10-05T12:17:17Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-02T21:14:06Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-03T14:46:53Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-10-03T15:10:12Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 4x, last 2026-10-03T15:10:12Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 410 (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 429 (failed the deep check 2x, last 2026-10-03T14:46:53Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 500 (failed the deep check 2x, last 2026-10-02T21:14:06Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 500 (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 500 (failed the deep check 2x, last 2026-10-03T15:10:12Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 502 (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 502 (failed the deep check 2x, last 2026-10-04T11:07:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 502 (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 503 (failed the deep check 2x, last 2026-10-03T10:25:19Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 503 (failed the deep check 2x, last 2026-10-03T15:00:01Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 503 (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 504 (failed the deep check 4x, last 2026-10-03T15:10:12Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP ConnectionResetError (failed the deep check 2x, last 2026-10-03T15:10:12Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP ConnectionResetError (failed the deep check 2x, last 2026-10-04T11:07:47Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP RemoteDisconnected (failed the deep check 2x, last 2026-10-02T20:58:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP RemoteDisconnected (failed the deep check 2x, last 2026-10-03T15:10:12Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP RemoteDisconnected (failed the deep check 2x, last 2026-10-06T12:02:47Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP RemoteDisconnected (failed the deep check 2x, last 2026-10-08T12:02:30Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP TimeoutError (failed the deep check 1x, last 2026-10-03T10:25:19Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-03T14:46:53Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP TimeoutError (failed the deep check 2x, last 2026-10-07T11:47:42Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP connection refused (failed the deep check 2x, last 2026-10-04T11:07:47Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP timeout (failed the deep check 2x, last 2026-10-02T21:46:31Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP timeout (failed the deep check 2x, last 2026-10-03T14:46:53Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP timeout (failed the deep check 2x, last 2026-10-03T15:00:01Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |

### Run/source issues

- 2748 links could not be confirmed after retries (see unverified details).
- 3863 links returned a confirmed failure (see dead details).
- This run started +5h 46m after its scheduled time (2026-10-08T13:41:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
