# Threat Model

## Objective

Evaluate whether an AI application preserves security boundaries when exposed to adversarial or untrusted inputs.

## Assets

- system/developer instructions
- confidential context
- user and tenant boundaries
- tool credentials and capabilities
- persistent memory
- retrieved documents
- downstream execution sinks
- application data

## Trust boundaries

```text
Untrusted user input
        │
        ▼
┌─────────────────┐
│ Model / Agent   │
└───────┬─────────┘
        │
  ┌─────┼─────────────┐
  ▼     ▼             ▼
RAG   Memory        Tools
  │     │             │
  └─────┴─────────────┘
        │
        ▼
Application / Data
```

The model is not treated as an authorization boundary.

## Primary threats

| Threat | Security property |
|---|---|
| Direct/indirect prompt injection | Instruction integrity |
| Context leakage | Confidentiality/isolation |
| Jailbreak | Policy enforcement |
| RAG poisoning | Retrieval trust/provenance |
| Memory manipulation | Persistence integrity |
| Tool abuse | Authorization |
| Parameter tampering | Input integrity |
| Excessive agency | Least privilege / human control |
| Unsafe output handling | Downstream execution safety |

## Mitigation philosophy

Security decisions should be enforced outside model-generated intent wherever practical.

Examples:

- authorize tools server-side
- validate tool parameters
- isolate tenant context
- constrain memory writes
- treat retrieved content as untrusted data
- validate/encode model output before downstream use
- require explicit confirmation for high-impact actions

## Testing philosophy

A finding should be treated as evidence of a violated security property, not merely a "bad prompt".

The assessment lifecycle is:

**attack → observation → evaluation → evidence → risk → remediation → retest**
