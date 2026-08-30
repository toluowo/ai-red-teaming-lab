# Challenge 6 — Remediation and Retest

The final step is to show that a proposed control actually changes the result.

Use the evaluator with a safe adapter and verify that protected-instruction tests return `PASS` rather than merely producing a low numeric score.

```bash
python3 -m unittest discover -s tests -v
python3 -m testing.run_evaluation --vulnerable-demo
python3 -m testing.run_evaluation
```

**Success condition:** Explain why the safe adapter passes refusal-oriented tests while the deliberately vulnerable adapter produces a failure signal.

**Learning outcome:** Security testing is incomplete until the control is retested and the result is evidenced.
