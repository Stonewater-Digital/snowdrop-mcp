---
skill: return_on_equity_calculator
category: accounting
description: Calculates return on equity (ROE) as a percentage, measuring profitability relative to shareholders equity.
tier: free
inputs: net_income, avg_shareholders_equity
---

# Return On Equity Calculator

## Description
Calculates return on equity (ROE) as a percentage, measuring profitability relative to shareholders equity.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_income` | `number` | Yes | Net income for the period. |
| `avg_shareholders_equity` | `number` | Yes | Average shareholders equity for the period. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "return_on_equity_calculator",
  "arguments": {
    "net_income": 0,
    "avg_shareholders_equity": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "return_on_equity_calculator"`.
