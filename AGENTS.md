# Agent guide — PremiumTV

## “New version” means the whole release

When the user says **“new version”**, do the complete release workflow in
[`docs/RELEASING.md`](docs/RELEASING.md): work out the number and the feature
name, bump `VERSION`, write short release notes and a short changelog entry,
push, publish, and verify the installers attached. Do not ask what version
number to use and do not invent a fourth part.

The naming system (1.1.11+) is two derived names, never invented ones:

```bash
python scripts/new_version.py --next        # 1.1.11 -> 1.1.12, versionCode, the known themes
python scripts/new_version.py --feature local-channels   # standard name + notes
```

- **Number:** always the next patch (`1.1.11` → `1.1.12`); a minor bump is a
  recorded decision, not a default.
- **Release name:** `PremiumTV <version> — <feature name>`, where the feature
  name is the one-to-five-word theme of the change (the phrase the changelog
  entry opens with). A follow-up to a release reuses that release's name.
- **Tag:** `v<version>`. **Release notes:** one heading, one build-target line,
  at most five notes, each under 110 characters — enforced by
  `python scripts/new_version.py --check-notes <version>`.

“New version” alone authorises the bump, the notes, the commit, the publish and
the support-notice move; nothing has to be spelled out for an agent.

## Local channels (1.1.7+, market-aware from 1.1.11)

Local stations are data, not hard-coded UI. `scripts/build_local_channels.py`
reads `playlists/live/USA.m3u` plus the reference tables in
`data/local-markets/` (callsign → market, market → city/position, ZIP prefix →
state/point, place → position; sources and licences are in that folder's
README) and writes `playlists/local-channels.json`: markets with their stations,
a ZIP prefix table, state and city lists, and a country list. The Android
(`data/LocalChannels.kt`) and macOS (`renderer/local-channels.js`) apps resolve a
location fix, a ZIP code, a state, a city or a country against that document;
the answer is stored on the device only. Regenerate it after a scrape and check
it:

```bash
python scripts/build_local_channels.py
python scripts/build_local_channels.py --check
```

## Categories

`scripts/categorize.py` is the one taxonomy. A+E Networks is one brand group: its
flagship channels (A&E, History, Lifetime, LMN, FYI, VICE, Crime + Investigation)
and its FAST channels (Crime 360, Cold Case Files, The First 48, Storage Wars,
Hoarders, 60 Days In, Home.Made.Nation) all belong on the A&E Networks shelf, with
`AE_EXCEPTIONS` keeping documentaries that merely use a brand word (History Hit,
True History) in Documentary. After changing classification rules, rebuild the
published playlists and shelf:

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
