#!/usr/bin/env python3
"""Check the published GitHub Pages site for broken pages and assets.

The Pages deploy job proves that the files were uploaded; it never reads them
back. A file can disappear from a branch, a generated page can link to an asset
the build stopped producing, or the deployed service worker can be left on an
older build id - and the deploy job still reports success.

This checker walks the live site from its entry pages, checks every same-origin
link, stylesheet, script, image and data file, then verifies that the service
worker's BUILD value matches data/meta.json. It is read-only and needs no
credentials.

    python scripts/pages_site_check.py
    python scripts/pages_site_check.py --base-url http://127.0.0.1:3001/

The base URL defaults to the project Pages site and can be overridden with
PAGES_SITE_URL. Exit status is 1 when any reference is broken.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "https://cgyegcvcecvoc.github.io/PremiumTV/"
USER_AGENT = (
    "PremiumTV-pages-site-check/1.0 "
    "(+https://github.com/cgyegcvcecvoc/PremiumTV)"
)
MAX_PAGES = 12
RETRY_STATUS = {429, 500, 502, 503, 504}
SKIP_SCHEMES = (
    "mailto:",
    "tel:",
    "javascript:",
    "data:",
    "blob:",
    "about:",
    "chrome:",
)
REF_RE = re.compile(
    r"""(?:\bhref|\bsrc)\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.IGNORECASE
)
CORE_RE = re.compile(r"\bconst\s+CORE\s*=\s*\[(.*?)\];", re.DOTALL)
BUILD_RE = re.compile(r'\bconst\s+BUILD\s*=\s*"([^"]*)"')


@dataclass
class Response:
    url: str
    status: int
    headers: dict[str, str] = field(default_factory=dict)
    body: bytes = b""
    error: str = ""

    @property
    def content_type(self) -> str:
        return self.headers.get("content-type", "")

    @property
    def content_length(self) -> int | None:
        raw = self.headers.get("content-length")
        if raw is None:
            return None
        try:
            return int(raw)
        except ValueError:
            return None


class Fetcher:
    """Small HTTP client that reports statuses instead of raising on 4xx/5xx."""

    def __init__(self, timeout: float = 20.0, retries: int = 2) -> None:
        self.timeout = timeout
        self.retries = max(0, retries)

    def request(self, url: str, *, method: str = "GET") -> Response:
        delay = 1.0
        last = Response(url, 0, error="request was not attempted")
        for attempt in range(self.retries + 1):
            request = Request(
                url,
                method=method,
                headers={
                    "User-Agent": USER_AGENT,
                    "Cache-Control": "no-cache",
                },
            )
            try:
                with urlopen(request, timeout=self.timeout) as response:
                    body = response.read() if method == "GET" else b""
                    return Response(
                        response.geturl(),
                        response.status,
                        {key.lower(): value for key, value in response.headers.items()},
                        body,
                    )
            except HTTPError as error:
                body = error.read() if method == "GET" else b""
                last = Response(
                    error.geturl(),
                    error.code,
                    {key.lower(): value for key, value in (error.headers or {}).items()},
                    body,
                )
                if error.code not in RETRY_STATUS or attempt >= self.retries:
                    return last
            except (URLError, TimeoutError, socket.timeout, OSError) as error:
                reason = getattr(error, "reason", error)
                last = Response(url, 0, error=str(reason) or type(error).__name__)
                if attempt >= self.retries:
                    return last
            time.sleep(delay)
            delay *= 2
        return last

    def get(self, url: str) -> Response:
        return self.request(url)

    def head(self, url: str) -> Response:
        """HEAD where supported, GET when a server refuses HEAD."""
        response = self.request(url, method="HEAD")
        if response.status in (405, 501):
            response = self.request(url)
        return response


@dataclass(frozen=True)
class Finding:
    url: str
    source: str
    ok: bool
    status: int
    detail: str


@dataclass
class Report:
    base_url: str
    findings: list[Finding] = field(default_factory=list)
    build_id: str = ""
    generated_utc: str = ""
    pages: int = 0

    @property
    def failures(self) -> list[Finding]:
        return [finding for finding in self.findings if not finding.ok]


def extract_refs(html: str) -> list[str]:
    """Return the href/src values in a document, in source order."""
    return [quoted or single for quoted, single in REF_RE.findall(html)]


def resolve_ref(base_url: str, ref: str) -> str | None:
    """Resolve a same-origin URL, or None for fragments, data: and other sites."""
    ref = ref.strip()
    if not ref or ref.startswith("#"):
        return None
    if ref.lower().startswith(SKIP_SCHEMES):
        return None
    target = urldefrag(urljoin(base_url, ref))[0]
    base, parsed = urlparse(base_url), urlparse(target)
    if parsed.scheme not in ("http", "https"):
        return None
    if parsed.netloc != base.netloc:
        return None
    return target


def looks_like_page(url: str) -> bool:
    path = urlparse(url).path
    suffix = Path(path).suffix.lower()
    return path.endswith("/") or suffix in ("", ".html", ".htm")


def is_html(response: Response) -> bool:
    return "text/html" in response.content_type


def _failure(url: str, source: str, response: Response) -> Finding:
    if response.error:
        detail = response.error
    elif response.status:
        detail = f"HTTP {response.status}"
    else:
        detail = "no response"
    if response.status and response.content_type:
        detail += f" ({response.content_type})"
    return Finding(url, source, False, response.status, detail)


def _check_asset(fetcher: Fetcher, url: str, source: str) -> Finding:
    response = fetcher.head(url)
    if response.status != 200:
        return _failure(url, source, response)
    if is_html(response) and not looks_like_page(url):
        return Finding(
            url,
            source,
            False,
            response.status,
            "served HTML instead of the requested file",
        )
    length = response.content_length
    if length == 0:
        return Finding(url, source, False, response.status, "empty file")
    detail = "HTTP 200"
    if length:
        detail += f", {length:,} bytes"
    return Finding(url, source, True, response.status, detail)


def run_checks(
    base_url: str = DEFAULT_BASE_URL,
    *,
    timeout: float = 20.0,
    retries: int = 2,
    jobs: int = 8,
) -> Report:
    base = base_url if base_url.endswith("/") else base_url + "/"
    web = urljoin(base, "web/")
    fetcher = Fetcher(timeout=timeout, retries=retries)
    report = Report(base_url=base)
    findings = report.findings

    def fail(url: str, source: str, detail: str) -> None:
        findings.append(Finding(url, source, False, 0, detail))

    # The build stamp lets a stale deployment (service worker serving an old
    # cache) fail even when every file still answers 200.
    meta_url = urljoin(web, "data/meta.json")
    meta_response = fetcher.get(meta_url)
    meta: dict = {}
    if meta_response.status != 200:
        findings.append(_failure(meta_url, "build metadata", meta_response))
    else:
        try:
            meta = json.loads(meta_response.body)
        except (ValueError, UnicodeDecodeError) as error:
            fail(meta_url, "build metadata", f"invalid JSON: {error}")
        else:
            report.build_id = str(meta.get("build_id") or "")
            report.generated_utc = str(meta.get("generated_utc") or "")
            if not report.build_id or "PLACEHOLDER" in report.build_id.upper():
                fail(meta_url, "build metadata", "missing or placeholder build_id")

    sw_url = urljoin(web, "sw.js")
    sw_response = fetcher.get(sw_url)
    assets: dict[str, str] = {}
    if sw_response.status != 200:
        findings.append(_failure(sw_url, "service worker", sw_response))
    else:
        text = sw_response.body.decode("utf-8", "replace")
        build = BUILD_RE.search(text)
        if not build:
            fail(sw_url, "service worker", "no BUILD constant found")
        else:
            sw_build = build.group(1)
            if "PLACEHOLDER" in sw_build.upper():
                fail(sw_url, "service worker", "BUILD is still the placeholder")
            elif report.build_id and sw_build != report.build_id:
                fail(
                    sw_url,
                    "service worker",
                    f"build {sw_build} does not match data/meta.json build "
                    f"{report.build_id}",
                )
        core = CORE_RE.search(text)
        if not core:
            fail(sw_url, "service worker", "no CORE precache list found")
        else:
            for ref in re.findall(r'"([^"]*)"', core.group(1)):
                target = resolve_ref(sw_url, ref)
                if target:
                    assets.setdefault(target, "service worker precache")

    manifest_url = urljoin(web, "manifest.webmanifest")
    manifest_response = fetcher.get(manifest_url)
    if manifest_response.status != 200:
        findings.append(_failure(manifest_url, "web manifest", manifest_response))
    else:
        try:
            manifest = json.loads(manifest_response.body)
        except (ValueError, UnicodeDecodeError) as error:
            fail(manifest_url, "web manifest", f"invalid JSON: {error}")
        else:
            for icon in manifest.get("icons", []):
                src = icon.get("src") if isinstance(icon, dict) else None
                if src:
                    target = resolve_ref(manifest_url, src)
                    if target:
                        assets.setdefault(target, "web manifest")
            for key in ("start_url", "scope"):
                ref = manifest.get(key)
                if isinstance(ref, str):
                    target = resolve_ref(manifest_url, ref)
                    if target:
                        assets.setdefault(target, "web manifest")

    # Walk the site from the two entry points. Pages are fetched with GET so
    # their links can be read; everything else is checked with HEAD.
    queue = [base, web]
    seen: set[str] = set()
    while queue and report.pages < MAX_PAGES:
        page_url = queue.pop(0)
        if page_url in seen:
            continue
        seen.add(page_url)
        response = fetcher.get(page_url)
        if response.status != 200:
            findings.append(_failure(page_url, "linked page", response))
            continue
        if not is_html(response):
            fail(
                page_url,
                "linked page",
                f"expected HTML, got {response.content_type or 'no content type'}",
            )
            continue
        report.pages += 1
        html = response.body.decode("utf-8", "replace")
        for ref in extract_refs(html):
            target = resolve_ref(page_url, ref)
            if not target or target == page_url:
                continue
            if looks_like_page(target):
                if target not in seen:
                    queue.append(target)
            else:
                assets.setdefault(target, page_url)

    if assets:
        with ThreadPoolExecutor(max_workers=max(1, min(jobs, len(assets)))) as pool:
            results = pool.map(
                lambda item: _check_asset(fetcher, item[0], item[1]),
                sorted(assets.items()),
            )
            findings.extend(results)

    findings.sort(key=lambda finding: (finding.ok, finding.url))
    return report


def _cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def write_summary(report: Report, path: str) -> None:
    lines = [
        "## Pages site check",
        "",
        f"- Site: {report.base_url}",
        f"- Pages crawled: {report.pages}",
        f"- References checked: {len(report.findings)}",
    ]
    if report.build_id:
        stamp = f"`{report.build_id}`"
        if report.generated_utc:
            stamp += f" ({report.generated_utc})"
        lines.append(f"- Deployed build: {stamp}")
    failures = report.failures
    if failures:
        lines += [
            "",
            f"### {len(failures)} broken reference(s)",
            "",
            "| URL | Reason | Referenced by |",
            "| --- | --- | --- |",
        ]
        lines += [
            f"| {_cell(f.url)} | {_cell(f.detail)} | {_cell(f.source)} |"
            for f in failures
        ]
    else:
        lines += ["", "All references resolved with HTTP 200."]
    with Path(path).open("a", encoding="utf-8") as summary:
        summary.write("\n".join(lines) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--base-url",
        default=os.environ.get("PAGES_SITE_URL", DEFAULT_BASE_URL),
        help=f"site root to check (default: {DEFAULT_BASE_URL})",
    )
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--jobs", type=int, default=8)
    args = parser.parse_args(argv)

    report = run_checks(
        args.base_url,
        timeout=args.timeout,
        retries=args.retries,
        jobs=args.jobs,
    )
    failures = report.failures
    checked = len(report.findings)
    print(f"Pages site check: {report.base_url}")
    if report.build_id:
        print(f"Deployed build: {report.build_id} ({report.generated_utc})")
    print(f"Crawled {report.pages} page(s); checked {checked} reference(s).")
    for finding in failures:
        print(f"FAIL {finding.url}")
        print(f"     {finding.detail} (referenced by {finding.source})")
        if os.environ.get("GITHUB_ACTIONS") == "true":
            print(f"::error title=Broken Pages reference::{finding.url} - {finding.detail}")
    if failures:
        print(f"{len(failures)} broken, {checked - len(failures)} OK")
    else:
        print(f"All {checked} references resolved with HTTP 200.")

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        write_summary(report, summary_path)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
