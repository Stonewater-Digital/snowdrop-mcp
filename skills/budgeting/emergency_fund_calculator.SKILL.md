---
skill: emergency_fund_calculator
category: budgeting
description: Calculates emergency fund target based on monthly expenses and provides timelines at 10% and 20% savings rates.
tier: free
inputs: monthly_expenses
---

# Emergency Fund Calculator

## Description
Calculates emergency fund target based on monthly expenses and provides timelines at 10% and 20% savings rates.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `monthly_expenses` | `number` | Yes | Total monthly essential expenses in dollars. |
| `months_target` | `number` | No | Number of months of expenses to save (default: 6). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "emergency_fund_calculator",
  "arguments": {
    "monthly_expenses": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "emergency_fund_calculator"`.
