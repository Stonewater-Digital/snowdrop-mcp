---
skill: profit_margin_analyzer
category: small_business
description: Builds a margin waterfall starting at revenue to show gross, operating, EBITDA, pretax, and net profit percentages.
tier: free
inputs: revenue, cogs, operating_expenses, interest_expense, tax_rate
---

# Profit Margin Analyzer

## Description
Builds a margin waterfall starting at revenue to show gross, operating, EBITDA, pretax, and net profit percentages.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `revenue` | `number` | Yes | Total revenue. |
| `cogs` | `number` | Yes | Cost of goods sold. |
| `operating_expenses` | `object` | Yes | Dictionary of operating expense categories and dollar amounts. |
| `interest_expense` | `number` | Yes | Interest expense. |
| `tax_rate` | `number` | Yes | Effective tax rate as decimal. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "profit_margin_analyzer",
  "arguments": {
    "revenue": 0,
    "cogs": 0,
    "operating_expenses": {},
    "interest_expense": 0,
    "tax_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "profit_margin_analyzer"`.
