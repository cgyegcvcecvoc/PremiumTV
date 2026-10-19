# PremiumTV 1.0.8

**Status: marked in source, not yet published.** The default build version is
now **1.0.8** (Android `versionCode 100080000`, derived by
`scripts/release_version.py`: `1.0.8` → `100080000` — above `1.0.7` /
`100070000`, so it installs over every earlier stable and the retired 1.1.x
previews). The download site and the in-app updaters promote it only once a
complete, published `v1.0.8` release (APK + all four Mac installers) exists;
until then 1.0.6.1 remains the recommended download and `v1.0.7` its
compatibility alias.

## What changes

- **Categories are a list, with the channel count small on the right.**
  Everywhere categories are listed, they now read as one row per category:
  the category name leads the row and its channel count sits small at the
  right edge.
  - Download site (`docs/`): the Channels section's category grid is now a
    list — name and sample channels on the left, the count small on the
    right, with backup counts and the category-playlist link underneath it.
  - Download hub (`hub/`): the Published / USA shelf / Global shelf category
    chips are now list rows with the same small right-hand count.
  - Android TV: each category header on the Channels tab now puts the small
    channel count at the right edge of the row instead of beside the name.
  - macOS already listed its sidebar categories this way (`.cat-count`,
    11 px, right-aligned); it is unchanged and is the pattern the other
    surfaces now follow.
- No channel, playlist, guide, refresh or updater behaviour changes. The
  1.0.7 → 1.0.6.1 compatibility-alias mapping is historical and stays.

## Verification

- `python3 scripts/release_version.py --code 1.0.8` prints `100080000`.
- Python test suite updated where it pins the default build version
  (`tests/test_android_bundle.py`, `tests/test_android_refresh.py`,
  `tests/test_app_updates.py`) and extended with a category-list layout
  regression check (`tests/test_site_data.py`).
