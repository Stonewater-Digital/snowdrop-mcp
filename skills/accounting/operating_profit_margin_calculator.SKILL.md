---
skill: operating_profit_margin_calculator
category: accounting
description: Calculates operating profit margin as a percentage, showing how much profit a company makes from operations before interest and taxes.
tier: free
inputs: operating_income, revenue
---

# Operating Profit Margin Calculator

## Description
Calculates operating profit margin as a percentage, showing how much profit a company makes from operations before interest and taxes.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operating_income` | `number` | Yes | Operating income (EBIT). |
| `revenue` | `number` | Yes | Total revenue. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "operating_profit_margin_calculator",
  "arguments": {
    "operating_income": 0,
    "revenue": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "operating_profit_margin_calculator"`.
