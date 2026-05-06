---
skill: long_term_care_cost_estimator
category: insurance
description: Estimate future long-term care costs adjusted for inflation. Calculates daily and total costs at the time care is needed.
tier: free
inputs: none
---

# Long Term Care Cost Estimator

## Description
Estimate future long-term care costs adjusted for inflation. Calculates daily and total costs at the time care is needed.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `daily_rate` | `number` | No | Current average daily LTC rate (default 300). |
| `years_of_care` | `number` | No | Expected years of care needed (default 3). |
| `inflation_rate` | `number` | No | Annual LTC cost inflation rate as decimal (default 0.03). |
| `years_until_need` | `integer` | No | Years from now until care is needed (default 20). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "long_term_care_cost_estimator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "long_term_care_cost_estimator"`.
