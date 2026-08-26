# Emerging LLM Security Risks

This note is a research checklist for expanding the lab. It is intentionally concise and should be updated as the AI-security landscape and application architectures evolve.

## Areas to investigate

- Indirect prompt injection through retrieved content
- Tool and function-call authorization failures
- Sensitive data leakage across context boundaries
- Multi-turn instruction manipulation
- Cross-application or agent-to-agent trust failures
- Unsafe downstream handling of model output
- Evaluation blind spots caused by brittle automated classifiers

## Research questions

1. What is the application's actual trust boundary?
2. Which model outputs can trigger external actions?
3. What data can enter model context, and under whose authority?
4. Which controls are enforced outside the model itself?
5. How are failed tests converted into regression tests?

## Evidence standard

Do not treat a single generated response as proof of a systemic vulnerability. Record the test conditions, reproduce the behaviour where possible, assess impact in application context, and retest after mitigation.
