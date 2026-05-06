---
skill: annual_run_rate_calculator
category: small_business
description: Calculate Annual Run Rate by annualizing a partial period's revenue: ARR = revenue * (12 / period_months).
tier: free
inputs: current_period_revenue, period_months
---

# Annual Run Rate Calculator

## Description
Calculate Annual Run Rate by annualizing a partial period's revenue: ARR = revenue * (12 / period_months).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_period_revenue` | `number` | Yes | Revenue earned in the current period. |
| `period_months` | `number` | Yes | Number of months in the current period. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "annual_run_rate_calculator",
  "arguments": {
    "current_period_revenue": 0,
    "period_months": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "annual_run_rate_calculator"`.
