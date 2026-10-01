import json
import unittest

from knowledge_assistant.app import handle_event
from knowledge_assistant.contracts import CONTRACT_VERSION
from knowledge_assistant.providers import ProviderError


class StubProvider:
    def __init__(self, content="Representative response.", failure=False):
        self.content = content
        self.failure = failure
        self.requests = []

    def generate(self, request):
        self.requests.append(request)
        if self.failure:
            raise ProviderError("simulated")
        return self.content


def event(body=None, method="POST", path="/v1/assistant"):
    if body is None:
        body = json.dumps(
            {
                "contractVersion": CONTRACT_VERSION,
                "correlationId": "request-001",
                "messages": [{"role": "user", "content": "Explain an AWS service."}],
            }
        )
    return {"httpMethod": method, "path": path, "body": body}


class ApplicationTests(unittest.TestCase):
    def test_valid_request_returns_deterministic_contract_response(self):
        provider = StubProvider()

        first = handle_event(event(), provider)
        second = handle_event(event(), provider)

        self.assertEqual(first, second)
        self.assertEqual(first["statusCode"], 200)
        self.assertEqual(first["headers"], {"Content-Type": "application/json"})
        self.assertEqual(
            json.loads(first["body"]),
            {
                "contractVersion": CONTRACT_VERSION,
                "correlationId": "request-001",
                "message": {
                    "role": "assistant",
                    "content": "Representative response.",
                },
            },
        )

    def test_malformed_json_returns_validation_response(self):
        response = handle_event(event(body="{"), StubProvider())

        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(json.loads(response["body"])["error"]["code"], "VALIDATION_ERROR")

    def test_missing_required_field_returns_validation_response(self):
        body = json.dumps(
            {
                "contractVersion": CONTRACT_VERSION,
                "correlationId": "request-001",
            }
        )

        response = handle_event(event(body=body), StubProvider())

        self.assertEqual(response["statusCode"], 400)

    def test_provider_failure_returns_bad_gateway_response(self):
        response = handle_event(event(), StubProvider(failure=True))

        self.assertEqual(response["statusCode"], 502)
        self.assertEqual(json.loads(response["body"])["error"]["code"], "PROVIDER_FAILURE")

    def test_wrong_method_is_rejected_without_calling_provider(self):
        provider = StubProvider()

        response = handle_event(event(method="GET"), provider)

        self.assertEqual(response["statusCode"], 405)
        self.assertEqual(provider.requests, [])

    def test_unknown_route_is_rejected_without_calling_provider(self):
        provider = StubProvider()

        response = handle_event(event(path="/unknown"), provider)

        self.assertEqual(response["statusCode"], 404)
        self.assertEqual(provider.requests, [])


if __name__ == "__main__":
    unittest.main()

