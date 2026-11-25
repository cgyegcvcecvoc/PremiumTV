"""1.1.21 contracts: the highlighted free providers, and no committed conflicts.

The request was to work through the iptv-org awesome-iptv ``Providers``
discussions - clicking the links rather than reading the titles - and see what
could be added as *sources*, then publish the small improvements found on the
way.

What the reading produced:

* 149 provider discussions, 86 of them labelled ``Free``. Most are players or
  country directories whose streams are resolved in the browser, so they have
  no static playlist; the four ad-supported services that do publish one -
  Samsung TV Plus, Plex, The Roku Channel and Tubi - are the additions.
* matthuisman's i.mjh.nz playlists were removed under DMCA in 2024 and that
  project now points at ``BuddyChewChew/app-m3u-generator``, so the generator
  is the source and i.mjh.nz stays the *guide* source it already was.
* the Tubi guide from the same generator matches the Tubi playlist id for id,
  so the lineup arrives with listings.

The small improvement found while writing the changelog entry was that
``CHANGELOG.md`` had been committed with git conflict markers in it. These
tests fail if either the sources or the marker rule stops being true.
"""

from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GENERATOR = "BuddyChewChew/app-m3u-generator"

# name -> (playlist file, measured entries on 2026-11-25, measured new URLs)
NEW_SOURCES = {
    "samsung-tv-plus": ("samsungtvplus_all.m3u", "2,669", "2,585"),
    "plex-live": ("plex_all.m3u", "2,889", "2,889"),
    "roku-channel": ("roku_all.m3u", "257", "230"),
    "tubi-live": ("tubi_all.m3u", "176", "163"),
}


def sources_config() -> dict:
    return json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))


def tracked_text_files() -> list[Path]:
    """Every tracked file, minus the ones that are not text."""
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


class HighlightedFreeProvidersTest(unittest.TestCase):
    def test_the_four_services_that_publish_a_lineup_are_enabled_sources(self):
        configured = {s.get("name"): s for s in sources_config()["sources"]}
        for name, (playlist, entries, new_urls) in NEW_SOURCES.items():
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
        configured = {s.get("name"): s for s in sources_config()["sources"]}
        for name in NEW_SOURCES:
            with self.subTest(source=name):
                mirrors = configured[name].get("mirrors") or []
                self.assertGreaterEqual(len(mirrors), 2)
                self.assertTrue(any("cdn.jsdelivr.net" in m for m in mirrors))
                self.assertTrue(any("raw.gitmirror.com" in m for m in mirrors))
                self.assertTrue(configured[name].get("mirror_note"))

    def test_each_new_source_records_what_it_was_measured_at(self):
        """A source is added with numbers, not adjectives."""
        configured = {s.get("name"): s for s in sources_config()["sources"]}
        for name, (_playlist, entries, new_urls) in NEW_SOURCES.items():
            with self.subTest(source=name):
                note = configured[name].get("note") or ""
                self.assertIn("Measured 2026-11-25", note)
                self.assertIn(entries, note)
                self.assertIn(new_urls, note)

    def test_the_tubi_guide_is_configured_because_it_matches_the_playlist(self):
        fixed = sources_config()["epg_sources"]["fixed"]
        guides = {g.get("name"): g for g in fixed}
        guide = guides.get("Tubi (app-m3u-generator)")
        self.assertIsNotNone(guide, "the Tubi guide must be listed in epg_sources.fixed")
        self.assertTrue(guide["enabled"])
        self.assertEqual(
            guide["url"],
            f"https://raw.githubusercontent.com/{GENERATOR}/main/playlists/tubi_epg.xml",
        )
        self.assertIn("176", guide["note"])

    def test_the_dmca_removed_playlists_are_not_configured(self):
        """i.mjh.nz playlists were removed in 2024; only its guides are used."""
        config = sources_config()
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
        for path in tracked_text_files():
            lines = path.read_text(encoding="utf-8").splitlines()
            starts = [i for i, line in enumerate(lines) if line.startswith("<<<<<<< ")]
            for start in starts:
                rest = lines[start + 1:]
                middle = next(
                    (i for i, line in enumerate(rest) if line.rstrip() == "======="), None
                )
                if middle is None:
                    continue
                if any(
                    line.startswith(">>>>>>> ") for line in rest[middle + 1:]
                ):
                    offenders.append(f"{path.relative_to(ROOT)}:{start + 1}")
                    break
        self.assertEqual(
            offenders,
            [],
            "resolve the conflict and remove its markers: " + ", ".join(offenders),
        )

    def test_the_changelog_has_one_entry_per_release_heading(self):
        """The same release must not be announced twice, as the conflict did."""
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        headings = re.findall(r"^## .+$", changelog, flags=re.M)
        duplicated = sorted({h for h in headings if headings.count(h) > 1})
        self.assertEqual(duplicated, [], "duplicate changelog heading")


if __name__ == "__main__":
    unittest.main()
