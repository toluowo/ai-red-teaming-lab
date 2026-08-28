import unittest

from ai_redteam.core.models import Outcome
from ai_redteam.core.orchestrator import AssessmentOrchestrator
from ai_redteam.targets import HardenedTarget, SyntheticTarget
from ai_redteam.tests.loader import discover_test_cases


class SecurityScoringTests(unittest.TestCase):
    def setUp(self):
        self.cases = discover_test_cases("test_cases")
        self.engine = AssessmentOrchestrator()

    def test_vulnerable_target_fails_security_cases(self):
        report = self.engine.run(self.cases, SyntheticTarget())
        self.assertGreater(report.counts["FAIL"], 0)

    def test_hardened_target_passes_security_cases(self):
        report = self.engine.run(self.cases, HardenedTarget())
        self.assertEqual(report.counts["FAIL"], 0)
        self.assertEqual(report.counts["REVIEW"], 0)
        self.assertTrue(all(f.outcome is Outcome.PASS for f in report.findings))


if __name__ == "__main__":
    unittest.main()
