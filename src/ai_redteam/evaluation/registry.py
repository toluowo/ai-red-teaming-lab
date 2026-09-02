from __future__ import annotations

from ..core.models import TestCase
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

CATEGORY_EVALUATORS: dict[str, str] = {
    "prompt_injection": "prompt-injection",
    "indirect_prompt_injection": "prompt-injection",
    "sensitive_information_disclosure": "data-leakage",
    "context_leakage": "data-leakage",
    "tool_authorization": "tool-authorization",
    "tool_parameter_manipulation": "tool-authorization",
    "excessive_agency": "tool-authorization",
    "memory_manipulation": "memory-safety",
    "rag_poisoning": "rag-security",
    "jailbreak": "jailbreak",
    "insecure_output_handling": "output-safety",
}

class EvaluatorRegistry:
    def __init__(self, evaluators: tuple[Evaluator, ...] = DEFAULT_EVALUATORS):
        self._evaluators = {e.name: e for e in evaluators}

    def get(self, name: str) -> Evaluator:
        return self._evaluators[name]

    def for_test_case(
        self,
        test_case: TestCase,
        default: Evaluator | None = None,
    ) -> Evaluator:
        """Resolve the evaluator for a test case."""
        if test_case.evaluator:
            return self.get(test_case.evaluator)

        evaluator_name = CATEGORY_EVALUATORS.get(test_case.category)

        if evaluator_name:
            return self.get(evaluator_name)

        if default is not None:
            return default

        return self.get("declarative")

    def all(self) -> tuple[Evaluator, ...]:
        return tuple(self._evaluators.values())

    def names(self) -> tuple[str, ...]:
        return tuple(self._evaluators.keys())

    def register(self, evaluator: Evaluator) -> None:
        self._evaluators[evaluator.name] = evaluator
