---
skill: burn_rate_calculator
category: treasury
description: Calculates gross/net burn, runway, and trend classification from recent data.
tier: free
inputs: monthly_expenses, monthly_revenue, current_cash
---

# Burn Rate Calculator

## Description
Calculates gross/net burn, runway, and trend classification from recent data.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `monthly_expenses` | `array` | Yes |  |
| `monthly_revenue` | `array` | Yes |  |
| `current_cash` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "burn_rate_calculator",
  "arguments": {
    "monthly_expenses": [],
    "monthly_revenue": [],
    "current_cash": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "burn_rate_calculator"`.
