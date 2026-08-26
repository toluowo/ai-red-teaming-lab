# Example LLM Security Finding

> **Illustrative example:** the content below demonstrates the reporting format. It is not evidence from a live model evaluation.

**Vulnerability ID:** LLM-2026-EXAMPLE  
**Category:** Prompt Injection  
**Severity:** High  

## Scenario

An authorized evaluator submits an instruction-override test designed to determine whether untrusted input can supersede higher-priority instructions.

## Expected behaviour

The model should reject the override and continue following its governing instructions.

## Observed behaviour

Record the exact model output here. Do not paraphrase the evidence.

## Impact

If the control fails, an attacker may be able to influence model behaviour beyond the intended trust boundary. The practical impact depends on what data, tools, and downstream actions are available to the application.

## Evidence

- Test ID and dataset version
- Model/provider and version
- Timestamp
- Exact prompt
- Exact response
- Relevant system/application configuration

## Mitigation

Consider stronger instruction hierarchy, trust-boundary separation, output validation, least-privilege tool access, monitoring, and adversarial regression testing as appropriate to the application.

## Retest criteria

Repeat the same test and confirm that the unsafe behaviour is no longer reproducible while legitimate application behaviour remains functional.
