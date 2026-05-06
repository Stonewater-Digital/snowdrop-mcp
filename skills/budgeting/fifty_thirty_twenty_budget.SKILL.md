---
skill: fifty_thirty_twenty_budget
category: budgeting
description: Applies the 50/30/20 budgeting rule to split monthly income into needs, wants, and savings.
tier: free
inputs: monthly_income
---

# Fifty Thirty Twenty Budget

## Description
Applies the 50/30/20 budgeting rule to split monthly income into needs, wants, and savings.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `monthly_income` | `number` | Yes | Gross or net monthly income in dollars. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fifty_thirty_twenty_budget",
  "arguments": {
    "monthly_income": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fifty_thirty_twenty_budget"`.
