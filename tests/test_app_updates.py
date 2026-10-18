"""Static integration checks for the in-app update center.

The sandbox cannot run an Android emulator or a Mac, so these checks guard the
contracts that make updates safe and repeatable:

  * only published stable releases above the installed version are offered;
  * installers are downloaded once, verified against the release checksum and
    reused instead of fetched again;
  * Settings exposes check / download / install on both platforms;
  * a stable release that is not above the current stable is demoted by the
    release guard;
  * an older build is told to go and get the newest release from GitHub by a
    popup whose wording, version range and end-of-support date are published in
    app-update-notice.json rather than compiled in.
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
MAC_NOTICE = MAC / "src" / "main" / "update-notice.js"
MAC_RENDERER = MAC / "src" / "renderer" / "app.js"
NOTICE_POLICY = UPDATE / "UpdateNotice.kt"
NOTICE_DIALOG = ANDROID / "kotlin" / "com" / "premiumtv" / "app" / "ui" / "UpdateNoticeDialog.kt"
APP_ROOT = ANDROID / "kotlin" / "com" / "premiumtv" / "app" / "ui" / "AppRoot.kt"
VIEW_MODEL = ANDROID / "kotlin" / "com" / "premiumtv" / "app" / "TvViewModel.kt"
M3U_PARSER = ANDROID / "kotlin" / "com" / "premiumtv" / "app" / "data" / "M3uParser.kt"
NOTICE_DOCUMENT = ROOT / "app-update-notice.json"

# The one address both apps read the popup from. It has to be identical, or the
# two platforms would drift apart the first time the wording is changed.
NOTICE_URL = ("https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/"
              "app-update-notice.json")


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
        # `gh release list --json` emits camelCase keys; the parser must read
        # exactly the fields the workflow requests or the guard silently
        # treats every release as absent and always passes.
        self.assertIn("tagName,isPrerelease,isDraft", guard)
        parser = text(ROOT / "scripts" / "release_version.py")
        for field in ("tagName", "isPrerelease", "isDraft"):
            self.assertIn(field, parser)

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


class UpdateNoticePopupTests(unittest.TestCase):
    """The popup that sends an older build to GitHub for the newest release.

    An installed app cannot be given new code, so the message has to come from a
    file the app was already built to fetch. These checks guard that contract on
    both platforms: the same document, the same targeting rule, a popup that is
    dismissible but returns, and an escalation nobody has to ship a build for.
    """

    def test_both_platforms_read_the_same_published_document(self):
        self.assertIn(NOTICE_URL, text(NOTICE_POLICY))
        self.assertIn(NOTICE_URL, text(MAC_NOTICE))
        document = json.loads(text(NOTICE_DOCUMENT))
        self.assertEqual(document["notice_url"], NOTICE_URL)

    def test_the_document_targets_every_build_below_the_one_with_a_popup(self):
        document = json.loads(text(NOTICE_DOCUMENT))
        self.assertEqual(document["schema"], 1)
        self.assertIs(document["enabled"], True)
        self.assertEqual(document["grace_days"], 30)
        self.assertTrue(document["rules"], "a notice with no rules can never be shown")
        targets = [rule["max_version"] for rule in document["rules"]]
        self.assertEqual(max(targets), "1.0.4", "1.0.5 is the first build that can show the popup")
        for rule in document["rules"]:
            self.assertLess(rule["max_version"], "1.0.5",
                            "a rule must never nag the build that can show the popup")
            self.assertIn("min_version", rule)
            self.assertIn("android", rule["platforms"])
            self.assertIn("macos", rule["platforms"])
            # The surprise is the reason to update, so it must be spelled out.
            self.assertIn("itself", rule["surprise"])
            self.assertIn("after_support_ends", rule,
                          "the escalation copy ships in the document, not in a build")
            self.assertEqual(rule["after_support_ends"]["level"], "end_of_support")

    def test_the_notice_is_refused_unless_it_is_enabled_and_a_known_schema(self):
        kotlin = text(NOTICE_POLICY)
        self.assertIn('optBoolean("enabled", false)', kotlin)
        self.assertIn('optInt("schema", 0) != SUPPORTED_SCHEMA', kotlin)
        notice_js = text(MAC_NOTICE)
        self.assertIn("document.enabled !== true", notice_js)
        self.assertIn("Number(document.schema) !== SUPPORTED_SCHEMA", notice_js)
        # Both refuse an unknown schema rather than guessing at moved fields.
        self.assertIn("SUPPORTED_SCHEMA = 1", kotlin)
        self.assertIn("SUPPORTED_SCHEMA = 1;", notice_js)

    def test_targeting_compares_versions_never_strings(self):
        self.assertIn("AppVersions.normalize", text(NOTICE_POLICY))
        self.assertIn("AppVersions.isNewer", text(NOTICE_POLICY))
        notice_js = text(MAC_NOTICE)
        self.assertIn("normalizeVersion(rule.min_version)", notice_js)
        self.assertIn("isNewer(current, max)", notice_js)

    def test_the_daily_check_reads_the_notice_and_caches_it(self):
        manager = text(UPDATE / "AppUpdateManager.kt")
        self.assertIn("KEY_NOTICE_BODY", manager)
        self.assertIn("refreshNoticeLocked(outcome)", manager)
        self.assertIn("UpdateNotice.MAX_NOTICE_BYTES", manager)
        # A throttled launch and a cold start both resolve the cached document,
        # so the popup is decided before any network call.
        self.assertIn("reevaluateNotice(before, now)", manager)
        self.assertIn("notice = UpdateNotice.select(", manager)

        updater = text(MAC_UPDATE)
        self.assertIn("await this.refreshNotice()", updater)
        self.assertIn("noticeBody", updater)
        self.assertIn("withCachedNotice", updater)
        self.assertIn("MAX_NOTICE_BYTES", updater)

    def test_a_notice_failure_can_never_break_the_update_check(self):
        manager = text(UPDATE / "AppUpdateManager.kt")
        refresh = manager.split("private fun refreshNoticeLocked", 1)[1].split(
            "private fun reevaluateNotice", 1)[0]
        self.assertIn("catch (e: Exception)", refresh)
        self.assertIn("keeping the last one", refresh)
        updater = text(MAC_UPDATE)
        body = updater.split("async refreshNotice()", 1)[1].split("reevaluateNotice(", 1)[0]
        self.assertIn("catch (error)", body)

    def test_the_dismissal_is_launch_scoped_on_both_platforms(self):
        manager = text(UPDATE / "AppUpdateManager.kt")
        dismiss = manager.split("fun dismissNotice()", 1)[1].split("private data class", 1)[0]
        self.assertIn("noticeDismissedForLaunch = true", dismiss)
        # It assigns the flow directly rather than publish(), which persists.
        self.assertNotIn("publish(", dismiss)

        updater = text(MAC_UPDATE)
        self.assertIn("noticeDismissedForLaunch: true", updater)
        written = updater.split("writeState()", 1)[1].split("pruneInstallers", 1)[0]
        self.assertIn("noticeDismissedForLaunch: false", written,
                      "a persisted dismissal would hide the notice for good")

    def test_the_android_popup_is_dismissible_and_operable_by_remote(self):
        dialog = text(NOTICE_DIALOG)
        self.assertIn("dismissOnBackPress = true", dialog)
        self.assertIn("dismissOnClickOutside = false", dialog)
        self.assertIn("FocusRequester()", dialog)
        self.assertIn("requestFocus()", dialog)
        self.assertIn("notice.surprise", dialog)
        self.assertIn("notice.releasesUrl", dialog)
        self.assertIn("FocusButton(", dialog)
        # The end-of-support escalation is visibly different, not just reworded.
        self.assertIn("NoticeLevel.EndOfSupport", dialog)
        self.assertIn("LiveRed", dialog)

    def test_the_android_popup_is_shown_but_never_over_a_playing_channel(self):
        root = text(APP_ROOT)
        self.assertIn("UpdateNoticeDialog(", root)
        self.assertIn("updateInfo.noticeVisible", root)
        self.assertIn("playing == null", root)
        self.assertIn("updateManager.dismissNotice()", text(VIEW_MODEL))

    def test_the_mac_popup_renders_the_notice_as_text_not_markup(self):
        renderer = text(MAC_RENDERER)
        block = renderer.split("function renderUpdateNotice()", 1)[1].split(
            "async function dismissUpdateNotice", 1)[0]
        self.assertNotIn("innerHTML", block,
                         "the wording is remote, so it must never be parsed as HTML")
        for field in ("notice.title", "notice.message", "notice.surprise",
                      "notice.releasesUrl", "notice.actionLabel"):
            self.assertIn(field, block)
        self.assertIn("state.noticeDismissedForLaunch", block)
        # Esc dismisses, and the primary action opens the update centre.
        self.assertIn("els.updateNotice && !els.updateNotice.hidden", renderer)
        self.assertIn("selectTab('settings')", renderer)

    def test_the_mac_popup_is_real_markup_the_renderer_can_find(self):
        page = text(MAC / "src" / "renderer" / "index.html")
        self.assertIn('id="update-notice"', page)
        self.assertIn('role="dialog"', page)
        self.assertIn('aria-modal="true"', page)
        for element in ("update-notice-title", "update-notice-surprise",
                        "update-notice-action", "update-notice-dismiss"):
            self.assertIn(f'id="{element}"', page)
        self.assertIn("notice-overlay", text(MAC / "src" / "renderer" / "app.css"))
        self.assertIn("dismissUpdateNotice:", text(MAC / "src" / "main" / "preload.js"))
        self.assertIn("'ptv:dismiss-update-notice'", text(MAC / "src" / "main" / "main.js"))

    def test_the_sanctioned_notice_entry_is_never_a_channel(self):
        kotlin = text(M3U_PARSER)
        self.assertIn('const val NOTICE_ATTR = "tvg-notice"', kotlin)
        self.assertIn('const val NOTICE_VALUE = "app-update"', kotlin)
        self.assertIn("if (skipEntry) {", kotlin)
        javascript = text(MAC / "src" / "main" / "parsers.js")
        self.assertIn("const NOTICE_ATTR = 'tvg-notice';", javascript)
        self.assertIn("if (pending.notice) {", javascript)

    def test_the_popup_is_documented_where_the_update_rules_are(self):
        updates = text(ROOT / "docs" / "UPDATES.md")
        self.assertIn("app-update-notice.json", updates)
        self.assertIn("popup", updates.lower())
        self.assertIn("end-of-support", updates.lower())


if __name__ == "__main__":
    unittest.main()
