# Releasing PremiumTV — the “new version” rule

Version 1.1.7 introduced the one-phrase rule; **1.1.11 adds the release name
and the publication check.** Nothing else changed: saying *“new version”* is
still the whole authorisation.

## Say only “new version”

When the request is **“new version”** (or “cut a new version”, “ship the next
version”, “make a new release”), it means the complete release, not a version
bump:

1. Work out the next **number and name** from the naming system below
   (`python scripts/new_version.py --next` prints both).
2. Bump `VERSION`, write the short release notes and the short changelog entry:
   `python scripts/new_version.py --name "<release name>" --note "<one line>" …`
   (add `--local-channels`, `--a-and-e` or `--version-scheme` when the release
   carries those features; the flag adds the standard one-line note itself).
3. Generate the local-market directory when the playlist changed:
   `python scripts/build_local_channels.py`.
4. Commit, push, and open the pull request for the branch.
5. Run **Actions → Publish a release → Run workflow** (or
   `gh workflow run publish-release.yml --ref main`). Publication is what makes
   an installed app see the version: the in-app update centre only offers a
   published, non-draft, non-prerelease release that is numerically above the
   installed build and has that platform's installer attached.
6. Record the publication (see “After publication” at the end).

No question back to the user is needed for any of those steps. The name, the
number and the notes all come from the rules below.

## The name this release uses

`1.1.13` is **PremiumTV 1.1.13 — Hardened sources**: verified TLS for source
and guide fetches, confined local files, pinned macOS player libraries, and
discovery that will not promote this repository. The next release is the next
patch and its own theme (`python scripts/new_version.py --next` prints both);
the standard themes this tooling already knows are `local-channels`, `a-and-e`,
`version-scheme`, `resilient-playback` and `hardened-sources`.

## The naming system

Every release has two names, and they are derived — never invented:

| Name | Shape | Example | Where it appears |
|---|---|---|---|
| **Number** | `MAJOR.MINOR.PATCH` | `1.1.12` | `VERSION`, tags, versionCode, every app surface |
| **Release name** | `PremiumTV <number> — <feature name>` | `PremiumTV 1.1.12 — Resilient playback` | release title, release-notes heading, changelog entry |

**The feature name is the release's theme, not a codename.** It is one to five
words taken from what the release actually changes — the same phrase the
changelog entry opens with. A follow-up that fixes or finishes the previous
release reuses its name (`… — Local channels by location` again for a fix to
local channels); a release that starts something new uses the new theme. There
are no version codenames, no dates, no “V patches” and no fourth number.

**The number rule:**

- Default: the next patch — `1.1.12` → `1.1.13`.
- A release that changes how the app fundamentally works **and** needs a fresh
  line may bump the minor — `1.1.x` → `1.2.0`. That is a decision recorded in
  the pull request, not a default; the patch bump is the rule.
- The Android `versionCode` is always derived, never typed:
  `python scripts/release_version.py --code <version>`.
- Tags are `v<version>`. Four-part versions are retired (they are still parsed
  for old installs, never created).

**Why numeric:** the updater compares numbers, so the next patch is exactly what
an installed build is offered. A date or codename scheme would break Android's
monotonic `versionCode` and the release guard.

## Short notes rule (every release)

The release-notes file is a short announcement, not a changelog essay:

- one heading (`# PremiumTV <version> — <feature name>`), one build-target line,
  and **at most five one-line notes**;
- each note **under 110 characters** — say what changed, not how it works;
- the changelog (`CHANGELOG.md`) may carry a little more detail; the full
  reasoning belongs in code comments and the detailed Doc.

`python scripts/new_version.py --check-notes <version>` enforces both limits,
and `python scripts/new_version.py --notes-report` lists every release that is
still long enough to trip the habit.

## “I want a new version” from any agent

Any agent in this repository can finish a release from these three commands and
one click:

```bash
python scripts/new_version.py --next                 # 1.1.12 "Resilient playback" -> 1.1.13 …
python scripts/new_version.py --name "…" --note "…"  # bump VERSION, notes, generated surfaces
python scripts/build_local_channels.py               # only when playlists/live/USA.m3u changed
```

`AGENTS.md` repeats the rule so a fresh agent session does not have to be told:
“new version” means bump, notes, changelog, commit, publish, verify. Nothing
else has to be said.

## Publishing and the in-app update

Both installer builds run `scripts/verify_release_bundle.py` on the packaged
APK and DMG before uploading them: ZIP prefixes 170–176 must resolve to WGAL,
CBS 21 and FOX 43, so a stale local-channel directory fails the build instead
of shipping.

`.github/workflows/publish-release.yml` creates the GitHub release from
`VERSION` and `release-notes-<version>.md`. It refuses a tag that already
exists, runs the version-drift check first, and the Android and macOS build
workflows then attach the APK and the four Mac installers. **Settings → App
updates** only offers a release that is published (not draft, not pre-release),
numerically above the installed version, and whose installer for that platform
is already attached. Once published, the next daily check — or pressing
**Check for update** — shows it, downloads once, verifies the SHA-256 file and
installs it.

## After publication

1. Set `PUBLISHED_VERSION` in `scripts/version_sync.py` to the new version and
   run `python scripts/version_sync.py --write`.
2. Move `app-update-notice.json` → `update-below-newest.max_version` to the
   previous version and update its `surprise` sentence, so builds one release
   behind get the popup (the Settings path works without this).
3. Update the download-site copy the version check names (`docs/README.md`,
   `docs/blocked/index.html`, `hub/static/index.html`, `README.md` table,
   `docs/UPDATES.md`) and commit that as the publication record.
4. Say what shipped, in one line, in the release's GitHub description — the
   same sentence as the first note.
