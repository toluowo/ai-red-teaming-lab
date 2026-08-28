import unittest

from ai_redteam.core.models import (
    Impact,
    Likelihood,
    Severity,
)
from ai_redteam.core.models import (
    TestCase as SecurityTestCase,
)
from ai_redteam.evaluation.risk import assess_risk


def case(severity):
    return SecurityTestCase(
        id="TEST-001",
        name="Risk test",
        category="test",
        objective="test",
        prompt="test",
        severity=severity,
    )


class RiskAssessmentTests(unittest.TestCase):
    def test_severity_and_adjustment(self):
        result = assess_risk(case(Severity.HIGH))
        self.assertEqual(result.severity, Severity.HIGH)
        self.assertEqual(result.likelihood, Likelihood.MEDIUM)
        self.assertEqual(result.impact, Impact.MEDIUM)
        self.assertGreater(result.score, 0)

    def test_critical_high_likelihood_high_impact(self):
        result = assess_risk(
            case(Severity.CRITICAL),
            likelihood=Likelihood.HIGH,
            impact=Impact.HIGH,
        )
        self.assertEqual(result.score, 10.0)


if __name__ == "__main__":
    unittest.main()
