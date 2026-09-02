from __future__ import annotations

import json
import os
from typing import Any
from urllib import request as urlrequest
from urllib.error import HTTPError, URLError

from ..core.models import AssessmentRequest, TargetResponse, ToolCall
from .base import TargetAdapter


class OpenAICompatibleTarget(TargetAdapter):
    """Adapter for OpenAI-compatible chat/completions endpoints.

    The endpoint is configurable so the adapter can target hosted APIs,
    private gateways, or self-hosted inference servers.
    """

    name = "openai-compatible"

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        api_key: str | None = None,
        timeout: int = 60,
    ):
        self.base_url = (
            base_url
            or os.getenv("AI_REDTEAM_BASE_URL")
            or "http://localhost:8000/v1"
        ).rstrip("/")

        self.model = model or os.getenv(
            "AI_REDTEAM_MODEL",
            "local-model",
        )

        self.api_key = (
            api_key
            if api_key is not None
            else os.getenv("AI_REDTEAM_API_KEY")
        )

        self.timeout = timeout

    @staticmethod
    def _parse_tool_arguments(arguments: Any) -> dict[str, Any]:
        if isinstance(arguments, dict):
            return arguments

        if isinstance(arguments, str):
            try:
                parsed = json.loads(arguments)

                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                pass

        return {}

    def invoke(
        self,
        request: AssessmentRequest,
    ) -> TargetResponse:
        url = f"{self.base_url}/chat/completions"

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": request.input_text,
                }
            ],
            "temperature": 0,
        }

        body = json.dumps(payload).encode("utf-8")

        headers = {
            "Content-Type": "application/json",
        }

        if self.api_key:
            headers["Authorization"] = (
                f"Bearer {self.api_key}"
            )

        req = urlrequest.Request(
            url,
            data=body,
            headers=headers,
            method="POST",
        )

        try:
            with urlrequest.urlopen(
                req,
                timeout=self.timeout,
            ) as response:
                data = json.loads(
                    response.read().decode("utf-8")
                )

        except HTTPError as exc:
            return TargetResponse(
                output="",
                metadata={
                    "adapter": self.name,
                    "error": "HTTPError",
                    "http_status": exc.code,
                    "error_detail": str(exc),
                },
            )

        except (URLError, TimeoutError) as exc:
            return TargetResponse(
                output="",
                metadata={
                    "adapter": self.name,
                    "error": type(exc).__name__,
                    "error_detail": str(exc),
                },
            )

        choices = data.get("choices") or []

        message = (
            choices[0].get("message") or {}
            if choices
            else {}
        )

        content = message.get("content") or ""

        tool_calls: list[ToolCall] = []

        for tool_call in message.get("tool_calls") or []:
            function = tool_call.get("function") or {}

            tool_calls.append(
                ToolCall(
                    name=function.get(
                        "name",
                        "unknown",
                    ),
                    arguments=self._parse_tool_arguments(
                        function.get("arguments", {})
                    ),
                    authorized=None,
                )
            )

        return TargetResponse(
            output=(
                content
                if isinstance(content, str)
                else json.dumps(content)
            ),
            tool_calls=tuple(tool_calls),
            metadata={
                "adapter": self.name,
                "model": data.get(
                    "model",
                    self.model,
                ),
                "usage": data.get(
                    "usage",
                    {},
                ),
            },
        )
