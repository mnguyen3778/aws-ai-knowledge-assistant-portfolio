# Architecture Decisions

These are concise, portfolio-specific decisions written for this public repository. They are not copied from private milestone or decision records.

## 1. Use a serverless request path

**Decision:** Represent the backend as API Gateway to a Lambda-compatible Python handler, with Amazon Bedrock as the managed model service.

**Rationale:** This keeps infrastructure operations small, supports request-driven scaling, and aligns cost with usage.

**Boundary:** API Gateway and the deployment environment are documented console experience; only the Python handler is implemented here.

## 2. Version the public contract

**Decision:** Require an explicit contract version in each request and response.

**Rationale:** Consumers receive predictable compatibility behavior, and unsupported versions fail clearly instead of being silently interpreted.

## 3. Separate application flow from the model provider

**Decision:** Route validated requests through a provider protocol.

**Rationale:** Provider-specific SDK mapping stays isolated, tests can inject fakes, and application routing does not need AWS access.

## 4. Demonstrate Bedrock Runtime with Nova Lite

**Decision:** Use a configurable Nova Lite default and the Bedrock Runtime `converse` interface.

**Rationale:** It demonstrates an AWS-managed Generative AI integration and a conversational message shape without embedding credentials or proprietary prompts.

**Tradeoff:** The portfolio does not compare model quality, implement dynamic routing, or perform live model tests.

## 5. Keep authentication at the gateway boundary

**Decision:** Document Cognito as an API Gateway authorizer rather than implement JWT verification in the public handler.

**Rationale:** This matches the console-configured architecture and avoids claiming application functionality that is absent.

**Tradeoff:** Correct authentication depends on deployment configuration that is not reproducible from this repository.

## 6. Validate before provider invocation

**Decision:** Reject malformed, unknown, unsupported, or oversized input before crossing the provider boundary.

**Rationale:** Defensive validation improves contract predictability and reduces unnecessary provider calls and cost exposure.

## 7. Separate evidence categories

**Decision:** Label repository implementation, console experience, historical prototypes, and limitations independently.

**Rationale:** Documentation should not imply that a diagram or console narrative is equivalent to tested code or reproducible infrastructure.

