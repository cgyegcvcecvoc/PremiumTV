# Scraper status

- **Last run:** 2026-11-25 08:40 AM EST (2026-11-25 13:40 UTC)
- **Run:** _manual re-scrape (run-scrape.txt)_ (`manual`; ID `20261125T133511Z-2992`)
- **Outcome:** **WARNING**
- **Confirmed working:** 13249 / 20397 unique links
- **Dead:** 2276  |  **Unverified:** 4872
- **Retained (unverified, within grace):** 834 previously published links kept so their channels do not vanish after one unverifiable run
- **Unique links found:** 20397 from 29697 source entries
- **Changes vs. PremiumTV_all.m3u:** +0 added / -0 removed
- **Player playlist updated:** yes
- **Country playlists:** [`countries/`](countries/README.md) (177 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (120 confirmed working / 156 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Published categories

The order below is the order of the groups in `PremiumTV.m3u`. Every category is
followed by its own Backups group; see [`checks/CATEGORIES.md`](checks/CATEGORIES.md)
for the full audit.

| # | Category | Channels |
|---|---|---:|
| 1 | Sports | 677 |
| 2 | Lifestyle | 517 |
| 3 | Fox Channels | 36 |
| 4 | CBS | 70 |
| 5 | NBC | 67 |
| 6 | NBC Sports Channels | 5 |
| 7 | Cartoons | 202 |
| 8 | PBS | 24 |
| 9 | Game Shows | 20 |
| 10 | International | 2198 |
| 11 | News | 1073 |
| 12 | Movies | 997 |
| 13 | Music | 913 |
| 14 | Entertainment | 844 |
| 15 | Religious | 666 |
| 16 | Series | 528 |
| 17 | United States | 509 |
| 18 | Europe | 437 |
| 19 | Kids | 425 |
| 20 | Documentary | 390 |
| 21 | Asia | 301 |
| 22 | India | 276 |
| 23 | South America | 253 |
| 24 | Comedy | 196 |
| 25 | North America | 167 |
| 26 | Education | 141 |
| 27 | Culture | 132 |
| 28 | Legislative | 115 |
| 29 | A&E Networks | 100 |
| 30 | Classic TV | 82 |
| 31 | Business | 78 |
| 32 | Canada | 64 |
| 33 | Reality | 55 |
| 34 | Andalucía | 52 |
| 35 | En Español | 44 |
| 36 | Drama | 33 |
| 37 | Family | 32 |
| 38 | Eventuales | 31 |
| 39 | United Kingdom | 31 |
| 40 | Home + Food | 30 |
| 41 | Online TV | 30 |
| 42 | Daytime + Game Shows | 29 |
| 43 | Musicales | 28 |
| 44 | Africa | 27 |
| 45 | Auto | 27 |
| 46 | UK | 21 |
| 47 | Weather | 21 |
| 48 | True Crime | 20 |
| 49 | Int. América | 19 |
| 50 | Int. Europa | 19 |
| 51 | Sci-Fi | 19 |
| 52 | Australia | 18 |
| 53 | Canarias | 18 |
| 54 | Cataluña | 18 |
| 55 | C. Valenciana | 17 |
| 56 | Anime | 16 |
| 57 | Galicia | 16 |
| 58 | DLTV | 15 |
| 59 | Aria Web Channels | 14 |
| 60 | Public TV | 14 |
| 61 | Westerns | 14 |
| 62 | Animals & Nature | 13 |
| 63 | Global TV | 12 |
| 64 | Animals + Nature | 11 |
| 65 | Int. Otros | 11 |
| 66 | Competition Reality | 10 |
| 67 | Tv Paranormal | 10 |
| 68 | C. de Madrid | 9 |
| 69 | Deportivos | 9 |
| 70 | Int. Asia | 9 |
| 71 | País Vasco | 9 |
| 72 | Religiosos | 9 |
| 73 | Tv Celebrities | 9 |
| 74 | Castilla-La Mancha | 7 |
| 75 | Infantiles | 7 |
| 76 | Int. África | 7 |
| 77 | Tv Reality | 7 |
| 78 | Generalistas | 6 |
| 79 | Informativos | 6 |
| 80 | Relax | 6 |
| 81 | Season's Greetings | 6 |
| 82 | Castilla y León | 5 |
| 83 | R. de Murcia | 5 |
| 84 | Tv Shows | 5 |
| 85 | C. Foral de Navarra | 4 |
| 86 | Cantabria | 4 |
| 87 | Extremadura | 3 |
| 88 | Bonaire | 2 |
| 89 | Illes Balears | 2 |
| 90 | Democratic Republic of the Congo | 1 |
| 91 | Halloween Hits | 1 |
| 92 | La Rioja | 1 |
| 93 | Local TV | 1 |
| 94 | Oceania | 1 |
| 95 | Paranormal | 1 |
| 96 | Other | 643 |

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 3 | 3 | 1 | 1 | 1 | 1 |
| priority-channels | ok | 13 | 13 | 11 | 13 | 0 | 0 |
| ae-networks | ok | 50 | 50 | 14 | 47 | 0 | 3 |
| curated-channels | ok | 1 | 1 | 0 | 1 | 0 | 0 |
| aria | ok | 234 | 223 | 223 | 153 | 16 | 54 |
| aria-plus | ok | 2039 | 1983 | 335 | 458 | 284 | 1241 |
| doms9 | ok | 478 | 478 | 90 | 162 | 22 | 294 |
| xtemus | ok | 317 | 317 | 0 | 31 | 108 | 178 |
| iptv-org | ok | 11497 | 11497 | 5598 | 8205 | 1228 | 2064 |
| free-tv | ok | 2203 | 2179 | 979 | 1243 | 451 | 485 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| pluto-us | ok | 458 | 458 | 0 | 0 | 0 | 458 |
| aria-overseas | ok | 42 | 42 | 24 | 40 | 1 | 1 |
| vbskycn-iptv | ok | 313 | 311 | 13 | 291 | 2 | 18 |
| m3upt | ok | 159 | 159 | 113 | 142 | 13 | 4 |
| tdtchannels | ok | 574 | 574 | 246 | 441 | 54 | 79 |
| nexonic-iptv | ok | 4458 | 4458 | 3998 | 4079 | 213 | 166 |
| VIP-m3u-playlist 🌱 | ok | 224 | 219 | 158 | 206 | 13 | 0 |
| israel-tv-plus 🌱 | ok | 353 | 350 | 149 | 265 | 6 | 79 |
| m3u 🌱 | ok | 853 | 848 | 179 | 684 | 79 | 84 |
| openstream 🌱 | ok | 5428 | 5428 | 3319 | 4925 | 428 | 75 |

**Group filters** (a source contributing only part of its file):

- `m3upt` kept 159 of 944 entries; dropped: PCNELID (216), Eixo do Mal (214), Beachcam (194), Rádios (85), IEGCQT (61), DRM test (6), O Planeta Vivo (6), 100 ou Mais (3).

🌱 = source added automatically by the monthly discovery engine: VIP-m3u-playlist, israel-tv-plus, m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Channel categories (published player playlists)

Every published channel is grouped into one fixed category (no more upstream `General`/`Undefined`/country groups), with US channels first inside each category and each channel's feeds side by side. Categories across **14083** channels:

| Category | Channels | Share |
|---|---:|---:|
| Sports | 677 | 4.8% |
| Lifestyle | 517 | 3.7% |
| Fox Channels | 36 | 0.3% |
| CBS | 70 | 0.5% |
| NBC | 67 | 0.5% |
| NBC Sports Channels | 5 | 0.0% |
| Cartoons | 202 | 1.4% |
| PBS | 24 | 0.2% |
| Game Shows | 20 | 0.1% |
| International | 2198 | 15.6% |
| News | 1073 | 7.6% |
| Movies | 997 | 7.1% |
| Music | 913 | 6.5% |
| Entertainment | 844 | 6.0% |
| Religious | 666 | 4.7% |
| Series | 528 | 3.7% |
| United States | 509 | 3.6% |
| Europe | 437 | 3.1% |
| Kids | 425 | 3.0% |
| Documentary | 390 | 2.8% |
| Asia | 301 | 2.1% |
| India | 276 | 2.0% |
| South America | 253 | 1.8% |
| Comedy | 196 | 1.4% |
| North America | 167 | 1.2% |
| Education | 141 | 1.0% |
| Culture | 132 | 0.9% |
| Legislative | 115 | 0.8% |
| A&E Networks | 100 | 0.7% |
| Classic TV | 82 | 0.6% |
| Business | 78 | 0.6% |
| Canada | 64 | 0.5% |
| Reality | 55 | 0.4% |
| Andalucía | 52 | 0.4% |
| En Español | 44 | 0.3% |
| Drama | 33 | 0.2% |
| Family | 32 | 0.2% |
| Eventuales | 31 | 0.2% |
| United Kingdom | 31 | 0.2% |
| Home + Food | 30 | 0.2% |
| Online TV | 30 | 0.2% |
| Daytime + Game Shows | 29 | 0.2% |
| Musicales | 28 | 0.2% |
| Africa | 27 | 0.2% |
| Auto | 27 | 0.2% |
| UK | 21 | 0.1% |
| Weather | 21 | 0.1% |
| True Crime | 20 | 0.1% |
| Int. América | 19 | 0.1% |
| Int. Europa | 19 | 0.1% |
| Sci-Fi | 19 | 0.1% |
| Australia | 18 | 0.1% |
| Canarias | 18 | 0.1% |
| Cataluña | 18 | 0.1% |
| C. Valenciana | 17 | 0.1% |
| Anime | 16 | 0.1% |
| Galicia | 16 | 0.1% |
| DLTV | 15 | 0.1% |
| Aria Web Channels | 14 | 0.1% |
| Public TV | 14 | 0.1% |
| Westerns | 14 | 0.1% |
| Animals & Nature | 13 | 0.1% |
| Global TV | 12 | 0.1% |
| Animals + Nature | 11 | 0.1% |
| Int. Otros | 11 | 0.1% |
| Competition Reality | 10 | 0.1% |
| Tv Paranormal | 10 | 0.1% |
| C. de Madrid | 9 | 0.1% |
| Deportivos | 9 | 0.1% |
| Int. Asia | 9 | 0.1% |
| País Vasco | 9 | 0.1% |
| Religiosos | 9 | 0.1% |
| Tv Celebrities | 9 | 0.1% |
| Castilla-La Mancha | 7 | 0.0% |
| Infantiles | 7 | 0.0% |
| Int. África | 7 | 0.0% |
| Tv Reality | 7 | 0.0% |
| Generalistas | 6 | 0.0% |
| Informativos | 6 | 0.0% |
| Relax | 6 | 0.0% |
| Season's Greetings | 6 | 0.0% |
| Castilla y León | 5 | 0.0% |
| R. de Murcia | 5 | 0.0% |
| Tv Shows | 5 | 0.0% |
| C. Foral de Navarra | 4 | 0.0% |
| Cantabria | 4 | 0.0% |
| Extremadura | 3 | 0.0% |
| Bonaire | 2 | 0.0% |
| Illes Balears | 2 | 0.0% |
| Democratic Republic of the Congo | 1 | 0.0% |
| Halloween Hits | 1 | 0.0% |
| La Rioja | 1 | 0.0% |
| Local TV | 1 | 0.0% |
| Oceania | 1 | 0.0% |
| Paranormal | 1 | 0.0% |
| Other | 643 | 4.6% |

## Country playlists (`playlists/countries/` — 177 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 3279 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 1820 | [`countries/International.m3u`](countries/International.m3u) |
| India | 1036 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 547 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 486 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| Germany | 376 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| France | 293 | [`countries/France.m3u`](countries/France.m3u) |
| UK | 280 | [`countries/UK.m3u`](countries/UK.m3u) |
| Sweden | 272 | [`countries/Sweden.m3u`](countries/Sweden.m3u) |
| Spain | 232 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| Dominican Republic | 221 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Poland | 201 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Canada | 197 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Chile | 193 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Brazil | 191 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Romania | 186 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Ukraine | 172 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Argentina | 171 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Peru | 166 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Netherlands | 164 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Turkey | 163 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Hungary | 144 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| Mexico | 136 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Colombia | 126 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| Indonesia | 114 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| _…and 152 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 120 / 156 unique links (dead: 5, unverified: 31)

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
| gradetv | reachable | - | 0 | not_imported | Grade TV (iptv-org Providers discussion #769) is a browser catalogue and M3U exporter over the iptv-org channel data - its ids are iptv-org ids such as 00sReplay.us and 3ABNEnglish.us - so it duplicates the iptv-org source already configured. Checked for reachability only and never imported. |
| broadcast-atlas | reachable | - | 0 | not_imported | Broadcast Atlas (iptv-org Providers discussion #845) is a directory and player built on iptv-org's channel data, with each channel keeping its iptv-org identifier; it publishes no playlist of its own, so importing it would only re-fetch the iptv-org source. Checked for reachability only and never imported as channels. |
| open-tv-atlas | reachable | - | 0 | not_imported | Open TV Atlas (iptv-org Providers discussion #968) generates M3U URLs by combining iptv-org language, category and quality slices, so every link it can produce already arrives through the configured iptv-org source. Checked for reachability only and never imported as channels. |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 403 | 0 | 1526 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| TimeoutError | 0 | 1333 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 404 | 1248 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 401 | 0 | 685 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| gaierror | 0 | 501 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| ConnectionRefusedError | 0 | 272 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 248 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| HTTP 429 | 0 | 163 | The host rate-limited the check; this scraper now limits parallel requests per host and retries with Retry-After/backoff. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 147 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| OSError | 0 | 122 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 400 | 111 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 109 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLError | 0 | 68 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 503 | 0 | 54 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 40 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 36 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 458 | 35 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 30 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| RemoteDisconnected | 0 | 29 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-24T17:46:53Z) | 28 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 502 | 0 | 27 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 504 | 0 | 22 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: playlist only, HTTP 400 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 19 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 500 | 0 | 17 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 530 | 0 | 15 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| empty response | 15 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| quarantined: variant HTTP 403 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 14 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme rtmp | 0 | 13 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 13 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 12 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-22T14:39:03Z) | 11 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 451 | 10 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP dns lookup failed (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 10 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| invalid URL | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 2x, last 2026-11-24T17:46:53Z) | 7 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| ConnectionResetError | 0 | 6 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 444 | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-24T17:46:53Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-24T17:46:53Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-24T17:46:53Z) | 6 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 511 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: HTTP 404 (failed the deep check 2x, last 2026-11-23T18:06:21Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-24T17:46:53Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 2x, last 2026-11-23T18:06:21Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, dns lookup failed (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 4 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 521 | 0 | 3 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| quarantined: connection refused (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 3 | 0 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| quarantined: playlist only, HTTP 403 (failed the deep check 1x, last 2026-11-22T14:39:03Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: playlist only, HTTP 404 (failed the deep check 1x, last 2026-11-18T15:41:24Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: variant HTTP 400 (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 2 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| not probed: unsupported scheme rtsp | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: dns lookup failed (failed the deep check 1x, last 2026-11-24T17:46:53Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 1x, last 2026-11-23T18:06:21Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-11-18T15:41:24Z) | 2 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
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
| HTTP 499 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 523 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
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
| quarantined: html page, not a stream (failed the deep check 2x, last 2026-11-23T18:06:21Z) | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
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
- 4872 links could not be confirmed after retries (see unverified details).
- 2276 links returned a confirmed failure (see dead details).
