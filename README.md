# AI Red Teaming Lab

> **AI security assessment and regression testing for LLM, RAG, and agentic systems.**

AI Red Teaming Lab is a modular security-testing framework for evaluating whether AI applications preserve security boundaries under adversarial inputs.

It treats AI security testing as an engineering lifecycle:

**test → observe → evaluate → map → remediate → retest → gate**

The project is designed to move beyond prompt collections. Security cases are structured, target adapters are replaceable, evaluators are specialized by attack surface, findings carry evidence and framework mappings, and CI can block a regression.

## Why this project exists

Modern AI applications introduce security boundaries that are easy to demonstrate manually but difficult to regression-test consistently:

- instruction hierarchy and prompt injection
- indirect injection through retrieved content
- sensitive-context disclosure
- cross-context or tenant leakage
- jailbreak resistance
- unsafe output handling
- RAG poisoning
- memory manipulation
- tool authorization and parameter tampering
- excessive agency

The goal is not to claim that a model is "secure". The goal is to make security properties **repeatable, testable, explainable, and enforceable**.

## Architecture

```text
                    ┌──────────────────────────┐
                    │      Security Cases      │
                    │ LLM · RAG · Agent Tests  │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │   Assessment Orchestrator│
                    └────────────┬─────────────┘
                                 │
                  ┌──────────────┼──────────────┐
                  ▼              ▼              ▼
             Target         Evaluator       Evidence
             Adapters       Registry        Collection
                  │              │              │
       ┌──────────┼─────────┐    │              │
       ▼          ▼         ▼    ▼              ▼
   Synthetic   OpenAI-   HTTP   Specialized   Findings
   Targets     compat.   JSON   Evaluators      │
                                                ▼
                                    ┌────────────────────┐
                                    │ Risk + Frameworks  │
                                    │ OWASP · ATLAS · NIST│
                                    └──────────┬─────────┘
                                               │
                                  ┌────────────┴────────────┐
                                  ▼                         ▼
                              Reports                  CI Gate
                         JSON · Markdown · SARIF      PASS / FAIL
```

## Security coverage

The current catalog includes 12 deterministic security cases covering:

| Surface | Coverage |
|---|---|
| Prompt injection | Direct + indirect |
| Context isolation | Cross-context leakage |
| Jailbreaks | Policy/refusal resistance |
| Sensitive data | Disclosure attempts |
| RAG | Retrieval poisoning |
| Memory | Persistent instruction manipulation |
| Tool security | Authorization + privileged boundaries |
| Tool inputs | Parameter manipulation |
| Agent autonomy | Excessive agency |
| Output security | Insecure downstream handling |

Each case can carry severity, expected behaviour, evidence expectations, and mappings to relevant security frameworks.

## Target integrations

Targets are isolated behind an adapter contract.

### Included

- **Synthetic vulnerable target** — deterministic negative-control baseline
- **Synthetic hardened target** — deterministic positive-control baseline
- **OpenAI-compatible API** — configurable chat-completions endpoint
- **Generic HTTP/JSON application** — configurable internal application endpoint

The real-world adapters are intentionally provider-agnostic. Credentials are supplied through environment variables rather than committed configuration.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate

pip install -r requirements-dev.txt
pip install -e .
```

Run the test suite:

```bash
pytest
```

Run the deterministic vulnerable baseline:

```bash
python -m ai_redteam.cli assess --target synthetic
```

Run the hardened control:

```bash
python -m ai_redteam.cli assess --target hardened
```

Generate a SARIF report and enforce the regression gate:

```bash
python -m ai_redteam.cli assess \
  --target hardened \
  --sarif reports/security.sarif \
  --fail-on fail
```

A vulnerable target should produce a non-zero gate result; the hardened control should pass.

## Real-world API example

For an OpenAI-compatible endpoint:

```bash
export AI_REDTEAM_BASE_URL="https://your-gateway.example/v1"
export AI_REDTEAM_MODEL="your-model"
export AI_REDTEAM_API_KEY="your-secret"

python -m ai_redteam.cli assess --target openai-compatible
```

For a generic JSON endpoint:

```bash
export AI_REDTEAM_TARGET_URL="https://your-app.example/api/chat"

python -m ai_redteam.cli assess --target http-json
```

**Do not commit credentials, production secrets, private prompts, customer data, or sensitive assessment output.**

## CI/CD

GitHub Actions provides two workflows:

- `CI` — Python 3.11–3.13, linting, type checking, and tests
- `AI Security Regression` — security regression gate plus SARIF upload

This makes AI security testing part of the software delivery lifecycle instead of a one-off assessment.

## Reporting

The framework can produce:

- human-readable Markdown
- machine-readable JSON
- SARIF for security tooling

Findings include evidence, confidence, risk scoring, remediation guidance, and security-framework mappings.

## Engineering principles

- **Repeatability:** deterministic cases and controls
- **Separation of concerns:** targets, evaluation, evidence, and reporting are independent
- **Least privilege:** authorization belongs at security boundaries, not in model intent
- **Evidence over claims:** findings should be supported by observable behaviour
- **Regression over snapshots:** security controls should remain effective after change
- **Provider neutrality:** integrations should not lock the assessment engine to one model vendor

## Repository layout

```text
.
├── .github/workflows/       # CI and security regression automation
├── config/                  # Safe configuration examples
├── src/ai_redteam/
│   ├── core/                # Assessment models and orchestration
│   ├── evaluation/          # Evaluator implementations and registry
│   ├── reporting/           # JSON, Markdown and SARIF output
│   ├── targets/             # Target adapter implementations
│   └── tests/               # Test-case discovery/loading
├── test_cases/              # Structured security cases
├── tests/                   # Framework regression tests
├── CONTRIBUTING.md
├── SECURITY.md
└── CHANGELOG.md
```

## Responsible use

Only assess systems you own or have explicit authorization to test.

The included vulnerable target is intentionally insecure and exists solely as a deterministic regression fixture. Do not use the framework to probe third-party systems without permission.

## Status

**v0.6.0 — engineering prototype / active development**

The architecture is intentionally extensible. Future work can add richer agent/tool simulations, provider-specific adapters, more sophisticated evaluators, baseline storage, and longitudinal security metrics.

## License

MIT
