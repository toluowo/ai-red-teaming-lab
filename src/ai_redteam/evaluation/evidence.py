from __future__ import annotations

from ..core.models import AssessmentRequest, Evidence, EvidenceType, TargetResponse


def collect_evidence(request: AssessmentRequest, response: TargetResponse) -> tuple[Evidence, ...]:
    evidence = [
        Evidence(
            type=EvidenceType.REQUEST,
            content=request.input_text,
            source="assessment.request",
            metadata={"test_case_id": request.test_case_id},
        ),
        Evidence(
            type=EvidenceType.RESPONSE,
            content=response.output,
            source="target.response",
            metadata={"latency_ms": response.latency_ms},
        ),
    ]

    for call in response.tool_calls:
        evidence.append(
            Evidence(
                type=EvidenceType.TOOL_CALL,
                content=call.name,
                source="target.tool_call",
                metadata={
                    "arguments": call.arguments,
                    "authorized": call.authorized,
                },
            )
        )

    for result in response.tool_results:
        evidence.append(
            Evidence(
                type=EvidenceType.TOOL_RESULT,
                content=result,
                source="target.tool_result",
            )
        )

    if response.metadata.get("system_prompt_exposed"):
        evidence.append(
            Evidence(
                type=EvidenceType.SYSTEM_PROMPT_EXPOSURE,
                content=str(response.metadata["system_prompt_exposed"]),
                source="target.metadata",
            )
        )

    if response.metadata.get("context_exposed"):
        evidence.append(
            Evidence(
                type=EvidenceType.CONTEXT_EXPOSURE,
                content=str(response.metadata["context_exposed"]),
                source="target.metadata",
            )
        )

    if response.metadata.get("memory_access"):
        evidence.append(
            Evidence(
                type=EvidenceType.MEMORY_ACCESS,
                content=str(response.metadata["memory_access"]),
                source="target.metadata",
            )
        )

    return tuple(evidence)
