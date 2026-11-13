"""Deep-link checks for the 1.1.4 release and the in-app updaters.

The repository was renamed ``PremiumTV1`` -> ``PremiumTV`` on 2026-10-21.
GitHub 301s the old slug, so builds already installed on TVs and Macs keep
working, but every URL this project *publishes* has to use the canonical
repository: a renamed project Pages site does not survive the rename, and a
redirect is one more thing that can break between an installed app and its
next update.

These tests pin the functional endpoints (the two updaters, the notice
document, the bundle builder and the download page) to the canonical name and
fail if the old slug creeps back into them.
"""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build_site_data  # noqa: E402

CANONICAL = "https://github.com/cgyegcvcecvoc/PremiumTV"
CANONICAL_API = "https://api.github.com/repos/cgyegcvcecvoc/PremiumTV"
CANONICAL_RAW = "https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV/main"

# Files whose URLs are read by an app, a workflow or a person. Historical
# change-log entries keep the old name on purpose: they describe what happened
# at the time, and their links still resolve through GitHub's redirect.
FUNCTIONAL_FILES = (
    "android/app/src/main/kotlin/com/premiumtv/app/update/AppUpdateManager.kt",
    "android/app/src/main/kotlin/com/premiumtv/app/update/UpdateNotice.kt",
    "macos/app/src/main/updater.js",
    "macos/app/src/main/update-notice.js",
    "macos/app/src/main/main.js",
    "app-update-notice.json",
    "android/tools/build_bundle.py",
    "android/app/src/test/kotlin/com/premiumtv/app/data/TvRepositoryTest.kt",
    "scripts/build_site_data.py",
    "docs/blocked/index.html",
    "hub/static/index.html",
    "hub/DEPLOY.md",
    "docs/UPDATES.md",
    "README.md",
    "categories/README.md",
    "EPG/README.md",
    "scripts/verify_update_chain.py",
    "scripts/build_categories.py",
    "scripts/epg_build.py",
    "scripts/legacy_sunset.py",
    "scripts/scraper.py",
    "scripts/vod_catalog.py",
    "hub/build_data.py",
    "hub/export_static.py",
    "hub/fetch_assets.py",
)


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class CanonicalDeepLinkTests(unittest.TestCase):
    def test_no_functional_file_uses_the_old_repository_slug(self):
        offenders = []
        for name in FUNCTIONAL_FILES:
            if "cgyegcvcecvoc/PremiumTV1" in text(name):
                offenders.append(name)
        self.assertEqual(offenders, [], f"old PremiumTV1 URL still in {offenders}")

    def test_no_macos_source_or_test_uses_the_old_repository_url(self):
        offenders = []
        for pattern in ("src/**/*.js", "test/*.test.js"):
            for path in (ROOT / "macos" / "app").glob(pattern):
                if "cgyegcvcecvoc/PremiumTV1" in path.read_text(encoding="utf-8"):
                    offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [], f"old PremiumTV1 URL still in {offenders}")

    def test_android_updater_uses_the_canonical_releases_api(self):
        manager = text(FUNCTIONAL_FILES[0])
        self.assertIn(f'"{CANONICAL_API}/releases?per_page=30"', manager)
        self.assertNotIn("PremiumTV1", manager)

    def test_both_platforms_read_the_same_canonical_notice(self):
        android_notice = text(FUNCTIONAL_FILES[1])
        mac_notice = text(FUNCTIONAL_FILES[3])
        self.assertIn(f'"{CANONICAL_RAW}/app-update-notice.json"', android_notice)
        self.assertIn(f"'{CANONICAL_RAW}/app-update-notice.json'", mac_notice)
        self.assertIn(f'"{CANONICAL}/releases/latest"', android_notice)
        self.assertIn(f"'{CANONICAL}/releases/latest'", mac_notice)

    def test_mac_updater_uses_the_canonical_releases_api(self):
        updater = text(FUNCTIONAL_FILES[2])
        self.assertIn(f"'{CANONICAL_API}/releases?per_page=30'", updater)

    def test_notice_document_points_at_the_canonical_repository(self):
        notice = json.loads(text("app-update-notice.json"))
        self.assertEqual(notice["notice_url"],
                         f"{CANONICAL_RAW}/app-update-notice.json")
        self.assertEqual(notice["releases_url"], f"{CANONICAL}/releases/latest")
        self.assertEqual(notice["repo_url"], CANONICAL)
        rules = {rule["id"]: rule for rule in notice["rules"]}
        self.assertEqual(rules["update-below-newest"]["max_version"], "1.1.5")
        self.assertIn("1.1.6", rules["update-below-newest"]["surprise"])

    def test_bundle_builder_publishes_canonical_raw_urls(self):
        builder = text("android/tools/build_bundle.py")
        self.assertIn(f'RAW_BASE = "{CANONICAL_RAW}"', builder)

    def test_site_generator_publishes_canonical_urls(self):
        self.assertEqual(build_site_data.REPO_NAME, "PremiumTV")
        self.assertEqual(build_site_data.RAW_BASE, CANONICAL_RAW)
        self.assertEqual(build_site_data.RELEASES_BASE,
                         f"{CANONICAL}/releases/download")
        self.assertEqual(build_site_data.PAGES_URL,
                         "https://cgyegcvcecvoc.github.io/PremiumTV/")

    def test_blocked_page_links_to_the_1_1_5_installers(self):
        page = text("docs/blocked/index.html")
        for asset in (
            "PremiumTV-1.1.5-debug.apk",
            "PremiumTV-1.1.5-mac-arm64.dmg",
            "PremiumTV-1.1.5-mac-x64.dmg",
        ):
            self.assertIn(
                f"{CANONICAL}/releases/download/v1.1.5/{asset}", page)
        self.assertIn(f"{CANONICAL}/releases/latest", page)
        self.assertIn("versionCode 101050000", page)

    def test_download_page_and_docs_use_the_canonical_repository(self):
        for name in ("README.md", "docs/UPDATES.md", "hub/DEPLOY.md",
                     "categories/README.md", "EPG/README.md"):
            body = text(name)
            self.assertNotIn("PremiumTV1", body, name)
            self.assertIn("cgyegcvcecvoc/PremiumTV", body, name)

    def test_release_asset_names_match_the_updater_contract(self):
        """The names the updaters look for must be the names CI uploads."""
        android_workflow = text(".github/workflows/android-build.yml")
        macos_workflow = text(".github/workflows/macos-build.yml")
        policy = text("macos/app/src/main/update-policy.js")
        self.assertIn("PremiumTV-${version}-debug.apk", android_workflow)
        self.assertIn("SHA256SUMS-android.txt", android_workflow)
        # The Mac workflow packages both architectures and both formats; the
        # updater itself only downloads the DMG for this Mac.
        self.assertIn("macos/app/dist/*.dmg", macos_workflow)
        self.assertIn("macos/app/dist/*.pkg", macos_workflow)
        self.assertIn("SHA256SUMS-macos.txt", macos_workflow)
        self.assertIn("PremiumTV-${version}-mac-${macArch(arch)}.dmg", policy)
        self.assertIn("macAssetName(version, this.arch)",
                      text("macos/app/src/main/updater.js"))

    def test_update_chain_verifier_covers_the_release_contract(self):
        script = text("scripts/verify_update_chain.py")
        self.assertIn("releases?per_page=30", script)
        self.assertIn("SHA256SUMS-android.txt", script)
        self.assertIn("SHA256SUMS-macos.txt", script)
        self.assertIn("PremiumTV-{version}-debug.apk", script)
        self.assertIn("PremiumTV-{mac_version}-mac-arm64.dmg", script)
        self.assertIn("PremiumTV-{mac_version}-mac-x64.pkg", script)

    def test_category_shelf_generator_and_readme_use_canonical_urls(self):
        """The shelf generator writes the README a player is pointed at.

        A generated file can reintroduce the old slug even after the committed
        README is fixed: the deep check regenerates the shelf, so the generator
        itself has to publish the canonical URL.
        """
        script = text("scripts/build_categories.py")
        self.assertIn('REPO_SLUG = "cgyegcvcecvoc/PremiumTV"', script)
        self.assertNotIn("cgyegcvcecvoc/PremiumTV1", script)
        readme = text("categories/README.md")
        self.assertNotIn("PremiumTV1", readme)
        self.assertIn(
            "raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV/main/categories/USA.m3u",
            readme)

    def test_the_1_1_4_release_notes_name_the_canonical_fix(self):
        notes = text("release-notes-1.1.4.md")
        self.assertIn("PremiumTV 1.1.4", notes)
        self.assertIn("PremiumTV", notes)
        self.assertIn("canonical", notes.lower())


if __name__ == "__main__":
    unittest.main()
