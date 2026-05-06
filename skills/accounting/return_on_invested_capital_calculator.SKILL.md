---
skill: return_on_invested_capital_calculator
category: accounting
description: Calculates return on invested capital (ROIC), measuring how effectively a company generates returns on capital invested by shareholders and debtholders.
tier: free
inputs: net_income, dividends, total_capital
---

# Return On Invested Capital Calculator

## Description
Calculates return on invested capital (ROIC), measuring how effectively a company generates returns on capital invested by shareholders and debtholders.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_income` | `number` | Yes | Net income for the period. |
| `dividends` | `number` | Yes | Dividends paid during the period. |
| `total_capital` | `number` | Yes | Total invested capital (debt + equity). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "return_on_invested_capital_calculator",
  "arguments": {
    "net_income": 0,
    "dividends": 0,
    "total_capital": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "return_on_invested_capital_calculator"`.
