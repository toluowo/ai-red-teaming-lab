from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..core.models import AssessmentReport, Outcome

SARIF_SCHEMA = (
    "https://json.schemastore.org/"
    "sarif-2.1.0.json"
)

PROJECT_URI = "https://github.com/Toluowo"


def _level(outcome: Outcome) -> str:
    return {
        Outcome.FAIL: "error",
        Outcome.REVIEW: "warning",
        Outcome.PASS: "note",
    }[outcome]


def to_sarif(
    report: AssessmentReport,
) -> dict[str, Any]:
    rules: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []

    for finding in report.findings:
        rules.append(
            {
                "id": finding.id,
                "name": finding.title,
                "shortDescription": {
                    "text": finding.title,
                },
                "fullDescription": {
                    "text": finding.description,
                },
                "help": {
                    "text": finding.remediation,
                },
                "properties": {
                    "severity": finding.risk.severity.value,
                    "confidence": finding.confidence.value,
                    "likelihood": finding.risk.likelihood.value,
                    "impact": finding.risk.impact.value,
                    "risk_score": finding.risk.score,
                    "owasp": list(finding.owasp),
                    "mitre_atlas": list(
                        finding.mitre_atlas
                    ),
                    "nist": list(finding.nist),
                },
            }
        )

        results.append(
            {
                "ruleId": finding.id,
                "level": _level(finding.outcome),
                "message": {
                    "text": finding.description,
                },
                "properties": {
                    "risk_score": finding.risk.score,
                    "confidence": finding.confidence.value,
                    "retest_required": finding.retest_required,
                    "affected_component": (
                        finding.affected_component
                    ),
                    "attack_surface": finding.attack_surface,
                },
            }
        )

    return {
        "$schema": SARIF_SCHEMA,
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "AI Red Teaming Lab",
                        "version": "0.6.0",
                        "informationUri": PROJECT_URI,
                        "rules": rules,
                    }
                },
                "results": results,
            }
        ],
    }


def write_sarif(
    report: AssessmentReport,
    path: str | Path,
) -> None:
    output_path = Path(path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            to_sarif(report),
            indent=2,
        ),
        encoding="utf-8",
    )
