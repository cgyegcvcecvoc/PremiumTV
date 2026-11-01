# Scraper status

- **Last run:** 2026-11-01 02:15 PM EST (2026-11-01 19:15 UTC)
- **Run:** _9:41 AM recheck_ (`recheck`; ID `20261101T191126Z-2711`)
- **Scheduled for:** 2026-11-01T14:41:00Z — started late by +4h 30m
- **Outcome:** **WARNING**
- **Confirmed working:** 12262 / 17310 unique links
- **Dead:** 2047  |  **Unverified:** 3001
- **Retained (unverified, within grace):** 152 previously published links kept so their channels do not vanish after one unverifiable run
- **Unique links found:** 17310 from 21713 source entries
- **Changes vs. PremiumTV_all.m3u:** +584 added / -660 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (173 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (71 confirmed working / 75 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 721 |
| 2 | Sports Backups | 2 |
| 3 | Lifestyle | 533 |
| 4 | Fox Channels | 23 |
| 5 | CBS | 38 |
| 6 | NBC | 61 |
| 7 | NBC Sports Channels | 9 |
| 8 | Cartoons | 195 |
| 9 | PBS | 20 |
| 10 | Game Shows | 19 |
| 11 | News | 1034 |
| 12 | Movies | 983 |
| 13 | Music | 909 |
| 14 | Entertainment | 880 |
| 15 | Europe | 821 |
| 16 | International | 821 |
| 17 | Religious | 676 |
| 18 | Series | 524 |
| 19 | Asia | 510 |
| 20 | South America | 500 |
| 21 | Documentary | 422 |
| 22 | Kids | 387 |
| 23 | United States | 372 |
| 24 | North America | 297 |
| 25 | Comedy | 179 |
| 26 | Education | 135 |
| 27 | Culture | 130 |
| 28 | Legislative | 102 |
| 29 | India | 85 |
| 30 | Classic TV | 78 |
| 31 | Africa | 71 |
| 32 | Business | 69 |
| 33 | A&E Networks | 50 |
| 34 | Family | 36 |
| 35 | UK | 33 |
| 36 | Online TV | 32 |
| 37 | Auto | 24 |
| 38 | Canada | 24 |
| 39 | Australia | 18 |
| 40 | Weather | 17 |
| 41 | DLTV | 15 |
| 42 | Public TV | 14 |
| 43 | Animals & Nature | 13 |
| 44 | Tv Reality | 13 |
| 45 | Global TV | 12 |
| 46 | Tv Paranormal | 11 |
| 47 | Tv Celebrities | 9 |
| 48 | Aria Web Channels | 6 |
| 49 | Tv Shows | 6 |
| 50 | Oceania | 5 |
| 51 | Relax | 5 |
| 52 | Shopping | 2 |
| 53 | 3-Radio#Chicago | 1 |
| 54 | IPTV | 1 |
| 55 | Live TV | 1 |
| 56 | MeTV | 1 |
| 57 | TEST | 1 |
| 58 | United Kingdom | 1 |
| 59 | USA Channels | 1 |
| 60 | Other | 456 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 4 | 4 | 3 | 2 | 2 | 0 |
| priority-channels | ok | 18 | 18 | 11 | 18 | 0 | 0 |
| ae-networks | ok | 53 | 53 | 16 | 50 | 0 | 3 |
| aria | ok | 291 | 287 | 87 | 214 | 18 | 55 |
| doms9 | ok | 812 | 812 | 88 | 286 | 132 | 394 |
| xtemus | ok | 317 | 317 | 0 | 31 | 231 | 55 |
| iptv-org | ok | 11388 | 11388 | 3695 | 8256 | 1129 | 2003 |
| free-tv | ok | 2053 | 2029 | 805 | 1169 | 420 | 440 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| VIP-m3u-playlist 🌱 | ok | 213 | 212 | 101 | 209 | 0 | 3 |
| israel-tv-plus 🌱 | ok | 297 | 276 | 72 | 197 | 1 | 78 |
| m3u 🌱 | ok | 839 | 835 | 174 | 670 | 80 | 84 |
| openstream 🌱 | ok | 5428 | 5428 | 3161 | 5119 | 292 | 17 |

🌱 = source added automatically by the monthly discovery engine: VIP-m3u-playlist, israel-tv-plus, m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **12414** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 721 | 5.8% |
| Sports Backups | 2 | 0.0% |
| Lifestyle | 533 | 4.3% |
| Fox Channels | 23 | 0.2% |
| CBS | 38 | 0.3% |
| NBC | 61 | 0.5% |
| NBC Sports Channels | 9 | 0.1% |
| Cartoons | 195 | 1.6% |
| PBS | 20 | 0.2% |
| Game Shows | 19 | 0.2% |
| News | 1034 | 8.3% |
| Movies | 983 | 7.9% |
| Music | 909 | 7.3% |
| Entertainment | 880 | 7.1% |
| Europe | 821 | 6.6% |
| International | 821 | 6.6% |
| Religious | 676 | 5.4% |
| Series | 524 | 4.2% |
| Asia | 510 | 4.1% |
| South America | 500 | 4.0% |
| Documentary | 422 | 3.4% |
| Kids | 387 | 3.1% |
| United States | 372 | 3.0% |
| North America | 297 | 2.4% |
| Comedy | 179 | 1.4% |
| Education | 135 | 1.1% |
| Culture | 130 | 1.0% |
| Legislative | 102 | 0.8% |
| India | 85 | 0.7% |
| Classic TV | 78 | 0.6% |
| Africa | 71 | 0.6% |
| Business | 69 | 0.6% |
| A&E Networks | 50 | 0.4% |
| Family | 36 | 0.3% |
| UK | 33 | 0.3% |
| Online TV | 32 | 0.3% |
| Auto | 24 | 0.2% |
| Canada | 24 | 0.2% |
| Australia | 18 | 0.1% |
| Weather | 17 | 0.1% |
| DLTV | 15 | 0.1% |
| Public TV | 14 | 0.1% |
| Animals & Nature | 13 | 0.1% |
| Tv Reality | 13 | 0.1% |
| Global TV | 12 | 0.1% |
| Tv Paranormal | 11 | 0.1% |
| Tv Celebrities | 9 | 0.1% |
| Aria Web Channels | 6 | 0.0% |
| Tv Shows | 6 | 0.0% |
| Oceania | 5 | 0.0% |
| Relax | 5 | 0.0% |
| Shopping | 2 | 0.0% |
| 3-Radio#Chicago | 1 | 0.0% |
| IPTV | 1 | 0.0% |
| Live TV | 1 | 0.0% |
| MeTV | 1 | 0.0% |
| TEST | 1 | 0.0% |
| United Kingdom | 1 | 0.0% |
| USA Channels | 1 | 0.0% |
| Other | 456 | 3.7% |

## Country playlists (`playlists/countries/` — 173 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 2839 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1360 | [`countries/International.m3u`](countries/International.m3u) |
| India | 785 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 529 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 428 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Sweden | 376 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| Germany | 369 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| UK | 250 | [`countries/UK.m3u`](countries/UK.m3u) |
| France | 217 | [`countries/France.m3u`](countries/France.m3u) |
| Dominican Republic | 210 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Spain | 200 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| Chile | 199 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Brazil | 186 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Ukraine | 177 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Poland | 168 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Argentina | 163 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Hungary | 150 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| Netherlands | 150 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Peru | 146 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Turkey | 141 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Canada | 139 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Romania | 138 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Mexico | 123 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Colombia | 114 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| Indonesia | 109 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| _…and 148 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 71 / 75 unique links (dead: 0, unverified: 4)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | reachable | - | 0 | no_static_playlist | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. (repository is archived) |
| dlive.sx | reachable | 899 | 0 | player_pages_only | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 403 | 0 | 1437 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 404 | 1157 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| TimeoutError | 0 | 807 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| gaierror | 0 | 411 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 386 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 149 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 118 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionRefusedError | 0 | 117 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 400 | 69 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 401 | 0 | 39 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 32 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 503 | 0 | 28 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 504 | 0 | 23 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| RemoteDisconnected | 0 | 22 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLError | 0 | 21 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| SSLEOFError | 0 | 19 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 400 (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 19 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 502 | 0 | 15 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| empty response | 14 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| not probed: unsupported scheme rtmp | 0 | 13 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: variant HTTP 403 (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 13 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| OSError | 0 | 12 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 500 | 0 | 11 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 11 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 9 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 451 | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-01T11:56:39Z) | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 6 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 530 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-01T11:56:39Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-01T11:56:39Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 521 | 0 | 4 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| invalid URL | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| deep check: offline (variant HTTP 404) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 2x, last 2026-11-01T11:56:39Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 2 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 523 | 0 | 2 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme mmsh | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: html page, not a stream (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 302 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 406 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 409 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 422 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| deep check: offline (variant HTTP 403) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme rtsp | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: empty response (failed the deep check 2x, last 2026-11-01T11:56:39Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist lists no segments (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 401 (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-11-01T11:56:39Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, segment too small (214 bytes) (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 410 (failed the deep check 1x, last 2026-11-01T11:56:39Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |

### Run/source issues

- 3001 links could not be confirmed after retries (see unverified details).
- 2047 links returned a confirmed failure (see dead details).
- This run started +4h 30m after its scheduled time (2026-11-01T14:41:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
