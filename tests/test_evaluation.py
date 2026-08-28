import unittest

from ai_redteam.comparison import compare
from ai_redteam.core.orchestrator import AssessmentOrchestrator
from ai_redteam.evaluation import EvaluatorRegistry
from ai_redteam.evaluation.evaluator import BehaviourEvaluator
from ai_redteam.targets import HardenedTarget, SyntheticTarget
from ai_redteam.tests.loader import discover_test_cases


class TestEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.cases = discover_test_cases("test_cases")
        self.engine = AssessmentOrchestrator(BehaviourEvaluator())

    def test_evaluator_registry_exposes_specialized_evaluators(self):
        names = set(EvaluatorRegistry().names())
        self.assertTrue({"prompt-injection", "tool-authorization", "data-leakage"} <= names)

    def test_vulnerable_target_has_security_failures(self):
        report = self.engine.run(self.cases, SyntheticTarget())
        self.assertEqual(report.counts["PASS"], 0)
        self.assertGreater(report.counts["FAIL"], 0)

    def test_hardened_target_resolves_failures(self):
        report = self.engine.run(self.cases, HardenedTarget())
        self.assertEqual(report.counts["FAIL"], 0)
        self.assertEqual(report.counts["PASS"], len(self.cases))

    def test_baseline_to_hardened_comparison(self):
        before = self.engine.run(self.cases, SyntheticTarget())
        after = self.engine.run(self.cases, HardenedTarget())
        delta = compare(before, after)
        self.assertEqual(delta.regression_count, 0)
        self.assertEqual(delta.resolved_count, len(self.cases))
        self.assertEqual(delta.improved_count, len(self.cases))

    def test_high_risk_findings_have_retest_flag(self):
        report = self.engine.run(self.cases, SyntheticTarget())
        high = [f for f in report.findings if f.risk.severity.value in {"HIGH", "CRITICAL"}]
        self.assertTrue(high)
        self.assertTrue(all(f.retest_required for f in high))

    def test_findings_include_remediation_and_framework_mapping(self):
        report = self.engine.run(self.cases, SyntheticTarget())
        for finding in report.findings:
            self.assertTrue(finding.remediation)
            self.assertTrue(finding.owasp)
            self.assertTrue(finding.mitre_atlas)


if __name__ == "__main__":
    unittest.main()
