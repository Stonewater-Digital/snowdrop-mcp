---
skill: corporate_business_interruption_calculator
category: corporate_insurance
description: Estimates business interruption exposure from revenue, expense, and standby time.
tier: free
inputs: annual_revenue, variable_expense_ratio_pct, restoration_period_days
---

# Corporate Business Interruption Calculator

## Description
Estimates business interruption exposure from revenue, expense, and standby time.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_revenue` | `number` | Yes |  |
| `variable_expense_ratio_pct` | `number` | Yes |  |
| `restoration_period_days` | `number` | Yes |  |
| `waiting_period_days` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "corporate_business_interruption_calculator",
  "arguments": {
    "annual_revenue": 0,
    "variable_expense_ratio_pct": 0,
    "restoration_period_days": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "corporate_business_interruption_calculator"`.
