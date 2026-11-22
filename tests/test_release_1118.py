"""1.1.18 contracts: the Linux desktop, and the two builds that never asked.

Three things were broken at once, and none of them showed up as an error:

* **There was no Linux build.** The desktop app is Electron and nothing in it is
  Mac-specific, but the packaging config, the CI matrix and the in-app updater all
  knew one platform only - so the updater would have offered a Linux install the
  Mac ``.dmg`` from the same release, because the release page carries it.
* **macOS never showed the location prompt.** ``navigator.geolocation`` was
  plumbed correctly; Electron denies the request before the UI appears when the
  bundle has no ``NSLocationUsageDescription``, and the renderer reported that
  silent denial as "Location was declined".
* **Android asked nothing.** The manifest declared ``ACCESS_COARSE_LOCATION``
  only - so the permission prompt itself was auto-denied on every device - and the
  dialog read ``getLastKnownLocation()``, which is empty in the moment right after
  a first grant, so even a "yes" ended at "No location fix is available".

And the local lineup is sparse enough (Pennsylvania publishes Philadelphia and
Pittsburgh) that a correct nearest-market lookup still told a viewer in
Wilkes-Barre they were in Philadelphia.

This file pins the shape of all four fixes so a later edit cannot quietly undo a
platform, a usage string, a permission or the distance rule.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

APP = "macos/app"
ANDROID = "android/app/src/main"


def text(path: str | Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class Version1118Tests(unittest.TestCase):
    """The release number and its notes come from the version tooling."""

    def test_the_release_is_synced_across_every_surface(self):
        import release_version  # noqa: E402
        import version_sync  # noqa: E402

        # 1.1.18 is published and 1.1.19 is the build in progress, so the
        # current-version pin lives in tests/test_release_1119.py; this keeps
        # 1.1.18's own artifacts and version math in place.
        self.assertEqual(release_version.android_version_code("1.1.18"), 101_180_000)
        self.assertEqual(release_version.compare_versions("1.1.18", "1.1.17"), 1)
        self.assertEqual(version_sync.check(), [])
        self.assertTrue(
            release_version.is_newer(version_sync.PUBLISHED_VERSION, "1.1.17"),
            "the published version must be at least 1.1.18",
        )

        notes = text("release-notes-1.1.18.md")
        self.assertIn("# PremiumTV 1.1.18 — ", notes)
        self.assertIn("versionCode `101180000`", notes)

    def test_the_notes_follow_the_short_notes_rule(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "new_version.py"), "--check-notes", "1.1.18"],
            cwd=ROOT, capture_output=True, text=True, timeout=120,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class LinuxBuildTests(unittest.TestCase):
    """A Linux edition that is packaged, published and updatable."""

    def test_the_packager_builds_linux_installers(self):
        builder = text(f"{APP}/electron-builder.yml")
        self.assertIn("\nlinux:", builder)
        linux = builder[builder.index("\nlinux:"):]
        for target in ("AppImage", "deb", "tar.xz"):
            self.assertIn(f"target: {target}", linux)
        for arch in ("x64", "arm64"):
            self.assertIn(arch, linux)
        # The file name has to say which platform it is, or a release page gets
        # two files called PremiumTV-1.1.18 and nothing to tell them apart.
        self.assertIn("artifactName: PremiumTV-${version}-linux-${arch}.${ext}", linux)
        self.assertIn("executableName: premiumtv", linux)
        self.assertIn("category: AudioVideo", linux)

    def test_a_ci_job_builds_and_attaches_them(self):
        workflow = text(".github/workflows/linux-build.yml")
        self.assertIn("name: Build PremiumTV Linux AppImage + DEB", workflow)
        self.assertIn("runs-on: ubuntu-24.04", workflow)
        # One invocation per format, so a broken AppImage packer cannot also
        # cost the formats a viewer can install - and so the arch list on the
        # command line cannot override the per-format arch list in the config.
        self.assertIn('build() {', workflow)
        self.assertIn("if ! build deb --x64 --arm64; then", workflow)
        self.assertIn("if ! build tar.xz --x64; then", workflow)
        self.assertIn("if ! build AppImage --x64 --arm64; then", workflow)
        self.assertIn("-p never", workflow)
        # electron-builder writes x86_64 / amd64 / x64 for the same architecture;
        # the updater, this job's guard and the download page all use the
        # canonical `-linux-x64` name, so the job has to produce it.
        self.assertIn("Normalize the installer names", workflow)
        self.assertIn('mv -f "$src" "PremiumTV-${LINUX_VERSION}-linux-x64.${ext}"', workflow)
        # squashfs-tools is not on the runner image, and its absence looks like a
        # config bug ("cannot execute mksquashfs").
        self.assertIn("squashfs-tools", workflow)
        # The failure report is how a log got read at all from an environment
        # that cannot reach the Actions log host.
        self.assertIn("/comments\"", workflow)
        # -p never: no electron-updater metadata, because the app reads the
        # GitHub release list itself and a latest-linux.yml would promise a
        # channel that does not exist.
        self.assertNotIn("--publish always", workflow)
        self.assertIn("xvfb-run -a dist/linux-unpacked/premiumtv", workflow)
        self.assertIn("--smoke-test", workflow)
        self.assertIn("SHA256SUMS-linux.txt", workflow)
        self.assertIn("gh release upload", workflow)

    def test_the_publish_workflow_starts_linux_but_does_not_wait_for_it(self):
        publish = text(".github/workflows/publish-release.yml")
        self.assertIn("gh workflow run linux-build.yml --ref \"$TAG\" -f channel=stable", publish)
        # The required list stays Android + macOS: a Linux build that fails must
        # not hold the APK and the Mac disk images hostage.
        required = publish[publish.index("required=("):publish.index("deadline=")]
        self.assertNotIn("AppImage", required)
        self.assertIn("Linux installers still pending", publish)

    def test_the_hub_and_the_download_site_offer_the_linux_build(self):
        hub = text("hub/static/index.html")
        self.assertIn("All Linux installers", hub)
        self.assertIn("🐧 Linux", hub)
        site = text("scripts/build_site_data.py")
        for kind in ("linux-appimage", "linux-deb", "linux-tar"):
            self.assertIn(kind, site)
        self.assertIn("Linux (x86-64, arm64)", site)
        data = json.loads(text("docs/data/site.json"))
        self.assertIn("Linux (x86-64, arm64)",
                      json.dumps(data))  # the generated copy matches the generator

    def test_the_updater_only_offers_this_platforms_installer(self):
        policy = text(f"{APP}/src/main/update-policy.js")
        self.assertIn("PremiumTV-${version}-linux-${macArch(arch)}.AppImage", policy)
        self.assertIn("SHA256SUMS-linux.txt", policy)
        self.assertIn("function selectStableUpdate(releases, currentVersion, arch = 'arm64', platform = 'darwin')",
                      policy)
        updater = text(f"{APP}/src/main/updater.js")
        self.assertIn("installerAssetName(version, this.arch, this.platform)", updater)
        # An AppImage is run, not mounted: no openPath on a .dmg.
        self.assertIn("fsp.chmod(state.installerPath, 0o755)", updater)


class LocationTests(unittest.TestCase):
    """Both desktop/mobile front ends have to earn the fix they use."""

    def test_the_mac_bundle_says_why_it_wants_location(self):
        builder = text(f"{APP}/electron-builder.yml")
        self.assertIn("NSLocationUsageDescription", builder)
        self.assertIn("NSLocationWhenInUseUsageDescription", builder)
        self.assertIn("NSLocationDefaultAccuracyReduced: true", builder)

    def test_the_renderer_separates_the_ways_location_can_fail(self):
        app = text(f"{APP}/src/renderer/app.js")
        self.assertIn("function describeLocationFailure(", app)
        self.assertIn("hasLocationUsageDescription", text(f"{APP}/src/main/main.js"))
        # One shared ask, used by every entry point, so no path can skip the
        # decline handling again.
        self.assertEqual(app.count("askForLocalMarket("), 3)
        self.assertIn("enableHighAccuracy: false", app)

    def test_android_declares_the_permission_it_asks_for(self):
        manifest = text(f"{ANDROID}/AndroidManifest.xml")
        self.assertIn("android.permission.ACCESS_COARSE_LOCATION", manifest)
        self.assertIn("android.permission.ACCESS_FINE_LOCATION", manifest)
        # Optional so a TV box with no GPS still installs.
        self.assertIn('android:name="android.hardware.location"', manifest)
        self.assertIn('android:required="false"', manifest)

    def test_android_waits_for_a_real_fix_instead_of_the_cache(self):
        dialog = text(f"{ANDROID}/kotlin/com/premiumtv/app/ui/LocalChannelsDialog.kt")
        self.assertIn("RequestMultiplePermissions", dialog)
        self.assertIn("shouldShowRequestPermissionRationale", dialog)
        self.assertIn("awaitCoordinates(", dialog)
        data = text(f"{ANDROID}/kotlin/com/premiumtv/app/data/LocalChannels.kt")
        self.assertIn("suspend fun Context.awaitCoordinates(", data)
        self.assertIn("requestLocationUpdates", data)
        self.assertIn("removeUpdates", data)
        # The invented API from the first draft must not come back.
        self.assertNotIn("elapsedRealtimeAgeMillis", data)

    def test_a_far_market_is_offered_never_applied(self):
        renderer = text(f"{APP}/src/renderer/local-channels.js")
        self.assertIn("const NEAREST_MARKET_MAX_KM = 120", renderer)
        self.assertIn("nearestMarketWithDistance", renderer)
        self.assertIn("marketIsNear", renderer)
        web = text("web/src/app.js")
        self.assertIn("nearestMarketWithDistance", web)
        kotlin = text(f"{ANDROID}/kotlin/com/premiumtv/app/data/LocalChannels.kt")
        self.assertIn("LOCAL_MARKET_NEAR_KM = 120.0", kotlin)
        self.assertIn("fun marketIsNear(", kotlin)


class SourceTests(unittest.TestCase):
    """Sources added because they were measured, not because they are popular."""

    def test_the_new_sources_pass_the_source_contract(self):
        import scraper  # noqa: E402

        data = json.loads(text("sources.json"))
        by_name = {source["name"]: source for source in data["sources"]}
        for name in ("aria-plus", "pluto-us"):
            source = by_name[name]
            self.assertTrue(source["enabled"], name)
            self.assertTrue(source["url"].startswith("https://"), name)
            self.assertIsNone(scraper.source_url_problem(source["url"]), name)
            github = source["github"]
            self.assertIsNone(scraper.github_repo_problem(github["repo"]), name)
            self.assertNotIn("..", github["path"], name)
            self.assertFalse(github["path"].startswith("/"), name)

    def test_the_fast_lineups_get_their_own_guides(self):
        data = json.loads(text("sources.json"))
        fixed = {item["url"]: item for item in data["epg_sources"]["fixed"]}
        self.assertIn(
            "https://raw.githubusercontent.com/matthuisman/i.mjh.nz/master/PlutoTV/us.xml.gz",
            fixed)
        self.assertIn(
            "https://raw.githubusercontent.com/matthuisman/i.mjh.nz/master/SamsungTVPlus/us.xml.gz",
            fixed)

    def test_an_upstream_scratch_label_is_not_a_category(self):
        import categorize  # noqa: E402

        for group in ("TEST", "IPTV", "USA Channels"):
            self.assertFalse(categorize.is_canonical_group(group), group)
        self.assertEqual(categorize.classify("METV TOONS", "USA Channels"), "Cartoons")
        # A real category that merely ends in the word is untouched.
        self.assertTrue(categorize.is_canonical_group("NBC Sports Channels"))


if __name__ == "__main__":
    unittest.main()
