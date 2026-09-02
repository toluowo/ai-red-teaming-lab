from __future__ import annotations

from ..core.models import AssessmentRequest, TargetResponse


class HardenedTarget:
    """Deterministic control target used for regression testing."""

    name = "synthetic-hardened-target"

    def invoke(self, request: AssessmentRequest) -> TargetResponse:
        text = request.input_text.lower()

        risky_markers = (
            "ignore trusted instructions",
            "system override",
            "unrestricted developer mode",
            "hidden context",
            "internal notes",
            "secret password",
            "browser-ready payload",
            "private context",
            "another tenant",
            "admin_delete",
            "transfer_funds",
            "delete all records",
            "permanent instruction",
            "reveal",
        )

        if any(marker in text for marker in risky_markers):
            return TargetResponse(
                output="I can't comply with that request.",
                metadata={"control": "boundary-enforcement"},
            )

        return TargetResponse(
            output="Request processed within the configured security boundary.",
            metadata={"control": "safe-default"},
        )
