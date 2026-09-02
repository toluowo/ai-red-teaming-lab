import unittest

from ai_redteam.comparison import compare
from ai_redteam.core.models import TestCase as SecurityTestCase
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

    def test_registry_resolves_evaluator_by_category(self):
        registry = EvaluatorRegistry()

        test_case = SecurityTestCase(
            id="TEST-001",
            name="Prompt injection test",
            category="prompt_injection",
            objective="test",
            prompt="test",
        )

        evaluator = registry.for_test_case(test_case)

        self.assertEqual(evaluator.name, "prompt-injection")

    def test_registry_respects_explicit_evaluator(self):
        registry = EvaluatorRegistry()

        test_case = SecurityTestCase(
            id="TEST-002",
            name="Explicit evaluator test",
            category="prompt_injection",
            objective="test",
            prompt="test",
            evaluator="data-leakage",
        )

        evaluator = registry.for_test_case(test_case)

        self.assertEqual(evaluator.name, "data-leakage")

    def test_registry_uses_default_for_unknown_category(self):
        registry = EvaluatorRegistry()
        default = BehaviourEvaluator()

        test_case = SecurityTestCase(
            id="TEST-003",
            name="Unknown category test",
            category="unknown_category",
            objective="test",
            prompt="test",
        )

        evaluator = registry.for_test_case(test_case, default=default)

        self.assertIs(evaluator, default)

    def test_registry_uses_declarative_fallback_without_default(self):
        registry = EvaluatorRegistry()

        test_case = SecurityTestCase(
            id="TEST-004",
            name="Unknown category fallback test",
            category="unknown_category",
            objective="test",
            prompt="test",
        )

        evaluator = registry.for_test_case(test_case)

        self.assertEqual(evaluator.name, "declarative")


if __name__ == "__main__":
    unittest.main()
