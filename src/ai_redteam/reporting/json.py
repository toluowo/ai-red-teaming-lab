from __future__ import annotations

import json
from dataclasses import asdict
from enum import Enum
from pathlib import Path
from typing import Any

from ..core.models import AssessmentReport


class _Encoder(json.JSONEncoder):
    def default(self, obj: Any):
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)


def report_to_dict(report: AssessmentReport) -> dict[str, Any]:
    return json.loads(json.dumps(asdict(report), cls=_Encoder))


def write_json(report: AssessmentReport, path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(report_to_dict(report), indent=2, cls=_Encoder) + "\n",
        encoding="utf-8",
    )
