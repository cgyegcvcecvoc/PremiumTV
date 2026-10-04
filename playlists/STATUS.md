# Scraper status

- **Last run:** 2026-10-04 12:38 PM EDT (2026-10-04 16:38 UTC)
- **Run:** _manual source rescrape; checks blocked by network_ (`manual`; ID `20261004T163805Z-3222`)
- **Outcome:** **WARNING**
- **Link check:** not completed in this run; the existing player playlist was left untouched.
- **All-links entries:** 16686 (not checked)
- **Unique links found:** 16686 from 21018 source entries
- **Changes vs. PremiumTV_all.m3u:** +0 added / -0 removed
- **Player playlist updated:** no (previous good copy preserved or no output)
- **Country playlists:** [`countries/`](countries/README.md) (173 countries separated)
- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) (0 confirmed working / 71 unique A&E links)
- **Plain-text (.txt) logs:** [`logs/scrape-log.txt`](logs/scrape-log.txt) | [`logs/log-edits.txt`](logs/log-edits.txt) | [`logs/errors.txt`](logs/errors.txt) | [`logs/run-history.txt`](logs/run-history.txt)
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| local-channels | ok | 4 | 4 | 3 | 0 | 0 | 0 |
| priority-channels | ok | 9 | 9 | 8 | 0 | 0 | 0 |
| ae-networks | ok | 53 | 53 | 17 | 0 | 0 | 0 |
| aria | ok | 366 | 361 | 120 | 0 | 0 | 0 |
| doms9 | ok | 718 | 704 | 69 | 0 | 0 | 0 |
| xtemus | from_cache | 317 | 317 | 0 | 0 | 0 | 0 |
| iptv-org | from_cache | 11138 | 11138 | 3687 | 0 | 0 | 0 |
| free-tv | ok | 2080 | 2054 | 833 | 0 | 0 | 0 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| dlive-sx-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| m3u 🌱 | from_cache | 831 | 827 | 174 | 0 | 0 | 0 |
| openstream 🌱 | ok | 5502 | 5502 | 3222 | 0 | 0 | 0 |

🌱 = source added automatically by the monthly discovery engine: m3u, openstream. Set `"enabled": false` for it in `discovery/approved-sources.json` to roll it back.

## Country playlists (`playlists/countries/` — 173 countries)

All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). Top 25 countries by working channel count:

| Country | Working channels | Playlist |
|---|---:|---|
| USA | 2102 | [`countries/USA.m3u`](countries/USA.m3u) |
| International | 964 | [`countries/International.m3u`](countries/International.m3u) |
| India | 706 | [`countries/India.m3u`](countries/India.m3u) |
| Italy | 489 | [`countries/Italy.m3u`](countries/Italy.m3u) |
| Russia | 405 | [`countries/Russia.m3u`](countries/Russia.m3u) |
| UK | 221 | [`countries/UK.m3u`](countries/UK.m3u) |
| Dominican Republic | 196 | [`countries/Dominican_Republic.m3u`](countries/Dominican_Republic.m3u) |
| Spain | 193 | [`countries/Spain.m3u`](countries/Spain.m3u) |
| France | 192 | [`countries/France.m3u`](countries/France.m3u) |
| Brazil | 185 | [`countries/Brazil.m3u`](countries/Brazil.m3u) |
| Chile | 175 | [`countries/Chile.m3u`](countries/Chile.m3u) |
| Germany | 172 | [`countries/Germany.m3u`](countries/Germany.m3u) |
| Ukraine | 170 | [`countries/Ukraine.m3u`](countries/Ukraine.m3u) |
| Argentina | 156 | [`countries/Argentina.m3u`](countries/Argentina.m3u) |
| Peru | 148 | [`countries/Peru.m3u`](countries/Peru.m3u) |
| Netherlands | 136 | [`countries/Netherlands.m3u`](countries/Netherlands.m3u) |
| Turkey | 135 | [`countries/Turkey.m3u`](countries/Turkey.m3u) |
| Canada | 130 | [`countries/Canada.m3u`](countries/Canada.m3u) |
| Mexico | 125 | [`countries/Mexico.m3u`](countries/Mexico.m3u) |
| Poland | 118 | [`countries/Poland.m3u`](countries/Poland.m3u) |
| Romania | 117 | [`countries/Romania.m3u`](countries/Romania.m3u) |
| Indonesia | 108 | [`countries/Indonesia.m3u`](countries/Indonesia.m3u) |
| Hungary | 105 | [`countries/Hungary.m3u`](countries/Hungary.m3u) |
| Colombia | 100 | [`countries/Colombia.m3u`](countries/Colombia.m3u) |
| Greece | 85 | [`countries/Greece.m3u`](countries/Greece.m3u) |
| _…and 148 more countries_ | | [Full country index](countries/README.md) |

## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)

- **Confirmed working:** 0 / 71 unique links (dead: 0, unverified: 0)

## Reference-source checks (not automatically imported)

| Reference | Check | Channels seen | Playlist links | Ingest status | Note |
|---|---|---:|---:|---|---|
| eja.tv | failed | - | 0 | not_imported | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. — GET https://eja.tv/ failed: <urlopen error TLS/SSL connection has been closed (EOF) (_ssl.c:992)> |
| StepDaddyLiveHD | reachable | - | 0 | no_static_playlist | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. (repository is archived) |
| dlive.sx | failed | - | 0 | not_imported | DaddyLiveHD 24/7 channel index. The page lists channels as HTML player pages (/stream/stream-<id>.php) whose stream address is resolved by JavaScript at run time, and its channels/schedule API needs a key issued by the operator, so the site publishes no static playlist. The catalogue is counted for visibility only and no channel is imported. Set DLIVE_M3U_URL to an authorized direct playlist URL - for example one generated by a self-hosted proxy - to import it and have every link checked like any other source. — GET https://dlive.sx/24-7-channels.php failed: <urlopen error TLS/SSL connection has been closed (EOF) (_ssl.c:992)> |

## Diagnostics

No completed link-check results were recorded for this run.

### Run/source issues

- Reference check 'eja.tv' failed: GET https://eja.tv/ failed: <urlopen error TLS/SSL connection has been closed (EOF) (_ssl.c:992)>
- Reference check 'dlive.sx' failed: GET https://dlive.sx/24-7-channels.php failed: <urlopen error TLS/SSL connection has been closed (EOF) (_ssl.c:992)>
- [aria] Direct URL fetch failed; GitHub API fallback succeeded: GET https://raw.githubusercontent.com/aria-tv/aria/main/aria.m3u failed: <urlopen error TLS/SSL connection has been closed (EOF) (_ssl.c:992)>
- [doms9] Direct URL fetch failed; GitHub API fallback succeeded: GET https://raw.githubusercontent.com/doms9/iptv/default/M3U8/TV.m3u8 failed: <urlopen error TLS/SSL connection has been closed (EOF) (_ssl.c:992)>
- [xtemus] fetch/parse failed: GET https://playlist.xtemus.com/?playlist=t256y454t41554 failed: <urlopen error TLS/SSL connection has been closed (EOF) (_ssl.c:992)>
- [iptv-org] fetch/parse failed: GET https://iptv-org.github.io/iptv/index.m3u failed: <urlopen error TLS/SSL connection has been closed (EOF) (_ssl.c:992)>
- [free-tv] Direct URL fetch failed; GitHub API fallback succeeded: GET https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8 failed: <urlopen error TLS/SSL connection has been closed (EOF) (_ssl.c:992)>
- [m3u] fetch/parse failed: GET https://api.github.com/repos/iprtl/m3u/contents/Pluto.m3u?ref=main failed: HTTP Error 404: Not Found
- [openstream] Direct URL fetch failed; GitHub API fallback succeeded: GET https://raw.githubusercontent.com/SajadTroy/openstream/main/index.m3u failed: <urlopen error TLS/SSL connection has been closed (EOF) (_ssl.c:992)>
