# Challenge 4 — Tool Authorization Failure

**Objective:** Identify an authorization flaw in a simulated customer-lookup tool.

The application exposes a customer lookup capability, but the tool boundary is deliberately weak. All customer records are synthetic.

**Hint 1:** Look at `/api/info` for the application's capabilities.

**Hint 2:** Try requesting a lookup for `CUST-1042` and observe whether the assistant checks authorization first.

**Success condition:** Demonstrate that a user-controlled prompt can trigger the lookup tool without an authorization decision.

**Flag:** `CYK{tool_authorization_failed}`

**Learning outcome:** Understand why tool access must be governed separately from natural-language intent.
