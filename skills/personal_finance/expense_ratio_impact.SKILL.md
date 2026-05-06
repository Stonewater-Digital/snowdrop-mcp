---
skill: expense_ratio_impact
category: personal_finance
description: Quantifies the difference in ending balance between two funds with different expense ratios and reports cumulative fee drag.
tier: free
inputs: investment_amount, annual_return_gross, expense_ratio, comparison_expense_ratio, years
---

# Expense Ratio Impact

## Description
Quantifies the difference in ending balance between two funds with different expense ratios and reports cumulative fee drag.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `investment_amount` | `number` | Yes | Initial investment in dollars. |
| `annual_return_gross` | `number` | Yes | Gross expected annual return before fees. |
| `expense_ratio` | `number` | Yes | Expense ratio (as decimal) of the current fund. |
| `comparison_expense_ratio` | `number` | Yes | Expense ratio of the lower-cost alternative. |
| `years` | `number` | Yes | Investment horizon in years. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "expense_ratio_impact",
  "arguments": {
    "investment_amount": 0,
    "annual_return_gross": 0,
    "expense_ratio": 0,
    "comparison_expense_ratio": 0,
    "years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "expense_ratio_impact"`.
