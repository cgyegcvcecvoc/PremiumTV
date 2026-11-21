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
    def test_the_1_1_13_record_is_kept(self):
        # 1.1.13 was prepared but never published or tagged; its hardened-sources
        # code ships in 1.1.14. The notes and changelog entry stay as the record
        # of what that work was, so this checks them without pinning VERSION.
        # Every-surface syncing is checked by test_release_1114 and
        # test_version_single_source against the current release.
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
