---
skill: errors_omissions_premium_estimator
category: corporate_insurance
description: Calculates E&O premium using rate per revenue and modifiers.
tier: free
inputs: annual_revenue, base_rate_per_million
---

# Errors Omissions Premium Estimator

## Description
Calculates E&O premium using rate per revenue and modifiers.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_revenue` | `number` | Yes |  |
| `base_rate_per_million` | `number` | Yes |  |
| `risk_modifier_pct` | `number` | No |  |
| `claims_history_credit_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "errors_omissions_premium_estimator",
  "arguments": {
    "annual_revenue": 0,
    "base_rate_per_million": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "errors_omissions_premium_estimator"`.
