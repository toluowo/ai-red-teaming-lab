"""Model adapter interfaces used by the evaluation pipeline."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class ModelResponse:
    text: str
    metadata: dict | None = None

class CallableAdapter:
    def __init__(self, fn: Callable[[str], str]):
        self.fn = fn

    def generate(self, prompt: str) -> ModelResponse:
        return ModelResponse(text=self.fn(prompt), metadata={"adapter": "callable"})
