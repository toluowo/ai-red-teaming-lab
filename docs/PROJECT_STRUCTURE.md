# Project Structure

```text
.
├── .github/workflows/       # CI and security regression automation
├── config/                  # Safe configuration examples
├── docs/                    # Architecture, threat model, research and training
├── examples/                # Reproducible demonstrations
├── src/ai_redteam/          # Canonical framework implementation
├── test_cases/              # Structured security cases
├── tests/                   # Automated framework regression tests
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
├── pyproject.toml
└── README.md
```

The `src/ai_redteam/` package is the canonical implementation. Training and
historical material is deliberately separated from runtime code so that the
repository can be used as both an engineering project and a learning resource.
