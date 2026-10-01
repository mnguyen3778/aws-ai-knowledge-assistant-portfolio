"""Defensive parsing and validation for the versioned request contract."""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Any

from knowledge_assistant.contracts import (
    CONTRACT_VERSION,
    AssistantRequest,
    Message,
)


_ALLOWED_FIELDS = frozenset({"contractVersion", "correlationId", "messages"})
_REQUIRED_FIELDS = ("contractVersion", "correlationId", "messages")
_MESSAGE_FIELDS = frozenset({"role", "content"})
_IDENTIFIER = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
_MAX_MESSAGES = 10
_MAX_MESSAGE_CHARACTERS = 2_000
_MAX_TOTAL_CHARACTERS = 8_000


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    field: str
    code: str
    message: str

    def to_wire(self) -> dict[str, str]:
        return {
            "field": self.field,
            "code": self.code,
            "message": self.message,
        }


class RequestValidationError(ValueError):
    def __init__(self, issues: list[ValidationIssue]):
        super().__init__("Request validation failed.")
        self.issues = tuple(issues)


class _DuplicateFieldError(ValueError):
    pass


def load_request(raw_body: Any) -> AssistantRequest:
    payload = _parse_body(raw_body)
    issues: list[ValidationIssue] = []

    if not isinstance(payload, dict):
        raise RequestValidationError(
            [_issue("body", "INVALID_TYPE", "Body must be a JSON object.")]
        )

    for field in _REQUIRED_FIELDS:
        if field not in payload:
            issues.append(_issue(field, "REQUIRED", "Field is required."))

    for field in sorted(payload.keys() - _ALLOWED_FIELDS):
        issues.append(
            _issue(field, "UNKNOWN_FIELD", "Unknown field is not allowed.")
        )

    if payload.get("contractVersion") != CONTRACT_VERSION:
        if "contractVersion" in payload:
            issues.append(
                _issue(
                    "contractVersion",
                    "UNSUPPORTED_VERSION",
                    "Contract version is not supported.",
                )
            )

    correlation_id = payload.get("correlationId")
    if "correlationId" in payload and (
        not isinstance(correlation_id, str)
        or _IDENTIFIER.fullmatch(correlation_id) is None
    ):
        issues.append(
            _issue(
                "correlationId",
                "INVALID_IDENTIFIER",
                "Correlation ID must use the supported identifier format.",
            )
        )

    messages: list[Message] = []
    if "messages" in payload:
        messages, message_issues = _load_messages(payload["messages"])
        issues.extend(message_issues)

    if issues:
        raise RequestValidationError(issues)

    return AssistantRequest(
        correlation_id=correlation_id,
        messages=tuple(messages),
    )


def _parse_body(raw_body: Any) -> Any:
    if not isinstance(raw_body, str):
        raise RequestValidationError(
            [_issue("body", "INVALID_TYPE", "Body must be a JSON string.")]
        )

    try:
        return json.loads(raw_body, object_pairs_hook=_reject_duplicate_fields)
    except _DuplicateFieldError as exc:
        raise RequestValidationError(
            [_issue("body", "DUPLICATE_FIELD", str(exc))]
        ) from None
    except json.JSONDecodeError:
        raise RequestValidationError(
            [_issue("body", "INVALID_JSON", "Body must contain valid JSON.")]
        ) from None


def _load_messages(value: Any) -> tuple[list[Message], list[ValidationIssue]]:
    if not isinstance(value, list):
        return [], [_issue("messages", "INVALID_TYPE", "Messages must be a list.")]
    if not value:
        return [], [_issue("messages", "REQUIRED", "At least one message is required.")]
    if len(value) > _MAX_MESSAGES:
        return [], [
            _issue("messages", "LIMIT_EXCEEDED", "Too many messages were supplied.")
        ]

    messages: list[Message] = []
    issues: list[ValidationIssue] = []
    total_characters = 0

    for index, item in enumerate(value):
        field = f"messages[{index}]"
        if not isinstance(item, dict):
            issues.append(_issue(field, "INVALID_TYPE", "Message must be an object."))
            continue

        for name in sorted(item.keys() - _MESSAGE_FIELDS):
            issues.append(
                _issue(
                    f"{field}.{name}",
                    "UNKNOWN_FIELD",
                    "Unknown field is not allowed.",
                )
            )

        role = item.get("role")
        content = item.get("content")
        if role != "user":
            issues.append(
                _issue(f"{field}.role", "INVALID_ROLE", "Role must be 'user'.")
            )
        if not isinstance(content, str) or not content.strip():
            issues.append(
                _issue(
                    f"{field}.content",
                    "INVALID_CONTENT",
                    "Content must be a non-empty string.",
                )
            )
            continue
        if len(content) > _MAX_MESSAGE_CHARACTERS:
            issues.append(
                _issue(
                    f"{field}.content",
                    "LIMIT_EXCEEDED",
                    "Message content is too long.",
                )
            )
            continue

        normalized_content = content.strip()
        total_characters += len(normalized_content)
        messages.append(Message(role="user", content=normalized_content))

    if total_characters > _MAX_TOTAL_CHARACTERS:
        issues.append(
            _issue(
                "messages",
                "LIMIT_EXCEEDED",
                "Combined message content is too long.",
            )
        )

    return messages, issues


def _reject_duplicate_fields(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for key, value in pairs:
        if key in payload:
            raise _DuplicateFieldError("Duplicate JSON fields are not allowed.")
        payload[key] = value
    return payload


def _issue(field: str, code: str, message: str) -> ValidationIssue:
    return ValidationIssue(field=field, code=code, message=message)

