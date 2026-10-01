import unittest

from knowledge_assistant.bedrock import BedrockConfig, BedrockConverseProvider
from knowledge_assistant.contracts import AssistantRequest, Message
from knowledge_assistant.providers import ProviderError


class FakeBedrockClient:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error
        self.calls = []

    def converse(self, **request):
        self.calls.append(request)
        if self.error is not None:
            raise self.error
        return self.response


def request() -> AssistantRequest:
    return AssistantRequest(
        correlation_id="request-001",
        messages=(Message(role="user", content="Explain serverless computing."),),
    )


class BedrockProviderTests(unittest.TestCase):
    def test_provider_maps_request_and_success_response(self):
        client = FakeBedrockClient(
            {
                "output": {
                    "message": {
                        "content": [{"text": "A managed execution model."}]
                    }
                }
            }
        )
        provider = BedrockConverseProvider(client, BedrockConfig())

        result = provider.generate(request())

        self.assertEqual(result, "A managed execution model.")
        self.assertEqual(client.calls[0]["modelId"], "amazon.nova-lite-v1:0")
        self.assertEqual(
            client.calls[0]["messages"][0]["content"][0]["text"],
            "Explain serverless computing.",
        )

    def test_client_exception_maps_to_provider_error(self):
        provider = BedrockConverseProvider(
            FakeBedrockClient(error=RuntimeError("simulated failure")),
            BedrockConfig(),
        )

        with self.assertRaises(ProviderError):
            provider.generate(request())

    def test_malformed_response_maps_to_provider_error(self):
        provider = BedrockConverseProvider(FakeBedrockClient({}), BedrockConfig())

        with self.assertRaises(ProviderError):
            provider.generate(request())


if __name__ == "__main__":
    unittest.main()

