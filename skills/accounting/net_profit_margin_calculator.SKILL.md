---
skill: net_profit_margin_calculator
category: accounting
description: Calculates net profit margin as a percentage, measuring the proportion of revenue that becomes bottom-line profit.
tier: free
inputs: net_income, revenue
---

# Net Profit Margin Calculator

## Description
Calculates net profit margin as a percentage, measuring the proportion of revenue that becomes bottom-line profit.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_income` | `number` | Yes | Net income for the period. |
| `revenue` | `number` | Yes | Total revenue. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "net_profit_margin_calculator",
  "arguments": {
    "net_income": 0,
    "revenue": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "net_profit_margin_calculator"`.
