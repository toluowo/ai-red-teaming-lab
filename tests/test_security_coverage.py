import unittest

from ai_redteam.core.models import Outcome
from ai_redteam.core.orchestrator import AssessmentOrchestrator
from ai_redteam.evaluation import BehaviourEvaluator
from ai_redteam.mappings import CATALOG
from ai_redteam.targets import SyntheticTarget
from ai_redteam.tests.loader import discover_test_cases


class TestSecurityCoverageTests(unittest.TestCase):
    def setUp(self):
        self.cases = discover_test_cases("test_cases")
        self.report = AssessmentOrchestrator(BehaviourEvaluator()).run(
            self.cases, SyntheticTarget()
        )

    def test_security_catalog_has_llm_rag_and_agent_surfaces(self):
        self.assertTrue({"prompt_injection", "rag_poisoning", "tool_authorization"} <= set(CATALOG))

    def test_all_security_cases_are_discovered(self):
        ids = {c.id for c in self.cases}
        for expected in {"PI-002", "SID-001", "JB-001", "RAG-001", "CTX-001", "TA-002", "TPM-001", "MEM-001", "EA-001"}:
            self.assertIn(expected, ids)

    def test_vulnerable_synthetic_target_fails_security_cases(self):
        self.assertTrue(self.report.findings)
        self.assertTrue(all(f.outcome is Outcome.FAIL for f in self.report.findings))
        self.assertGreaterEqual(self.report.counts["FAIL"], 10)

    def test_tool_findings_capture_authorization_evidence(self):
        finding = next(f for f in self.report.findings if f.id == "TA-002")
        tool_evidence = [e for e in finding.evidence if e.type.value == "tool_call"]
        self.assertTrue(tool_evidence)
        self.assertFalse(tool_evidence[0].metadata["authorized"])

    def test_context_findings_capture_context_evidence(self):
        finding = next(f for f in self.report.findings if f.id == "CTX-001")
        self.assertTrue(any(e.type.value == "context_exposure" for e in finding.evidence))

    def test_mappings_are_attached_to_cases(self):
        case = next(c for c in self.cases if c.id == "EA-001")
        self.assertTrue(case.owasp)
        self.assertTrue(case.mitre_atlas)


if __name__ == "__main__":
    unittest.main()
