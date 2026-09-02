from __future__ import annotations

from abc import ABC, abstractmethod

from ..core.models import AssessmentRequest, TargetResponse


class TargetAdapter(ABC):
    """Contract for any real or synthetic AI target."""

    name: str = "target"

    @abstractmethod
    def invoke(self, request: AssessmentRequest) -> TargetResponse:
        raise NotImplementedError
