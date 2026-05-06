---
skill: cac_ltv_calculator
category: small_business
description: Calculates CAC, gross-margin LTV, payback period, and ratio health to evaluate growth efficiency for subscription and transactional businesses.
tier: free
inputs: marketing_spend, new_customers, avg_revenue_per_customer, avg_customer_lifespan_months, gross_margin_pct, churn_rate
---

# Cac Ltv Calculator

## Description
Calculates CAC, gross-margin LTV, payback period, and ratio health to evaluate growth efficiency for subscription and transactional businesses.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `marketing_spend` | `number` | Yes | Total acquisition spend over the period. |
| `new_customers` | `number` | Yes | Number of customers acquired from that spend. |
| `avg_revenue_per_customer` | `number` | Yes | Average monthly revenue per customer. |
| `avg_customer_lifespan_months` | `number` | Yes | Average active months before churn. |
| `gross_margin_pct` | `number` | Yes | Gross margin percentage as decimal. |
| `churn_rate` | `number` | Yes | Monthly churn rate as decimal. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cac_ltv_calculator",
  "arguments": {
    "marketing_spend": 0,
    "new_customers": 0,
    "avg_revenue_per_customer": 0,
    "avg_customer_lifespan_months": 0,
    "gross_margin_pct": 0,
    "churn_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cac_ltv_calculator"`.
