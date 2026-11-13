"""App-only 1.1.6 navigation and setup contracts (device smoke tests run in CI)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UI = ROOT / 'android/app/src/main/kotlin/com/premiumtv/app/ui'


class App116Tests(unittest.TestCase):
    def test_android_starts_with_categories_and_keeps_selection_over_playback(self):
        root = (UI / 'AppRoot.kt').read_text()
        home = (UI / 'HomeScreen.kt').read_text()
        self.assertIn('var selectedCategory by rememberSaveable', root)
        self.assertIn('onCategoryChange = { selectedCategory = it }', root)
        self.assertIn('if (selectedCategory == null && matches == null)', home)
        self.assertIn('onCategoryChange(it ?: SHELF_ALL)', home)
        self.assertIn('SHELF_ALL -> library.channels', home)
        self.assertIn('library.channels.filter { it.group == selectedCategory }', home)
        self.assertIn('MiniAction("◀ All categories")', home)
        self.assertIn('Searching every category', home)

    def test_setup_does_not_replace_existing_shelves(self):
        root = (UI / 'AppRoot.kt').read_text()
        setup = (UI / 'SetupDialog.kt').read_text()
        shelves = (UI / 'PersonalShelves.kt').read_text()
        self.assertIn('"premiumtv_setup"', root)
        self.assertIn('"premiumtv_personal"', shelves)
        self.assertIn('putBoolean("complete", true)', root)
        self.assertIn('onComplete("Viewer")', setup)
        self.assertIn('Multiple profiles and cloud sync are not available yet', setup)

    def test_tv_launcher_banner_is_declared_and_both_app_icons_exist(self):
        manifest = (ROOT / 'android/app/src/main/AndroidManifest.xml').read_text()
        self.assertIn('android:banner="@drawable/tv_banner"', manifest)
        for path in ('android/app/src/main/res/drawable-nodpi/tv_banner.png',
                     'android/art/app-icon.png', 'macos/app/build/icon.png'):
            self.assertTrue((ROOT / path).is_file(), path)

    def test_android_smoke_gate_visits_new_flow(self):
        smoke = (ROOT / 'android/tools/smoke_apk.py').read_text()
        self.assertIn('"Welcome to PremiumTV" in texts', smoke)
        self.assertIn('"category picker"', smoke)
        self.assertIn('"a visible channel card"', smoke)


if __name__ == '__main__':
    unittest.main()
