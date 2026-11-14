# Agent guide — PremiumTV

## “New version” means the whole release

When the user says **“new version”**, do the complete release workflow in
[`docs/RELEASING.md`](docs/RELEASING.md): bump `VERSION` by one patch, write
short release notes, add a short changelog entry, push to `main`, and run
**Actions → Publish a release**. Do not ask what version number to use and do
not invent a fourth part: the rule is the next patch (`1.1.7` → `1.1.8`).

Release notes are **short by rule** — at most five one-line notes under 110
characters each. Use:

```bash
python scripts/new_version.py --name "Local channels" --note "..."
python scripts/new_version.py --check-notes 1.1.7
```

## Version policy

`VERSION` is the only hand-edited release number. `MAJOR.MINOR.PATCH` always;
the Android `versionCode` is derived, never typed; tags are `v<version>`. The
V-patch and compatibility-alias schemes are retired. Full rules and the
post-publication steps are in `docs/RELEASING.md`.

## Local channels (1.1.7+)

Local stations are data, not hard-coded UI. `scripts/build_local_channels.py`
reads `playlists/live/USA.m3u` and writes `playlists/local-channels.json`
(markets, callsigns/EPG ids, ZIP prefix ranges, state centroids). The Android
(`data/LocalChannels.kt`) and macOS (`renderer/local-channels.js`) apps match a
viewer's location/ZIP/state/country against that document; the answer is stored
on the device only. Regenerate the document after a scrape and check it:

```bash
python scripts/build_local_channels.py
python scripts/build_local_channels.py --check
```

## Categories

`scripts/categorize.py` is the one taxonomy. A&E Networks is its own brand
group so all A&E channels (including Crime 360) stay together; after changing
classification rules, rebuild the published playlists and shelf:

```bash
python scripts/rebuild_playlists.py
python scripts/rebuild_playlists.py --no-categories playlists/live/USA.m3u playlists/countries/USA.m3u
python scripts/build_categories.py
python -m unittest tests.test_categorize
```

## Checks

- Python: `python -m unittest discover -s tests`
- macOS logic: `cd macos/app && node --test test/*.test.js` (after `npm ci`)
- Version drift: `python scripts/version_sync.py`
- The Android app needs the Android SDK/Gradle; do not claim a Kotlin build
  passed if it was not run.
