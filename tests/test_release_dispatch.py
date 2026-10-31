import unittest
from pathlib import Path


class ReleaseDispatchTest(unittest.TestCase):
    def test_token_created_release_dispatches_builds_at_tag_and_waits(self):
        workflow = (Path(__file__).resolve().parents[1] / '.github/workflows/publish-release.yml').read_text()
        self.assertIn('actions: write', workflow)
        self.assertIn('gh workflow run android-build.yml --ref "$TAG"', workflow)
        self.assertIn('gh workflow run macos-build.yml --ref "$TAG"', workflow)
        self.assertIn('PremiumTV-$VERSION-debug.apk', workflow)
        self.assertIn('for arch in arm64 x64', workflow)
        self.assertIn('for ext in dmg pkg', workflow)
        self.assertIn('gh workflow run pages.yml --ref main', workflow)
        self.assertLess(workflow.index('if [ "${#missing[@]}" -eq 0 ]'), workflow.index('gh workflow run pages.yml --ref main'))


if __name__ == '__main__':
    unittest.main()
