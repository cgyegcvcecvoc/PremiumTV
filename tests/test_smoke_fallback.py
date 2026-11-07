"""The smoke gate must distinguish a wedged uiautomator from a broken app."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
GATE_PATH = ROOT / "android/tools/smoke_apk.py"


def load_gate():
    spec = importlib.util.spec_from_file_location("smoke_apk_fallback_test", GATE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class NullRootFallbackTests(unittest.TestCase):
    def test_dump_ui_raises_infrastructure_not_parse_error(self):
        gate = load_gate()
        completed = mock.Mock(
            returncode=0,
            stdout="",
            stderr=f"ERROR: {gate.UI_AUTOMATION_NULL_ROOT}\n",
        )
        with mock.patch.object(gate.subprocess, "run", return_value=completed):
            with self.assertRaises(gate.UiAutomationUnavailable):
                gate.dump_ui()

    def test_wait_for_fails_as_infrastructure_after_the_grace_window(self):
        gate = load_gate()
        with mock.patch.object(
            gate,
            "dump_ui",
            side_effect=gate.UiAutomationUnavailable(gate.UI_AUTOMATION_NULL_ROOT),
        ), mock.patch.object(
            gate,
            "fail_ui_automation",
            side_effect=gate.UiAutomationUnavailable("reported"),
        ) as failure, mock.patch.object(gate, "UI_AUTOMATION_GRACE_SECONDS", 0):
            with self.assertRaises(gate.UiAutomationUnavailable):
                gate.wait_for(lambda texts, nodes: True, "the channel UI")
        failure.assert_called_once()

    def test_failure_report_names_infrastructure_and_keeps_screenshot_evidence(self):
        gate = load_gate()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shot = root / "build-out/smoke-uiautomator-failure.png"
            with mock.patch.object(gate, "ROOT", root), mock.patch.object(
                gate, "screenshot", return_value=shot
            ), mock.patch.object(
                gate,
                "adb",
                side_effect=["  mCurrentFocus=Window{app/MainActivity}", "1234"],
            ):
                with self.assertRaises(gate.UiAutomationUnavailable):
                    gate.fail_ui_automation("the Guide", "null root", "<hierarchy/>")

            report = (root / "build-out/smoke-infrastructure.txt").read_text()
            self.assertIn("SMOKE INFRASTRUCTURE FAILURE", report)
            self.assertIn("the Guide", report)
            self.assertIn("mCurrentFocus=Window{app/MainActivity}", report)
            self.assertIn("smoke-uiautomator-failure.png", report)
            self.assertIn("null root", report)

    def test_the_failure_exit_code_is_distinct_from_an_app_failure(self):
        gate = load_gate()
        self.assertEqual(gate.INFRASTRUCTURE_EXIT_CODE, 75)
        self.assertNotIn(gate.INFRASTRUCTURE_EXIT_CODE, (0, 1))

    def test_require_ui_turns_a_null_root_into_a_reported_failure(self):
        gate = load_gate()
        with mock.patch.object(
            gate,
            "dump_ui",
            side_effect=gate.UiAutomationUnavailable(gate.UI_AUTOMATION_NULL_ROOT),
        ), mock.patch.object(
            gate,
            "fail_ui_automation",
            side_effect=gate.UiAutomationUnavailable("reported"),
        ) as failure:
            with self.assertRaises(gate.UiAutomationUnavailable):
                gate.require_ui("the player")
        failure.assert_called_once()
        self.assertIn("null root", failure.call_args.args[1])

    def test_infrastructure_errors_are_not_rediagnosed_as_app_crashes(self):
        gate = load_gate()
        self.assertFalse(gate.needs_diagnose(gate.UiAutomationUnavailable("null root")))
        self.assertFalse(gate.needs_diagnose(RuntimeError("the Guide not seen in time")))
        self.assertTrue(gate.needs_diagnose(RuntimeError("Guide check crashed")))

    def test_main_uses_the_shared_dump_path_for_cold_launch(self):
        source = GATE_PATH.read_text(encoding="utf-8")
        self.assertIn("last_dump, nodes = dump_ui()", source)
        self.assertIn("except UiAutomationUnavailable", source)
        self.assertIn("fail_ui_automation(label, last_error, last_dump)", source)
        self.assertIn("if needs_diagnose(error):", source)
        self.assertIn("sys.exit(INFRASTRUCTURE_EXIT_CODE)", source)


class ForcedNullRootSwitchTests(unittest.TestCase):
    """The fallback can be exercised on purpose, without a PATH wrapper."""

    def test_the_switch_is_opt_in(self):
        gate = load_gate()
        self.assertFalse(gate.parse_args([]).force_null_root)
        self.assertTrue(gate.parse_args(["--force-null-root"]).force_null_root)

    def test_configure_arms_the_switch_only_when_asked(self):
        gate = load_gate()
        with mock.patch.object(gate, "progress"):
            gate.configure(gate.parse_args(["--force-null-root"]))
            self.assertTrue(gate._force_null_root)
            gate.configure(gate.parse_args([]))
            self.assertFalse(gate._force_null_root)

    def test_forced_dump_fails_without_touching_adb(self):
        gate = load_gate()
        gate._force_null_root = True
        with mock.patch.object(gate.subprocess, "run") as run:
            with self.assertRaises(gate.UiAutomationUnavailable) as raised:
                gate.dump_ui()
        run.assert_not_called()
        self.assertIn(gate.UI_AUTOMATION_NULL_ROOT, str(raised.exception))
        self.assertIn("forced", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
