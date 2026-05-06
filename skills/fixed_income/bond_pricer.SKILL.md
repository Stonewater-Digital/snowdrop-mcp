---
skill: bond_pricer
category: fixed_income
description: Computes clean/dirty price, duration, convexity, and current yield.
tier: free
inputs: face_value, coupon_rate, yield_to_maturity, years_to_maturity
---

# Bond Pricer

## Description
Computes clean/dirty price, duration, convexity, and current yield.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `face_value` | `number` | Yes |  |
| `coupon_rate` | `number` | Yes |  |
| `yield_to_maturity` | `number` | Yes |  |
| `years_to_maturity` | `integer` | Yes |  |
| `payments_per_year` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "bond_pricer",
  "arguments": {
    "face_value": 0,
    "coupon_rate": 0,
    "yield_to_maturity": 0,
    "years_to_maturity": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bond_pricer"`.
