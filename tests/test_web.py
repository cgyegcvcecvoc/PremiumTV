"""Offline contracts for the independent web edition (no Node/npm required)."""
from __future__ import annotations

import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
sys.path.insert(0, str(WEB / "tools"))
import build as web_build  # noqa: E402


class WebIsolationTests(unittest.TestCase):
    def test_web_has_its_own_version_and_native_version_is_untouched(self):
        package = json.loads((WEB / "package.json").read_text())
        self.assertEqual(package["name"], "premiumtv-web")
        self.assertRegex(package["version"], r"^\d+\.\d+\.\d+$")
        self.assertNotEqual(package["version"], (ROOT / "VERSION").read_text().strip())
        self.assertEqual(json.loads((WEB / "package-lock.json").read_text())["version"], package["version"])

    def test_web_workflow_never_publishes_a_native_release(self):
        workflow = (ROOT / ".github/workflows/web-build.yml").read_text()
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("upload-artifact", workflow)
        self.assertIn("WEBKIT_TESTS=1", workflow)
        for forbidden in ("gh release", "publish-release.yml", "android-build.yml", "macos-build.yml", "version_sync.py --write", "electron-builder", "gradlew"):
            self.assertNotIn(forbidden, workflow)
        self.assertNotIn("contents: write", workflow)

    def test_pages_publishes_web_as_a_separate_path(self):
        workflow = (ROOT / ".github/workflows/pages.yml").read_text()
        self.assertIn("cp -a dist ../docs/web", workflow)
        self.assertIn("python tools/verify_export.py", workflow)
        self.assertIn('<a class="btn btn-primary" href="web/">', (ROOT / "docs/index.html").read_text())

    def test_shared_policies_are_copied_not_forked(self):
        source = (WEB / "tools/build.py").read_text()
        for name in web_build.SHARED:
            self.assertIn(name, source)
            self.assertTrue((ROOT / "macos/app/src/renderer" / name).is_file())
            self.assertFalse((WEB / "src" / name).exists(), "Shared policy must not be forked")
            exported = WEB / "dist/shared" / name
            if exported.exists():
                self.assertEqual(exported.read_bytes(), (ROOT / "macos/app/src/renderer" / name).read_bytes())
        self.assertIn("build_bundle.build", source)

    def test_generated_outputs_are_ignored(self):
        ignore = (ROOT / ".gitignore").read_text()
        for path in ("web/node_modules/", "web/dist/", "web/test-results/", "web/playwright-report/", "docs/web/"):
            self.assertIn(path, ignore)

    def test_no_electron_or_forbidden_header_bridge_in_web_source(self):
        source = "\n".join(p.read_text() for p in (WEB / "src").glob("*.js"))
        self.assertNotIn("window.premiumtv", source)
        self.assertNotIn("ipcRenderer", source)
        self.assertNotIn("mode: 'no-cors'", source)
        self.assertNotIn('mode: "no-cors"', source)
        self.assertIn("playsinline", (WEB / "src/index.html").read_text())

    def test_service_worker_does_not_cache_media_or_cross_origin_requests(self):
        source = (WEB / "src/sw.js").read_text()
        self.assertIn("url.origin !== self.location.origin", source)
        self.assertRegex(source, r'request\.headers\.has\(["\']range["\']\)')
        self.assertIn("mp4|m4v", source)

    def test_icons_are_real_pngs_and_directory_escapes_source_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            web_build.make_icons(out)
            for size in (192, 512):
                data = (out / f"icon-{size}.png").read_bytes()
                self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
                self.assertGreater(len(data), 100)
            self.assertEqual(web_build.escape('<script>"x"&'), "&lt;script&gt;&quot;x&quot;&amp;")

    def test_export_refuses_root_as_output(self):
        with self.assertRaises(ValueError):
            web_build.build(ROOT)
        with self.assertRaises(ValueError):
            web_build.build(WEB / "src")


if __name__ == "__main__":
    unittest.main()
