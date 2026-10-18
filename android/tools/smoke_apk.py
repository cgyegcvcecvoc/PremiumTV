#!/usr/bin/env python3
"""Cold-launch the built APK and verify its channel UI on an Android emulator.

Every adb call gets an explicit timeout. The stable USA bundle is ~6 MB
(2,133 channels, 24k programmes) while the 1.1.0 preview bundles the global
library at ~21 MB (9,788 channels, 105k programmes): the APK install, the cold
start and especially `uiautomator dump` all take much longer there, so the gate
sizes its waits for the larger library instead of assuming the stable one.
A dump that times out is retried rather than counted as a failed check.

A build inside the range published in `app-update-notice.json` (1.0.0-1.0.4
today) opens the update popup over the channel list on first launch. That is the
behaviour the notice exists for, so the gate records it, screenshots it once and
presses Back - the remote's own dismissal - instead of failing as though the
channel list never drew.

After the channel check, the Guide tab is opened. A preview build (bundle
preview_features: cable-guide) must show the cable-style grid - channels down
the left, half-hour times across the top, shows to the right - and answer the
remote: the highlight moves with the D-pad, OK opens the player, and Back
returns to the same guide. A stable build must show the "what's on now" list.
Preview runs save screenshots of the guide to build-out/ so the grid can be
checked by eye.

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
    sections = {"reason": reason}
    probes = {
        "pidof": ("shell", "pidof", PACKAGE),
        "current focus": ("shell", "dumpsys", "window"),
        "top activity": ("shell", "dumpsys", "activity", "activities"),
        "meminfo": ("shell", "dumpsys", "meminfo", PACKAGE),
        "logcat": ("logcat", "-d", "-t", "600"),
        "crash log": ("logcat", "-b", "crash", "-d", "-t", "200"),
    }
    for label, args in probes.items():
        try:
            sections[label] = adb(*args, timeout=150)
        except subprocess.SubprocessError as error:
            sections[label] = f"{label} unavailable: {error}"
    # Keep the parts that answer "did the app start, did it die, did the system
    # hand it to the launcher": the full dumpsys output is far too big to save.
    focus = [line for line in sections["current focus"].splitlines() if "mCurrentFocus" in line or "mFocusedApp" in line]
    top = [line for line in sections["top activity"].splitlines() if PACKAGE in line][:12]
    mem = sections["meminfo"].splitlines()[:24]
    body = "\n\n".join([
        reason,
        "=== process ===\n" + sections["pidof"].strip(),
        "=== focus ===\n" + "\n".join(focus),
        "=== premiumtv activity lines ===\n" + "\n".join(top),
        "=== meminfo ===\n" + "\n".join(mem),
        "=== crash log ===\n" + sections["crash log"],
        "=== logcat ===\n" + sections["logcat"],
        "=== last UI dump ===\n" + last_dump,
    ])
    print(body[:20000])
    try:
        out = ROOT / "build-out"
        out.mkdir(parents=True, exist_ok=True)
        (out / "smoke-log.txt").write_text(body)
    except OSError as error:
        print(f"could not write build-out/smoke-log.txt: {error}")


# Newer ICU puts a narrow no-break space before AM/PM; \s matches either.
TIME_TICK = re.compile(r"^\d{1,2}:\d{2}\s(AM|PM)$")
GUIDE_DATE = re.compile(r"^[A-Z][a-z]{2}, [A-Z][a-z]{2}\s\d{1,2}$")
# The global guide (~105k listings) can still be parsing when the channel cards
# are already up, so the first guide check gets the same room as the UI check.
GUIDE_DEADLINE_SECONDS = 240


def dump_ui():
    """One uiautomator dump: (xml text, parsed nodes)."""
    adb("shell", "uiautomator", "dump", "/sdcard/premiumtv-ui.xml", timeout=DUMP_TIMEOUT_SECONDS)
    xml = adb("shell", "cat", "/sdcard/premiumtv-ui.xml", timeout=DUMP_TIMEOUT_SECONDS)
    return xml, list(ET.fromstring(xml).iter("node"))


def texts_of(nodes):
    return [node.get("text", "") for node in nodes if node.get("text", "")]


def centre_of(node):
    left, top, right, bottom = map(int, re.findall(r"\d+", node.get("bounds", "")))
    return (left + right) // 2, (top + bottom) // 2


def progress(line):
    """Appends a milestone to build-out/smoke-progress.txt as the run goes."""
    print(line)
    try:
        out = ROOT / "build-out"
        out.mkdir(parents=True, exist_ok=True)
        with (out / "smoke-progress.txt").open("a", encoding="utf-8") as handle:
            handle.write(f"{time.strftime('%H:%M:%S')} {line}\n")
    except OSError:
        pass


def screenshot(name):
    """Saves the emulator screen to build-out/<name> (PNG)."""
    out = ROOT / "build-out"
    out.mkdir(parents=True, exist_ok=True)
    try:
        data = subprocess.check_output(["adb", "exec-out", "screencap", "-p"], timeout=ADB_TIMEOUT_SECONDS)
        if data.startswith(b"\x89PNG"):
            (out / name).write_bytes(data)
            print(f"saved build-out/{name} ({len(data) // 1024} KB)")
    except subprocess.SubprocessError as error:
        print(f"screenshot {name} skipped: {error}")


def wait_for(check, label):
    """Polls the UI until check(texts) is truthy; returns (value, texts, xml)."""
    deadline = time.monotonic() + GUIDE_DEADLINE_SECONDS
    last_xml, last_texts, last_error = "", [], ""
    while time.monotonic() < deadline:
        try:
            last_xml, nodes = dump_ui()
            last_texts = texts_of(nodes)
            # The update check is asynchronous: the popup can arrive after the
            # channel list has already drawn and land on top of the Guide tab.
            if dismiss_update_notice(last_texts):
                continue
            value = check(last_texts, nodes)
            if value:
                return value, last_texts, last_xml
        except (subprocess.SubprocessError, ET.ParseError) as error:
            last_error = f"{type(error).__name__}: {error}"
        time.sleep(2)
    diagnose(f"{label} not seen within {GUIDE_DEADLINE_SECONDS} seconds. "
             f"Texts: {sorted(set(last_texts))[:40]} {last_error}", last_xml)
    raise RuntimeError(f"{label} not seen in time")


def key(code, times=1):
    for _ in range(times):
        adb("shell", "input", "keyevent", code)
        time.sleep(0.6)


# The popup's own headline, not the published copy: the wording in
# app-update-notice.json can change without breaking this gate.
NOTICE_EYEBROWS = {"PREMIUMTV UPDATE", "SUPPORT HAS ENDED"}
_notice_seen = False


def dismiss_update_notice(texts):
    """Dismisses the startup update popup if this build is showing one.

    A targeted build is *supposed* to be told to update, so the gate treats the
    dialog as expected rather than as a missing channel list: it records the
    milestone, keeps one screenshot as evidence, and presses Back, which is the
    dismissal a TV remote has (the dialog sets dismissOnBackPress).
    """
    global _notice_seen
    if not any(text.strip().upper() in NOTICE_EYEBROWS for text in texts):
        return False
    if not _notice_seen:
        _notice_seen = True
        progress("update popup shown: this build is inside the published notice range")
        screenshot("smoke-update-notice.png")
    key(4)  # KEYCODE_BACK - dismisses for this launch only, by design
    time.sleep(1.0)
    return True


def check_guide(meta, names):
    """Opens the Guide tab and checks the grid (preview) or the list (stable)."""
    cable = "cable-guide" in (meta.get("preview_features") or [])

    def guide_tab(texts, nodes):
        # Return coordinates, not the element: an ElementTree element with no
        # children is falsy, which made the first version of this wait loop
        # until its deadline with the tab plainly on screen.
        node = next((node for node in nodes if node.get("text") == "Guide"), None)
        return centre_of(node) if node is not None else None

    (x, y), _, _ = wait_for(guide_tab, "the Guide tab")
    progress(f"tapping the Guide tab at {x},{y} (cable grid expected: {cable})")
    adb("shell", "input", "tap", str(x), str(y))

    if not cable:
        wait_for(lambda texts, nodes: any("channels with listings" in t for t in texts),
                 "the stable guide list")
        progress("GUIDE PASS (stable): the Guide tab shows the what's-on-now list")
        return

    def grid(texts, nodes):
        ticks = [t for t in texts if TIME_TICK.match(t)]
        dated = any(GUIDE_DATE.match(t) for t in texts)
        listed = any(t.endswith("channels listed") for t in texts)
        rows = [t for t in texts if t in names]
        return (ticks, rows) if len(ticks) >= 3 and dated and listed and rows else None

    (ticks, rows), texts, _ = wait_for(grid, "the cable-style guide grid")
    progress(f"GUIDE PASS (cable grid): times across the top {ticks[:6]}, "
             f"channels down the left {rows[:4]}")
    screenshot("android-guide.png")

    # The remote: the grid takes focus when it opens; move right and down.
    before = set(texts)
    key("KEYCODE_DPAD_RIGHT", 2)
    key("KEYCODE_DPAD_DOWN", 2)
    moved, texts, _ = wait_for(lambda t, n: set(t) != before and grid(t, n), "the guide after D-pad moves")
    progress("GUIDE PASS (remote): the highlight and the detail strip follow the D-pad")
    screenshot("android-guide-remote.png")

    # OK plays the highlighted channel; Back returns to the same guide.
    key("KEYCODE_DPAD_CENTER")
    wait_for(lambda t, n: not grid(t, n), "the player after OK in the guide")
    key("KEYCODE_BACK")
    wait_for(grid, "the guide again after Back from the player")
    progress("GUIDE PASS (player): OK opened the channel and Back returned to the guide")


def main():
    bundle = ROOT / "android/app/src/main/assets/bundle"
    meta = json.loads((bundle / "meta.json").read_text())
    names = {json.loads(row)["name"] for row in (bundle / "channels.jsonl").read_text().splitlines() if row}
    progress(f"bundled library: {meta['channel_count']} channels, {len(names)} names, version {meta['version']}, "
             f"preview features {meta.get('preview_features') or []}")
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
                if dismiss_update_notice(texts):
                    continue
                count = any(re.search(rf"\b{meta['channel_count']} channels\b", value) for value in texts)
                named = [value for value in texts for name in names if name and name in value]
                if count and named:
                    progress(f"APK SMOKE PASS ({'cold launch' if attempt == 0 else 'relaunch'}): "
                             f"{meta['channel_count']} channels and visible channel cards")
                    try:
                        check_guide(meta, names)
                    except Exception as error:  # noqa: BLE001 - always leave a diagnosable log
                        import traceback
                        if not (ROOT / "build-out" / "smoke-log.txt").exists():
                            diagnose(f"Guide check crashed: {type(error).__name__}: {error}\n"
                                     f"{traceback.format_exc()}", last_dump)
                        raise
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
