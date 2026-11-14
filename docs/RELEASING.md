# Releasing PremiumTV — the “new version” rule

Version 1.1.7 is the first release under this system.

## Say only “new version”

When the request is **“new version”** (or “cut a new version”, “ship the next
version”), it means the whole release, not just a version bump:

1. Bump `VERSION` by one patch and write the short release notes:
   `python scripts/new_version.py --name "<short name>" --note "<one line>" …`
2. Add a short dated entry to `CHANGELOG.md`.
3. Commit and push the branch to `main` (`cloud_git` push).
4. Run **Actions → Publish a release → Run workflow** from `main`. An agent
   with an authenticated `gh` can do the same without the browser:
   `gh workflow run publish-release.yml --ref main`.
5. Confirm the release exists, the APK and all four Mac installers are
   attached, and an installed build sees it.

No other phrase is needed: “new version” authorises steps 1–4. Step 5 is the
publication check, not a second decision.

## The naming system

- **Technical version:** `MAJOR.MINOR.PATCH`, always three parts. A new version
  is the **next patch** (`1.1.7` → `1.1.8`); a feature set that changes how the
  app works may bump the minor (`1.2.0`). No fourth part, no “V patches”, no
  compatibility twins — those schemes are retired.
- **Release title:** `PremiumTV <version> — <short name>`; the short name is one
  or two words (“Local channels”, “Guide fix”). It appears in the release title
  and the notes file, never in the app’s version plaque.
- **Tag:** `v<version>`.
- **Android versionCode:** derived, never typed:
  `python scripts/release_version.py --code <version>`.
- **Why:** the updater compares numeric versions, so the next patch is exactly
  what an installed build is offered. A date or codename scheme would break
  Android’s monotonic `versionCode` and the release guard.

## Short notes rule (applies to every release)

The release-notes file is a short announcement, not a changelog essay:

- one heading, one build-target line, and **at most five one-line notes**;
- each note **under 110 characters** — say what changed, not how it works;
- the changelog (`CHANGELOG.md`) may carry a little more detail; the full
  reasoning belongs in code comments and the detailed Doc.

`python scripts/new_version.py --check-notes <version>` enforces the limits.

## Publishing and the in-app update

`.github/workflows/publish-release.yml` creates the GitHub release from
`VERSION` and `release-notes-<version>.md`. It refuses a tag that already
exists and runs the version-drift check first. The Android and macOS build
workflows then attach the APK and the four Mac installers. This matters for
the real app: **Settings → App updates** only offers a release that is
published (not draft, not pre-release), numerically above the installed
version, and whose installer for that platform is already attached. Once the
release is published, the next daily check — or pressing **Check for update** —
shows it, downloads once, verifies the SHA-256 file and installs it.

After publication:

1. Set `PUBLISHED_VERSION` in `scripts/version_sync.py` to the new version and
   run `python scripts/version_sync.py --write`.
2. Move `app-update-notice.json` → `update-below-newest.max_version` to the
   previous version and update its `surprise` sentence, so builds one release
   behind get the popup (the Settings path works without this).
3. Update the download-site copy the version check names (`docs/README.md`,
   `docs/blocked/index.html`, `hub/static/index.html`, `README.md` table,
   `docs/UPDATES.md`) and commit that as the publication record, as 1.1.6 did.
