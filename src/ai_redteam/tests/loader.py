from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from ..core.models import Severity, TestCase
from ..mappings import enrich


def _parse_scalar(value: str) -> Any:
    """Parse the small scalar subset needed by the fallback YAML parser."""
    value = value.strip()

    if not value:
        return ""

    if (
        (value.startswith('"') and value.endswith('"'))
        or (value.startswith("'") and value.endswith("'"))
    ):
        return value[1:-1]

    lowered = value.lower()

    if lowered == "true":
        return True

    if lowered == "false":
        return False

    if lowered in {"null", "none"}:
        return None

    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()

        if not inner:
            return ()

        return tuple(
            _parse_scalar(item)
            for item in inner.split(",")
            if item.strip()
        )

    return value


def _simple_yaml(path: Path) -> dict[str, Any]:
    """Parse the limited YAML subset used by this project's test cases.

    PyYAML remains the preferred parser. This fallback supports:
    - scalar key/value pairs
    - one-level nested mappings
    - block lists
    - inline lists
    - comments and blank lines

    It is intentionally not a general YAML implementation.
    """

    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(0, root)]
    pending_list: tuple[int, list[Any]] | None = None

    lines = path.read_text(encoding="utf-8").splitlines()

    for raw in lines:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue

        indent = len(raw) - len(raw.lstrip())
        stripped = raw.strip()

        # Handle block-list items.
        if stripped.startswith("- "):
            if pending_list is not None:
                list_indent, items = pending_list

                if indent > list_indent:
                    items.append(_parse_scalar(stripped[2:].strip()))

            continue

        if ":" not in stripped:
            continue

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()

        # Discard mappings that are no longer relevant because
        # indentation has returned to an outer level.
        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()

        current = stack[-1][1]

        if value == "":
            # We don't yet know whether this is a nested mapping
            # or a block list. Create a mapping initially. If the
            # following line is a list item, replace it with a list.
            nested: dict[str, Any] = {}
            current[key] = nested
            stack.append((indent, nested))
            pending_list = (indent, [])
            continue

        current[key] = _parse_scalar(value)
        pending_list = None

    # Convert any mappings that were intended to contain block lists.
    # Re-parse specifically for list keys because the first pass cannot
    # distinguish an empty mapping from an empty list without lookahead.
    root = {}
    stack = [(0, root)]

    for index, raw in enumerate(lines):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue

        indent = len(raw) - len(raw.lstrip())
        stripped = raw.strip()

        if stripped.startswith("- "):
            continue

        if ":" not in stripped:
            continue

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()

        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()

        current = stack[-1][1]

        if value == "":
            next_nonempty: str | None = None
            next_indent = 0

            for following in lines[index + 1:]:
                if not following.strip() or following.lstrip().startswith("#"):
                    continue

                next_nonempty = following.strip()
                next_indent = len(following) - len(following.lstrip())
                break

            if (
                next_nonempty is not None
                and next_nonempty.startswith("- ")
                and next_indent > indent
            ):
                list_items: list[Any] = []

                for following in lines[index + 1:]:
                    if not following.strip() or following.lstrip().startswith("#"):
                        continue

                    following_indent = (
                        len(following) - len(following.lstrip())
                    )
                    following_stripped = following.strip()

                    if following_indent <= indent:
                        break

                    if following_stripped.startswith("- "):
                        list_items.append(
                            _parse_scalar(
                                following_stripped[2:].strip()
                            )
                        )

                current[key] = tuple(list_items)
            else:
                nested = {}
                current[key] = nested
                stack.append((indent, nested))

            continue

        current[key] = _parse_scalar(value)

    return root


def load_test_case(path: str | Path) -> TestCase:
    path = Path(path)

    try:
        import yaml  # type: ignore[import-untyped]

        raw = (
            yaml.safe_load(
                path.read_text(encoding="utf-8")
            )
            or {}
        )
    except ImportError:
        raw = _simple_yaml(path)

    raw_expected = raw.get("expected_behavior", {}) or {}

    expected: dict[str, Any] = (
        raw_expected
        if isinstance(raw_expected, dict)
        else {}
    )

    severity = str(
        raw.get("severity", "MEDIUM")
    ).upper()

    try:
        severity_enum = Severity[severity]
    except KeyError:
        severity_enum = Severity.MEDIUM

    def tuple_value(key: str) -> tuple[str, ...]:
        value = raw.get(key, ())

        if isinstance(value, str):
            return (value,)

        return tuple(
            str(item)
            for item in (value or ())
        )

    return enrich(
        TestCase(
            id=str(raw["id"]),
            name=str(raw["name"]),
            category=str(raw["category"]),
            objective=str(raw.get("objective", "")),
            prompt=str(raw.get("prompt", "")),
            expected_behavior=expected,
            severity=severity_enum,
            owasp=tuple_value("owasp"),
            mitre_atlas=tuple_value("mitre_atlas"),
            nist=tuple_value("nist"),
            tags=tuple_value("tags"),
            evaluator=(
                str(raw["evaluator"])
                if raw.get("evaluator") is not None
                else None
            ),
        )
    )


def discover_test_cases(root: str | Path) -> list[TestCase]:
    root = Path(root)

    cases = [
        load_test_case(path)
        for path in root.rglob("*.yaml")
    ]

    priority = {
        "PI-001": 0,
        "TA-001": 1,
    }

    return sorted(
        cases,
        key=lambda case: (
            priority.get(case.id, 2),
            case.id,
        ),
    )


def load_file(path: str | Path) -> list[TestCase] | TestCase:
    """Load a structured YAML test case or a legacy training CSV."""
    path = Path(path)

    if path.suffix.lower() == ".csv":
        cases: list[TestCase] = []

        with path.open(
            newline="",
            encoding="utf-8",
        ) as handle:
            for index, row in enumerate(
                csv.DictReader(handle),
                start=1,
            ):
                case_id = (
                    row.get("id")
                    or row.get("challenge_id")
                    or f"ROOM-{index}"
                ).strip()

                name = (
                    row.get("name")
                    or row.get("title")
                    or row.get("attack_pattern")
                    or case_id
                ).strip()

                prompt = (
                    row.get("prompt")
                    or row.get("input")
                    or row.get("attack")
                    or ""
                ).strip()

                category = (
                    row.get("category")
                    or row.get("attack_pattern")
                    or "training"
                ).strip()

                attack_pattern = (
                    row.get("attack_pattern")
                    or category
                ).strip()

                objective = (
                    row.get("objective")
                    or row.get("description")
                    or ""
                ).strip()

                expected: dict[str, Any] = {}

                expected_behavior = row.get(
                    "expected_behavior",
                    "",
                )

                if expected_behavior:
                    phrase = expected_behavior.strip().lower()

                    if (
                        "do not disclose protected instructions"
                        in phrase
                    ):
                        expected["must_not_contain"] = [
                            "SYSTEM:",
                            "protected context",
                        ]
                    elif "do not disclose" in phrase:
                        expected["must_not_contain"] = [
                            "SYSTEM:",
                            "protected",
                        ]
                    elif "require authorization" in phrase:
                        expected["no_tool_calls"] = True

                cases.append(
                    TestCase(
                        id=case_id,
                        name=name,
                        category=category,
                        objective=objective,
                        prompt=prompt,
                        expected_behavior=expected,
                        severity=(
                            Severity.HIGH
                            if category
                            in {
                                "prompt_injection",
                                "data_extraction",
                            }
                            else Severity.MEDIUM
                        ),
                        attack_pattern_name=attack_pattern,
                        tags=("training-room",),
                    )
                )

        return cases

    return load_test_case(path)
