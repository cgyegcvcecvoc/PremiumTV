"""1.1.21 contracts: the free provider directory.

The request was to read the iptv-org `awesome-iptv` provider directory
thoroughly, see what it can add to this playlist, and publish the result as a
minor release. The contracts below are what "added properly" means here:

* every new source is measured against the corpus and carries its measurement,
  a mirror and a note, so a reader can tell a measured import from a guess;
* a source that mixes television with radio, cameras or podcast episodes
  contributes only the groups it declares - the run report and STATUS.md say
  what was dropped, so a filtered source never looks like a source that shrank;
* the free providers that were *not* imported are named with the reason, so the
  question does not have to be re-opened;
* a country playlist's header cannot advertise every source's guides, which is
  the defect that failed the scrape gate before this release.

Nothing here is a style test: each case fails if the rule the release makes
stops being true.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))


def text(path: str | Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class Version1121Tests(unittest.TestCase):
    """The release number and its notes come from the version tooling."""

    def test_the_release_is_synced_across_every_surface(self):
        import release_version  # noqa: E402
        import version_sync  # noqa: E402

        current = release_version.current_version()
        self.assertEqual(release_version.compare_versions(current, "1.1.21"), 0, current)
        self.assertEqual(release_version.android_version_code("1.1.21"), 101_210_000)
        self.assertEqual(version_sync.check(), [])
        self.assertEqual(version_sync.PUBLISHED_VERSION, current)

        notes = text("release-notes-1.1.21.md")
        self.assertIn("# PremiumTV 1.1.21 — ", notes)
        self.assertIn("versionCode `101210000`", notes)

    def test_the_notes_follow_the_short_notes_rule(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "new_version.py"), "--check-notes", "1.1.21"],
            cwd=ROOT, capture_output=True, text=True, timeout=120,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_the_changelog_records_the_release(self):
        changelog = text("CHANGELOG.md")
        self.assertIn("## 2026-11-25 — Free provider directory (1.1.21)", changelog)
        # No committed merge-conflict markers anywhere in the log.
        for marker in ("<<<<<<<", ">>>>>>>"):
            self.assertNotIn(marker, changelog)
        self.assertIn("docs/SOURCE-HUNT-2026-11-25.md", changelog)


class SourceDirectoryTests(unittest.TestCase):
    """The three added sources, and the ones deliberately left out."""

    def test_the_three_sources_carry_their_measurement_and_a_mirror(self):
        config = json.loads(text("sources.json"))
        by_name = {source["name"]: source for source in config["sources"]}
        for name in ("m3upt", "tdtchannels", "nexonic-iptv"):
            with self.subTest(name=name):
                source = by_name[name]
                self.assertTrue(source["enabled"])
                self.assertTrue(source["url"].startswith("https://"))
                self.assertTrue(source.get("mirrors"), "a single address is a single point of failure")
                # The measurement is what separates an import from a guess.
                self.assertRegex(source["note"], r"\d")
                self.assertIn("2026-11-25", source["note"])

    def test_the_mixed_portuguese_source_contributes_only_television(self):
        config = json.loads(text("sources.json"))
        by_name = {source["name"]: source for source in config["sources"]}
        self.assertEqual(by_name["m3upt"]["include_groups"], ["TV"])
        # The other two are single-purpose lists: no group filter is needed, and
        # adding one with no evidence would silently shrink them.
        for name in ("tdtchannels", "nexonic-iptv"):
            self.assertNotIn("include_groups", by_name[name])

    def test_the_rejected_providers_are_recorded_with_a_reason(self):
        doc = text("docs/SOURCE-HUNT-2026-11-25.md")
        for provider, why in (
            ("BuddyChewChew/pluto", "session"),
            ("FreeIPTV", "account"),
            ("Grade TV", "iptv-org"),
        ):
            with self.subTest(provider=provider):
                self.assertIn(provider, doc)
                section = doc.split(provider, 1)[1][:600].lower()
                self.assertIn(why, section)

    def test_the_reference_checks_never_become_channels(self):
        config = json.loads(text("sources.json"))
        references = {item["name"]: item for item in config["reference_checks"]}
        for name in ("gradetv", "broadcast-atlas", "open-tv-atlas"):
            with self.subTest(name=name):
                self.assertEqual(references[name]["type"], "website")
                self.assertIn("imported", references[name]["note"].lower())


class GuideHeaderTests(unittest.TestCase):
    """A published playlist header stays inside its guide budget."""

    def test_no_published_playlist_advertises_more_than_the_maximum(self):
        import scraper  # noqa: E402

        worst: list[tuple[int, str]] = []
        for path in sorted((ROOT / "playlists" / "countries").glob("*.m3u")):
            header = path.read_text(encoding="utf-8").splitlines()[0]
            if "x-tvg-url=" not in header:
                continue
            guides = header.split('x-tvg-url="', 1)[1].rstrip('"').split(",")
            worst.append((len(guides), path.name))
        self.assertTrue(worst, "no country playlist advertises a guide")
        over = [(count, name) for count, name in worst if count > 1 + scraper.MAX_HEADER_GUIDES]
        self.assertEqual(over, [])


if __name__ == "__main__":
    unittest.main()
