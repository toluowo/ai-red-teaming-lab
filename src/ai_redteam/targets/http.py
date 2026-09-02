from __future__ import annotations

import json
import os
from urllib import request as urlrequest
from urllib.error import HTTPError, URLError

from ..core.models import AssessmentRequest, TargetResponse
from .base import TargetAdapter


class HTTPJSONTarget(TargetAdapter):
    """Adapter for an HTTP JSON application endpoint.

    Request/response field names are configurable for integration with
    internal test applications without coupling the framework to one schema.
    """

    name = "http-json"

    def __init__(
        self,
        url: str | None = None,
        input_field: str = "prompt",
        output_field: str = "response",
        headers: dict[str, str] | None = None,
        timeout: int = 60,
    ):
        self.url = (
            url
            or os.getenv("AI_REDTEAM_TARGET_URL")
            or "http://localhost:8080/ai"
        )

        self.input_field = input_field
        self.output_field = output_field
        self.headers = headers or {}
        self.timeout = timeout

    def invoke(
        self,
        request: AssessmentRequest,
    ) -> TargetResponse:
        payload = {
            self.input_field: request.input_text,
        }

        req = urlrequest.Request(
            self.url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                **self.headers,
            },
            method="POST",
        )

        try:
            with urlrequest.urlopen(
                req,
                timeout=self.timeout,
            ) as response:
                status = response.status
                raw_body = response.read().decode("utf-8")

            data = json.loads(raw_body)

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

        except json.JSONDecodeError as exc:
            return TargetResponse(
                output="",
                metadata={
                    "adapter": self.name,
                    "error": "InvalidJSON",
                    "http_status": status,
                    "error_detail": str(exc),
                },
            )

        value = data.get(self.output_field, "")

        return TargetResponse(
            output=(
                value
                if isinstance(value, str)
                else json.dumps(value)
            ),
            metadata={
                "adapter": self.name,
                "http_status": status,
            },
        )
