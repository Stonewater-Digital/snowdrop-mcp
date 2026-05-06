---
skill: monthly_cash_flow_analyzer
category: budgeting
description: Analyzes monthly cash flow by comparing total income to total expenses and calculating net cash flow.
tier: free
inputs: income_items, expense_items
---

# Monthly Cash Flow Analyzer

## Description
Analyzes monthly cash flow by comparing total income to total expenses and calculating net cash flow.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `income_items` | `array` | Yes | List of income sources with name and amount. |
| `expense_items` | `array` | Yes | List of expense categories with name and amount. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "monthly_cash_flow_analyzer",
  "arguments": {
    "income_items": [],
    "expense_items": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "monthly_cash_flow_analyzer"`.
