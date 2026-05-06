---
skill: annual_expense_projector
category: budgeting
description: Projects monthly expenses to annual totals with category breakdown.
tier: free
inputs: monthly_expenses
---

# Annual Expense Projector

## Description
Projects monthly expenses to annual totals with category breakdown.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `monthly_expenses` | `array` | Yes | List of monthly expense categories with amounts. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "annual_expense_projector",
  "arguments": {
    "monthly_expenses": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "annual_expense_projector"`.
