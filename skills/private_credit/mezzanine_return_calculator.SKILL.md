---
skill: mezzanine_return_calculator
category: private_credit
description: Calculates blended cash, PIK, and equity kicker returns for mezzanine debt.
tier: free
inputs: principal, cash_coupon_pct, pik_coupon_pct, term_years, equity_kicker_pct, equity_value_at_exit
---

# Mezzanine Return Calculator

## Description
Calculates blended cash, PIK, and equity kicker returns for mezzanine debt.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `principal` | `number` | Yes |  |
| `cash_coupon_pct` | `number` | Yes |  |
| `pik_coupon_pct` | `number` | Yes |  |
| `term_years` | `number` | Yes |  |
| `equity_kicker_pct` | `number` | Yes |  |
| `equity_value_at_exit` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mezzanine_return_calculator",
  "arguments": {
    "principal": 0,
    "cash_coupon_pct": 0,
    "pik_coupon_pct": 0,
    "term_years": 0,
    "equity_kicker_pct": 0,
    "equity_value_at_exit": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mezzanine_return_calculator"`.
