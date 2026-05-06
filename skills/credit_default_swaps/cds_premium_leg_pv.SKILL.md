---
skill: cds_premium_leg_pv
category: credit_default_swaps
description: Discounts CDS premium leg coupons to compute PV and annuity.
tier: free
inputs: notional, spread_bps, discount_factors
---

# Cds Premium Leg Pv

## Description
Discounts CDS premium leg coupons to compute PV and annuity.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `notional` | `number` | Yes |  |
| `spread_bps` | `number` | Yes |  |
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
  "tool": "cds_premium_leg_pv",
  "arguments": {
    "notional": 0,
    "spread_bps": 0,
    "discount_factors": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_premium_leg_pv"`.
