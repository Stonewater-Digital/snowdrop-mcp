---
skill: unitranche_yield_calculator
category: private_credit
description: Calculates unitranche cash yield plus amortized OID and fees.
tier: free
inputs: coupon_pct, oid_pct, origination_fee_pct, tenor_years
---

# Unitranche Yield Calculator

## Description
Calculates unitranche cash yield plus amortized OID and fees.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `coupon_pct` | `number` | Yes |  |
| `oid_pct` | `number` | Yes |  |
| `origination_fee_pct` | `number` | Yes |  |
| `tenor_years` | `number` | Yes |  |
| `payment_frequency` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "unitranche_yield_calculator",
  "arguments": {
    "coupon_pct": 0,
    "oid_pct": 0,
    "origination_fee_pct": 0,
    "tenor_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "unitranche_yield_calculator"`.
