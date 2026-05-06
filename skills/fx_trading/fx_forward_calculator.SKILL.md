---
skill: fx_forward_calculator
category: fx_trading
description: Calculates forward rates, points, and hedging costs for currency hedges.
tier: free
inputs: spot_rate, domestic_rate, foreign_rate, tenor_days, notional_base
---

# Fx Forward Calculator

## Description
Calculates forward rates, points, and hedging costs for currency hedges.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spot_rate` | `number` | Yes |  |
| `domestic_rate` | `number` | Yes |  |
| `foreign_rate` | `number` | Yes |  |
| `tenor_days` | `integer` | Yes |  |
| `notional_base` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fx_forward_calculator",
  "arguments": {
    "spot_rate": 0,
    "domestic_rate": 0,
    "foreign_rate": 0,
    "tenor_days": 0,
    "notional_base": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fx_forward_calculator"`.
