---
skill: money_market_yield_calculator
category: banking
description: Calculate the money market yield (MMY) for a discount instrument. MMY = ((face - price) / price) * (360 / days_to_maturity).
tier: free
inputs: face_value, purchase_price, days_to_maturity
---

# Money Market Yield Calculator

## Description
Calculate the money market yield (MMY) for a discount instrument. MMY = ((face - price) / price) * (360 / days_to_maturity).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `face_value` | `number` | Yes | Face (par) value of the instrument. |
| `purchase_price` | `number` | Yes | Purchase price paid for the instrument. |
| `days_to_maturity` | `integer` | Yes | Number of days until maturity. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "money_market_yield_calculator",
  "arguments": {
    "face_value": 0,
    "purchase_price": 0,
    "days_to_maturity": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "money_market_yield_calculator"`.
