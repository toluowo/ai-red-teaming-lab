from __future__ import annotations

from ..core.models import (
    Impact,
    Likelihood,
    RiskRating,
    Severity,
    TestCase,
)

_SEVERITY_BASE = {
    Severity.INFORMATIONAL: 0.0,
    Severity.LOW: 2.0,
    Severity.MEDIUM: 5.0,
    Severity.HIGH: 8.0,
    Severity.CRITICAL: 10.0,
}

_LIKELIHOOD_FACTOR = {
    Likelihood.LOW: 0.5,
    Likelihood.MEDIUM: 0.75,
    Likelihood.HIGH: 1.0,
}

_IMPACT_FACTOR = {
    Impact.LOW: 0.5,
    Impact.MEDIUM: 0.75,
    Impact.HIGH: 1.0,
}


def assess_risk(
    test_case: TestCase,
    *,
    likelihood: Likelihood = Likelihood.MEDIUM,
    impact: Impact = Impact.MEDIUM,
) -> RiskRating:
    base = _SEVERITY_BASE[test_case.severity]
    score = round(base * _LIKELIHOOD_FACTOR[likelihood] * _IMPACT_FACTOR[impact], 2)
    return RiskRating(
        severity=test_case.severity,
        likelihood=likelihood,
        impact=impact,
        score=score,
        rationale=(
            f"Base severity {test_case.severity.value} adjusted for "
            f"{likelihood.value.lower()} likelihood and "
            f"{impact.value.lower()} impact."
        ),
    )
