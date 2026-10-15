# Repository cleanup

- **Run:** biweekly deep cleanup (`20261015T160004Z-388`)
- **Started:** 2026-10-15T16:00:04Z | **Finished:** 2026-10-15T16:00:04Z | **Duration:** 0.61s
- **Outcome:** **CLEAN**
- **Space freed:** 4846 KB
- **Append-only logs trimmed:** 4 file(s), 234 run block(s) dropped (budget: the last 30 runs and 2500 lines per file)
- **Files removed: 2** (orphaned guides, swap files, caches)
- **Problems left for a maintainer:** 0

The biweekly run does the deep, slow sweep: `link_check.py --archives` re-tests and prunes the playlists no daily run patches (the priority playlist, the per-category playlists, the `categories/` shelf and the local source copies), then this report covers the repository itself. Removing dead channels stays `link_check.py`'s job; this tool never edits a playlist entry.

## Logs

| Log | Lines | Run blocks | Dropped | Size before | Size after |
|---|---:|---:|---:|---:|---:|
| `link-check-edits.txt` | 12852 | 27 | 23 | 1458 KB | 258 KB |
| `epg-check-edits.txt` | 13190 | 27 | 13 | 1376 KB | 22 KB |
| `epg-build-edits.txt` | 8618 | 127 | 118 | 629 KB | 155 KB |
| `log-edits.txt` | 7803 | 110 | 80 | 837 KB | 234 KB |

## Guide currency

- Merged guide `EPG/PremiumTV.xml`: 37 MB, 1725 channel(s) with a listing in the live window - current
- Quarantine: 2732 read, 2682 kept, 50 expired or malformed dropped

## Removed

- `scripts/__pycache__`
- `tests/__pycache__`

Nothing needs a maintainer: every artifact is current and no orphan was found.
