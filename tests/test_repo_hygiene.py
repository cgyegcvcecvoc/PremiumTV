"""Built installers and generated bundles are never tracked in Git."""

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TrackedArtifactTests(unittest.TestCase):
    def setUp(self):
        if not (ROOT / ".git").exists():
            self.skipTest("not a Git checkout")
        result = subprocess.run(
            ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=False
        )
        if result.returncode != 0:
            self.skipTest("git ls-files is not available")
        self.tracked = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    def test_no_installer_is_tracked(self):
        apks = [path for path in self.tracked if path.lower().endswith(".apk")]
        self.assertEqual([], apks, "APKs belong to releases/Actions artifacts, not Git")

    def test_no_generated_installer_checksum_is_tracked(self):
        self.assertNotIn("build-out/SHA256SUMS-android.txt", self.tracked)

    def test_the_hub_export_zip_is_not_tracked(self):
        self.assertNotIn("premiumtv-hub-static-site.zip", self.tracked)

    def test_the_ignore_rules_stay_in_place(self):
        ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        for pattern in ("build-out/", "*.apk", "premiumtv-hub-static-site.zip"):
            self.assertIn(pattern, ignore, pattern)


if __name__ == "__main__":
    unittest.main()
