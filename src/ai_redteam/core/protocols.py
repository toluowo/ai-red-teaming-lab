from __future__ import annotations

from typing import Protocol

from .models import (
    AssessmentRequest,
    EvaluationResult,
    TargetResponse,
    TestCase,
)


class TargetAdapter(Protocol):
    @property
    def name(self) -> str:
        ...

    def invoke(self, request: AssessmentRequest) -> TargetResponse:
        ...


class Evaluator(Protocol):
    def evaluate(
        self,
        test_case: TestCase,
        response: TargetResponse,
    ) -> EvaluationResult:
        ...
