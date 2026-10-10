# Repository cleanup

- **Run:** biweekly deep cleanup (`20261010T123533Z-715`)
- **Started:** 2026-10-10T12:35:33Z | **Finished:** 2026-10-10T12:35:33Z | **Duration:** 0.12s
- **Outcome:** **NEEDS ATTENTION**
- **Space freed:** 3715 KB
- **Append-only logs trimmed:** 4 file(s), 112 run block(s) dropped (budget: the last 30 runs and 2500 lines per file)
- **Files removed: 2** (orphaned guides, swap files, caches)
- **Problems left for a maintainer:** 3

The biweekly run does the deep, slow sweep: `link_check.py --archives` re-tests and prunes the playlists no daily run patches (the priority playlist, the per-category playlists, the `categories/` shelf and the local source copies), then this report covers the repository itself. Removing dead channels stays `link_check.py`'s job; this tool never edits a playlist entry.

## Logs

| Log | Lines | Run blocks | Dropped | Size before | Size after |
|---|---:|---:|---:|---:|---:|
| `link-check-edits.txt` | 9710 | 20 | 13 | 1102 KB | 284 KB |
| `epg-check-edits.txt` | 13176 | 20 | 13 | 1376 KB | 22 KB |
| `epg-build-edits.txt` | 886 | 72 | 42 | 107 KB | 5 KB |
| `log-edits.txt` | 5192 | 74 | 44 | 563 KB | 251 KB |

## Guide currency

- Merged guide `EPG/PremiumTV.xml`: 10 MB, 187 channel(s) with a listing in the live window - current
- Quarantine: 1389 read, 1389 kept, 0 expired or malformed dropped

## Empty playlists

- `playlists/countries/Bermuda.m3u` holds no channel
- `playlists/countries/Macau.m3u` holds no channel
- `playlists/countries/San_Marino.m3u` holds no channel

## Removed

- `scripts/__pycache__`
- `tests/__pycache__`

## Needs a maintainer

- playlists/countries/Bermuda.m3u is published but holds no channel
- playlists/countries/Macau.m3u is published but holds no channel
- playlists/countries/San_Marino.m3u is published but holds no channel
