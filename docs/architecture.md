# Lab Architecture

```text
Learner / Tester
      |
      v
+-----------------------+
| Synthetic AI Target   |
| app/vulnerable_ai.py  |
+-----------+-----------+
            |
    synthetic context/tools
            |
            v
+-----------------------+
| Evidence / Responses  |
+-----------+-----------+
            |
            v
+-----------------------+
| testing/evaluation.py |
| behaviour-aware triage|
+-----------+-----------+
            |
            v
+-----------------------+
| Risk + PASS/FAIL/     |
| REVIEW + evidence     |
+-----------------------+
```

The target is deliberately vulnerable and completely offline. It contains no real credentials, customer data, model API calls, or external integrations.
