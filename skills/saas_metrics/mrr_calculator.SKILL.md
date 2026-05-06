---
skill: mrr_calculator
category: saas_metrics
description: Calculates MRR components and growth for Watering Hole subscriptions.
tier: free
inputs: sions
---

# Mrr Calculator

## Description
Calculates MRR components and growth for Watering Hole subscriptions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sions` | `array` | Yes | Subscription entries containing agent_id, plan, monthly_rate, status, and start_date (ISO 8601). |
| `analysis_date` | `string` | No | ISO date overriding today's date for month selection. |
| `previous_month_mrr` | `number` | No | Optional prior month MRR to compute MoM growth. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mrr_calculator",
  "arguments": {
    "sions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mrr_calculator"`.
