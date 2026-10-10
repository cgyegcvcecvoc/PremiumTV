# Repository cleanup

- **Run:** post-scrape verification (`20261010T122448Z-510`)
- **Started:** 2026-10-10T12:24:48Z | **Finished:** 2026-10-10T12:24:48Z | **Duration:** 0.09s
- **Outcome:** **CLEAN** (report only - pass `--apply` to change files)
- **Space this run would free:** 2545 KB
- **Append-only logs trimmed:** 4 file(s), 108 run block(s) dropped (budget: the last 30 runs and 2500 lines per file)
- **Files to remove: 2** (orphaned guides, swap files, caches)
- **Problems left for a maintainer:** 0

The biweekly run does the deep, slow sweep: `link_check.py --archives` re-tests and prunes the playlists no daily run patches (the priority playlist, the per-category playlists, the `categories/` shelf and the local source copies), then this report covers the repository itself. Removing dead channels stays `link_check.py`'s job; this tool never edits a playlist entry.

## Logs

*Nothing was written by this run - the last column below is the size `--apply` would leave.*

| Log | Lines | Run blocks | Dropped | Size before | Size after |
|---|---:|---:|---:|---:|---:|
| `link-check-edits.txt` | 8157 | 19 | 10 | 909 KB | 132 KB |
| `epg-check-edits.txt` | 13174 | 19 | 13 | 1376 KB | 22 KB |
| `epg-build-edits.txt` | 883 | 71 | 41 | 107 KB | 5 KB |
| `log-edits.txt` | 5192 | 74 | 44 | 563 KB | 251 KB |

## Guide currency

- Merged guide `EPG/PremiumTV.xml`: 10 MB, 188 channel(s) with a listing in the live window - current
- Quarantine: 560 read, 560 kept, 0 expired or malformed dropped

## Removed

- `scripts/__pycache__`
- `tests/__pycache__`

Nothing needs a maintainer: every artifact is current and no orphan was found.
