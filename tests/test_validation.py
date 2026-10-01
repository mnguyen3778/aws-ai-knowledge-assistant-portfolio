import json
import unittest

from knowledge_assistant.contracts import CONTRACT_VERSION
from knowledge_assistant.validation import RequestValidationError, load_request


def valid_body() -> str:
    return json.dumps(
        {
            "contractVersion": CONTRACT_VERSION,
            "correlationId": "request-001",
            "messages": [{"role": "user", "content": "  Explain Lambda.  "}],
        }
    )


class RequestValidationTests(unittest.TestCase):
    def test_valid_request_is_normalized(self):
        request = load_request(valid_body())

        self.assertEqual(request.correlation_id, "request-001")
        self.assertEqual(request.messages[0].content, "Explain Lambda.")

    def test_malformed_json_is_rejected(self):
        with self.assertRaises(RequestValidationError) as raised:
            load_request("{")

        self.assertEqual(raised.exception.issues[0].code, "INVALID_JSON")

    def test_missing_required_field_is_rejected(self):
        body = json.dumps(
            {
                "contractVersion": CONTRACT_VERSION,
                "correlationId": "request-001",
            }
        )

        with self.assertRaises(RequestValidationError) as raised:
            load_request(body)

        self.assertIn("messages", [issue.field for issue in raised.exception.issues])

    def test_duplicate_json_field_is_rejected(self):
        body = (
            '{"contractVersion":"knowledge-assistant-v1",'
            '"correlationId":"first","correlationId":"second",'
            '"messages":[{"role":"user","content":"Hello"}]}'
        )

        with self.assertRaises(RequestValidationError) as raised:
            load_request(body)

        self.assertEqual(raised.exception.issues[0].code, "DUPLICATE_FIELD")


if __name__ == "__main__":
    unittest.main()

