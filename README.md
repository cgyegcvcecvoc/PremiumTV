# PremiumTV1

## Load the playlist

After the playlist changes are merged into `main`, open this URL in an M3U-compatible player:

```text
https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/PremiumTV.m3u
```

**Before the merge, the `main` URL can still return 404.** A file on a pull-request branch is not a file on `main`. Open [`playlists/PremiumTV.m3u`](playlists/PremiumTV.m3u) in this branch to inspect the starter playlist.

| File | Purpose |
|---|---|
| [`playlists/PremiumTV.m3u`](playlists/PremiumTV.m3u) | Player URL. Initially a **not-checked** source snapshot; replaced with link-checked results after a successful scheduled/manual checked run. |
| [`playlists/PremiumTV_all.m3u`](playlists/PremiumTV_all.m3u) | All unique source entries, including unverified/dead links. |
| [`playlists/STATUS.md`](playlists/STATUS.md) | Snapshot note, then the last successful run's summary. |
| `playlists/report.json` | Created on a successful scraper run; link-check results and per-source counts. |
| `playlists/sources/*.m3u` | Normalized source snapshots, used by the scraper if an upstream fetch fails. |

The initial snapshot was assembled from the publicly available **aria** and **doms9** M3U sources on 2026-09-27 with the existing scraper's parser and formatter. It has **not** been link-checked. **xtemus** is configured but could not be reached from the snapshot environment; a successful scraper run will add its allowed live-TV groups when available. Some links may expire, be geo-restricted, require authorization, or not actually play; even a passing HTTP check does not guarantee playback or rights to view a stream.

## Update automatically

The existing [scraper](scripts/scraper.py) downloads the sources in [`sources.json`](sources.json), parses/merges/deduplicates them, checks stream responses, and writes the playlist files. The [GitHub Actions workflow](.github/workflows/scrape.yml) schedules it daily at **3:00 AM**, **6:00 AM**, and **4:15 PM America/New_York** (daylight saving time is handled by GitHub).

1. Merge this branch's playlist and workflow into `main` to make the raw URL available. Scheduled runs only use the default branch (`main`); they cannot publish an unmerged pull request.
2. To run immediately, open **Actions → Scrape playlists → Run workflow**, select **main**, leave **Skip link checking** off, and start the run. Check its logs and `playlists/STATUS.md` / `playlists/report.json` on `main` afterwards. No runs had been recorded when this starter playlist was created; workflow configuration alone is not evidence a scheduled run has succeeded.
3. The workflow commits changed `playlists/` files back to the branch it ran on. On a scheduled run this is `main`; a manually dispatched run on a feature branch only updates that feature branch. Repository Actions must have permission to write contents; branch protection may require allowing the Actions bot to push or using a PR instead.

The checked run keeps the previous player playlist if too few links pass (the scraper returns an error). The optional **Skip link checking** dispatch refreshes the all-links list and caches but **does not replace** the player playlist with untested links. Scheduled runs may start late under load.

## Update sources or run locally

Edit [`sources.json`](sources.json) to enable/disable a source or add one with `name`, `type` (`m3u` or `w3u`), and `url`. W3U sources support `include_groups`, `exclude_groups`, and `max_depth`; the xtemus movie, series, radio, and highlight folders are excluded by the current settings. Review permissions and source quality before publishing new links.

Python 3.9+ is sufficient; no third-party packages are needed:

```bash
python scripts/scraper.py --help
python scripts/scraper.py                          # fetch, merge, link-check, and write playlists/
python scripts/scraper.py --no-check               # local unchecked merge (also overwrites local PremiumTV.m3u)
python -m unittest discover -s tests -v           # offline integration tests
```

Inspect the diff and the status report before committing. To publish changes, push them on a branch, open a pull request, and merge into `main`. For an immediate checked refresh after merging, dispatch the workflow on `main` as above. Do not publish a local `--no-check` result as if it were link-checked.

This repository does not host video. Verify that you are permitted to use and redistribute source links in your region.
