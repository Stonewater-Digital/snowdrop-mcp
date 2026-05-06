---
skill: bond_yield_calculator
category: personal_finance
description: Provides quick estimates for a bond's current yield, yield to maturity, yield to call, and duration approximation from price and coupon inputs.
tier: free
inputs: face_value, coupon_rate, purchase_price, years_to_maturity
---

# Bond Yield Calculator

## Description
Provides quick estimates for a bond's current yield, yield to maturity, yield to call, and duration approximation from price and coupon inputs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `face_value` | `number` | Yes | Principal amount payable at maturity. |
| `coupon_rate` | `number` | Yes | Annual coupon rate as decimal. |
| `purchase_price` | `number` | Yes | Clean price paid for the bond. |
| `years_to_maturity` | `number` | Yes | Years remaining until maturity date. |
| `call_price` | `number` | No | Optional call price if the bond is callable. |
| `years_to_call` | `number` | No | Optional years until first call date. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "bond_yield_calculator",
  "arguments": {
    "face_value": 0,
    "coupon_rate": 0,
    "purchase_price": 0,
    "years_to_maturity": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bond_yield_calculator"`.
