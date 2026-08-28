import json
import tempfile
import unittest
from pathlib import Path

from ai_redteam.core.orchestrator import AssessmentOrchestrator
from ai_redteam.reporting.sarif import to_sarif, write_sarif
from ai_redteam.targets import HardenedTarget, SyntheticTarget
from ai_redteam.tests.loader import discover_test_cases


class TestCIProfessionalizationTests(unittest.TestCase):
    def setUp(self):
        self.cases = discover_test_cases("test_cases")
        self.engine = AssessmentOrchestrator()

    def test_sarif_is_valid_shape(self):
        report = self.engine.run(self.cases, SyntheticTarget())
        sarif = to_sarif(report)
        self.assertEqual(sarif["version"], "2.1.0")
        self.assertEqual(len(sarif["runs"]), 1)
        self.assertEqual(
            len(sarif["runs"][0]["results"]),
            len(report.findings),
        )

    def test_sarif_can_be_written(self):
        report = self.engine.run(self.cases, HardenedTarget())
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.sarif"
            write_sarif(report, path)
            loaded = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(loaded["runs"][0]["tool"]["driver"]["name"], "AI Red Teaming Lab")

    def test_hardened_target_is_a_clean_ci_gate(self):
        report = self.engine.run(self.cases, HardenedTarget())
        self.assertEqual(report.counts["FAIL"], 0)
        self.assertEqual(report.counts["REVIEW"], 0)

    def test_vulnerable_target_would_block_a_fail_gate(self):
        report = self.engine.run(self.cases, SyntheticTarget())
        self.assertGreater(report.counts["FAIL"], 0)


if __name__ == "__main__":
    unittest.main()
