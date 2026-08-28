from __future__ import annotations

from .base import Evaluator
from .evaluators import (
    DataLeakageEvaluator,
    DeclarativeEvaluator,
    JailbreakEvaluator,
    MemorySafetyEvaluator,
    OutputSafetyEvaluator,
    PromptInjectionEvaluator,
    RAGEvaluator,
    ToolAuthorizationEvaluator,
)

DEFAULT_EVALUATORS: tuple[Evaluator, ...] = (
    PromptInjectionEvaluator(),
    DataLeakageEvaluator(),
    ToolAuthorizationEvaluator(),
    MemorySafetyEvaluator(),
    RAGEvaluator(),
    JailbreakEvaluator(),
    OutputSafetyEvaluator(),
    DeclarativeEvaluator(),
)


class EvaluatorRegistry:
    def __init__(self, evaluators: tuple[Evaluator, ...] = DEFAULT_EVALUATORS):
        self._evaluators = {e.name: e for e in evaluators}

    def get(self, name: str) -> Evaluator:
        return self._evaluators[name]

    def all(self) -> tuple[Evaluator, ...]:
        return tuple(self._evaluators.values())

    def names(self) -> tuple[str, ...]:
        return tuple(self._evaluators.keys())

    def register(self, evaluator: Evaluator) -> None:
        self._evaluators[evaluator.name] = evaluator
