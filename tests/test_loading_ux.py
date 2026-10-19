"""Offline release routing and Android activity wiring regression checks."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / 'android/app/src/main/kotlin/com/premiumtv/app/ui'
spec = importlib.util.spec_from_file_location('hub_build_data', ROOT / 'hub/build_data.py')
hub = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hub)


class LoadingUxTests(unittest.TestCase):
    def test_android_busy_panel_and_finish_notice_do_not_replace_channels(self):
        source = (UI / 'HomeScreen.kt').read_text()
        self.assertIn('LibraryActivity(', source)
        self.assertIn('delay(15_000L)', source)
        self.assertIn('refreshInfo.lastMessage', source)
        self.assertIn('val busy = refreshInfo.inProgress || library.guideLoading', source)
        components = (UI / 'Components.kt').read_text()
        self.assertIn('LinearProgressIndicator', components)
        self.assertIn('delay(8_000L)', components)
        self.assertIn('FACT · XMLTV', components)
        self.assertIn('if (active) LoadingTip()', components)

    def test_hub_ignores_draft_and_partial_stable_and_never_promotes_preview(self):
        def release(version, **flags):
            return dict(tag='v' + version, assets=[dict(name=f'PremiumTV-{version}-{suffix}')
                for suffix in ['debug.apk', 'mac-arm64.dmg', 'mac-arm64.pkg', 'mac-x64.dmg', 'mac-x64.pkg']], **flags)
        stable = release('1.0.2')
        next_stable = release('1.0.3', draft=True)
        preview = release('1.1.1', prerelease=True)
        self.assertEqual(hub.release_channels([stable, next_stable, preview]), '1.0.2')
        next_stable['draft'] = False
        missing = next_stable['assets'].pop()
        self.assertEqual(hub.release_channels([stable, next_stable, preview]), '1.0.2')
        next_stable['assets'].append(missing)
        self.assertEqual(hub.release_channels([stable, next_stable, preview]), '1.0.3')

    def test_retired_preview_switch_is_gone_and_assets_stay_exact_sha_guarded(self):
        for name in ('android-build.yml', 'macos-build.yml'):
            workflow = (ROOT / '.github/workflows' / name).read_text()
            self.assertNotIn('v1.1.1', workflow)
            self.assertNotIn('[preview-build]', workflow)
            self.assertIn('keeping its assets', workflow)
            self.assertIn('BUILD-SOURCE-', workflow)
        self.assertFalse((ROOT / '.github/preview-build.txt').exists())

    def test_netlify_no_longer_hardcodes_old_stable_or_embeds_apks(self):
        script = (ROOT / 'hub/static/assets/app.js').read_text()
        self.assertNotIn('a.version === "1.0.2"', script)
        export = (ROOT / 'hub/export_static.py').read_text()
        self.assertNotIn('copy_into("build-out/', export)
        self.assertNotIn('Encore Preview', script)
        self.assertNotIn('previewApk', script)
