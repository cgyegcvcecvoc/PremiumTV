# Repository cleanup

- **Run:** biweekly deep cleanup (`20261010T131938Z-111`)
- **Started:** 2026-10-10T13:19:38Z | **Finished:** 2026-10-10T13:19:38Z | **Duration:** 0.19s
- **Outcome:** **CLEAN**
- **Space freed:** 1429 KB
- **Append-only logs trimmed:** 2 file(s), 8 run block(s) dropped (budget: the last 30 runs and 2500 lines per file)
- **Files removed: 6** (orphaned guides, swap files, caches)
- **Problems left for a maintainer:** 0

The biweekly run does the deep, slow sweep: `link_check.py --archives` re-tests and prunes the playlists no daily run patches (the priority playlist, the per-category playlists, the `categories/` shelf and the local source copies), then this report covers the repository itself. Removing dead channels stays `link_check.py`'s job; this tool never edits a playlist entry.

## Logs

| Log | Lines | Run blocks | Dropped | Size before | Size after |
|---|---:|---:|---:|---:|---:|
| `link-check-edits.txt` | 4702 | 9 | 7 | 554 KB | 270 KB |
| `epg-check-edits.txt` | 193 | 8 | 0 | 22 KB | 22 KB |
| `epg-build-edits.txt` | 93 | 31 | 1 | 5 KB | 5 KB |
| `log-edits.txt` | 2284 | 30 | 0 | 251 KB | 251 KB |

## Guide currency

- Merged guide `EPG/PremiumTV.xml`: 10 MB, 186 channel(s) with a listing in the live window - current
- Quarantine: 3320 read, 3320 kept, 0 expired or malformed dropped

## Removed

- `EPG/Bermuda.xml`
- `EPG/Macau.xml`
- `EPG/San_Marino.xml`
- `EPG/Sierra_Leone.xml`
- `scripts/__pycache__`
- `tests/__pycache__`

Nothing needs a maintainer: every artifact is current and no orphan was found.
