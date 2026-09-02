"""CSV-driven evaluation engine."""
from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path

from testing.adapters import CallableAdapter
from testing.redteam_scoring import assess_response


def load_dataset(file: str) -> list[dict]:
    with open(file, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    required = {"id", "prompt", "expected_behavior"}
    missing = required - set(rows[0].keys()) if rows else required
    if missing:
        raise ValueError(f"dataset missing required columns: {sorted(missing)}")
    return rows

def evaluate(model, dataset: list[dict]) -> list[dict]:
    adapter = model if hasattr(model, "generate") else CallableAdapter(model)
    results = []
    for case in dataset:
        model_response = adapter.generate(case["prompt"])
        assessment = assess_response(model_response.text, case.get("expected_behavior", ""))
        results.append({
            "id": case.get("id"),
            "category": case.get("category"),
            "attack_pattern": case.get("attack_pattern"),
            "prompt": case.get("prompt"),
            "expected_behavior": case.get("expected_behavior"),
            "response": model_response.text,
            "metadata": model_response.metadata or {},
            **assessment,
        })
    return results

def save_results(results: list[dict], directory: str = "reports") -> Path:
    output_dir = Path(directory)
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output = output_dir / f"test_results_{timestamp}.json"
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return output
