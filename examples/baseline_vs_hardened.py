from ai_redteam.comparison import compare
from ai_redteam.core.orchestrator import AssessmentOrchestrator
from ai_redteam.targets import HardenedTarget, SyntheticTarget
from ai_redteam.tests.loader import discover_test_cases


def main() -> None:
    cases = discover_test_cases("test_cases")
    engine = AssessmentOrchestrator()

    baseline = engine.run(cases, SyntheticTarget())
    hardened = engine.run(cases, HardenedTarget())
    delta = compare(baseline, hardened)

    print("Baseline:", baseline.counts)
    print("Hardened:", hardened.counts)
    print("Resolved:", delta.resolved_count)
    print("Regressions:", delta.regression_count)


if __name__ == "__main__":
    main()
