#!/usr/bin/env python3
"""Summarize the most recent scraper run without treating unknown links as dead.

The report names the servers that failed, not just a total: a host with dozens
of confirmed failures is an outage, while one bad link on a healthy host is a
single dead channel. That distinction is what makes a health report actionable
for the next scrape and for a viewer report about a channel.
"""
import argparse
import json
import urllib.parse
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_SERVERS = 20
MAX_CHANNELS = 25


def host_of(url):
    """The server a link lives on, including a non-default port."""
    try:
        parts = urllib.parse.urlsplit(str(url or "").strip())
    except ValueError:
        return ""
    host = (parts.netloc or "").lower()
    if "@" in host:
        host = host.rsplit("@", 1)[-1]
    return host


def server_failures(run):
    """Group confirmed and unconfirmed failures by server.

    ``dead_details`` rows are conclusive (404/410, DNS, HTML instead of media);
    ``unverified_details`` rows are timeouts, 429s and 5xx answers that may
    recover. Keeping them apart stops a busy CDN from looking like a dead
    provider. The counts live in the run-history record, the per-link details
    in playlists/report.json; ``attach_details`` joins the two.
    """
    servers = defaultdict(lambda: {"dead": 0, "unverified": 0, "example": ""})
    for status, key in (("dead_details", "dead"), ("unverified_details", "unverified")):
        for item in run.get(status) or []:
            if not isinstance(item, dict):
                continue
            host = host_of(item.get("url"))
            if not host:
                continue
            row = servers[host]
            row[key] += 1
            if not row["example"]:
                row["example"] = str(item.get("name") or "")[:48]
    return sorted(servers.items(),
                  key=lambda pair: (-pair[1]["dead"], -pair[1]["unverified"], pair[0]))


def dead_channels(run):
    """The confirmed-dead channels, worst first (a channel can have backups)."""
    rows = []
    for item in run.get("dead_details") or []:
        if isinstance(item, dict):
            rows.append((str(item.get("name") or "Unknown")[:60],
                         str(item.get("reason") or "")[:60]))
    return rows[:MAX_CHANNELS]


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

    servers = server_failures(run)
    lines += ["", "Servers with failing links:"]
    if servers:
        for host, counts in servers[:MAX_SERVERS]:
            example = f" - e.g. {counts['example']}" if counts["example"] else ""
            lines.append(f"- {host}: {counts['dead']:,} confirmed dead, "
                         f"{counts['unverified']:,} unverified{example}")
    else:
        lines.append("- No per-server failures recorded in this run.")

    channels = dead_channels(run)
    lines += ["", "Channels confirmed dead:"]
    if channels:
        for name, reason in channels:
            lines.append(f"- {name}" + (f" ({reason})" if reason else ""))
        if len(run.get('dead_details') or []) > len(channels):
            lines.append(f"- ... and {len(run.get('dead_details') or []) - len(channels):,} more "
                         "in playlists/STATUS.md")
    else:
        lines.append("- None recorded in this run.")

    lines += ["", "Notes:",
              "- Reachable means the automated probe succeeded, not guaranteed playback or signal quality.",
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


def attach_details(run, report_path):
    """Join the per-link failures from report.json onto the history summary.

    run-history.jsonl keeps small records (counts per source) so it stays
    quick to read. The latest full run in playlists/report.json carries the
    dead and unverified rows this report names; only a matching run_id is
    used, so an old report can never describe a newer run.
    """
    if not run or not report_path.exists():
        return run
    try:
        report = json.loads(report_path.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return run
    if not isinstance(report, dict) or report.get('run_id') != run.get('run_id'):
        return run
    merged = dict(run)
    merged['dead_details'] = report.get('dead') or []
    merged['unverified_details'] = report.get('unverified') or []
    return merged


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--history', type=Path, default=ROOT / 'playlists/run-history.jsonl')
    parser.add_argument('--report', type=Path, default=ROOT / 'playlists/report.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'playlists/HEALTH.txt')
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    run = attach_details(latest_run(args.history), args.report)
    args.output.write_text(render(run), encoding='utf-8')
    print(f'Wrote {args.output}')


if __name__ == '__main__':
    main()
