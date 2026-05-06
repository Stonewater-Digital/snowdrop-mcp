---
skill: daily_spending_limit_calculator
category: budgeting
description: Converts a monthly budget into daily and weekly spending limits.
tier: free
inputs: monthly_budget
---

# Daily Spending Limit Calculator

## Description
Converts a monthly budget into daily and weekly spending limits.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `monthly_budget` | `number` | Yes | Total monthly discretionary budget in dollars. |
| `days_in_month` | `integer` | No | Number of days in the current month (default: 30). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "daily_spending_limit_calculator",
  "arguments": {
    "monthly_budget": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "daily_spending_limit_calculator"`.
