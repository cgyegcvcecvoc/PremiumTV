# PremiumTV1
Premium ACCESS TV CHANNELS

FEEL FREE TO Contribute--> Place In Issues If you want a specific channel, and I'll try to add it

---

## Playlist

Load this URL in any IPTV player (VLC, TiviMate, IPTV Smarters, Kodi PVR IPTV Simple, etc.):

```
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/PremiumTV.m3u
```

| File | What it is |
|---|---|
| [`playlists/PremiumTV.m3u`](playlists/PremiumTV.m3u) | Merged playlist, **working links only** (use this one) |
| [`playlists/PremiumTV_all.m3u`](playlists/PremiumTV_all.m3u) | Every link found, not filtered |
| [`playlists/STATUS.md`](playlists/STATUS.md) | Results of the last run (counts per source and per group) |
| [`playlists/report.json`](playlists/report.json) | Same, machine-readable, including the dead links and why they failed |
| `playlists/sources/*.m3u` | Raw copy of each source, used as a backup if a source is down |

## Automatic updates

A GitHub Action ([`.github/workflows/scrape.yml`](.github/workflows/scrape.yml)) runs the scraper
**three times a day, New York time** (EDT in summer, EST in winter; daylight saving is handled automatically):

| Time | Run |
|---|---|
| 3:00 AM | Daily scrape |
| 6:00 AM | Recheck (3 hours later) |
| 4:15 PM | Final daily check |

Every run does the same job:
1. Downloads every source in [`sources.json`](sources.json)
2. Merges them into one list and removes duplicate links
3. Tests every link the way a player would (with the same User-Agent/Referer headers) and drops dead ones
4. Commits the updated playlists back to the repo

You can also run it any time from **Actions → Scrape playlists → Run workflow**.

> GitHub may start scheduled runs a few minutes late when it's busy. Scheduled workflows only run from the
> default branch (`main`).

## Sources

Configured in [`sources.json`](sources.json):

| Name | Format | URL |
|---|---|---|
| aria | M3U | https://github.com/aria-tv/aria/blob/main/aria.m3u |
| doms9 | M3U8 | https://github.com/doms9/iptv/blob/default/M3U8/TV.m3u8 |
| xtemus | W3U (Wiseplay JSON) | https://xtemus.com/ → `playlist.xtemus.com` XTEMUS TV list |

To add a source, add an entry with `name`, `type` (`m3u` or `w3u`) and `url`. For W3U lists you can
choose which groups to follow with `include_groups` / `exclude_groups` and `max_depth`.
By default the xtemus movie, series, radio and highlight folders are skipped, so only live TV is pulled.

## Run it locally

Needs Python 3.9 or newer. There's nothing to install.

```bash
python scripts/scraper.py                 # scrape + check links
python scripts/scraper.py --no-check      # scrape and merge only
python scripts/scraper.py --help          # all options (timeout, workers, ...)
```

## Disclaimer

This repo doesn't host any video. It only collects links that other people have already published.
Whether a stream is authorized depends on who runs it and where you are, so it's up to you to make
sure you have the right to watch what you open.
