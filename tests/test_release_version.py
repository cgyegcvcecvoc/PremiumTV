"""Tests for the shared release-version policy.

The Android updater, the Mac updater and the release guard all rely on these
rules: a stable release above the installed version is an update; anything
older, equal, draft or pre-release is not, and Android's versionCode always
increases with the version.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import release_version  # noqa: E402

SCRIPT = ROOT / "scripts" / "release_version.py"


class VersionParsingTests(unittest.TestCase):
    def test_accepts_tags_and_build_suffixes(self):
        self.assertEqual(release_version.parse_version("1.0.4"), (1, 0, 4))
        self.assertEqual(release_version.parse_version("v1.0.4"), (1, 0, 4))
        self.assertEqual(release_version.parse_version("1.0.4-debug"), (1, 0, 4))
        self.assertEqual(release_version.parse_version("v1.1.1-preview"), (1, 1, 1))
        self.assertEqual(release_version.parse_version("1.0.6.1"), (1, 0, 6, 1))
        self.assertEqual(release_version.parse_version("v1.0.6.1-debug"), (1, 0, 6, 1))
        self.assertEqual(release_version.normalize_version("v1.0.4-debug"), "1.0.4")
        self.assertEqual(release_version.normalize_version("v1.0.6.1-debug"), "1.0.6.1")
        self.assertEqual(release_version.tag_for("1.0.4"), "v1.0.4")
        self.assertEqual(release_version.canonical_version("1.0.7"), "1.0.6.1")
        self.assertEqual(release_version.canonical_version("1.0.6.1"), "1.0.6.1")
        self.assertTrue(release_version.is_compatibility_alias("1.0.7", "1.0.6.1"))
        self.assertFalse(release_version.is_compatibility_alias("1.0.7", "1.0.6"))

    def test_rejects_versions_this_project_does_not_write(self):
        for value in ("", "latest", "1.0", "1.0.4.1.2", "v1.0.x", "1.0.4 beta"):
            self.assertIsNone(release_version.parse_version(value), value)

    def test_macos_version_uses_the_three_part_compatibility_build(self):
        # electron-builder rejects a four-part version, so the Mac installers
        # are built as the alias and live on that alias release.
        self.assertEqual(release_version.macos_version("1.0.6.1"), "1.0.7")
        self.assertEqual(release_version.macos_version("v1.0.5-debug"), "1.0.5")
        self.assertEqual(release_version.macos_version("1.0.7"), "1.0.7")
        self.assertEqual(release_version.macos_version("1.1.1"), "1.1.1")
        self.assertIsNone(release_version.macos_version("nonsense"))
        self.assertIsNone(release_version.macos_version("1.0.9.2"),
                          "a four-part version without an alias cannot be packaged")

    def test_1_0_9_is_a_real_release_and_the_v_series_is_retired(self):
        # 1.0.9 briefly existed as the compatibility alias of 1.0.8.1 (the
        # only V patch ever cut); it then became a real release - the
        # crash-on-watch fix - and the V scheme ended with it: no four-part
        # releases and no forward aliases (a real 1.0.10 must never read as
        # the alias of a 1.0.8.2 that was never published).
        self.assertEqual(release_version.canonical_version("1.0.9"), "1.0.9")
        self.assertEqual(release_version.canonical_version("1.0.10"), "1.0.10")
        self.assertFalse(release_version.is_compatibility_alias("1.0.9", "1.0.8.1"))
        self.assertFalse(release_version.is_compatibility_alias("1.0.10", "1.0.8.2"))
        self.assertIsNone(release_version.macos_version("1.0.8.1"),
                          "a four-part version without a historical alias cannot be packaged")
        # The historical names still resolve: old tags and documents use them.
        self.assertEqual(release_version.display_version("1.0.8.1"), "1.0.8 V1")
        self.assertEqual(release_version.display_version("1.0.8"), "1.0.8")
        self.assertEqual(release_version.display_version("1.0.9"), "1.0.9")
        self.assertEqual(release_version.patch_version("1.0.8", 1), "1.0.8.1")
        # Codes still order the whole history, patch era included.
        self.assertEqual(release_version.android_version_code("1.0.8"), 100_080_000)
        self.assertEqual(release_version.android_version_code("1.0.8.1"), 100_080_001)
        self.assertEqual(release_version.android_version_code("1.0.9"), 100_090_000)
        self.assertTrue(release_version.is_newer("1.0.9", "1.0.8.1"))
        self.assertTrue(release_version.is_newer("1.0.8.1", "1.0.8"))

    def test_semantic_ordering_is_numeric_not_lexical(self):
        self.assertTrue(release_version.is_newer("1.0.10", "1.0.9"))
        self.assertTrue(release_version.is_newer("1.0.6.1", "1.0.6"))
        self.assertTrue(release_version.is_newer("1.1.0", "1.0.6.1"))
        self.assertFalse(release_version.is_newer("1.0.6.1", "1.1.0"))
        self.assertTrue(release_version.is_newer("1.1.0", "1.0.99"))
        self.assertTrue(release_version.is_newer("2.0.0", "1.99.99"))
        self.assertFalse(release_version.is_newer("1.0.3", "1.0.4"))
        self.assertFalse(release_version.is_newer("1.1.1", "1.1.1"))
        self.assertFalse(release_version.is_newer("garbage", "1.0.4"))


class AndroidVersionCodeTests(unittest.TestCase):
    def test_codes_are_monotonic_and_above_every_historical_code(self):
        versions = ["1.0.4", "1.0.5", "1.0.10", "1.0.6.1", "1.1.0", "1.1.1", "1.2.0", "2.0.0"]
        versions = sorted(versions, key=lambda value: release_version._pad(release_version.parse_version(value)))
        codes = [release_version.android_version_code(v) for v in versions]
        self.assertEqual(codes, sorted(codes))
        self.assertEqual(len(codes), len(set(codes)))
        # The original published previews used 7, 8, 9, 10 and 11.  Every
        # future code must install over all of them.
        self.assertGreater(min(codes), 11)
        self.assertEqual(release_version.android_version_code("1.0.4"), 100_040_000)
        self.assertEqual(release_version.android_version_code("1.1.1"), 101_010_000)
        # 1.0.6.1 must install over the retired preview's published code.
        self.assertGreater(release_version.android_version_code("1.0.6.1"), 100_010_001)
        self.assertEqual(release_version.android_version_code("1.0.6.1"), 100_060_001)
        self.assertGreater(
            release_version.android_version_code("1.0.6.1"),
            release_version.android_version_code("1.0.6"),
        )

    def test_the_derived_code_fits_an_android_int(self):
        code = release_version.android_version_code("21.0.0")
        self.assertLessEqual(code, release_version.ANDROID_CODE_MAX)
        with self.assertRaises(ValueError):
            release_version.android_version_code("22.0.0")
        with self.assertRaises(ValueError):
            release_version.android_version_code("1.100.0")

    def test_cli_prints_the_code(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--code", "1.0.6.1"],
            capture_output=True, text=True, check=True,
        )
        self.assertEqual(result.stdout.strip(), "100060001")

    def test_cli_prints_the_canonical_version_behind_an_alias(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--canonical", "v1.0.7"],
            capture_output=True, text=True, check=True,
        )
        self.assertEqual(result.stdout.strip(), "1.0.6.1")


def release(tag: str, *, draft: bool = False, prerelease: bool = False) -> dict:
    return {
        "tag": tag,
        "draft": draft,
        "prerelease": prerelease,
        "assets": [
            {"name": f"PremiumTV-{tag[1:]}-debug.apk"},
            {"name": f"PremiumTV-{tag[1:]}-mac-arm64.dmg"},
            {"name": f"PremiumTV-{tag[1:]}-mac-x64.dmg"},
        ],
    }


class GhReleaseListFormatTests(unittest.TestCase):
    """`gh release list --json` returns camelCase keys, not the REST names."""

    def test_gh_release_list_shape_is_understood(self):
        releases = [
            {"tagName": "v1.0.4", "isPrerelease": False, "isDraft": False},
            {"tagName": "v1.0.3", "isPrerelease": False, "isDraft": False},
            {"tagName": "v1.1.1", "isPrerelease": True, "isDraft": False},
            {"tagName": "v1.0.5", "isPrerelease": False, "isDraft": True},
        ]
        self.assertEqual(release_version.newest_stable(releases), "1.0.4")
        status, message = release_version.guard("v1.0.4", releases)
        self.assertEqual(status, 0)
        self.assertIn("above the previous stable v1.0.3", message)
        status, message = release_version.guard("v1.0.3", releases)
        self.assertEqual(status, 2)
        self.assertIn("not above the newest stable v1.0.4", message)


class ReleaseGuardTests(unittest.TestCase):
    def test_a_later_compatibility_alias_does_not_demote_the_canonical_release(self):
        # Both releases are published from the same tree; the alias is created
        # after the canonical one, so the guard must not treat it as "newer
        # stable" when it checks 1.0.6.1 (this really happened once and marked
        # 1.0.6.1 as a pre-release).
        releases = [
            {"tag_name": "v1.0.6", "draft": False, "prerelease": False},
            {"tag_name": "v1.0.6.1", "draft": False, "prerelease": False},
            {"tag_name": "v1.0.7", "draft": False, "prerelease": False},
        ]
        status, message = release_version.guard("v1.0.6.1", releases)
        self.assertEqual(status, 0, message)
        self.assertIn("above the previous stable v1.0.6", message)
        status, message = release_version.guard("v1.0.7", releases)
        self.assertEqual(status, 0, message)
        self.assertIn("above the previous stable v1.0.6.1", message)
        # A genuinely newer stable still blocks an older canonical release.
        status, message = release_version.guard("v1.0.6", releases)
        self.assertEqual(status, 2, message)
        self.assertIn("not above the newest stable v1.0.6.1", message)

    def test_1_0_9_guards_above_the_v1_history(self):
        # The exact sequence the real 1.0.9 release uses: v1.0.8.1 (the one
        # V patch) is already published above v1.0.8; the real v1.0.9 must
        # guard above it, and re-publishing anything from the patch era
        # afterwards is below the stable and rejected - patches are retired.
        before = [{"tag_name": "v1.0.8", "draft": False, "prerelease": False}]
        status, message = release_version.guard("v1.0.8.1", before)
        self.assertEqual(status, 0, message)
        self.assertIn("above the previous stable v1.0.8", message)
        both = before + [
            {"tag_name": "v1.0.8.1", "draft": False, "prerelease": False},
            {"tag_name": "v1.0.9", "draft": False, "prerelease": False},
        ]
        status, message = release_version.guard("v1.0.9", both)
        self.assertEqual(status, 0, message)
        self.assertIn("above the previous stable v1.0.8.1", message)
        status, message = release_version.guard("v1.0.8.1", both)
        self.assertEqual(status, 2, message)
        self.assertIn("not above the newest stable v1.0.9", message)

    def test_a_documented_bridge_release_passes_even_below_the_stable(self):
        # 1.0.8.2 is the one-time rescue for stranded 1.0.8.1 installs. It is
        # published below the current stable on purpose and must stay a full
        # stable release: the builds it rescues ignore pre-releases, so the
        # guard must neither fail nor demote it. This is the red guard run the
        # v1.0.8.2 release produced before the allowlist existed.
        releases = [
            release("v1.0.8.1"),
            release("v1.0.8.2"),
            release("v1.0.9"),
            release("v1.1.0"),
        ]
        status, message = release_version.guard("v1.0.8.2", releases)
        self.assertEqual(status, 0, message)
        self.assertIn("bridge", message)
        self.assertIn("1.0.9", message)
        # The allowlist is opt-in: any other below-stable tag is still rejected.
        status, message = release_version.guard("v1.0.8.1", releases)
        self.assertEqual(status, 2, message)
        self.assertIn("not above the newest stable", message)

    def test_bridge_release_is_still_version_checked(self):
        # A malformed tag fails closed before the bridge lookup.
        self.assertEqual(release_version.guard("v1.0.8.2.1", [])[0], 1)

    def test_a_newer_stable_release_passes(self):
        releases = [release("v1.0.2"), release("v1.0.3"), release("v1.1.1", prerelease=True)]
        status, message = release_version.guard("v1.0.4", releases)
        self.assertEqual(status, 0, message)
        self.assertIn("above the previous stable v1.0.3", message)

    def test_a_release_below_the_stable_is_rejected(self):
        releases = [release("v1.0.3"), release("v1.0.4"), release("v1.1.1", prerelease=True)]
        status, message = release_version.guard("v1.0.3", releases)
        self.assertEqual(status, 2)
        self.assertIn("not above the newest stable v1.0.4", message)

    def test_an_equal_release_is_rejected(self):
        releases = [release("v1.0.4")]
        # Even the release being checked is excluded, so there is no previous
        # stable: the very first stable release passes.
        self.assertEqual(release_version.guard("v1.0.4", releases)[0], 0)
        releases.append(release("v1.0.5"))
        self.assertEqual(release_version.guard("v1.0.4", releases)[0], 2)

    def test_drafts_and_previews_do_not_count_as_stable(self):
        releases = [
            release("v1.0.4", draft=True),
            release("v1.1.2", prerelease=True),
            release("v1.0.3"),
        ]
        status, message = release_version.guard("v1.0.5", releases)
        self.assertEqual(status, 0, message)
        self.assertIn("v1.0.3", message)

    def test_malformed_tags_fail_closed(self):
        self.assertEqual(release_version.guard("latest", [])[0], 1)
        self.assertEqual(release_version.guard("v1.0.4.1.2", [])[0], 1)

    def test_guard_reads_the_release_list_from_disk(self):
        releases = [release("v1.0.4")]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "releases.json"
            path.write_text(json.dumps(releases), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--guard", "--tag", "v1.0.3",
                 "--releases", str(path)],
                capture_output=True, text=True,
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn("not above the newest stable", result.stdout)

    def test_github_api_field_names_are_accepted(self):
        releases = [
            {"tag_name": "v1.0.3", "draft": False, "prerelease": False},
            {"tag_name": "v1.0.4", "draft": False, "prerelease": False},
        ]
        self.assertEqual(release_version.newest_stable(releases), "1.0.4")


if __name__ == "__main__":
    unittest.main()
