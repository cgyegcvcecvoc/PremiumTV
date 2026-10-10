# Repository cleanup

- **Run:** repository cleanup (`20261010T120739Z-958`)
- **Started:** 2026-10-10T12:07:39Z | **Finished:** 2026-10-10T12:07:40Z | **Duration:** 0.29s
- **Outcome:** **NEEDS ATTENTION** (report only - pass `--apply` to change files)
- **Space this run would free:** 2536 KB
- **Append-only logs trimmed:** 4 file(s), 106 run block(s) dropped (budget: the last 30 runs and 2500 lines per file)
- **Files to remove: 2** (orphaned guides, swap files, caches)
- **Problems left for a maintainer:** 1

The biweekly run does the deep, slow sweep: `link_check.py --archives` re-tests and prunes the playlists no daily run patches (the priority playlist, the per-category playlists, the `categories/` shelf and the local source copies), then this report covers the repository itself. Removing dead channels stays `link_check.py`'s job; this tool never edits a playlist entry.

## Logs

*Nothing was written by this run - the last column below is the size `--apply` would leave.*

| Log | Lines | Run blocks | Dropped | Size before | Size after |
|---|---:|---:|---:|---:|---:|
| `link-check-edits.txt` | 8157 | 19 | 10 | 909 KB | 132 KB |
| `epg-check-edits.txt` | 13174 | 19 | 13 | 1376 KB | 22 KB |
| `epg-build-edits.txt` | 880 | 70 | 40 | 106 KB | 5 KB |
| `log-edits.txt` | 5117 | 73 | 43 | 555 KB | 251 KB |

## Guide currency

- Merged guide `EPG/PremiumTV.xml`: 59 MB, 0 channel(s) with a listing in the live window - **no listing inside the next 48h - the guide is 59 MB of expired data; scripts/epg_build.py --force --patch has to publish a fresh one**
- Quarantine: 560 read, 560 kept, 0 dropped

## Removed

- `scripts/__pycache__`
- `tests/__pycache__`

## Needs a maintainer

- published guide: no listing inside the next 48h - the guide is 59 MB of expired data; scripts/epg_build.py --force --patch has to publish a fresh one
