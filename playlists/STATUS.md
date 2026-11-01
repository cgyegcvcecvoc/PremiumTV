# Scraper status

- **Last run:** 2026-11-01 01:15 AM EST (2026-11-01 06:15 UTC)
- **Run:** _8:17 PM recheck_ (`recheck`; ID `20261101T061150Z-2935`)
- **Scheduled for:** 2026-11-01T00:17:00Z — started late by +5h 55m
- **Outcome:** **WARNING**
- **Confirmed working:** 12392 / 16854 unique links
- **Dead:** 1564  |  **Unverified:** 2898
- **Retained (unverified, within grace):** 130 previously published links kept so their channels do not vanish after one unverifiable run
- **Unique links found:** 16854 from 21065 source entries
- **Changes vs. PremiumTV_all.m3u:** +385 added / -200 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (178 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (71 confirmed working / 75 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 639 |
| 2 | Sports Backups | 3 |
| 3 | Lifestyle | 538 |
| 4 | Fox Channels | 24 |
| 5 | CBS | 40 |
| 6 | NBC | 62 |
| 7 | NBC Sports Channels | 9 |
| 8 | Cartoons | 194 |
| 9 | PBS | 19 |
| 10 | Game Shows | 19 |
| 11 | News | 1071 |
| 12 | Movies | 986 |
| 13 | Music | 920 |
| 14 | International | 879 |
| 15 | Europe | 854 |
| 16 | Entertainment | 826 |
| 17 | Religious | 691 |
| 18 | Asia | 544 |
| 19 | Series | 526 |
| 20 | South America | 495 |
| 21 | Documentary | 423 |
| 22 | United States | 383 |
| 23 | Kids | 378 |
| 24 | North America | 301 |
| 25 | Comedy | 181 |
| 26 | Education | 143 |
| 27 | Culture | 133 |
| 28 | Legislative | 121 |
| 29 | India | 108 |
| 30 | Classic TV | 79 |
| 31 | Africa | 76 |
| 32 | Business | 69 |
| 33 | A&E Networks | 50 |
| 34 | Family | 37 |
| 35 | UK | 33 |
| 36 | Australia | 24 |
| 37 | Auto | 24 |
| 38 | Canada | 24 |
| 39 | Public TV | 20 |
| 40 | Weather | 17 |
| 41 | DLTV | 15 |
| 42 | Animals & Nature | 13 |
| 43 | Global TV | 13 |
| 44 | Tv Reality | 13 |
| 45 | Tv Paranormal | 11 |
| 46 | Online TV | 10 |
| 47 | Tv Celebrities | 9 |
| 48 | Tv Shows | 7 |
| 49 | Aria Web Channels | 6 |
| 50 | Oceania | 5 |
| 51 | Relax | 5 |
| 52 | Shopping | 2 |
| 53 | United Kingdom | 2 |
| 54 | 3-Radio#Chicago | 1 |
| 55 | MeTV | 1 |
| 56 | TEST | 1 |
| 57 | USA Channels | 1 |
| 58 | Other | 444 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 4 | 4 | 3 | 2 | 2 | 0 |
| priority-channels | ok | 17 | 17 | 10 | 17 | 0 | 0 |
| ae-networks | ok | 53 | 53 | 16 | 50 | 0 | 3 |
| aria | ok | 291 | 287 | 86 | 221 | 10 | 56 |
| doms9 | ok | 675 | 672 | 87 | 208 | 62 | 402 |
| xtemus | ok | 317 | 317 | 0 | 32 | 233 | 52 |
| iptv-org | ok | 11388 | 11388 | 3600 | 8522 | 888 | 1978 |
| free-tv | ok | 2053 | 2029 | 803 | 1281 | 317 | 431 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| m3u 🌱 | ok | 839 | 835 | 174 | 678 | 69 | 87 |
| openstream 🌱 | ok | 5428 | 5428 | 3146 | 5329 | 81 | 18 |

🌱 = source added automatically by the monthly discovery engine: m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **12522** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 639 | 5.1% |
| Sports Backups | 3 | 0.0% |
| Lifestyle | 538 | 4.3% |
| Fox Channels | 24 | 0.2% |
| CBS | 40 | 0.3% |
| NBC | 62 | 0.5% |
| NBC Sports Channels | 9 | 0.1% |
| Cartoons | 194 | 1.5% |
| PBS | 19 | 0.2% |
| Game Shows | 19 | 0.2% |
| News | 1071 | 8.6% |
| Movies | 986 | 7.9% |
| Music | 920 | 7.3% |
| International | 879 | 7.0% |
| Europe | 854 | 6.8% |
| Entertainment | 826 | 6.6% |
| Religious | 691 | 5.5% |
| Asia | 544 | 4.3% |
| Series | 526 | 4.2% |
| South America | 495 | 4.0% |
| Documentary | 423 | 3.4% |
| United States | 383 | 3.1% |
| Kids | 378 | 3.0% |
| North America | 301 | 2.4% |
| Comedy | 181 | 1.4% |
| Education | 143 | 1.1% |
| Culture | 133 | 1.1% |
| Legislative | 121 | 1.0% |
| India | 108 | 0.9% |
| Classic TV | 79 | 0.6% |
| Africa | 76 | 0.6% |
| Business | 69 | 0.6% |
| A&E Networks | 50 | 0.4% |
| Family | 37 | 0.3% |
| UK | 33 | 0.3% |
| Australia | 24 | 0.2% |
| Auto | 24 | 0.2% |
| Canada | 24 | 0.2% |
| Public TV | 20 | 0.2% |
| Weather | 17 | 0.1% |
| DLTV | 15 | 0.1% |
| Animals & Nature | 13 | 0.1% |
| Global TV | 13 | 0.1% |
| Tv Reality | 13 | 0.1% |
| Tv Paranormal | 11 | 0.1% |
| Online TV | 10 | 0.1% |
| Tv Celebrities | 9 | 0.1% |
| Tv Shows | 7 | 0.1% |
| Aria Web Channels | 6 | 0.0% |
| Oceania | 5 | 0.0% |
| Relax | 5 | 0.0% |
| Shopping | 2 | 0.0% |
| United Kingdom | 2 | 0.0% |
| 3-Radio#Chicago | 1 | 0.0% |
| MeTV | 1 | 0.0% |
| TEST | 1 | 0.0% |
| USA Channels | 1 | 0.0% |
| Other | 444 | 3.5% |

## Country playlists (`playlists/countries/` — 178 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 2831 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1205 | [`countries/International.m3u`](countries/International.m3u) |
| India | 813 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 533 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 442 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Germany | 393 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| Sweden | 376 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| UK | 262 | [`countries/UK.m3u`](countries/UK.m3u) |
| Spain | 231 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| France | 217 | [`countries/France.m3u`](countries/France.m3u) |
| Dominican Republic | 213 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Chile | 199 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Brazil | 188 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Ukraine | 179 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Argentina | 173 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Poland | 171 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Netherlands | 159 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Hungary | 155 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| Turkey | 151 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Canada | 142 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Romania | 140 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Peru | 134 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Mexico | 124 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Indonesia | 123 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| Colombia | 117 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| _…and 153 more countries_ | | [Full country index](countries/README.md) |

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
| HTTP 403 | 0 | 1373 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 404 | 1071 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| TimeoutError | 0 | 783 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| gaierror | 0 | 412 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 377 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| ConnectionRefusedError | 0 | 107 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 400 | 69 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 401 | 0 | 40 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 504 | 0 | 23 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 503 | 0 | 22 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| SSLError | 0 | 21 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| SSLEOFError | 0 | 19 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 410 | 18 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 502 | 0 | 16 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| RemoteDisconnected | 0 | 16 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 500 | 0 | 14 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| empty response | 14 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| OSError | 0 | 13 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme rtmp | 0 | 13 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| HTTP 451 | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 530 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 521 | 0 | 4 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| invalid URL | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 523 | 0 | 2 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme mmsh | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| HTTP 302 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 406 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 409 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme rtsp | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |

### Run/source issues

- 2898 links could not be confirmed after retries (see unverified details).
- 1564 links returned a confirmed failure (see dead details).
- This run started +5h 55m after its scheduled time (2026-11-01T00:17:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
