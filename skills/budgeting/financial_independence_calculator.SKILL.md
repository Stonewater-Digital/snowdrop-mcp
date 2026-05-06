---
skill: financial_independence_calculator
category: budgeting
description: Calculates your FI number (25x annual expenses) and estimates years to financial independence using compound growth.
tier: free
inputs: annual_expenses, current_savings, annual_savings
---

# Financial Independence Calculator

## Description
Calculates your FI number (25x annual expenses) and estimates years to financial independence using compound growth.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_expenses` | `number` | Yes | Current annual living expenses in dollars. |
| `current_savings` | `number` | Yes | Current total invested savings/portfolio in dollars. |
| `annual_savings` | `number` | Yes | Amount saved and invested per year in dollars. |
| `expected_return` | `number` | No | Expected annual real (inflation-adjusted) investment return as a decimal (default: 0.07 for 7%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "financial_independence_calculator",
  "arguments": {
    "annual_expenses": 0,
    "current_savings": 0,
    "annual_savings": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "financial_independence_calculator"`.
