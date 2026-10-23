"""The current release version has exactly one hand-edited source."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import release_version  # noqa: E402
import version_sync  # noqa: E402


class SingleSourceTests(unittest.TestCase):
    def test_the_version_file_is_valid_and_readable(self):
        version = release_version.current_version()
        self.assertRegex(version, r"^\d+\.\d+\.\d+(?:\.\d+)?$")
        self.assertEqual(
            release_version.android_version_code(version),
            release_version.current_version_code(),
        )

    def test_every_surface_agrees_with_the_version_file(self):
        self.assertEqual([], version_sync.check())

    def test_ci_runs_the_drift_check(self):
        workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("scripts/version_sync.py", workflow)
        paths = workflow.split("paths:", 1)[1].split("permissions:", 1)[0]
        for required in ("VERSION", "README.md", "app-update-notice.json"):
            self.assertIn(required, paths, f"{required} must trigger the check")

    def test_drift_is_detected_when_the_version_file_moves_alone(self):
        original = release_version.VERSION_FILE
        with tempfile.NamedTemporaryFile("w", suffix="-VERSION", delete=False) as handle:
            handle.write("9.9.9\n")
            temporary = Path(handle.name)
        release_version.VERSION_FILE = temporary
        try:
            problems = version_sync.check()
        finally:
            release_version.VERSION_FILE = original
            temporary.unlink(missing_ok=True)
        self.assertTrue(problems, "a version bump without the other surfaces must fail")
        joined = "\n".join(problems)
        # Gradle itself cannot drift: it reads the generated properties. The
        # hand-written surfaces are what the check has to catch.
        for expected in ("version.properties", "package.json", "README.md", "release-notes-9.9.9.md"):
            self.assertIn(expected, joined)


if __name__ == "__main__":
    unittest.main()
