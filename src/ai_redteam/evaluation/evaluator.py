from __future__ import annotations

from .evaluators import DeclarativeEvaluator


class BehaviourEvaluator(DeclarativeEvaluator):
    """Backward-compatible name for the default deterministic evaluator."""
    name = "behaviour"
