import tempfile
import unittest
from pathlib import Path
from scripts.health_report import latest_run, render


class HealthReportTest(unittest.TestCase):
    def test_completed_check_includes_unknown_in_strength(self):
        text = render({'checked': True, 'check_completed': True, 'working': 6,
                       'dead': 2, 'unverified': 2, 'sources': {'example': {'status': 'ok'}}})
        self.assertIn('60.0% reachable', text)
        self.assertIn('Unverified: 2', text)
        self.assertIn('example: ok', text)

    def test_incomplete_and_empty_checks_do_not_claim_strength(self):
        self.assertIn('unavailable', render({'checked': True, 'check_completed': False, 'working': 9}))
        self.assertIn('unavailable', render({'checked': True, 'check_completed': True}))
        self.assertIn('No scraper run available', render(None))

    def test_last_valid_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'history'
            path.write_text('{"label":"first"}\n{"label":"last"}\n{broken\n')
            self.assertEqual(latest_run(path)['label'], 'last')
            self.assertIsNone(latest_run(path.with_name('missing')))


if __name__ == '__main__':
    unittest.main()
