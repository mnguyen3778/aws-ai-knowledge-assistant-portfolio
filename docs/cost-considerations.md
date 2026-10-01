# Cost Considerations

This document describes generic cost drivers and controls. It contains no account spending, usage totals, forecasts, or deployment identifiers.

## Primary cost drivers

| Service | Typical driver |
|---|---|
| Amazon Bedrock | Model input/output usage and selected model |
| AWS Lambda | Invocation count, duration, memory configuration, and concurrency |
| Amazon API Gateway | API request volume and data transfer |
| Amazon CloudWatch | Log ingestion, retention, queries, custom metrics, dashboards, and alarms |
| AWS WAF | Web ACLs, enabled rules, and evaluated requests |
| Amazon S3 | Stored log volume, requests, lifecycle, and retrieval patterns |
| AWS Glue | Crawler runs and Data Catalog usage |
| Amazon Athena | Data scanned by each query |
| Amazon CloudFront | Requests, data transfer, and optional edge features |
| Amazon SNS | Published notifications and delivery type |

## Application-level controls

- Limit the number of messages per request.
- Limit per-message and aggregate content size.
- Reject unsupported routes and methods before invoking a model.
- Use a cost-conscious model appropriate for the workload.
- Treat provider failures as failures rather than retrying without bounds.

The public implementation includes message-count and content-size limits. It does not include a token estimator, usage accounting, or adaptive model routing.

## Platform controls

- Apply API Gateway throttling and quotas appropriate to the consumer model.
- Use AWS WAF rate-based rules as an additional abuse-control layer.
- Set Lambda concurrency controls where cost or downstream protection requires them.
- Configure CloudWatch log retention instead of retaining all logs indefinitely.
- Use metrics and alarms for abnormal error, latency, invocation, and model-usage patterns.
- Configure budgets and cost alerts for deployed accounts.

## Analytics controls

- Store logs in compressed, query-friendly formats where practical.
- Partition analytics data by useful dimensions such as date.
- Scope Athena queries to required columns and partitions to reduce bytes scanned.
- Schedule Glue crawler runs according to data-arrival needs rather than continuously.
- Apply S3 lifecycle policies to transition or expire old analytics data.

## Cost-evidence boundary

The repository documents architectural cost awareness. It does not claim a measured production cost baseline or guarantee a specific monthly cost.

