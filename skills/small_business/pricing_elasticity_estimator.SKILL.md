---
skill: pricing_elasticity_estimator
category: small_business
description: Uses observed price/volume pairs to estimate demand elasticity and recommends revenue/profit maximizing price points.
tier: free
inputs: current_price, current_volume, test_prices, test_volumes
---

# Pricing Elasticity Estimator

## Description
Uses observed price/volume pairs to estimate demand elasticity and recommends revenue/profit maximizing price points.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_price` | `number` | Yes | Existing list price. |
| `current_volume` | `number` | Yes | Units sold at the current price. |
| `test_prices` | `array` | Yes | List of tested prices. |
| `test_volumes` | `array` | Yes | List of observed volumes corresponding to test_prices. |
| `unit_cost` | `number` | No | Optional variable cost per unit for profit calculations. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "pricing_elasticity_estimator",
  "arguments": {
    "current_price": 0,
    "current_volume": 0,
    "test_prices": [],
    "test_volumes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pricing_elasticity_estimator"`.
