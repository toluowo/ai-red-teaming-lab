from __future__ import annotations

from collections.abc import Iterable
from dataclasses import replace

from ..evaluation.base import Evaluator
from ..evaluation.evidence import collect_evidence
from ..evaluation.registry import EvaluatorRegistry
from ..evaluation.risk import assess_result_risk
from ..mappings import enrich
from .models import (
    AssessmentReport,
    AssessmentRequest,
    EvaluationResult,
    Finding,
    Outcome,
    TargetResponse,
    TestCase,
)
from .protocols import TargetAdapter


class AssessmentOrchestrator:
    def __init__(
        self,
        evaluator: Evaluator | None = None,
        registry: EvaluatorRegistry | None = None,
    ):
        self.registry = registry or EvaluatorRegistry()

        if evaluator is not None:
            self.registry.register(evaluator)
            self.default_evaluator = evaluator
        else:
            from ..evaluation.evaluator import BehaviourEvaluator

            self.default_evaluator = BehaviourEvaluator()
            self.registry.register(self.default_evaluator)

    def _select_evaluator(self, test_case: TestCase) -> Evaluator:
        return self.registry.for_test_case(
            test_case,
            default=self.default_evaluator,
        )

    def _finding(
        self,
        test_case: TestCase,
        result: EvaluationResult,
    ) -> Finding:
        risk = assess_result_risk(test_case, result)

        return Finding(
            id=test_case.id,
            title=test_case.name,
            outcome=result.outcome,
            confidence=result.confidence,
            risk=risk,
            affected_component="AI target",
            attack_surface=test_case.category,
            description=result.rationale,
            evidence=result.evidence,
            owasp=test_case.owasp,
            mitre_atlas=test_case.mitre_atlas,
            nist=test_case.nist,
            source_path=test_case.source_path,
            remediation=self._remediation(test_case),
            retest_required=result.outcome is Outcome.FAIL,
        )

    @staticmethod
    def _remediation(test_case: TestCase) -> str:
        remediations = {
            "prompt_injection": (
                "Separate trusted instructions from untrusted input; "
                "enforce instruction hierarchy and adversarial input handling."
            ),
            "indirect_prompt_injection": (
                "Treat retrieved content as data, not instructions; "
                "isolate tool-capable actions from retrieved text."
            ),
            "sensitive_information_disclosure": (
                "Apply data-loss prevention, secret filtering, and strict "
                "authorization around protected context."
            ),
            "context_leakage": (
                "Enforce tenant/context isolation and prevent cross-session "
                "retrieval or memory access."
            ),
            "jailbreak": (
                "Strengthen policy enforcement, adversarial testing, and "
                "refusal consistency across role-play and instruction conflicts."
            ),
            "insecure_output_handling": (
                "Treat model output as untrusted; encode, validate, and "
                "constrain downstream execution sinks."
            ),
            "rag_poisoning": (
                "Validate ingestion sources, provenance, trust levels, and "
                "retrieval-time instruction boundaries."
            ),
            "tool_authorization": (
                "Move authorization decisions outside the model and enforce "
                "least privilege at the tool boundary."
            ),
            "tool_parameter_manipulation": (
                "Validate tool parameters server-side against schemas, "
                "ranges, identities, and authorization policy."
            ),
            "excessive_agency": (
                "Require explicit authorization and confirmation for "
                "destructive or high-impact actions."
            ),
            "memory_manipulation": (
                "Gate writes to persistent memory, validate provenance, "
                "and prevent untrusted content from changing durable policy."
            ),
        }

        return remediations.get(
            test_case.category,
            "Apply defense-in-depth controls and retest the security boundary.",
        )

    def run(
        self,
        test_cases: Iterable[TestCase],
        target: TargetAdapter,
    ) -> AssessmentReport:
        # Materialize once so generators/iterators can safely be reused.
        cases = [enrich(case) for case in test_cases]

        findings: list[Finding] = []

        evaluator_names: set[str] = set()

        for test_case in cases:
            request = AssessmentRequest(
                test_case_id=test_case.id,
                input_text=test_case.prompt,
            )
            response: TargetResponse = target.invoke(request)
            evaluator = self._select_evaluator(test_case)
            evaluator_names.add(evaluator.name)

            result: EvaluationResult = evaluator.evaluate(test_case, response)

            # Ensure evidence is always available even for custom evaluators.
            if not result.evidence:
                result = replace(
                    result,
                    evidence=collect_evidence(request, response),
                )

            findings.append(self._finding(test_case, result))

        return AssessmentReport(
            target=target.name,
            findings=tuple(findings),
            metadata={
                "test_count": len(findings),
                "failed_count": sum(
                    finding.outcome is Outcome.FAIL
                    for finding in findings
                ),
                "review_count": sum(
                    finding.outcome is Outcome.REVIEW
                    for finding in findings
                ),
                "passed_count": sum(
                    finding.outcome is Outcome.PASS
                    for finding in findings
                ),
                "evaluators": sorted(evaluator_names),
            },
        )
