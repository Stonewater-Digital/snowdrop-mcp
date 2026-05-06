---
skill: bond_duration_calculator
category: derivatives
description: Computes Macaulay duration, modified duration, and convexity for a coupon bond.
tier: free
inputs: face_value, coupon_rate_pct, years_to_maturity, yield_to_maturity_pct
---

# Bond Duration Calculator

## Description
Computes Macaulay duration, modified duration, and convexity for a coupon bond.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `face_value` | `number` | Yes | Par/face value of the bond. |
| `coupon_rate_pct` | `number` | Yes | Annual coupon rate as a percentage. |
| `years_to_maturity` | `number` | Yes | Years until bond matures (must be > 0). |
| `yield_to_maturity_pct` | `number` | Yes | Annual YTM as a percentage. |
| `payments_per_year` | `integer` | No | Coupon payment frequency (2 = semi-annual). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "bond_duration_calculator",
  "arguments": {
    "face_value": 0,
    "coupon_rate_pct": 0,
    "years_to_maturity": 0,
    "yield_to_maturity_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bond_duration_calculator"`.
