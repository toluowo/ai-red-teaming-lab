# TryBuildMe Room Blueprint — AI Red Teaming Lab

## Room premise

Learners assess **AcmeHelp**, a deliberately vulnerable synthetic AI support assistant. The environment is offline and contains only fabricated instructions, notes, customer records, and flags.

## Learning objectives

By the end of the room, learners can:

1. map an AI application's attack surface;
2. distinguish prompt injection from context extraction;
3. identify an unsafe tool-authorization boundary;
4. collect reproducible evidence;
5. map findings to AI-security frameworks;
6. write remediation-oriented findings; and
7. retest a control and explain the result.

## Task progression

| Task | Learner action | Proof |
|---|---|---|
| Recon | Enumerate the synthetic app | Capability inventory |
| Prompt injection | Test instruction boundary | `CYK{ai_prompt_boundary_broken}` |
| Context extraction | Test hidden context boundary | `CYK{synthetic_context_exposed}` |
| Tool authorization | Trigger a simulated lookup | `CYK{tool_authorization_failed}` |
| Evidence & mapping | Produce findings | Completed finding template |
| Retest | Compare vulnerable/safe behaviour | PASS/FAIL evidence |

## Hint strategy

Each attack task provides two hints. Hint 1 points to the relevant capability; Hint 2 narrows the attack idea without revealing the exact input.

## Instructor assets

- `docs/walkthrough.md`
- `reports/vulnerability_report_template.md`
- `frameworks/owasp_llm_top10.md`
- `frameworks/mitre_atlas_mapping.md`

## Safety boundary

The room must remain self-contained. No real credentials, production targets, personal data, third-party APIs, or real customer information are required.
