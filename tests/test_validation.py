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
    def assert_validation_issue(self, raw_body, field, code):
        with self.assertRaises(RequestValidationError) as raised:
            load_request(raw_body)

        self.assertEqual(
            [(issue.field, issue.code) for issue in raised.exception.issues],
            [(field, code)],
        )

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

    def test_unknown_top_level_field_is_rejected(self):
        payload = json.loads(valid_body())
        payload["unexpectedField"] = "unexpected value"

        self.assert_validation_issue(
            json.dumps(payload),
            "unexpectedField",
            "UNKNOWN_FIELD",
        )

    def test_unsupported_contract_version_is_rejected(self):
        payload = json.loads(valid_body())
        payload["contractVersion"] = "knowledge-assistant-v2"

        self.assert_validation_issue(
            json.dumps(payload),
            "contractVersion",
            "UNSUPPORTED_VERSION",
        )

    def test_invalid_correlation_identifier_is_rejected(self):
        payload = json.loads(valid_body())
        payload["correlationId"] = "request identifier with spaces"

        self.assert_validation_issue(
            json.dumps(payload),
            "correlationId",
            "INVALID_IDENTIFIER",
        )

    def test_invalid_message_role_is_rejected(self):
        payload = json.loads(valid_body())
        payload["messages"][0]["role"] = "assistant"

        self.assert_validation_issue(
            json.dumps(payload),
            "messages[0].role",
            "INVALID_ROLE",
        )

    def test_message_count_limit_is_enforced(self):
        payload = json.loads(valid_body())
        payload["messages"] = [
            {"role": "user", "content": f"Message {index}"}
            for index in range(11)
        ]

        self.assert_validation_issue(
            json.dumps(payload),
            "messages",
            "LIMIT_EXCEEDED",
        )

    def test_individual_message_content_limit_is_enforced(self):
        payload = json.loads(valid_body())
        payload["messages"][0]["content"] = "x" * 2_001

        self.assert_validation_issue(
            json.dumps(payload),
            "messages[0].content",
            "LIMIT_EXCEEDED",
        )

    def test_total_message_content_limit_is_enforced(self):
        payload = json.loads(valid_body())
        payload["messages"] = [
            {"role": "user", "content": "x" * 2_000}
            for _ in range(5)
        ]

        self.assert_validation_issue(
            json.dumps(payload),
            "messages",
            "LIMIT_EXCEEDED",
        )

    def test_non_string_request_body_is_rejected(self):
        self.assert_validation_issue(
            {"contractVersion": CONTRACT_VERSION},
            "body",
            "INVALID_TYPE",
        )


if __name__ == "__main__":
    unittest.main()

