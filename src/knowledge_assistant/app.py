"""REST-oriented application adapter for Lambda proxy events."""

from __future__ import annotations

from typing import Any

from knowledge_assistant.contracts import (
    CONTRACT_VERSION,
    AssistantReply,
    dumps_wire_json,
)
from knowledge_assistant.providers import AssistantProvider, ProviderError
from knowledge_assistant.validation import RequestValidationError, load_request


ENDPOINT_PATH = "/v1/assistant"
_FALLBACK_CORRELATION_ID = "unavailable"


def handle_event(
    event: dict[str, Any],
    provider: AssistantProvider,
) -> dict[str, Any]:
    method, path = _method_and_path(event)
    if path != ENDPOINT_PATH:
        return _error_response(
            status_code=404,
            code="NOT_FOUND",
            message="Endpoint is not supported.",
        )
    if method != "POST":
        return _error_response(
            status_code=405,
            code="METHOD_NOT_ALLOWED",
            message="Only POST is supported.",
        )

    try:
        request = load_request(event.get("body"))
    except RequestValidationError as exc:
        return _error_response(
            status_code=400,
            code="VALIDATION_ERROR",
            message="Request payload is invalid.",
            details=[issue.to_wire() for issue in exc.issues],
        )

    try:
        content = provider.generate(request)
    except ProviderError:
        return _error_response(
            status_code=502,
            code="PROVIDER_FAILURE",
            message="The AI provider could not complete the request.",
            correlation_id=request.correlation_id,
        )

    return _http_response(
        200,
        AssistantReply(
            correlation_id=request.correlation_id,
            content=content,
        ).to_wire(),
    )


def _method_and_path(event: dict[str, Any]) -> tuple[Any, Any]:
    method = event.get("httpMethod")
    path = event.get("path")
    if method is None:
        http_context = event.get("requestContext", {}).get("http", {})
        method = http_context.get("method")
        path = event.get("rawPath")
    return method, path


def _error_response(
    *,
    status_code: int,
    code: str,
    message: str,
    correlation_id: str = _FALLBACK_CORRELATION_ID,
    details: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    return _http_response(
        status_code,
        {
            "contractVersion": CONTRACT_VERSION,
            "correlationId": correlation_id,
            "error": {
                "code": code,
                "message": message,
                "details": details or [],
            },
        },
    )


def _http_response(status_code: int, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": dumps_wire_json(payload),
    }

