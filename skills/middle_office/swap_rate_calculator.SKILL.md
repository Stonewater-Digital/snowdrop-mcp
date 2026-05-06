---
skill: swap_rate_calculator
category: middle_office
description: Computes par swap rate, fixed leg PV, float leg PV, and NPV.
tier: free
inputs: notional, fixed_payment_dates, float_payment_dates, discount_factors
---

# Swap Rate Calculator

## Description
Computes par swap rate, fixed leg PV, float leg PV, and NPV.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `notional` | `number` | Yes |  |
| `fixed_payment_dates` | `array` | Yes |  |
| `float_payment_dates` | `array` | Yes |  |
| `discount_factors` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "swap_rate_calculator",
  "arguments": {
    "notional": 0,
    "fixed_payment_dates": [],
    "float_payment_dates": [],
    "discount_factors": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "swap_rate_calculator"`.
