# Implementation Status

This matrix is the authoritative boundary between public implementation evidence, AWS console experience, historical prototype exposure, and known limitations.

## Evidence classifications

1. **IMPLEMENTED AND TESTED** — code and automated tests exist in this public portfolio repository.
2. **CONFIGURED AND VALIDATED IN AWS CONSOLE** — personally configured and exercised in AWS, but reproducible IaC was not retained.
3. **ARCHITECTURE / PROTOTYPE EXPOSURE** — architecture/design work or a separate historical prototype exists, but the capability is not implemented in the current public source.
4. **KNOWN LIMITATION** — not implemented or not sufficiently evidenced.

## Capability matrix

| Capability | Classification | Evidence and boundary |
|---|---|---|
| Python | **IMPLEMENTED AND TESTED** | The package under [`src/knowledge_assistant`](../src/knowledge_assistant/) contains typed Python application code. |
| AWS Lambda-compatible handler | **IMPLEMENTED AND TESTED** | [`lambda_handler.py`](../src/knowledge_assistant/lambda_handler.py) implements the Lambda handler signature and injected-provider test seam. |
| REST-oriented routing | **IMPLEMENTED AND TESTED** | [`app.py`](../src/knowledge_assistant/app.py) recognizes a bounded versioned route and returns HTTP-style envelopes. |
| Versioned request/response contract | **IMPLEMENTED AND TESTED** | [`contracts.py`](../src/knowledge_assistant/contracts.py) and [`validation.py`](../src/knowledge_assistant/validation.py). |
| Defensive JSON validation | **IMPLEMENTED AND TESTED** | Duplicate keys, missing/unknown fields, identifiers, roles, counts, and content bounds are tested. |
| Deterministic serialization | **IMPLEMENTED AND TESTED** | Stable key ordering and compact JSON output in [`contracts.py`](../src/knowledge_assistant/contracts.py). |
| Provider abstraction | **IMPLEMENTED AND TESTED** | [`providers.py`](../src/knowledge_assistant/providers.py) defines the model-provider boundary. |
| Amazon Bedrock Runtime | **IMPLEMENTED AND TESTED** | [`bedrock.py`](../src/knowledge_assistant/bedrock.py) constructs and maps a `converse` request; tests use a fake client, not AWS. |
| Amazon Nova Lite | **IMPLEMENTED AND TESTED** | Safe default model selection and request mapping are covered by [`test_bedrock.py`](../tests/test_bedrock.py). |
| Provider failure handling | **IMPLEMENTED AND TESTED** | Provider exceptions and malformed responses map to a safe provider error and HTTP 502 response. |
| API Gateway REST integration | **CONFIGURED AND VALIDATED IN AWS CONSOLE** | Prior AWS console configuration and validation are documented in [AWS Console Experience](aws-console-experience.md); no IaC is present. |
| Amazon Cognito | **CONFIGURED AND VALIDATED IN AWS CONSOLE** | A User Pool authorizer was configured at the API Gateway boundary; the public handler does not verify JWTs. |
| Amazon CloudWatch | **CONFIGURED AND VALIDATED IN AWS CONSOLE** | Logs, metrics, dashboards, and alarms were configured and exercised; no deployment definitions are included. |
| Amazon SNS | **CONFIGURED AND VALIDATED IN AWS CONSOLE** | Alarm notification delivery was configured and validated; no topic configuration is published. |
| Amazon S3 | **CONFIGURED AND VALIDATED IN AWS CONSOLE** | Used in the separately documented WAF-log analytics workflow. |
| AWS Glue Data Catalog / crawler | **CONFIGURED AND VALIDATED IN AWS CONSOLE** | WAF log discovery and cataloging were configured and queried; no crawler definition is included. |
| Amazon Athena | **CONFIGURED AND VALIDATED IN AWS CONSOLE** | Queries against cataloged WAF log data were validated; no deployment-specific query or identifier is published. |
| Amazon CloudFront | **CONFIGURED AND VALIDATED IN AWS CONSOLE** | Edge delivery and TLS/custom-domain behavior were configured and validated; live delivery identifiers are omitted. |
| AWS WAF managed rules | **CONFIGURED AND VALIDATED IN AWS CONSOLE** | Managed rule protections were configured and exercised; this is not a claim of complete web-attack prevention. |
| AWS WAF rate-based protection | **CONFIGURED AND VALIDATED IN AWS CONSOLE** | Rate-based request protection was configured and validated; configuration is not represented as IaC. |
| Authentication | **CONFIGURED AND VALIDATED IN AWS CONSOLE** | Authentication was enforced at the API Gateway Cognito-authorizer boundary; no application JWT-verification claim is made. |
| Authorization | **ARCHITECTURE / PROTOTYPE EXPOSURE** | See [Private authorization boundary](security.md#private-authorization-boundary). |
| CORS | **KNOWN LIMITATION** | No CORS response headers, policy, or tests exist in the public implementation. |
| Targeted unit tests | **IMPLEMENTED AND TESTED** | Four test modules currently provide 22 passing tests without AWS calls. |
| Production readiness | **KNOWN LIMITATION** | The repository demonstrates selected production-readiness foundations, not a production deployment or production-ready system. |

## Architecture / prototype exposure

DynamoDB conversation-history persistence was explored and validated as a separate historical prototype. It is not part of the active request path, and the current public source contains no DynamoDB client, persistence adapter, table configuration, or integration test.

