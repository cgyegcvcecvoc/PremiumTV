#!/usr/bin/env python3
"""Summarize the most recent scraper run without treating unknown links as dead."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def render(run):
    lines = ["PremiumTV channel health", "========================", ""]
    if not run:
        return "\n".join(lines + ["No scraper run available.", ""])
    lines += [f"Run finished: {run.get('finished_utc', 'unknown')}",
              f"Label: {run.get('label', 'unknown')}",
              f"Status: {run.get('status', 'unknown')} (exit code: {run.get('exit_code', 'unknown')})",
              f"Check completed: {'yes' if run.get('checked') and run.get('check_completed') else 'no'}",
              f"Playlist written: {'yes' if run.get('final_playlist_written') else 'no'}"]
    if run.get('checked') and run.get('check_completed'):
        working = run.get('working', 0)
        dead = run.get('dead', 0)
        unknown = run.get('unverified', 0)
        total = working + dead + unknown
        lines += ["", f"Working / reachable: {working:,}", f"Confirmed failed: {dead:,}",
                  f"Unverified: {unknown:,}", f"Total unique checked: {total:,}",
                  f"Overall channel strength: {working / total * 100:.1f}% reachable" if total else
                  "Overall channel strength: unavailable (no links checked)"]
    else:
        lines += ["", "Overall channel strength: unavailable (check was not completed)."]
    lines += ["", "Source status:"]
    for name, source in sorted(run.get('sources', {}).items()):
        lines.append(f"- {name}: {source.get('status', 'unknown')} (working {source.get('alive', 0):,}, failed {source.get('dead', 0):,}, unverified {source.get('unverified', 0):,})")
    if not run.get('sources'):
        lines.append("- No source results recorded.")
    lines += ["", "Notes:", "- Reachable means the automated probe succeeded, not guaranteed playback or signal quality.",
              "- Unverified links are not counted as confirmed failures. Results are a point-in-time snapshot.",
              "- Details and run history: playlists/STATUS.md and playlists/run-history.jsonl.", ""]
    return "\n".join(lines)


def latest_run(path):
    if not path.exists():
        return None
    latest = None
    for line in path.read_text(encoding='utf-8').splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict):
            latest = record
    return latest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--history', type=Path, default=ROOT / 'playlists/run-history.jsonl')
    parser.add_argument('--output', type=Path, default=ROOT / 'playlists/HEALTH.txt')
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(latest_run(args.history)), encoding='utf-8')
    print(f'Wrote {args.output}')


if __name__ == '__main__':
    main()
