# Repository cleanup

- **Run:** biweekly deep cleanup (`20261115T193652Z-911`)
- **Started:** 2026-11-15T19:36:52Z | **Finished:** 2026-11-15T19:36:53Z | **Duration:** 0.4s
- **Outcome:** **CLEAN**
- **Space freed:** 8375 KB
- **Append-only logs trimmed:** 4 file(s), 463 run block(s) dropped (budget: the last 30 runs and 2500 lines per file)
- **Files removed: 2** (orphaned guides, swap files, caches)
- **Problems left for a maintainer:** 0

The biweekly run does the deep, slow sweep: `link_check.py --archives` re-tests and prunes the playlists no daily run patches (the priority playlist, the per-category playlists, the `categories/` shelf and the local source copies), then this report covers the repository itself. Removing dead channels stays `link_check.py`'s job; this tool never edits a playlist entry.

## Logs

| Log | Lines | Run blocks | Dropped | Size before | Size after |
|---|---:|---:|---:|---:|---:|
| `link-check-edits.txt` | 10002 | 36 | 32 | 1135 KB | 285 KB |
| `epg-check-edits.txt` | 267 | 45 | 15 | 25 KB | 2 KB |
| `epg-build-edits.txt` | 66148 | 259 | 250 | 4461 KB | 153 KB |
| `log-edits.txt` | 13970 | 196 | 166 | 1525 KB | 251 KB |

## Guide currency

- Merged guide `EPG/PremiumTV.xml`: 36 MB, 1948 channel(s) with a listing in the live window - current
- Quarantine: 2768 read, 2768 kept, 0 dropped

## Removed

- `scripts/__pycache__`
- `tests/__pycache__`

Nothing needs a maintainer: every artifact is current and no orphan was found.
