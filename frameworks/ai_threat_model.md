# AI Threat Model

## Attack surfaces

- User input and prompt interfaces
- System and developer instructions
- Retrieval-augmented generation pipelines
- External tools and function calls
- Plugin/integration boundaries
- Conversation memory and context
- Model outputs consumed by downstream systems

## Adversarial goals

- Override higher-priority instructions
- Extract protected instructions or sensitive context
- Induce unsafe or unauthorized model behaviour
- Manipulate tool-use decisions
- Exploit context confusion or instruction ambiguity
- Cause unsafe downstream actions

## Defensive controls to evaluate

- Clear instruction hierarchy
- Input validation and trust-boundary separation
- Output validation and policy checks
- Tool authorization and least privilege
- Retrieval/data-access controls
- Logging and monitoring
- Adversarial testing and regression testing
- Human review for high-impact actions

## Test design principle

For each attack surface, document:

1. the trusted and untrusted components;
2. the adversarial objective;
3. the expected safe behaviour;
4. the evidence to capture;
5. the impact if the control fails; and
6. the mitigation and retest criteria.
