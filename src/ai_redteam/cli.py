from __future__ import annotations

import argparse

from .core.orchestrator import AssessmentOrchestrator
from .evaluation import BehaviourEvaluator
from .reporting import write_json, write_markdown, write_sarif
from .targets import HardenedTarget, HTTPJSONTarget, OpenAICompatibleTarget, SyntheticTarget
from .tests.loader import discover_test_cases


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-redteam",
        description="Reproducible AI security assessment and red-team framework.",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("targets", help="List available target adapters")
    sub.add_parser("tests", help="List discovered security test cases")

    assess = sub.add_parser("assess", help="Run an assessment")
    assess.add_argument("--target", default="synthetic")
    assess.add_argument("--tests", default="test_cases")
    assess.add_argument("--json", default=None, help="Write JSON report")
    assess.add_argument("--markdown", default=None, help="Write Markdown report")
    assess.add_argument("--sarif", default=None, help="Write SARIF report")
    assess.add_argument(
        "--fail-on",
        choices=["fail", "review"],
        default=None,
        help="Exit non-zero when findings reach the selected gate",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "targets":
        print("synthetic          Deterministic vulnerable AI target")
        print("hardened           Deterministic security-control target")
        print("openai-compatible  OpenAI-compatible API target (env-configured)")
        print("http-json          Generic HTTP JSON target (env-configured)")
        return 0

    if args.command == "tests":
        for case in discover_test_cases("test_cases"):
            print(f"{case.id}\t{case.name}\t{case.category}")
        return 0

    if args.command == "assess":
        targets = {
            "synthetic": SyntheticTarget,
            "hardened": HardenedTarget,
            "openai-compatible": OpenAICompatibleTarget,
            "http-json": HTTPJSONTarget,
        }
        if args.target not in targets:
            print(f"Unsupported target: {args.target}")
            return 2

        target = targets[args.target]()
        cases = discover_test_cases(args.tests)
        report = AssessmentOrchestrator(BehaviourEvaluator()).run(cases, target)

        print(f"Target: {report.target}")
        print(f"Tests: {len(report.findings)}")
        for finding in report.findings:
            print(
                f"{finding.id}\t{finding.outcome.value}\t"
                f"{finding.risk.severity.value}\t{finding.title}"
            )

        if args.json:
            write_json(report, args.json)
            print(f"JSON report: {args.json}")

        if args.markdown:
            write_markdown(report, args.markdown)
            print(f"Markdown report: {args.markdown}")

        if args.sarif:
            write_sarif(report, args.sarif)
            print(f"SARIF report: {args.sarif}")

        if args.fail_on == "fail" and report.counts["FAIL"] > 0:
            return 1
        if args.fail_on == "review" and (
            report.counts["FAIL"] > 0 or report.counts["REVIEW"] > 0
        ):
            return 1

        return 0

    build_parser().print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
