---
skill: operating_expense_ratio
category: reits
description: Calculates operating expense ratio and efficiency gap versus target.
tier: free
inputs: operating_expenses, gross_revenue
---

# Operating Expense Ratio

## Description
Calculates operating expense ratio and efficiency gap versus target.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operating_expenses` | `number` | Yes |  |
| `gross_revenue` | `number` | Yes |  |
| `target_ratio_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "operating_expense_ratio",
  "arguments": {
    "operating_expenses": 0,
    "gross_revenue": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "operating_expense_ratio"`.
