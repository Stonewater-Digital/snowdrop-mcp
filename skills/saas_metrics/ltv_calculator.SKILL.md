---
skill: ltv_calculator
category: saas_metrics
description: Computes LTV, discounted LTV, and payback metrics for each agent tier.
tier: free
inputs: tier_metrics
---

# Ltv Calculator

## Description
Computes LTV, discounted LTV, and payback metrics for each agent tier.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tier_metrics` | `array` | Yes | List of tier dictionaries with tier, avg_monthly_revenue, avg_lifetime_months, gross_margin_pct, and optional acquisition_cost. |
| `discount_rate_monthly` | `number` | No | Monthly discount rate used for present-value LTV. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ltv_calculator",
  "arguments": {
    "tier_metrics": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ltv_calculator"`.
