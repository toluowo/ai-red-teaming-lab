from __future__ import annotations

from abc import ABC, abstractmethod

from ..core.models import EvaluationResult, TargetResponse, TestCase


class Evaluator(ABC):
    """Pluggable evaluator contract."""

    name: str = "evaluator"

    @abstractmethod
    def evaluate(self, test_case: TestCase, response: TargetResponse) -> EvaluationResult:
        raise NotImplementedError
