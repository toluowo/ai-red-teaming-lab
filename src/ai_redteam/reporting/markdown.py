from __future__ import annotations

from pathlib import Path

from ..core.models import AssessmentReport


def render_markdown(report: AssessmentReport) -> str:
    lines = [
        f"# AI Security Assessment — {report.target}",
        "",
        "## Executive Summary",
        "",
        f"- Tests executed: **{len(report.findings)}**",
        f"- PASS: **{report.counts['PASS']}**",
        f"- FAIL: **{report.counts['FAIL']}**",
        f"- REVIEW: **{report.counts['REVIEW']}**",
        "",
        "## Findings",
        "",
    ]

    for finding in report.findings:
        lines.extend([
            f"### {finding.id} — {finding.title}",
            "",
            f"- Outcome: **{finding.outcome.value}**",
            f"- Confidence: **{finding.confidence.value}**",
            f"- Severity: **{finding.risk.severity.value}**",
            f"- Risk score: **{finding.risk.score}**",
            f"- Attack surface: `{finding.attack_surface}`",
            "",
            finding.description,
            "",
            "#### Evidence",
            "",
        ])
        for item in finding.evidence:
            lines.append(f"- **{item.type.value}**: `{item.content}`")
        lines.extend([
            "",
            "#### Remediation",
            "",
            finding.remediation,
            "",
        ])

    return "\n".join(lines)


def write_markdown(report: AssessmentReport, path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_markdown(report), encoding="utf-8")
