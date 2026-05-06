---
skill: expense_categorizer
category: payroll
description: Maps expense strings to IRS categories using heuristics.
tier: free
inputs: expenses
---

# Expense Categorizer

## Description
Maps expense strings to IRS categories using heuristics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `expenses` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "expense_categorizer",
  "arguments": {
    "expenses": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "expense_categorizer"`.
