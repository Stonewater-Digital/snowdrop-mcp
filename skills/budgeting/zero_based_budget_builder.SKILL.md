---
skill: zero_based_budget_builder
category: budgeting
description: Builds a zero-based budget: every dollar of income is assigned to a category. Shows remaining unallocated funds.
tier: free
inputs: monthly_income, expenses
---

# Zero Based Budget Builder

## Description
Builds a zero-based budget: every dollar of income is assigned to a category. Shows remaining unallocated funds.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `monthly_income` | `number` | Yes | Total monthly income in dollars. |
| `expenses` | `array` | Yes | List of expense categories with amounts. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "zero_based_budget_builder",
  "arguments": {
    "monthly_income": 0,
    "expenses": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "zero_based_budget_builder"`.
