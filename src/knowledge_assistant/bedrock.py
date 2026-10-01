"""Amazon Bedrock Runtime provider using the Converse API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from knowledge_assistant.contracts import AssistantRequest
from knowledge_assistant.providers import ProviderError


@dataclass(frozen=True, slots=True)
class BedrockConfig:
    model_id: str = "amazon.nova-lite-v1:0"
    region_name: str = "us-east-1"


class BedrockConverseProvider:
    def __init__(self, client: Any, config: BedrockConfig):
        self._client = client
        self._config = config

    def generate(self, request: AssistantRequest) -> str:
        try:
            response = self._client.converse(
                modelId=self._config.model_id,
                messages=[
                    {
                        "role": message.role,
                        "content": [{"text": message.content}],
                    }
                    for message in request.messages
                ],
            )
            text = response["output"]["message"]["content"][0]["text"]
        except Exception as exc:
            raise ProviderError("The AI provider request failed.") from exc

        if not isinstance(text, str) or not text.strip():
            raise ProviderError("The AI provider returned an invalid response.")
        return text.strip()


def create_bedrock_provider(
    config: BedrockConfig | None = None,
    client: Any | None = None,
) -> BedrockConverseProvider:
    resolved_config = config or BedrockConfig()
    if client is None:
        import boto3

        client = boto3.client(
            "bedrock-runtime",
            region_name=resolved_config.region_name,
        )
    return BedrockConverseProvider(client=client, config=resolved_config)

