# Scraper status

- **Last run:** 2026-10-31 04:25 PM EDT (2026-10-31 20:25 UTC)
- **Run:** _12:53 PM recheck_ (`recheck`; ID `20261031T202157Z-2932`)
- **Scheduled for:** 2026-10-31T16:53:00Z — started late by +3h 29m
- **Outcome:** **WARNING**
- **Confirmed working:** 12438 / 17171 unique links
- **Dead:** 1685  |  **Unverified:** 3048
- **Retained (unverified, within grace):** 149 previously published links kept so their channels do not vanish after one unverifiable run
- **Unique links found:** 17171 from 21380 source entries
- **Changes vs. PremiumTV_all.m3u:** +474 added / -401 removed
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
| 1 | Sports | 722 |
| 2 | Sports Backups | 3 |
| 3 | Lifestyle | 536 |
| 4 | Fox Channels | 24 |
| 5 | CBS | 40 |
| 6 | NBC | 62 |
| 7 | NBC Sports Channels | 6 |
| 8 | Cartoons | 193 |
| 9 | PBS | 19 |
| 10 | Game Shows | 19 |
| 11 | News | 1069 |
| 12 | Movies | 976 |
| 13 | Music | 920 |
| 14 | International | 886 |
| 15 | Europe | 849 |
| 16 | Entertainment | 830 |
| 17 | Religious | 689 |
| 18 | Asia | 541 |
| 19 | Series | 527 |
| 20 | South America | 511 |
| 21 | Documentary | 419 |
| 22 | United States | 382 |
| 23 | Kids | 371 |
| 24 | North America | 303 |
| 25 | Comedy | 181 |
| 26 | Education | 141 |
| 27 | Culture | 135 |
| 28 | Legislative | 121 |
| 29 | India | 108 |
| 30 | Classic TV | 78 |
| 31 | Africa | 76 |
| 32 | Business | 68 |
| 33 | A&E Networks | 50 |
| 34 | Family | 36 |
| 35 | UK | 33 |
| 36 | Canada | 25 |
| 37 | Australia | 24 |
| 38 | Auto | 24 |
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
| 58 | Other | 438 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 4 | 4 | 3 | 2 | 2 | 0 |
| priority-channels | ok | 17 | 17 | 10 | 17 | 0 | 0 |
| ae-networks | ok | 53 | 53 | 16 | 50 | 0 | 3 |
| aria | ok | 291 | 287 | 86 | 224 | 7 | 56 |
| doms9 | ok | 1023 | 1019 | 84 | 283 | 230 | 506 |
| xtemus | ok | 317 | 317 | 0 | 32 | 233 | 52 |
| iptv-org | ok | 11355 | 11355 | 3597 | 8489 | 848 | 2018 |
| free-tv | ok | 2053 | 2029 | 803 | 1281 | 309 | 439 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| m3u 🌱 | ok | 839 | 835 | 174 | 678 | 69 | 87 |
| openstream 🌱 | ok | 5428 | 5428 | 3146 | 5354 | 61 | 13 |

🌱 = source added automatically by the monthly discovery engine: m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **12587** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 722 | 5.7% |
| Sports Backups | 3 | 0.0% |
| Lifestyle | 536 | 4.3% |
| Fox Channels | 24 | 0.2% |
| CBS | 40 | 0.3% |
| NBC | 62 | 0.5% |
| NBC Sports Channels | 6 | 0.0% |
| Cartoons | 193 | 1.5% |
| PBS | 19 | 0.2% |
| Game Shows | 19 | 0.2% |
| News | 1069 | 8.5% |
| Movies | 976 | 7.8% |
| Music | 920 | 7.3% |
| International | 886 | 7.0% |
| Europe | 849 | 6.7% |
| Entertainment | 830 | 6.6% |
| Religious | 689 | 5.5% |
| Asia | 541 | 4.3% |
| Series | 527 | 4.2% |
| South America | 511 | 4.1% |
| Documentary | 419 | 3.3% |
| United States | 382 | 3.0% |
| Kids | 371 | 2.9% |
| North America | 303 | 2.4% |
| Comedy | 181 | 1.4% |
| Education | 141 | 1.1% |
| Culture | 135 | 1.1% |
| Legislative | 121 | 1.0% |
| India | 108 | 0.9% |
| Classic TV | 78 | 0.6% |
| Africa | 76 | 0.6% |
| Business | 68 | 0.5% |
| A&E Networks | 50 | 0.4% |
| Family | 36 | 0.3% |
| UK | 33 | 0.3% |
| Canada | 25 | 0.2% |
| Australia | 24 | 0.2% |
| Auto | 24 | 0.2% |
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
| Other | 438 | 3.5% |

## Country playlists (`playlists/countries/` — 178 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 2903 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1205 | [`countries/International.m3u`](countries/International.m3u) |
| India | 810 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 536 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 441 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Germany | 391 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| Sweden | 376 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| UK | 253 | [`countries/UK.m3u`](countries/UK.m3u) |
| Spain | 232 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| France | 219 | [`countries/France.m3u`](countries/France.m3u) |
| Dominican Republic | 212 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Chile | 202 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Brazil | 188 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Ukraine | 179 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Argentina | 170 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Poland | 169 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Netherlands | 160 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Hungary | 155 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| Turkey | 151 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Peru | 147 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Canada | 142 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Romania | 137 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Mexico | 124 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Colombia | 122 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| Indonesia | 118 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
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
| HTTP 403 | 0 | 1467 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 404 | 1206 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| TimeoutError | 0 | 825 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| gaierror | 0 | 412 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 379 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| ConnectionRefusedError | 0 | 104 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 400 | 69 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 401 | 0 | 38 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 503 | 0 | 35 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 504 | 0 | 23 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| RemoteDisconnected | 0 | 22 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLError | 0 | 22 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| SSLEOFError | 0 | 19 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 502 | 0 | 15 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| OSError | 0 | 14 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| empty response | 14 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| not probed: unsupported scheme rtmp | 0 | 13 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| HTTP 500 | 0 | 12 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 451 | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 530 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 521 | 0 | 4 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| invalid URL | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 2 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 523 | 0 | 2 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme mmsh | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| HTTP 302 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 406 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 409 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 422 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 429 | 0 | 1 | The host rate-limited the check; this scraper now limits parallel requests per host and retries with Retry-After/backoff. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme rtsp | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |

### Run/source issues

- 3048 links could not be confirmed after retries (see unverified details).
- 1685 links returned a confirmed failure (see dead details).
- This run started +3h 29m after its scheduled time (2026-10-31T16:53:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
