#!/usr/bin/env python3
"""Cold-launch the built APK and verify its channel UI on an Android emulator."""
import json
from pathlib import Path
import re
import subprocess
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = "com.premiumtv.app.debug"


def adb(*args):
    return subprocess.check_output(["adb", *args], text=True, timeout=30)


def main():
    bundle = ROOT / "android/app/src/main/assets/bundle"
    meta = json.loads((bundle / "meta.json").read_text())
    names = {json.loads(row)["name"] for row in (bundle / "channels.jsonl").read_text().splitlines() if row}
    adb("install", "-r", str(ROOT / "android/app/build/outputs/apk/debug/app-debug.apk"))
    for attempt in range(2):
        adb("shell", "am", "force-stop", PACKAGE)
        if attempt == 0:
            adb("shell", "pm", "clear", PACKAGE)
        adb("shell", "am", "start", "-W", "-n", f"{PACKAGE}/com.premiumtv.app.MainActivity")
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline:
            try:
                adb("shell", "uiautomator", "dump", "/sdcard/premiumtv-ui.xml")
                xml = adb("shell", "cat", "/sdcard/premiumtv-ui.xml")
                nodes = ET.fromstring(xml)
                texts = {node.get("text", "") for node in nodes.iter("node")}
                count = any(re.search(rf"\b{meta['channel_count']} channels\b", value) for value in texts)
                if count and names.intersection(texts):
                    print(f"APK SMOKE PASS ({'cold launch' if attempt == 0 else 'relaunch'}): {meta['channel_count']} channels and visible channel cards")
                    break
            except (subprocess.SubprocessError, ET.ParseError):
                pass
            time.sleep(2)
        else:
            print(adb("logcat", "-d", "-t", "300"))
            raise RuntimeError("APK did not show bundled channels within 90 seconds")


if __name__ == "__main__":
    main()
