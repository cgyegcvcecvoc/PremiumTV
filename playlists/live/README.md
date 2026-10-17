# `playlists/live/` — the USA feed current app builds refresh from

`USA.m3u` here is the playlist **PremiumTV 1.0.5 and newer** download when it
refreshes. It is published by `scripts/legacy_sunset.py`, which every playlist
workflow runs after the scrape and before the `categories/` shelf is built.

## Why this directory exists

An installed app can only be pointed at one URL, baked into its bundle at build
time:

| Feed | Path | Who reads it |
|---|---|---|
| **Live** | `playlists/live/USA.m3u` | PremiumTV 1.0.5+, the `categories/` shelf, the download site |
| **Legacy** | `playlists/countries/USA.m3u` | PremiumTV 1.0.0–1.0.4 only |

`raw.githubusercontent.com` serves the same bytes to every caller and cannot
look at a version, so the only way to stop feeding one set of builds is to give
the others a different address. While support lasts the two files are identical.
On the end-of-support date published in `app-update-notice.json` the legacy feed
is **pinned**: it keeps the channels that worked that day, gains one sanctioned
notice entry telling those builds to go and get the newest release from GitHub,
and stops receiving scrape updates. This file carries on.

## The notice entry

The pinned legacy feed's first entry is marked `tvg-notice="app-update"`. Both
apps' M3U parsers (`android/.../data/M3uParser.kt`, `macos/app/src/main/parsers.js`)
drop an entry carrying that marker, so it can never reach a channel list, a
category, the shelf or the download site. Only builds too old to know the marker
render it — which is exactly who it is for: 1.0.0–1.0.3 ship no updater and no
popup, so a row in the channel list they already download is the only in-app
message that can reach them.

Its URL is the GitHub releases page rather than a stream. Selecting it in an old
build fails to play, which is honest: the row is a notice, not a channel, and its
name is the message.

## Do not edit these files by hand

`python scripts/legacy_sunset.py check` fails a publishing run when the legacy
feed no longer matches its pin, when the live feed carries a notice entry, or
when the sunset date has passed and nothing was pinned. Use:

```bash
python scripts/legacy_sunset.py status   # which phase, how many days left
python scripts/legacy_sunset.py apply    # mirror, then pin when the date passes
```

See `docs/UPDATES.md` for the whole update and end-of-support policy.
