import unittest

from ai_redteam.core.models import AssessmentRequest, Outcome, Severity
from ai_redteam.core.orchestrator import AssessmentOrchestrator
from ai_redteam.targets import SyntheticTarget


class ArchitectureTests(unittest.TestCase):
    def test_synthetic_target_exposes_stable_interface(self):
        target = SyntheticTarget()
        self.assertEqual(target.name, "synthetic-vulnerable-target")
        response = target.invoke(
            AssessmentRequest(test_case_id="PI-001", input_text="hello")
        )
        self.assertTrue(response.output)

    def test_orchestrator_produces_structured_findings(self):
        from ai_redteam.tests.loader import discover_test_cases

        cases = discover_test_cases("test_cases")
        report = AssessmentOrchestrator().run(cases, SyntheticTarget())
        self.assertTrue(report.findings)
        self.assertTrue(all(f.outcome in Outcome for f in report.findings))
        self.assertTrue(all(f.risk.severity in Severity for f in report.findings))


if __name__ == "__main__":
    unittest.main()
