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

        # A release test must survive the next release: 1.1.21 was current when
        # it shipped, so ask for "at least 1.1.21" the way the 1.1.16-1.1.19
        # suites do. Pinning the exact string here broke the 1.1.20 suite when
        # 1.1.21 was cut, and pinning it again would break this one now.
        current = release_version.current_version()
        self.assertGreaterEqual(release_version.compare_versions(current, "1.1.21"), 0, current)
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
        self.assertIn("## 2026-11-25 — Version 1.1.21 published: Free provider directory", changelog)
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


# --- The highlighted free providers (added in the same release) -------------
#
# The same reading produced a second group: the four ad-supported services that
# publish a lineup. i.mjh.nz, which used to republish their playlists, lost them
# to a DMCA notice in 2024 and now points at the generator used here, so these
# tests also pin the addresses that must never come back.

GENERATOR = "BuddyChewChew/app-m3u-generator"

# name -> (playlist file, measured entries on 2026-11-25, measured new URLs)
HIGHLIGHTED_SOURCES = {
    "samsung-tv-plus": ("samsungtvplus_all.m3u", "2,669", "2,585"),
    "plex-live": ("plex_all.m3u", "2,889", "2,889"),
    "roku-channel": ("roku_all.m3u", "257", "230"),
    "tubi-live": ("tubi_all.m3u", "176", "163"),
}


class HighlightedFreeProvidersTest(unittest.TestCase):
    def test_the_four_services_that_publish_a_lineup_are_enabled_sources(self):
        configured = {s.get("name"): s for s in json.loads(text("sources.json"))["sources"]}
        for name, (playlist, entries, new_urls) in HIGHLIGHTED_SOURCES.items():
            with self.subTest(source=name):
                self.assertIn(name, configured)
                source = configured[name]
                self.assertTrue(source.get("enabled"), f"{name} must be enabled")
                self.assertEqual(source.get("type"), "m3u")
                self.assertEqual(
                    source["url"],
                    f"https://raw.githubusercontent.com/{GENERATOR}/main/playlists/{playlist}",
                )
                self.assertEqual(
                    source["github"],
                    {"repo": GENERATOR, "path": f"playlists/{playlist}", "ref": "main"},
                )

    def test_each_new_source_keeps_backup_addresses(self):
        """1.1.20's mirror rule applies to a new source like to an old one."""
        configured = {s.get("name"): s for s in json.loads(text("sources.json"))["sources"]}
        for name in HIGHLIGHTED_SOURCES:
            with self.subTest(source=name):
                mirrors = configured[name].get("mirrors") or []
                self.assertGreaterEqual(len(mirrors), 2)
                self.assertTrue(all(m.startswith("https://") for m in mirrors))
                self.assertTrue(configured[name].get("mirror_note"))

    def test_each_new_source_records_what_it_was_measured_at(self):
        """A source is added with numbers, not adjectives."""
        configured = {s.get("name"): s for s in json.loads(text("sources.json"))["sources"]}
        for name, (_playlist, entries, new_urls) in HIGHLIGHTED_SOURCES.items():
            with self.subTest(source=name):
                note = configured[name].get("note") or ""
                self.assertIn("Measured 2026-11-25", note)
                self.assertIn(entries, note)
                self.assertIn(new_urls, note)

    def test_the_tubi_guide_is_configured_because_it_matches_the_playlist(self):
        fixed = json.loads(text("sources.json"))["epg_sources"]["fixed"]
        guide = {g.get("name"): g for g in fixed}.get("Tubi (app-m3u-generator)")
        self.assertIsNotNone(guide, "the Tubi guide must be listed in epg_sources.fixed")
        self.assertTrue(guide["enabled"])
        self.assertEqual(
            guide["url"],
            f"https://raw.githubusercontent.com/{GENERATOR}/main/playlists/tubi_epg.xml",
        )
        self.assertIn("176", guide["note"])

    def test_the_dmca_removed_playlists_are_not_configured(self):
        """i.mjh.nz playlists were removed in 2024; only its guides are used."""
        config = json.loads(text("sources.json"))
        playlist_urls = [s.get("url") or "" for s in config["sources"]]
        playlist_urls += [m for s in config["sources"] for m in (s.get("mirrors") or [])]
        for url in playlist_urls:
            with self.subTest(url=url):
                self.assertNotIn("i.mjh.nz", url)
                self.assertNotIn("jmp2.uk", url)

        guide_urls = [g.get("url") or "" for g in config["epg_sources"]["fixed"]]
        self.assertTrue(
            any("i.mjh.nz" in url for url in guide_urls),
            "the i.mjh.nz guides are still expected in epg_sources.fixed",
        )


class NoCommittedConflictMarkersTest(unittest.TestCase):
    """A conflict left in a tracked file is a bug, whatever the file is."""

    def test_no_tracked_file_carries_git_conflict_markers(self):
        offenders: list[str] = []
        for path in _tracked_text_files():
            lines = path.read_text(encoding="utf-8").splitlines()
            for start, line in enumerate(lines):
                if not line.startswith("<<<<<<< "):
                    continue
                rest = lines[start + 1:]
                middle = next((i for i, l in enumerate(rest) if l.rstrip() == "======="), None)
                if middle is None:
                    continue
                if any(l.startswith(">>>>>>> ") for l in rest[middle + 1:]):
                    offenders.append(f"{path.relative_to(ROOT)}:{start + 1}")
                    break
        self.assertEqual(offenders, [], "resolve the conflict: " + ", ".join(offenders))

    def test_the_1121_record_names_its_tag_and_its_missing_apk(self):
        """The log must be able to tell a prepared release from a published one.

        It may not quietly imply that v1.1.21 shipped every installer: its APK
        is the reason 1.1.22 exists, and a reader has to be able to see that.
        (A duplicate heading is not itself a defect here - this log repeats
        historical headings legitimately - which is why only the conflict
        markers above are fatal.)
        """
        changelog = text("CHANGELOG.md")
        heading = "## 2026-11-25 — Version 1.1.21 published: Free provider directory"
        self.assertIn(heading, changelog)
        record = changelog.split(heading, 1)[1].split("\n## ", 1)[0]
        self.assertIn("releases/tag/v1.1.21", record)
        self.assertIn("101210000", record)
        self.assertIn("No APK is attached", record)


def _tracked_text_files() -> list[Path]:
    listed = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True
    ).stdout.split(b"\0")
    files: list[Path] = []
    for raw in listed:
        if not raw:
            continue
        path = ROOT / raw.decode("utf-8", "surrogateescape")
        if not path.is_file() or path.stat().st_size > 2_000_000:
            continue
        try:
            path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        files.append(path)
    return files


if __name__ == "__main__":
    unittest.main()
