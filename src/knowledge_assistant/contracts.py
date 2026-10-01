"""Versioned request and response models for the public example."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Mapping


CONTRACT_VERSION = "knowledge-assistant-v1"


@dataclass(frozen=True, slots=True)
class Message:
    role: str
    content: str

    def to_wire(self) -> dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass(frozen=True, slots=True)
class AssistantRequest:
    correlation_id: str
    messages: tuple[Message, ...]


@dataclass(frozen=True, slots=True)
class AssistantReply:
    correlation_id: str
    content: str

    def to_wire(self) -> dict[str, Any]:
        return {
            "contractVersion": CONTRACT_VERSION,
            "correlationId": self.correlation_id,
            "message": {
                "role": "assistant",
                "content": self.content,
            },
        }


def dumps_wire_json(payload: Mapping[str, Any]) -> str:
    """Serialize a wire payload in a stable form suitable for tests."""

    return json.dumps(
        payload,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )

