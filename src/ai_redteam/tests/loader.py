from __future__ import annotations

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

def select_test_cases(
    selector: str,
    root: str | Path = "test_cases",
) -> list[TestCase]:
    """Discover all tests or select specific test cases by ID.

    The selector may be:
    - a directory containing YAML test cases
    - a single test case ID
    - a comma-separated list of test case IDs
    """
    selector = selector.strip()

    if not selector:
        raise ValueError("Test selector cannot be empty.")

    selector_path = Path(selector)

    # Preserve directory-based discovery.
    if selector_path.is_dir():
        cases = discover_test_cases(selector_path)
        if not cases:
            raise ValueError(
                f"No test cases found in directory: {selector}"
            )
        return cases

    # Otherwise interpret the selector as one or more test IDs.
    requested_ids = [
        item.strip()
        for item in selector.split(",")
        if item.strip()
    ]

    if not requested_ids:
        raise ValueError("No test case IDs were provided.")

    available = discover_test_cases(root)
    by_id = {case.id: case for case in available}

    missing = [
        case_id
        for case_id in requested_ids
        if case_id not in by_id
    ]

    if missing:
        raise ValueError(
            "Unknown test case ID(s): "
            + ", ".join(missing)
        )

    return [by_id[case_id] for case_id in requested_ids]
