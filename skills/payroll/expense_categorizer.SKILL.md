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
| `expenses` | `array` | Yes | List of expense objects, each with keys: `vendor` (string), `description` (string), `amount` (number). |

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
    "expenses": [
      {"vendor": "OpenAI", "description": "API usage May 2024", "amount": 120.00},
      {"vendor": "Fly.io", "description": "Hosting - snowdrop-mcp", "amount": 45.00}
    ]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "expense_categorizer"`.
