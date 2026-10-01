"""Provider boundary used by the application layer."""

from typing import Protocol

from knowledge_assistant.contracts import AssistantRequest


class ProviderError(RuntimeError):
    """Safe application-facing provider failure."""


class AssistantProvider(Protocol):
    def generate(self, request: AssistantRequest) -> str:
        """Return assistant text or raise ProviderError."""
        ...

