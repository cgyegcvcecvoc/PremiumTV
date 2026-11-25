import tempfile
import unittest
from pathlib import Path
import json

from scripts.health_report import attach_details, latest_run, render, server_failures


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

    def test_a_failing_server_and_a_dead_channel_are_named(self):
        run = {
            'checked': True, 'check_completed': True, 'working': 10,
            'dead': 3, 'unverified': 1,
            'dead_details': [
                {'name': 'BBC America', 'url': 'http://23.237.104.106:8080/bbc/index.m3u8',
                 'reason': 'HTTP 404'},
                {'name': 'BBC America (Backup 1)', 'url': 'http://23.237.104.106:8080/bbc/b.m3u8',
                 'reason': 'HTTP 404'},
                {'name': 'Other', 'url': 'https://cdn.example.test/other.m3u8',
                 'reason': 'dns lookup failed'},
            ],
            'unverified_details': [
                {'name': 'Slow', 'url': 'https://cdn.example.test/slow.m3u8'},
            ],
            'sources': {'example': {'status': 'ok', 'alive': 10, 'dead': 3, 'unverified': 1}},
        }
        text = render(run)
        self.assertIn('Servers with failing links:', text)
        self.assertIn('23.237.104.106:8080: 2 confirmed dead', text)
        self.assertIn('cdn.example.test: 1 confirmed dead, 1 unverified', text)
        self.assertIn('Channels confirmed dead:', text)
        self.assertIn('BBC America (HTTP 404)', text)
        rows = server_failures(run)
        self.assertEqual('23.237.104.106:8080', rows[0][0])

    def test_a_run_without_details_still_renders(self):
        text = render({'checked': True, 'check_completed': True, 'working': 1})
        self.assertIn('No per-server failures recorded', text)
        self.assertIn('None recorded in this run', text)

    def test_details_are_joined_only_for_the_same_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'report.json'
            path.write_text(json.dumps({
                'run_id': 'run-2',
                'dead': [{'name': 'Gone', 'url': 'https://dead.example/x.m3u8', 'reason': 'HTTP 410'}],
            }))
            self.assertEqual([], attach_details({'run_id': 'run-1'}, path).get('dead_details', []))
            merged = attach_details({'run_id': 'run-2'}, path)
            self.assertEqual('Gone', merged['dead_details'][0]['name'])


if __name__ == '__main__':
    unittest.main()
