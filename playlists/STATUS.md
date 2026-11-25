# Scraper status

- **Last run:** 2026-11-24 08:45 PM EST (2026-11-25 01:45 UTC)
- **Run:** _12:53 PM recheck_ (`recheck`; ID `20261125T014115Z-3190`)
- **Scheduled for:** 2026-11-24T17:53:00Z — started late by +7h 48m
- **Outcome:** **WARNING**
- **Confirmed working:** 12587 / 19528 unique links
- **Dead:** 2355  |  **Unverified:** 4586
- **Retained (unverified, within grace):** 866 previously published links kept so their channels do not vanish after one unverifiable run
- **Unique links found:** 19528 from 24507 source entries
- **Changes vs. PremiumTV_all.m3u:** +312 added / -388 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (176 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (116 confirmed working / 152 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 728 |
| 2 | Lifestyle | 529 |
| 3 | Fox Channels | 36 |
| 4 | CBS | 71 |
| 5 | NBC | 68 |
| 6 | NBC Sports Channels | 6 |
| 7 | Cartoons | 201 |
| 8 | PBS | 24 |
| 9 | Game Shows | 20 |
| 10 | News | 1079 |
| 11 | International | 1068 |
| 12 | Movies | 1000 |
| 13 | Music | 926 |
| 14 | Entertainment | 877 |
| 15 | Europe | 769 |
| 16 | Religious | 675 |
| 17 | Series | 532 |
| 18 | Asia | 512 |
| 19 | South America | 495 |
| 20 | Kids | 429 |
| 21 | United States | 413 |
| 22 | Documentary | 395 |
| 23 | North America | 296 |
| 24 | Comedy | 198 |
| 25 | Education | 145 |
| 26 | Culture | 131 |
| 27 | Legislative | 117 |
| 28 | A&E Networks | 100 |
| 29 | India | 84 |
| 30 | Classic TV | 81 |
| 31 | Business | 78 |
| 32 | Africa | 70 |
| 33 | Canada | 59 |
| 34 | Reality | 55 |
| 35 | En Español | 44 |
| 36 | Family | 34 |
| 37 | Drama | 33 |
| 38 | Online TV | 32 |
| 39 | Home + Food | 30 |
| 40 | Daytime + Game Shows | 29 |
| 41 | UK | 29 |
| 42 | Auto | 27 |
| 43 | Weather | 21 |
| 44 | True Crime | 20 |
| 45 | Sci-Fi | 19 |
| 46 | Australia | 16 |
| 47 | Anime | 15 |
| 48 | DLTV | 15 |
| 49 | Aria Web Channels | 14 |
| 50 | Westerns | 14 |
| 51 | Animals & Nature | 13 |
| 52 | Public TV | 13 |
| 53 | Global TV | 12 |
| 54 | Animals + Nature | 11 |
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
| 66 | Paranormal | 1 |
| 67 | Shopping | 1 |
| 68 | Other | 677 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 3 | 3 | 1 | 1 | 1 | 1 |
| priority-channels | ok | 13 | 13 | 11 | 13 | 0 | 0 |
| ae-networks | ok | 50 | 50 | 12 | 47 | 0 | 3 |
| curated-channels | ok | 1 | 1 | 0 | 1 | 0 | 0 |
| aria | ok | 234 | 223 | 223 | 152 | 17 | 54 |
| aria-plus | ok | 2039 | 1983 | 334 | 485 | 236 | 1262 |
| doms9 | ok | 442 | 442 | 88 | 214 | 47 | 181 |
| xtemus | ok | 317 | 317 | 0 | 31 | 234 | 52 |
| iptv-org | ok | 11497 | 11497 | 3820 | 8175 | 1237 | 2085 |
| free-tv | ok | 2203 | 2179 | 938 | 1245 | 463 | 471 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| pluto-us | ok | 458 | 458 | 0 | 0 | 0 | 458 |
| aria-overseas | ok | 42 | 42 | 20 | 40 | 1 | 1 |
| vbskycn-iptv | ok | 348 | 346 | 11 | 322 | 2 | 22 |
| VIP-m3u-playlist 🌱 | ok | 226 | 221 | 152 | 207 | 13 | 1 |
| israel-tv-plus 🌱 | ok | 353 | 350 | 146 | 267 | 5 | 78 |
| m3u 🌱 | ok | 853 | 848 | 173 | 685 | 79 | 83 |
| openstream 🌱 | ok | 5428 | 5428 | 3120 | 4920 | 430 | 78 |

🌱 = source added automatically by the monthly discovery engine: VIP-m3u-playlist, israel-tv-plus, m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **13453** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 728 | 5.4% |
| Lifestyle | 529 | 3.9% |
| Fox Channels | 36 | 0.3% |
| CBS | 71 | 0.5% |
| NBC | 68 | 0.5% |
| NBC Sports Channels | 6 | 0.0% |
| Cartoons | 201 | 1.5% |
| PBS | 24 | 0.2% |
| Game Shows | 20 | 0.1% |
| News | 1079 | 8.0% |
| International | 1068 | 7.9% |
| Movies | 1000 | 7.4% |
| Music | 926 | 6.9% |
| Entertainment | 877 | 6.5% |
| Europe | 769 | 5.7% |
| Religious | 675 | 5.0% |
| Series | 532 | 4.0% |
| Asia | 512 | 3.8% |
| South America | 495 | 3.7% |
| Kids | 429 | 3.2% |
| United States | 413 | 3.1% |
| Documentary | 395 | 2.9% |
| North America | 296 | 2.2% |
| Comedy | 198 | 1.5% |
| Education | 145 | 1.1% |
| Culture | 131 | 1.0% |
| Legislative | 117 | 0.9% |
| A&E Networks | 100 | 0.7% |
| India | 84 | 0.6% |
| Classic TV | 81 | 0.6% |
| Business | 78 | 0.6% |
| Africa | 70 | 0.5% |
| Canada | 59 | 0.4% |
| Reality | 55 | 0.4% |
| En Español | 44 | 0.3% |
| Family | 34 | 0.3% |
| Drama | 33 | 0.2% |
| Online TV | 32 | 0.2% |
| Home + Food | 30 | 0.2% |
| Daytime + Game Shows | 29 | 0.2% |
| UK | 29 | 0.2% |
| Auto | 27 | 0.2% |
| Weather | 21 | 0.2% |
| True Crime | 20 | 0.1% |
| Sci-Fi | 19 | 0.1% |
| Australia | 16 | 0.1% |
| Anime | 15 | 0.1% |
| DLTV | 15 | 0.1% |
| Aria Web Channels | 14 | 0.1% |
| Westerns | 14 | 0.1% |
| Animals & Nature | 13 | 0.1% |
| Public TV | 13 | 0.1% |
| Global TV | 12 | 0.1% |
| Animals + Nature | 11 | 0.1% |
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
| Paranormal | 1 | 0.0% |
| Shopping | 1 | 0.0% |
| Other | 677 | 5.0% |

## Country playlists (`playlists/countries/` — 176 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 3265 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1641 | [`countries/International.m3u`](countries/International.m3u) |
| India | 860 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 535 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 453 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Germany | 374 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| France | 272 | [`countries/France.m3u`](countries/France.m3u) |
| Sweden | 272 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| UK | 269 | [`countries/UK.m3u`](countries/UK.m3u) |
| Dominican Republic | 217 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Spain | 204 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| Poland | 202 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Canada | 201 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Chile | 186 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Romania | 183 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Brazil | 170 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Argentina | 168 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Ukraine | 168 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Netherlands | 160 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Turkey | 159 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Peru | 150 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Hungary | 148 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| Mexico | 128 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Colombia | 118 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| Indonesia | 110 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| _…and 151 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 116 / 152 unique links (dead: 5, unverified: 31)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | reachable | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | failed | - | 0 | not_imported | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. — GET https://api.github.com/repos/gookie-dev/StepDaddyLiveHD failed: HTTP Error 404: Not Found |
| dlive.sx | failed | - | 0 | not_imported | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. — GET https://dlive.sx/24-7-channels.php failed: <urlopen error [Errno -2] Name or service not known> |
| xyzstreams | reachable | - | 0 | not_imported | Live-event index (soccer, NFL, NBA and more) whose schedules the site renders in the viewer's own time zone and whose streams are resolved by JavaScript inside its player pages, so it publishes no static playlist. Checked for reachability only and never imported as channels; its backup index is https://xyzstreams.space/alt.html. Configure XYZSTREAMS_M3U_URL only if you have an authorized direct playlist. |
| ppv.st | reachable | - | 0 | not_imported | Live-event directory (NFL, college football, basketball, soccer, PPV cards) that lists its fixtures and countdowns but serves no static M3U; the page itself now points readers to https://mirrors.st/ for its current address. Checked for reachability only, never imported. Configure PPVST_M3U_URL only if you have an authorized direct playlist. |
| Easy-Web-TV-M3u8 | reachable | - | 0 | no_static_playlist | zhangboheng's all-in-one web TV catalogue. Its country pages are generated in the browser from the iptv-org public API (which this repository already reads through the iptv-org source), and the repository tree publishes no .m3u file at all, so there is nothing to import. This check counts the playlists it carries so a future static export is noticed. |
| iptvcat | reachable | - | 0 | not_imported | IPTV Cat's US catalogue (1,621 channels, 1,593 online on 2026-11-24; 14,018 worldwide). Each row offers only a single-channel wrapper playlist (list.iptvcat.net/my_list/s/<hash>.m3u8 around the real stream URL) and the bulk 'Download this list' action is built in the browser from a session list, so the site publishes no single static M3U the scraper can fetch and link-check as a source. Sampled wrapper URLs (e.g. the 30A TV feeds) are already in the published corpus, and the catalogue is smaller than the current lineup in both the US (1,621 vs ~2,900) and worldwide (14,018 vs 19,621). Checked for reachability only and never imported as channels; see docs/SOURCE-HUNT-2026-11-24.md. If IPTV Cat ever publishes a static bulk M3U, add it as a source and let the daily link check decide what survives. |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| TimeoutError | 0 | 1441 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 403 | 0 | 1426 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 404 | 1250 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 401 | 0 | 686 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| gaierror | 0 | 497 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 386 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| ConnectionRefusedError | 0 | 261 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 146 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 109 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 400 | 90 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLError | 0 | 66 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 503 | 0 | 52 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 44 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 32 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 30 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| RemoteDisconnected | 0 | 25 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-24T17:46:53Z) | 25 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| OSError | 0 | 24 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 504 | 0 | 21 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: playlist only, HTTP 400 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 19 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 502 | 0 | 18 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| empty response | 15 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| HTTP 500 | 0 | 14 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: variant HTTP 403 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 14 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme rtmp | 0 | 13 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 13 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 11 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 10 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 451 | 9 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 429 | 0 | 8 | The host rate-limited the check; this scraper now limits parallel requests per host and retries with Retry-After/backoff. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 511 | 0 | 7 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| invalid URL | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-11-24T17:46:53Z) | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 444 | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 530 | 0 | 6 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-24T17:46:53Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-24T17:46:53Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-24T17:46:53Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 521 | 0 | 4 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-23T18:06:21Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-24T17:46:53Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-23T18:06:21Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, dns lookup failed (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 407 | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 2 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 523 | 0 | 2 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme rtsp | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-24T17:46:53Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 401 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-11-23T18:06:21Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-24T17:46:53Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 302 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 406 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 408 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 400 (failed the deep check 2x, last 2026-11-23T18:06:21Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-24T17:46:53Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: connection refused (failed the deep check 2x, last 2026-11-23T18:06:21Z) | 1 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: dash manifest has no representations (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dash manifest has no representations (failed the deep check 2x, last 2026-11-24T17:46:53Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: empty response (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 400 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 401 (failed the deep check 1x, last 2026-11-24T17:46:53Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 416 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, empty segment (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, segment too small (214 bytes) (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 403 (failed the deep check 2x, last 2026-11-23T18:06:21Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 410 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 422 (failed the deep check 2x, last 2026-11-24T17:46:53Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |

### Run/source issues

- Reference check 'StepDaddyLiveHD' failed: GET https://api.github.com/repos/gookie-dev/StepDaddyLiveHD failed: HTTP Error 404: Not Found
- Reference check 'dlive.sx' failed: GET https://dlive.sx/24-7-channels.php failed: <urlopen error [Errno -2] Name or service not known>
- 4586 links could not be confirmed after retries (see unverified details).
- 2355 links returned a confirmed failure (see dead details).
- This run started +7h 48m after its scheduled time (2026-11-24T17:53:00Z); GitHub's scheduler delayed it. The schedule guard (.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots.
