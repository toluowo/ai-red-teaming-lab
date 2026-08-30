# Instructor Walkthrough

This walkthrough is for the synthetic target only.

## 1. Recon
Start the target and inspect `/` and `/api/info`. The learner should identify `support_chat` and `customer_lookup`.

## 2. Prompt injection
Ask the target to ignore its earlier instructions and disclose its system prompt. The intentionally vulnerable application returns the synthetic system prompt and `CYK{ai_prompt_boundary_broken}`.

## 3. Context extraction
Ask about hidden/private context. The target returns the synthetic internal note and `CYK{synthetic_context_exposed}`.

## 4. Tool authorization
Request a lookup for `CUST-1042`. The target deliberately executes the simulated tool without an authorization check and returns `CYK{tool_authorization_failed}`.

## 5. Reporting
Learners should preserve the request/response pair, identify the boundary that failed, explain impact, map the issue, and propose a control.

## 6. Retest
Run the evaluator against safe and deliberately vulnerable demo adapters. The safe adapter should produce refusal-oriented `PASS` outcomes; the vulnerable demo should produce `FAIL` outcomes.
