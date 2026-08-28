# Challenge 1 — Recon the AI Application

**Objective:** Identify the application endpoints and determine what capabilities the target exposes.

Start the target locally:

```bash
python -m ai_redteam.cli assess --target synthetic
```

Then inspect the root and API information endpoints.

**Hint 1:** Start with `/` and `/api/info`.

**Hint 2:** Look for functionality that may create a security boundary.

**Flag:** None. Record the capabilities you discover and move to Challenge 2.

**Learning outcome:** Learners should map an AI application's attack surface before attempting adversarial testing.
