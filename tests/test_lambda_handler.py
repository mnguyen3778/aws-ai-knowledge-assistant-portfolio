import json
import unittest

from knowledge_assistant.contracts import CONTRACT_VERSION
from knowledge_assistant.lambda_handler import lambda_handler


class StubProvider:
    def generate(self, request):
        return f"Processed {len(request.messages)} message."


class LambdaHandlerTests(unittest.TestCase):
    def test_http_api_v2_event_routes_through_injected_provider(self):
        event = {
            "rawPath": "/v1/assistant",
            "requestContext": {"http": {"method": "POST"}},
            "body": json.dumps(
                {
                    "contractVersion": CONTRACT_VERSION,
                    "correlationId": "request-002",
                    "messages": [{"role": "user", "content": "Hello"}],
                }
            ),
        }

        response = lambda_handler(event, object(), provider=StubProvider())

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(
            json.loads(response["body"])["message"]["content"],
            "Processed 1 message.",
        )


if __name__ == "__main__":
    unittest.main()

