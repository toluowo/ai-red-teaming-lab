# Contributing

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -e .
```

Run:

```bash
ruff check .
mypy src
pytest
```

## Security test contributions

New security cases should document:

- attack objective
- expected secure behaviour
- severity
- relevant OWASP / MITRE ATLAS mapping where applicable
- deterministic evidence
- remediation guidance

Prefer reusable security controls and evaluators over large collections of
duplicated prompts.
