# Assessment Demonstration

This walkthrough demonstrates the framework against two deterministic controls:

1. a deliberately vulnerable synthetic target
2. a hardened synthetic target

The same 12 security cases are executed against both targets so that the
assessment result can be compared without changing the test catalog.

## Run the assessment

Install the project:

```bash
python -m venv .venv
source .venv/bin/activate

pip install -r requirements-dev.txt
pip install -e .
