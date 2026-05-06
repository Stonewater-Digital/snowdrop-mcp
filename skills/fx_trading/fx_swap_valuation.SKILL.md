---
skill: fx_swap_valuation
category: fx_trading
description: Values currency basis swaps using discounted cash flows.
tier: free
inputs: notional_domestic, notional_foreign, domestic_fixed_rate, foreign_fixed_rate, spot_at_inception, current_spot, remaining_years, domestic_discount_rate, foreign_discount_rate
---

# Fx Swap Valuation

## Description
Values currency basis swaps using discounted cash flows.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `notional_domestic` | `number` | Yes |  |
| `notional_foreign` | `number` | Yes |  |
| `domestic_fixed_rate` | `number` | Yes |  |
| `foreign_fixed_rate` | `number` | Yes |  |
| `spot_at_inception` | `number` | Yes |  |
| `current_spot` | `number` | Yes |  |
| `remaining_years` | `number` | Yes |  |
| `domestic_discount_rate` | `number` | Yes |  |
| `foreign_discount_rate` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fx_swap_valuation",
  "arguments": {
    "notional_domestic": 0,
    "notional_foreign": 0,
    "domestic_fixed_rate": 0,
    "foreign_fixed_rate": 0,
    "spot_at_inception": 0,
    "current_spot": 0,
    "remaining_years": 0,
    "domestic_discount_rate": 0,
    "foreign_discount_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fx_swap_valuation"`.
