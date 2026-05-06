---
skill: cds_breakeven_spread
category: credit_default_swaps
description: Calculates running spread that equates premium and protection PVs.
tier: free
inputs: notional, protection_leg_pv, discount_factors
---

# Cds Breakeven Spread

## Description
Calculates running spread that equates premium and protection PVs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `notional` | `number` | Yes |  |
| `protection_leg_pv` | `number` | Yes |  |
| `discount_factors` | `array` | Yes |  |
| `payment_interval_years` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_breakeven_spread",
  "arguments": {
    "notional": 0,
    "protection_leg_pv": 0,
    "discount_factors": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_breakeven_spread"`.
