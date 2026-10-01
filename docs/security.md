# Security

## Scope and non-goals

This repository is a sanitized portfolio implementation. It demonstrates defensive application boundaries and documents prior AWS console experience. It does not contain a production environment, deployment configuration, customer data, live identifiers, credentials, or a complete enterprise security program.

## Trust boundaries

The documented architecture has these primary boundaries:

1. Internet client to the CloudFront and AWS WAF edge.
2. Edge services to API Gateway.
3. Cognito authorizer evaluation at API Gateway.
4. API Gateway to the Lambda-compatible Python handler.
5. The application provider boundary to Amazon Bedrock Runtime.
6. API and Lambda operational signals to CloudWatch and SNS.
7. WAF logs to the S3, Glue, and Athena analytics workflow.

Only the Python contract, validation, routing, provider abstraction, Bedrock adapter, and unit tests are implemented in this repository.

## Gateway-level authentication

A Cognito User Pool authorizer was configured and validated at API Gateway. Cognito attaches to the gateway as an authorizer; it is not a serial network hop in the request path.

The public handler does not verify JWTs and does not consume Cognito identity claims. Authentication depends on correct gateway configuration in a deployed environment, and no IaC is included to reproduce or prove that configuration.

## Input validation

The representative application:

- Accepts one documented versioned route and method.
- Requires a versioned JSON contract.
- Rejects malformed JSON and duplicate keys.
- Rejects missing and unknown fields.
- Restricts identifier syntax and length.
- Accepts only user-role messages.
- Limits message count, individual message size, and total message content.
- Normalizes accepted content before provider invocation.

These controls reduce malformed-input and unbounded-cost risk but are not a replacement for gateway payload limits, WAF rules, quotas, or operational monitoring.

## Provider boundary

The application depends on a small provider protocol rather than directly coupling routing logic to the AWS SDK. The Bedrock adapter maps normalized messages to the `converse` request shape and converts client or response-shape failures into sanitized application errors.

Unit tests use injected fakes. They validate mapping and failure behavior without contacting AWS.

## IAM and secrets principles

- No credentials or secret values are embedded in the repository.
- A deployed Lambda should use an IAM execution role and the AWS SDK credential provider chain.
- Bedrock permissions should be limited to the required invocation actions and approved model resources.
- Deployment configuration and secret values should be supplied outside source control.
- Least-privilege policies should be reviewed independently because no IaC is included here.

## Edge and WAF controls

The documented AWS console experience includes CloudFront, AWS WAF managed rules, and rate-based protection. These are defense-in-depth controls, not guarantees against all attacks. Direct-origin exposure, rule tuning, false positives, logging, and cost should be evaluated for each deployment.

## Rate and cost controls

The public code bounds message count and content size. A deployed system should additionally use gateway throttling, WAF rate-based rules, service quotas, concurrency controls, model usage monitoring, and budget alerts.

## Logging and data handling

- Avoid logging credentials, authorization headers, identity claims, raw prompts, model responses, or sensitive request bodies.
- Prefer structured operational events and correlation identifiers.
- Redact sensitive fields before logging.
- Configure retention according to operational and data-governance needs.
- Restrict access to logs and analytics data using least privilege.

No production data or deployment logs are included in this repository.

## Failure handling

Validation failures return a deterministic 400 response. Unsupported routes and methods return 404 and 405 responses. Normalized provider failures return a sanitized 502 response without exposing SDK exceptions or upstream response bodies.

## Private authorization boundary

The underlying private engineering project includes a more extensive fail-closed server-side authorization implementation. That proprietary implementation is intentionally excluded from this public portfolio.

## Known security gaps

- No application JWT verification
- No Cognito-claim consumption
- No CORS implementation
- No reproducible gateway, authorizer, IAM, WAF, or logging configuration
- No live AWS integration test
- No penetration or load testing
- No formal threat-model artifact beyond this summary
- No SLO, incident-response, backup, or disaster-recovery implementation

## Public-release checklist

Locally verified:

- [x] No account identifiers, ARNs, endpoints, domains, resource identifiers, or personal information
- [x] No credentials, tokens, secret values, or local environment files
- [x] No production prompts, responses, logs, screenshots, or customer data
- [x] No private repository paths, history, tags, or commit identifiers
- [x] Evidence labels agree across the README, status matrix, and architecture
- [x] Unit tests pass without AWS access
- [x] Locally installed secret scanner reports no findings
- [x] Mermaid source contains only generic service labels
- [ ] Dependency vulnerability review is complete

Pending after GitHub publication:

- [x] GitHub-hosted Actions test workflow completed successfully on push using CPython 3.11.16; package installation succeeded and all 22 tests passed (`OK`)
- [x] GitHub-native Mermaid rendering was verified through human visual inspection

