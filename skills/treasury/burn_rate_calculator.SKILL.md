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
| `monthly_expenses` | `array` | Yes | Ordered list of monthly expense totals in USD (numbers), most recent last. Minimum 1 entry; 3+ entries needed for trend classification. |
| `monthly_revenue` | `array` | Yes | Ordered list of monthly revenue totals in USD (numbers), matching length of `monthly_expenses`. |
| `current_cash` | `number` | Yes | Current total cash on hand in USD. Must be >= 0. |

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
    "monthly_expenses": [42000, 44500, 47000],
    "monthly_revenue": [15000, 18000, 21000],
    "current_cash": 380000
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "burn_rate_calculator"`.
