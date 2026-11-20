"""1.1.13 contracts: hardened sources, pinned player libraries, named notes."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class Version1113Tests(unittest.TestCase):
    def test_the_release_is_synced_across_every_surface(self):
        import release_version  # noqa: E402
        import version_sync  # noqa: E402

        self.assertEqual(release_version.current_version(), "1.1.13")
        self.assertEqual(release_version.android_version_code("1.1.13"), 101_130_000)
        self.assertEqual(version_sync.check(), [])
        self.assertEqual(version_sync.PUBLISHED_VERSION, "1.1.13")

        notes = text(ROOT / "release-notes-1.1.13.md")
        self.assertIn("# PremiumTV 1.1.13 — Hardened sources", notes)
        self.assertIn("versionCode `101130000`", notes)
        self.assertIn("Version 1.1.13 prepared: hardened sources", text(ROOT / "CHANGELOG.md"))

    def test_source_fetches_are_verified_and_stream_probes_are_not(self):
        scraper = text(ROOT / "scripts/scraper.py")
        self.assertIn("SECURE_CTX = ssl.create_default_context()", scraper)
        self.assertIn("context=SECURE_CTX", scraper)
        self.assertIn("context=INSECURE_CTX", scraper)
        self.assertIn("def source_url_problem(", scraper)
        self.assertIn("def configured_local_path(", scraper)
        self.assertIn("context=scraper.SECURE_CTX", text(ROOT / "scripts/epg_check.py"))
        self.assertIn("context=scraper.SECURE_CTX", text(ROOT / "scripts/epg_build.py"))
        self.assertIn("context=INSECURE_CTX", text(ROOT / "scripts/link_check.py"))

    def test_ci_and_discovery_stay_locked(self):
        ci = text(ROOT / ".github/workflows/ci.yml")
        self.assertIn("sources.json", ci)
        self.assertIn("actions/setup-node@v5", ci)
        self.assertIn("actions/setup-node@v5", text(ROOT / ".github/workflows/pages.yml"))
        self.assertIn("actions/setup-node@v5", text(ROOT / ".github/workflows/web-build.yml"))
        config = json.loads(text(ROOT / "sources.json"))
        self.assertIn("cgyegcvcecvoc", config["discovery"]["github_search"]["exclude_owners"])
