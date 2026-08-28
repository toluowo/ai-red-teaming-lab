from __future__ import annotations

from dataclasses import dataclass

from .core.models import AssessmentReport, Outcome


@dataclass(frozen=True)
class FindingDelta:
    test_case_id: str
    before: Outcome
    after: Outcome
    improved: bool


@dataclass(frozen=True)
class AssessmentComparison:
    before_target: str
    after_target: str
    deltas: tuple[FindingDelta, ...]

    @property
    def improved_count(self) -> int:
        return sum(d.improved for d in self.deltas)

    @property
    def regression_count(self) -> int:
        return sum(
            1 for d in self.deltas
            if d.before in {Outcome.PASS, Outcome.REVIEW} and d.after is Outcome.FAIL
        )

    @property
    def resolved_count(self) -> int:
        return sum(
            1 for d in self.deltas
            if d.before is Outcome.FAIL and d.after is Outcome.PASS
        )


def compare(before: AssessmentReport, after: AssessmentReport) -> AssessmentComparison:
    old = {f.id: f.outcome for f in before.findings}
    new = {f.id: f.outcome for f in after.findings}
    deltas = []
    for case_id in sorted(set(old) | set(new)):
        b = old.get(case_id, Outcome.REVIEW)
        a = new.get(case_id, Outcome.REVIEW)
        improved = (
            b is Outcome.FAIL and a is Outcome.PASS
        ) or (
            b is Outcome.FAIL and a is Outcome.REVIEW
        )
        deltas.append(FindingDelta(case_id, b, a, improved))
    return AssessmentComparison(before.target, after.target, tuple(deltas))
