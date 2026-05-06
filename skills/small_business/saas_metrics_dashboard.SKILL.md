---
skill: saas_metrics_dashboard
category: small_business
description: Generates a snapshot of SaaS health including net new MRR, churn metrics, ARPU, net revenue retention, and the quick ratio.
tier: free
inputs: mrr, new_mrr, churned_mrr, expansion_mrr, customers, new_customers, churned_customers
---

# Saas Metrics Dashboard

## Description
Generates a snapshot of SaaS health including net new MRR, churn metrics, ARPU, net revenue retention, and the quick ratio.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `mrr` | `number` | Yes | Monthly recurring revenue at period start. |
| `new_mrr` | `number` | Yes | MRR from new customers in the period. |
| `churned_mrr` | `number` | Yes | MRR lost from churn in the period. |
| `expansion_mrr` | `number` | Yes | MRR gained from existing customers (upsell/cross-sell). |
| `customers` | `number` | Yes | Active customer count at period start. |
| `new_customers` | `number` | Yes | Customers added during the period. |
| `churned_customers` | `number` | Yes | Customers lost during the period. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "saas_metrics_dashboard",
  "arguments": {
    "mrr": 0,
    "new_mrr": 0,
    "churned_mrr": 0,
    "expansion_mrr": 0,
    "customers": 0,
    "new_customers": 0,
    "churned_customers": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "saas_metrics_dashboard"`.
