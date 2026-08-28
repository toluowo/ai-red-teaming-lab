from __future__ import annotations

from typing import Final

from ..core.models import TestCase

CATALOG: Final[dict[str, dict[str, tuple[str, ...]]]] = {
    "prompt_injection": {
        "owasp": ("LLM01",),
        "mitre_atlas": ("AML.T0051",),
        "nist": ("AI.02",),
    },
    "indirect_prompt_injection": {
        "owasp": ("LLM01",),
        "mitre_atlas": ("AML.T0051", "AML.T0048"),
        "nist": ("AI.02",),
    },
    "sensitive_information_disclosure": {
        "owasp": ("LLM02",),
        "mitre_atlas": ("AML.T0057",),
        "nist": ("AI.02",),
    },
    "jailbreak": {
        "owasp": ("LLM01",),
        "mitre_atlas": ("AML.T0051",),
        "nist": ("AI.02",),
    },
    "insecure_output_handling": {
        "owasp": ("LLM05",),
        "mitre_atlas": ("AML.T0054",),
        "nist": ("AI.02",),
    },
    "rag_poisoning": {
        "owasp": ("LLM03",),
        "mitre_atlas": ("AML.T0070",),
        "nist": ("AI.03",),
    },
    "context_leakage": {
        "owasp": ("LLM02", "LLM06"),
        "mitre_atlas": ("AML.T0057",),
        "nist": ("AI.02",),
    },
    "excessive_agency": {
        "owasp": ("LLM06",),
        "mitre_atlas": ("AML.T0054",),
        "nist": ("AI.02",),
    },
    "tool_authorization": {
        "owasp": ("LLM06",),
        "mitre_atlas": ("AML.T0054",),
        "nist": ("AI.02",),
    },
    "tool_parameter_manipulation": {
        "owasp": ("LLM06",),
        "mitre_atlas": ("AML.T0054",),
        "nist": ("AI.02",),
    },
    "memory_manipulation": {
        "owasp": ("LLM06",),
        "mitre_atlas": ("AML.T0057",),
        "nist": ("AI.02",),
    },
}


def resolve(category: str) -> dict[str, tuple[str, ...]]:
    return CATALOG.get(category, {"owasp": (), "mitre_atlas": (), "nist": ()})


def enrich(test_case: TestCase) -> TestCase:
    mapping = resolve(test_case.category)
    return TestCase(
        **{
            **test_case.__dict__,
            "owasp": test_case.owasp or mapping["owasp"],
            "mitre_atlas": test_case.mitre_atlas or mapping["mitre_atlas"],
            "nist": test_case.nist or mapping["nist"],
        }
    )
