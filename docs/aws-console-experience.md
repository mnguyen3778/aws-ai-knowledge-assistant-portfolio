# AWS Console Experience

## Evidence boundary

The services in this document were personally configured and validated through AWS. Reproducible infrastructure as code was not retained. Live identifiers are intentionally omitted, and this repository is not a deployable or reproducible record of those environments.

This documentation records **CONFIGURED AND VALIDATED IN AWS CONSOLE** experience. It does not reclassify those services as **IMPLEMENTED AND TESTED** in the public source.

## API and identity

### Amazon API Gateway

- Configured a REST API integration with a Lambda backend.
- Configured protected methods and exercised expected request/response behavior.
- Validated authenticated and rejected request paths at the gateway boundary.

### Amazon Cognito

- Configured a User Pool and API Gateway authorizer.
- Validated that the gateway required authentication for protected API access.
- The public portfolio handler does not verify JWTs or consume Cognito claims.

## Observability and alerting

### Amazon CloudWatch

- Reviewed Lambda execution logs and API Gateway operational signals.
- Configured metrics, dashboards, and alarms for request failures, latency, invocation errors, and duration.
- Data tracing of request/response payloads is not represented as a public portfolio feature.

### Amazon SNS

- Connected CloudWatch alarm state changes to notification delivery.
- No notification destination or deployment-specific topic information is published.

## Edge delivery and protection

### Amazon CloudFront and TLS delivery

- Configured CloudFront in front of the API origin.
- Validated encrypted delivery and custom-domain behavior.
- No domain, origin hostname, distribution identifier, or certificate identifier is published.

### AWS WAF

- Configured AWS managed rules.
- Configured rate-based protection.
- Exercised request handling and reviewed associated operational metrics.
- These controls reduce risk; they are not described as guaranteeing protection against every web attack.

## Security analytics

### Amazon S3

- Used object storage for WAF log delivery and analytics input.

### AWS Glue Data Catalog and crawler workflow

- Configured discovery of structured WAF log data.
- Validated catalog availability for query use.

### Amazon Athena

- Queried cataloged WAF log data to examine request actions and traffic patterns.
- No deployment-specific table, storage location, or query-result identifier is published.

## What this repository does not provide

- Infrastructure as code
- Console screenshots
- Live endpoints or resource identifiers
- Deployment automation
- Evidence of a currently running public environment
- Live AWS integration tests

