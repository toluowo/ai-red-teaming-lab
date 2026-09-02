from __future__ import annotations

from .hardened import HardenedTarget
from .http import HTTPJSONTarget
from .openai_compatible import OpenAICompatibleTarget
from .synthetic import SyntheticTarget


def build_target(name: str, **kwargs):
    targets = {
        "synthetic": SyntheticTarget,
        "hardened": HardenedTarget,
        "openai-compatible": OpenAICompatibleTarget,
        "http-json": HTTPJSONTarget,
    }
    try:
        return targets[name](**kwargs)
    except KeyError as exc:
        raise ValueError(f"Unsupported target: {name}") from exc
