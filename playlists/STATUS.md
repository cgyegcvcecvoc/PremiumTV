# Scraper status

- **Last run:** 2026-09-29 04:26 PM EDT (2026-09-29 20:26 UTC)
- **Run:** _probe_ (`manual`; ID `20260929T200731Z-2331`)
- **Outcome:** **WARNING**
- **Confirmed working:** 9449 / 13389 unique links
- **Dead:** 1382  |  **Unverified:** 2558
- **Unique links found:** 13389 from 14304 source entries
- **Changes vs. PremiumTV_all.m3u:** +284 added / -211 removed
- **Player playlist updated:** yes
- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)

## Playlist sources

| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |
|---|---|---:|---:|---:|---:|---:|---:|
| aria | ok | 407 | 401 | 121 | 323 | 8 | 70 |
| doms9 | ok | 506 | 504 | 63 | 286 | 37 | 181 |
| xtemus | ok | 317 | 317 | 0 | 32 | 214 | 71 |
| iptv-org | ok | 10994 | 10994 | 835 | 8239 | 848 | 1907 |
| free-tv | ok | 2080 | 2054 | 711 | 1306 | 308 | 440 |
| eja-tv-feed | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |
| stepdaddylivehd-instance | not_configured | 0 | 0 | 0 | 0 | 0 | 0 |

## Reference-source checks (not automatically imported)

| Reference | Check | Playlist files | Note |
|---|---|---:|---|
| eja.tv | reachable | 0 | The site is checked for reachability only. No static M3U export was verified; it is not scraped/imported as channels. Configure EJA_M3U_URL only if you have an authorized direct playlist URL. |
| StepDaddyLiveHD | reachable | 0 | Repository tree is checked for static M3U files. The project describes a self-hosted proxy whose playlist is generated at an instance URL; configure STEPDADDYLIVEHD_PLAYLIST_URL to check a hosted instance. (repository is archived) |

## Diagnostics

| Result | Dead | Unverified | What to check next |
|---|---:|---:|---|
| HTTP 403 | 0 | 1140 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| HTTP 404 | 920 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| TimeoutError | 0 | 736 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| html page, not a stream | 380 | 0 | The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect. |
| gaierror | 0 | 294 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| ConnectionRefusedError | 0 | 94 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 503 | 0 | 49 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 400 | 46 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 429 | 0 | 43 | The host rate-limited the check; this scraper now limits parallel requests per host and retries with Retry-After/backoff. |
| HTTP 401 | 0 | 33 | Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region. |
| RemoteDisconnected | 0 | 27 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLError | 0 | 23 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 502 | 0 | 22 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 504 | 0 | 19 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| empty response | 14 | 0 | The server returned no stream data; check whether the source requires an active session or has expired. |
| HTTP 500 | 0 | 12 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| OSError | 0 | 12 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| SSLEOFError | 0 | 12 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 451 | 8 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme rtmp | 0 | 8 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| HTTP 530 | 0 | 6 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| ConnectionResetError | 0 | 5 | Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network. |
| HTTP 406 | 5 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 567 | 0 | 5 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 458 | 3 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 521 | 0 | 3 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 408 | 0 | 2 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 523 | 0 | 2 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| checker error: IncompleteRead | 0 | 2 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| checker error: UnicodeEncodeError | 0 | 2 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme mmsh | 0 | 2 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| HTTP 302 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 409 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 410 | 1 | 0 | The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one. |
| HTTP 421 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 477 | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| HTTP 511 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| HTTP 574 | 0 | 1 | The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link. |
| checker error: InvalidURL | 0 | 1 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| invalid URL | 1 | 0 | Inspect the channel URL and source entry in report.json; this result was not confirmed as playable. |
| not probed: unsupported scheme rtsp | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |
| not probed: unsupported scheme srt | 0 | 1 | This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working. |

### Run/source issues

- [xtemus] nested group 'Youtube Music' fetch failed: Expecting property name enclosed in double quotes: line 8 column 1 (char 239)
- 2558 links could not be confirmed after retries (see unverified details).
- 1382 links returned a confirmed failure (see dead details).
