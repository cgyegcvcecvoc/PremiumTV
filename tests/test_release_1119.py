"""1.1.19 contracts: the whole area, not the single nearest market.

1.1.18 taught the apps that "nearest" is not "yours" and stopped a far market
being adopted silently. 1.1.19 finishes the idea: a fix is inside *every*
published market within the radius, because the directory splits several metros
into entries a short drive apart (Dallas, Fort Worth and Garland; Newark,
Paterson and New York City). The nearest is saved, the rest are offered as
alternatives, and a typed city matches the place rather than the spelling.

The Linux edition ships in this release too. 1.1.18's release never carried its
installers - they were built at a later commit than the tag pointed at, and the
exact-SHA asset gate kept them off - so this file also pins the surfaces that
make 1.1.19 the release that actually delivers them.
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

APP = "macos/app"
ANDROID = "android/app/src/main/kotlin/com/premiumtv/app"
ANDROID_TEST = "android/app/src/test/kotlin/com/premiumtv/app"


def text(path: str | Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class Version1119Tests(unittest.TestCase):
    """The release number and its notes come from the version tooling."""

    def test_the_release_is_synced_across_every_surface(self):
        import release_version  # noqa: E402
        import version_sync  # noqa: E402

        self.assertEqual(release_version.current_version(), "1.1.19")
        self.assertEqual(release_version.android_version_code("1.1.19"), 101_190_000)
        self.assertEqual(version_sync.check(), [])
        self.assertEqual(version_sync.PUBLISHED_VERSION, "1.1.19")

        notes = text("release-notes-1.1.19.md")
        self.assertIn("# PremiumTV 1.1.19 — ", notes)
        self.assertIn("versionCode `101190000`", notes)

    def test_the_notes_follow_the_short_notes_rule(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "new_version.py"), "--check-notes", "1.1.19"],
            cwd=ROOT, capture_output=True, text=True, timeout=120,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class AreaDetectionTests(unittest.TestCase):
    """Every market in reach, nearest first, on every front end."""

    def test_android_reports_the_area_not_just_the_nearest_market(self):
        data = text(f"{ANDROID}/data/LocalChannels.kt")
        self.assertIn("fun nearbyMarketsWithDistance(", data)
        self.assertIn("maxKm: Double = LOCAL_MARKET_NEAR_KM", data)
        self.assertIn("fun stateForLocation(", data)
        self.assertIn("fun normalizePlace(name: String): String", data)
        # The city comparison goes through the same folding.
        self.assertIn("normalizePlace(market.city) == wantedCity", data)
        # The dialog saves the nearest and offers the rest.
        dialog = text(f"{ANDROID}/ui/LocalChannelsDialog.kt")
        self.assertIn("known.nearbyMarketsWithDistance(latitude, longitude)", dialog)
        self.assertIn("nearby = area.drop(1)", dialog)
        self.assertIn("fun useNearbyMarket(", dialog)

    def test_the_shared_renderer_reports_the_same_area(self):
        local = text(f"{APP}/src/renderer/local-channels.js")
        self.assertIn("function nearbyMarketsWithDistance(", local)
        self.assertIn("function normalizePlace(", local)
        self.assertIn("normalizePlace(market.city)", local)
        self.assertIn("nearbyMarketsWithDistance, normalizePlace", local)
        self.assertIn("local.nearbyMarketsWithDistance(", text("web/src/app.js"))
        mac = text(f"{APP}/src/renderer/app.js")
        self.assertIn("local.nearbyMarketsWithDistance(", mac)
        self.assertIn("function nearbyMarketsMessage(", mac)

    def test_the_suites_pin_the_area_rules(self):
        jvm = text(f"{ANDROID_TEST}/data/LocalChannelsTest.kt")
        for needle in (
            "nearbyMarketsWithDistance",
            "normalizePlace",
            "stateForLocation",
            "marketIsNear",
        ):
            self.assertIn(needle, jvm)
        for path in (
            f"{APP}/test/local-channels.test.js",
            "web/test/local-channels.test.cjs",
        ):
            suite = text(path)
            self.assertIn("nearbyMarketsWithDistance", suite, path)
            self.assertIn("normalizePlace", suite, path)


class LinuxShipsInThisReleaseTests(unittest.TestCase):
    """The packaging from 1.1.18, plus the release that carries its files."""

    def test_the_linux_build_is_dispatched_at_the_tag_the_release_points_at(self):
        publish = text(".github/workflows/publish-release.yml")
        self.assertIn('gh workflow run linux-build.yml --ref "$TAG" -f channel=stable', publish)
        # The installers attach only when the tag's commit is the build's commit,
        # which is why 1.1.18's assets stayed in an Actions artifact.
        linux = text(".github/workflows/linux-build.yml")
        self.assertIn('tagged=$(git ls-remote origin "refs/tags/$tag"', linux)
        self.assertIn('gh release upload "$tag"', linux)

    def test_the_desktop_updater_still_offers_only_this_platform(self):
        policy = text(f"{APP}/src/main/update-policy.js")
        self.assertIn("PremiumTV-${version}-linux-${macArch(arch)}.AppImage", policy)
        self.assertIn("SHA256SUMS-linux.txt", policy)


if __name__ == "__main__":
    unittest.main()
