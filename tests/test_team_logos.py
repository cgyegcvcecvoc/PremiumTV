"""Regression checks for the bundled, exact-name team crest catalog."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TeamLogoTests(unittest.TestCase):
    def test_pro_teams_have_real_image_urls(self):
        logos = json.loads((ROOT / 'playlists/team-logos.json').read_text())['logos']
        for name, league in [('philadelphiaeagles', 'nfl'), ('losangeleslakers', 'nba'),
                             ('philadelphiaphillies', 'mlb'), ('philadelphiaflyers', 'nhl'),
                             ('newyorkliberty', 'wnba')]:
            self.assertIn(f'/teamlogos/{league}/', logos[name])
            self.assertTrue(logos[name].startswith('https://'))
        self.assertNotIn('ny', logos)  # ambiguous short names should not guess

    def test_android_can_decode_bundled_svg_crests_and_retry_new_images(self):
        app = (ROOT / 'android/app/src/main/kotlin/com/premiumtv/app/PremiumTvApplication.kt').read_text()
        home = (ROOT / 'android/app/src/main/kotlin/com/premiumtv/app/ui/HomeScreen.kt').read_text()
        gradle = (ROOT / 'android/app/build.gradle.kts').read_text()
        self.assertIn('coil-svg:2.6.0', gradle)
        self.assertIn('SvgDecoder.Factory()', app)
        self.assertIn('remember(name, logoUrl) { mutableStateOf(false) }', home)
