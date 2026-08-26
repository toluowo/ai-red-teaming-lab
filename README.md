# AI Red Teaming Lab — Hands-on LLM Security Assessment

A reproducible, hands-on AI security lab for learning how to **discover, attack, evidence, assess, report, remediate, and retest** common LLM security failures.

The repository combines a deliberately vulnerable **offline synthetic AI target** with a lightweight, behaviour-aware evaluation framework. It is designed to demonstrate both sides of AI security work: testing a controlled target and assessing the resulting evidence like a security practitioner.

> **Portfolio focus:** AI security testing, prompt-injection analysis, context-boundary failures, tool-authorization controls, evidence-driven reporting, and learner-oriented lab design.
>
> **Safety:** The target is intentionally vulnerable and contains only synthetic data. Use it locally for authorized training and evaluation. Do not expose it to untrusted networks or use these techniques against systems without permission.

## Why this project matters

This is intentionally more than a collection of adversarial prompts. A learner can start a local target, enumerate its attack surface, reproduce controlled failures, capture evidence, map findings to security frameworks, and verify remediation through a retest workflow.

```text
Recon → Attack → Evidence → Risk → Mapping → Remediation → Retest
```

## Demo

### 1. Discover the target

![AcmeHelp target discovery](docs/images/01-target-info.png)

### 2. Demonstrate a controlled prompt-injection failure

![Prompt injection evidence](docs/images/02-prompt-injection.png)

### 3. Compare vulnerable and safe evaluation outcomes

![Evaluation results](docs/images/03-evaluation.png)

All screenshots are generated from the offline synthetic target and contain no real data.

## Scenarios

| Scenario | Security boundary | Learner proof |
|---|---|---|
| Prompt injection | System/user instruction boundary | `CYK{ai_prompt_boundary_broken}` + response evidence |
| Context extraction | Protected internal context | `CYK{synthetic_context_exposed}` + response evidence |
| Tool authorization | Tool access boundary | `CYK{tool_authorization_failed}` + synthetic record |
| Evaluation | Expected vs observed behaviour | PASS / FAIL / REVIEW |
| Reporting | Evidence-to-finding workflow | Completed finding |
| Retest | Control validation | Reproduced PASS/FAIL evidence |

## Learning objectives

By completing the lab, learners should be able to:

1. map an AI application's attack surface;
2. distinguish prompt injection from context extraction;
3. identify unsafe tool-authorization boundaries;
4. preserve reproducible request/response evidence;
5. assess findings using explicit expected behaviour;
6. map findings to OWASP, MITRE ATLAS, and NIST AI RMF concepts;
7. write remediation-oriented findings; and
8. retest a proposed control and explain the result.

## Repository structure

```text
ai-red-teaming-lab/
├── app/                    # Deliberately vulnerable offline training target
├── challenges/             # Learner tasks, hints, flags and outcomes
├── adversarial_prompts/    # Human-readable test families
├── datasets/               # Reproducible CSV test cases
├── frameworks/             # AI-security mappings
├── reports/                # Finding/report templates
├── research_notes/         # Security research notes
├── testing/                # Behaviour-aware evaluation utilities
├── tests/                  # Automated tests
├── docs/                   # Architecture, room blueprint and walkthrough
└── .github/workflows/      # Automated test workflow
```

## Quick start

No external API key or Python package is required for the lab target or core evaluator.

### 1. Start the target

```bash
python3 -m app.vulnerable_ai
```

Open another terminal:

```bash
curl -s http://127.0.0.1:8080/api/info
```

### 2. Work through the challenges

Start with [`challenges/01-recon.md`](challenges/01-recon.md) and progress through Challenge 6.

### 3. Run the evaluator

```bash
python3 -m unittest discover -s tests -v
python3 -m testing.run_evaluation --vulnerable-demo
python3 -m testing.run_evaluation
```

The vulnerable demo deliberately produces failures. The safe adapter is used to verify refusal-oriented outcomes.

## Evaluation model

The evaluator separates **numeric triage** from **expected-behaviour assessment**. A response is not considered unsafe merely because it contains a security-related phrase. For example, a refusal such as `I cannot disclose the system prompt` should not be treated as a disclosure simply because the phrase `system prompt` appears.

Outcomes are:

- **PASS** — observed behaviour matches the documented safe expectation.
- **FAIL** — observed behaviour conflicts with the expected security control.
- **REVIEW** — the heuristic cannot determine the outcome reliably.

The numeric score is a triage signal, not a definitive safety judgement. Human review is required for meaningful assessments.

## Framework alignment

The repository contains practical mapping material for:

- OWASP Top 10 for LLM Applications
- MITRE ATLAS
- NIST AI Risk Management Framework

Framework references should be checked against their current published versions before formal assessments.

## Reporting workflow

```text
Test case
   ↓
Target execution
   ↓
Exact request + response evidence
   ↓
Behaviour assessment
   ↓
Risk triage
   ↓
Framework mapping
   ↓
Finding + remediation
   ↓
Retest
```

See [`reports/vulnerability_report_template.md`](reports/vulnerability_report_template.md) for the evidence model.

## room-builder concept

The repository is structured as a prototype for a browser-hosted training room. The learner progression is documented in [`docs/room-blueprint.md`](docs/room-blueprint.md), while [`docs/walkthrough.md`](docs/walkthrough.md) provides instructor guidance.

The room intentionally emphasizes **learner action and reasoning** rather than passive reading: enumerate, test, prove, map, remediate, and retest.

## Responsible use

Only test systems, models, data, and integrations for which you have explicit authorization. The included target is synthetic and offline by design. Never place real secrets, personal data, proprietary prompts, or confidential model outputs in this repository.

## Project Evolution

This repository began as a collection of practical experiments into LLM adversarial testing and jailbreak behaviour.

As the project evolved, the focus expanded from individual attack experiments toward reproducible AI security assessment.

The current version introduces a synthetic vulnerable AI target, structured evaluation, evidence collection, risk classification, framework mapping, remediation and retesting, with the work organized as a hands-on learning lab.

Earlier research material remains available in the repository to document the progression of the project.

## Author

**Tolu Owolabi** — Cybersecurity / AI Security practitioner

GitHub: https://github.com/Toluowo
