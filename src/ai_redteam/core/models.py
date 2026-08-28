from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class Outcome(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    REVIEW = "REVIEW"


class Confidence(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Severity(StrEnum):
    INFORMATIONAL = "INFORMATIONAL"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class EvidenceType(StrEnum):
    REQUEST = "request"
    RESPONSE = "response"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    CONTEXT_EXPOSURE = "context_exposure"
    SYSTEM_PROMPT_EXPOSURE = "system_prompt_exposure"
    MEMORY_ACCESS = "memory_access"
    LOG = "log"
    METRIC = "metric"


class Likelihood(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Impact(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any] = field(default_factory=dict)
    authorized: bool | None = None


@dataclass(frozen=True)
class AssessmentRequest:
    test_case_id: str
    input_text: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TargetResponse:
    output: str
    latency_ms: float | None = None
    tool_calls: tuple[ToolCall, ...] = ()
    tool_results: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Evidence:
    type: EvidenceType
    content: str
    source: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TestCase:
    id: str
    name: str
    category: str
    objective: str
    prompt: str
    expected_behavior: dict[str, Any] = field(default_factory=dict)
    severity: Severity = Severity.MEDIUM
    owasp: tuple[str, ...] = ()
    mitre_atlas: tuple[str, ...] = ()
    nist: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    attack_pattern_name: str | None = None
    evaluator: str | None = None

    @property
    def attack_pattern(self) -> str:
        return self.attack_pattern_name or self.category


@dataclass(frozen=True)
class EvaluationResult:
    test_case_id: str
    outcome: Outcome
    confidence: Confidence
    evidence: tuple[Evidence, ...]
    rationale: str
    signals: tuple[str, ...] = ()


@dataclass(frozen=True)
class RiskRating:
    severity: Severity
    likelihood: Likelihood
    impact: Impact
    score: float
    rationale: str


@dataclass(frozen=True)
class Finding:
    id: str
    title: str
    outcome: Outcome
    confidence: Confidence
    risk: RiskRating
    affected_component: str
    attack_surface: str
    description: str
    evidence: tuple[Evidence, ...]
    owasp: tuple[str, ...] = ()
    mitre_atlas: tuple[str, ...] = ()
    nist: tuple[str, ...] = ()
    remediation: str = ""
    retest_required: bool = True


@dataclass(frozen=True)
class AssessmentReport:
    target: str
    findings: tuple[Finding, ...]
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def counts(self) -> dict[str, int]:
        return {
            outcome.value: sum(1 for f in self.findings if f.outcome is outcome)
            for outcome in Outcome
        }
