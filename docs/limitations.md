# Limitations and Non-Claims

This repository is a simplified, sanitized portfolio representation. It is not a production deployment and is not described as production-ready or production-grade.

## Infrastructure and deployment

- No infrastructure as code
- No live endpoint published
- No deployment-specific identifiers
- No deployment automation
- A GitHub Actions test workflow is included. Hosted CI execution will be validated after the portfolio repository is created on GitHub.
- No reproducible API Gateway, Cognito, CloudFront, WAF, IAM, monitoring, or analytics configuration

## Application capabilities

- No CORS implementation
- No application JWT verification
- No Cognito-claim consumption by the public handler
- No DynamoDB integration or persistence in the public source
- No RAG or vector database
- No conversation-history service
- No model-quality evaluation or prompt-management system

## Verification and operations

- No live AWS integration tests
- No load, stress, penetration, or resilience testing
- No formal SLOs or error budgets
- No incident-response automation
- No backup or disaster-recovery implementation
- No measured production cost baseline

## Intellectual-property boundary

Proprietary security and business-specific implementation details remain private. The public repository intentionally demonstrates only the small set of capabilities represented by its source and tests.

## Documentation build limitation

Local SVG rendering is not currently configured. Mermaid source is provided in [`architecture/architecture.mmd`](architecture/architecture.mmd), and the README uses GitHub-native Mermaid rendering. A rendered SVG may be added only in a later, separately authorized phase.

## Production-readiness wording

The repository demonstrates production-readiness foundations such as bounded validation, versioned contracts, provider isolation, deterministic errors, and targeted tests. Those techniques do not establish that the repository is a complete or production-ready system.
