"""AWS Lambda-compatible entry point for the representative application."""

from __future__ import annotations

import os
from typing import Any

from knowledge_assistant.app import handle_event
from knowledge_assistant.bedrock import BedrockConfig, create_bedrock_provider
from knowledge_assistant.providers import AssistantProvider


_DEFAULT_MODEL_ID = "amazon.nova-lite-v1:0"
_DEFAULT_REGION = "us-east-1"
_cached_provider: AssistantProvider | None = None


def lambda_handler(
    event: dict[str, Any],
    context: Any,
    provider: AssistantProvider | None = None,
) -> dict[str, Any]:
    """Handle a Lambda proxy event; tests may inject a provider."""

    del context
    return handle_event(event, provider or _default_provider())


def _default_provider() -> AssistantProvider:
    global _cached_provider
    if _cached_provider is None:
        _cached_provider = create_bedrock_provider(
            BedrockConfig(
                model_id=os.getenv("BEDROCK_MODEL_ID", _DEFAULT_MODEL_ID),
                region_name=os.getenv("AWS_REGION", _DEFAULT_REGION),
            )
        )
    return _cached_provider

