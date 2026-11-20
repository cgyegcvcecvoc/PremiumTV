"""Android unit tests must not depend on Robolectric's runtime Maven fetch.

The 2026-11-19 Android unit-test run failed 21 of 92 tests, all with
`MavenArtifactFetcher` / `HttpURLConnection` IOExceptions: Robolectric tried to
download its SDK 28 runtime jar directly from Maven Central during the test
run. Gradle now resolves the exact jars and copies them to a local dependency
directory, which `robolectric.dependency.dir` reads without a network call.
"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRADLE = ROOT / "android" / "app" / "build.gradle.kts"
CI = ROOT / ".github" / "workflows" / "ci.yml"
README = ROOT / "android" / "README.md"


class HermeticRobolectricTests(unittest.TestCase):
    def test_the_sdk_28_runtime_is_resolved_by_gradle_and_used_offline(self):
        text = GRADLE.read_text(encoding="utf-8")
        self.assertIn("robolectric.dependency.dir", text)
        self.assertIn(
            'add("robolectricSdk28", "org.robolectric:android-all-instrumented:9-robolectric-4913185-2-i7")',
            text,
        )
        self.assertIn(
            'add("robolectricSdk28", "org.robolectric:android-all:9-robolectric-4913185-2")',
            text,
        )
        self.assertIn("isTransitive = false", text)
        self.assertIn("tasks.withType<Test>().configureEach", text)
        self.assertIn("dependsOn(copyRobolectricSdk)", text)

    def test_the_sdk_28_tests_are_still_pinned_to_sdk_28(self):
        for name in (
            "android/app/src/test/kotlin/com/premiumtv/app/data/TvRepositoryTest.kt",
            "android/app/src/test/kotlin/com/premiumtv/app/ui/VodShelfTest.kt",
        ):
            self.assertIn("@Config(sdk = [28]", (ROOT / name).read_text(encoding="utf-8"))

    def test_ci_runs_the_unit_tests_and_the_readme_explains_the_fix(self):
        self.assertIn("./gradlew --no-daemon testDebugUnitTest",
                      CI.read_text(encoding="utf-8"))
        self.assertIn("robolectric.dependency.dir", README.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
