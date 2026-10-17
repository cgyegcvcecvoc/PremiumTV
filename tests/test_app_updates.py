"""Static integration checks for the in-app update center.

The sandbox cannot run an Android emulator or a Mac, so these checks guard the
contracts that make updates safe and repeatable:

  * only published stable releases above the installed version are offered;
  * installers are downloaded once, verified against the release checksum and
    reused instead of fetched again;
  * Settings exposes check / download / install on both platforms;
  * a stable release that is not above the current stable is demoted by the
    release guard.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANDROID = ROOT / "android" / "app" / "src" / "main"
UPDATE = ANDROID / "kotlin" / "com" / "premiumtv" / "app" / "update"
HOME = ANDROID / "kotlin" / "com" / "premiumtv" / "app" / "ui" / "HomeScreen.kt"
MANIFEST = ANDROID / "AndroidManifest.xml"
MAC = ROOT / "macos" / "app"
MAC_UPDATE = MAC / "src" / "main" / "updater.js"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class AndroidUpdateTests(unittest.TestCase):
    def test_manifest_declares_the_installer_permission_and_file_provider(self):
        manifest = text(MANIFEST)
        self.assertIn("android.permission.REQUEST_INSTALL_PACKAGES", manifest)
        self.assertIn("androidx.core.content.FileProvider", manifest)
        self.assertIn('android:authorities="${applicationId}.updates"', manifest)
        self.assertIn("@xml/update_paths", manifest)
        paths = text(ANDROID / "res" / "xml" / "update_paths.xml")
        self.assertIn('<files-path name="updates" path="updates/" />', paths)

    def test_checker_reads_only_complete_stable_releases(self):
        manager = text(UPDATE / "AppUpdateManager.kt")
        self.assertIn("releases?per_page=30", manager)
        self.assertIn('release.optBoolean("draft")', manager)
        self.assertIn('release.optBoolean("prerelease")', manager)
        self.assertIn("PremiumTV-$version-debug.apk", manager)
        self.assertIn('"SHA256SUMS-android.txt"', manager)
        self.assertIn("AppVersions.isNewer(version, currentVersion)", manager)
        # The update is offered only when its own APK exists, not merely when
        # the release exists.
        self.assertIn("val apk = findAsset(assets", manager)

    def test_daily_check_is_conditional_and_never_downloads_automatically(self):
        manager = text(UPDATE / "AppUpdateManager.kt")
        self.assertIn("CHECK_INTERVAL_MILLIS = 24L * 60L * 60L * 1000L", manager)
        self.assertIn('setRequestProperty("If-None-Match", etag)', manager)
        self.assertIn("HTTP_NOT_MODIFIED", manager)
        # The only installer download is inside downloadLocked, called by the
        # Settings action; checkLocked contains no file download.
        check_part = manager.split("private fun checkLocked", 1)[1].split(
            "private data class SelectedUpdate", 1)[0]
        self.assertNotIn("FileOutputStream", check_part)
        self.assertIn("suspend fun download()", manager)

    def test_a_verified_installer_is_reused_once_per_version(self):
        manager = text(UPDATE / "AppUpdateManager.kt")
        self.assertIn("before.downloadedVersion == version && target.isFile", manager)
        self.assertIn("it will not be downloaded again", manager)
        self.assertIn("verifyChecksum(part, target.name)", manager)
        self.assertIn("sha256(file).equals(expected, ignoreCase = true)", manager)
        self.assertIn("directory.listFiles()?.forEach", manager)

    def test_installer_uses_android_package_installer_not_a_silent_install(self):
        installer = text(UPDATE / "UpdateInstaller.kt")
        self.assertIn("FileProvider.getUriForFile", installer)
        self.assertIn('"${BuildConfig.APPLICATION_ID}.updates"', installer)
        self.assertIn("application/vnd.android.package-archive", installer)
        self.assertIn("ACTION_MANAGE_UNKNOWN_APP_SOURCES", installer)
        self.assertNotIn("PackageInstaller", installer)  # no silent session commit

    def test_settings_exposes_the_update_actions(self):
        home = text(HOME)
        for expected in (
            '"App updates"',
            '"Check for updates"',
            '"Download update"',
            '"Install update"',
            "updateInfo.updateAvailable",
            "onCheckForUpdate",
            "onDownloadUpdate",
            "onInstallUpdate",
        ):
            self.assertIn(expected, home)
        view_model = text(ANDROID / "kotlin" / "com" / "premiumtv" / "app" / "TvViewModel.kt")
        self.assertIn("updateManager.checkIfDue()", view_model)
        self.assertIn("updateManager.check(force = true)", view_model)
        self.assertIn("updateManager.download()", view_model)
        self.assertIn("updateManager.installDownloaded()", view_model)

    def test_version_is_one_policy_above_every_historical_code(self):
        gradle = text(ROOT / "android" / "app" / "build.gradle.kts")
        self.assertIn('orElse("1.0.4")', gradle)
        self.assertIn('orElse("100000004")', gradle)


class MacUpdateTests(unittest.TestCase):
    def test_update_policy_rejects_drafts_previews_and_older_versions(self):
        policy = text(MAC / "src" / "main" / "update-policy.js")
        self.assertIn("release.draft || release.prerelease", policy)
        self.assertIn("isNewer(version, current)", policy)
        self.assertIn("macAssetName(version, arch)", policy)
        self.assertIn("SHA256SUMS-macos.txt", policy)

    def test_updater_is_throttled_conditional_and_downloads_once(self):
        updater = text(MAC_UPDATE)
        self.assertIn("CHECK_INTERVAL_MS = 24 * 60 * 60 * 1000", updater)
        self.assertIn("If-None-Match", updater)
        self.assertIn("response.status === 304", updater)
        self.assertIn("state.downloadedVersion === version && fs.existsSync(target)", updater)
        self.assertIn("it will not be downloaded again", updater)
        self.assertIn("verifyChecksum(part, path.basename(target))", updater)
        self.assertIn("sha256File", updater)

    def test_mac_settings_and_bridge_wire_the_update_actions(self):
        main = text(MAC / "src" / "main" / "main.js")
        for channel in (
            "'ptv:check-update'",
            "'ptv:download-update'",
            "'ptv:install-update'",
            "'ptv:open-release'",
        ):
            self.assertIn(channel, main)
        self.assertIn("updater.start()", main)
        self.assertIn("updates: updater ? updater.status() : null", main)
        preload = text(MAC / "src" / "main" / "preload.js")
        self.assertIn("checkForUpdate:", preload)
        self.assertIn("downloadUpdate:", preload)
        self.assertIn("installUpdate:", preload)
        self.assertIn("onUpdate:", preload)
        renderer = text(MAC / "src" / "renderer" / "app.js")
        for expected in (
            "<h2>App updates</h2>",
            "Check for updates",
            "Download update",
            "Open installer",
            "api.checkForUpdate(true)",
            "api.installUpdate()",
        ):
            self.assertIn(expected, renderer)

    def test_app_version_is_1_0_4(self):
        package = json.loads(text(MAC / "package.json"))
        self.assertEqual(package["version"], "1.0.4")


class AndroidSigningTests(unittest.TestCase):
    """The update chain only works if every APK shares one signing identity."""

    def test_long_lived_update_keystore_is_committed_and_pinned(self):
        keystore = ROOT / "android" / "keystore" / "premiumtv-updates.p12"
        fingerprint = ROOT / "android" / "keystore" / "fingerprint.txt"
        self.assertTrue(keystore.is_file(), "the update keystore must be committed")
        self.assertGreater(keystore.stat().st_size, 1000)
        pin = text(fingerprint).strip()
        self.assertRegex(pin, r"^[0-9a-f]{64}$")
        # Pinned deliberately: changing this key breaks in-place updates for
        # every installed 1.0.4+ app.
        self.assertEqual(
            pin,
            "18baf0dc6ed12d263b02f7cf7d69f1275b9c3d5357a81160182567c917e7a7eb",
        )

    def test_gradle_signs_every_debug_apk_with_the_pinned_key(self):
        gradle = text(ROOT / "android" / "app" / "build.gradle.kts")
        self.assertIn('"keystore/premiumtv-updates.p12"', gradle)
        self.assertIn('create("updates")', gradle)
        self.assertIn('storeType = "PKCS12"', gradle)
        self.assertIn('keyAlias = updateKeyAlias', gradle)
        self.assertIn('signingConfig = signingConfigs.getByName("updates")', gradle)
        self.assertIn("PREMIUMTV_ANDROID_KEYSTORE", gradle)

    def test_ci_verifies_the_apk_certificate_matches_the_pin(self):
        workflow = text(ROOT / ".github" / "workflows" / "android-build.yml")
        self.assertIn("android/keystore/fingerprint.txt", workflow)
        self.assertIn("keytool -printcert -jarfile", workflow)
        self.assertIn("does not match the pinned update key", workflow)
        self.assertLess(
            workflow.index("Verify the update signing identity"),
            workflow.index("Attach the APKs to the release"),
        )

    def test_upgrade_note_explains_the_one_time_uninstall(self):
        updates = text(ROOT / "docs" / "UPDATES.md")
        self.assertIn("same signing certificate", updates)
        self.assertIn("uninstall it once", updates)
        notes = text(ROOT / "release-notes-1.0.4.md")
        self.assertIn("uninstall it once", notes)
        readme = text(ROOT / "android" / "README.md")
        self.assertIn("android/keystore/", readme)


class ReleasePolicyTests(unittest.TestCase):
    def test_release_guard_demotes_out_of_order_stable_releases(self):
        guard = text(ROOT / ".github" / "workflows" / "release-guard.yml")
        self.assertIn("release:", guard)
        self.assertIn("types: [published]", guard)
        self.assertIn("scripts/release_version.py", guard)
        self.assertIn('--guard --tag "$TAG" --releases', guard)
        self.assertIn('gh release edit "$TAG" --prerelease', guard)
        self.assertIn('github.event.release.prerelease == false', guard)

    def test_both_platform_workflows_are_generic_and_build_every_release(self):
        for name in ("android-build.yml", "macos-build.yml"):
            workflow = text(ROOT / ".github" / "workflows" / name)
            self.assertIn("workflow_dispatch:", workflow)
            self.assertIn("type: string", workflow)
            self.assertIn("channel:", workflow)
            self.assertIn("scripts/release_version.py", workflow)
            self.assertNotIn("github.event.release.tag_name ==", workflow)
            self.assertNotIn("v1.1.1:false", workflow)

    def test_1_0_4_is_the_documented_stable_release(self):
        for name in ("README.md", "android/README.md", "release-notes-1.0.4.md",
                     "docs/UPDATES.md"):
            source = text(ROOT / name)
            self.assertIn("1.0.4", source, name)
        notes = text(ROOT / "release-notes-1.0.4.md")
        self.assertIn("last version that has to be downloaded by", notes)
        self.assertIn("100000004", notes)
        updates = text(ROOT / "docs" / "UPDATES.md")
        self.assertIn("One download per version", updates)


if __name__ == "__main__":
    unittest.main()
