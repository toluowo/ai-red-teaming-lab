# Architecture

## Design goals

The framework separates four concerns:

1. **Target integration** — how the system under test is invoked.
2. **Assessment orchestration** — how test cases are executed.
3. **Evaluation** — how observed behaviour is classified.
4. **Reporting** — how evidence and findings are consumed.

## Extension points

### Target adapters

Implement `TargetAdapter` when integrating a new application or inference endpoint.

### Evaluators

Register a specialized evaluator when a security surface needs behaviour beyond generic pass/fail heuristics.

### Reporters

Add a reporter when findings need to be consumed by another system.

This structure prevents provider-specific integration logic from leaking into the security assessment core.
