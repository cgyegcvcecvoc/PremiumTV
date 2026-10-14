#!/usr/bin/env python3
"""Cold-launch the built APK and verify its channel UI on an Android emulator.

Every adb call gets an explicit timeout. The stable USA bundle is ~6 MB
(2,133 channels, 24k programmes) while the 1.1.0 preview bundles the global
library at ~21 MB (9,788 channels, 105k programmes): the APK install, the cold
start and especially `uiautomator dump` all take much longer there, so the gate
sizes its waits for the larger library instead of assuming the stable one.
A dump that times out is retried rather than counted as a failed check.

On failure the logcat tail and the last UI dump are written to
build-out/smoke-log.txt. Actions logs live behind a host some sandboxes cannot
reach, and for branch builds build-out/ is committed back to the branch, which
is what makes a failed emulator run diagnosable.
"""
import json
from pathlib import Path
import re
import subprocess
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = "com.premiumtv.app.debug"

# The preview APK is roughly twice the stable one and its channel list is ~4.6x
# larger, so adb needs far more room than the default 30s everywhere.
ADB_TIMEOUT_SECONDS = 60
INSTALL_TIMEOUT_SECONDS = 600
LAUNCH_TIMEOUT_SECONDS = 180
DUMP_TIMEOUT_SECONDS = 120
# How long the UI may take to publish the channel count and a channel card.
# The stable bundle settles well inside a minute; the global one needs longer
# because the guide it parses on start is ~3.4x bigger.
UI_DEADLINE_SECONDS = 240


def adb(*args, timeout=ADB_TIMEOUT_SECONDS):
    return subprocess.check_output(["adb", *args], text=True, timeout=timeout)


def diagnose(reason, last_dump=""):
    """Save what the emulator saw, because the Actions log may not travel."""
    print(reason)
    try:
        logcat = adb("logcat", "-d", "-t", "400", timeout=120)
    except subprocess.SubprocessError as error:
        logcat = f"logcat unavailable: {error}"
    print(logcat)
    if last_dump:
        print(f"last UI dump ({len(last_dump)} chars): {last_dump[:4000]}")
    try:
        out = ROOT / "build-out"
        out.mkdir(parents=True, exist_ok=True)
        (out / "smoke-log.txt").write_text(
            f"{reason}\n\n=== logcat ===\n{logcat}\n\n=== last UI dump ===\n{last_dump}\n"
        )
    except OSError as error:
        print(f"could not write build-out/smoke-log.txt: {error}")


def main():
    bundle = ROOT / "android/app/src/main/assets/bundle"
    meta = json.loads((bundle / "meta.json").read_text())
    names = {json.loads(row)["name"] for row in (bundle / "channels.jsonl").read_text().splitlines() if row}
    print(f"bundled library: {meta['channel_count']} channels, {len(names)} names, version {meta['version']}")
    adb("install", "-r", str(ROOT / "android/app/build/outputs/apk/debug/app-debug.apk"),
        timeout=INSTALL_TIMEOUT_SECONDS)
    for attempt in range(2):
        adb("shell", "am", "force-stop", PACKAGE)
        if attempt == 0:
            adb("shell", "pm", "clear", PACKAGE)
        adb("shell", "am", "start", "-W", "-n", f"{PACKAGE}/com.premiumtv.app.MainActivity",
            timeout=LAUNCH_TIMEOUT_SECONDS)
        deadline = time.monotonic() + UI_DEADLINE_SECONDS
        last_dump = ""
        last_error = ""
        while time.monotonic() < deadline:
            try:
                adb("shell", "uiautomator", "dump", "/sdcard/premiumtv-ui.xml", timeout=DUMP_TIMEOUT_SECONDS)
                xml = adb("shell", "cat", "/sdcard/premiumtv-ui.xml", timeout=DUMP_TIMEOUT_SECONDS)
                last_dump = xml
                nodes = ET.fromstring(xml)
                texts = {node.get("text", "") for node in nodes.iter("node")}
                count = any(re.search(rf"\b{meta['channel_count']} channels\b", value) for value in texts)
                named = [value for value in texts for name in names if name and name in value]
                if count and named:
                    print(f"APK SMOKE PASS ({'cold launch' if attempt == 0 else 'relaunch'}): "
                          f"{meta['channel_count']} channels and visible channel cards")
                    return
                last_error = f"channel count seen: {count}; visible channel names: {named[:3]}; texts: {sorted(texts)[:12]}"
            except (subprocess.SubprocessError, ET.ParseError) as error:
                # A dump that did not finish is not evidence of a broken app.
                last_error = f"{type(error).__name__}: {error}"
            time.sleep(2)
        diagnose(f"APK did not show bundled channels within {UI_DEADLINE_SECONDS} seconds "
                 f"(attempt {'cold launch' if attempt == 0 else 'relaunch'}). Last check: {last_error}",
                 last_dump)
        raise RuntimeError("APK did not show bundled channels in time")


if __name__ == "__main__":
    main()
