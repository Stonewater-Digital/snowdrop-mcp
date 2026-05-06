---
skill: swap_points_calculator
category: fx
description: Calculate FX swap points (forward points) from spot rate and interest rate differential. Swap points = forward - spot, expressed in pips.
tier: free
inputs: spot_rate, domestic_rate, foreign_rate
---

# Swap Points Calculator

## Description
Calculate FX swap points (forward points) from spot rate and interest rate differential. Swap points = forward - spot, expressed in pips.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spot_rate` | `number` | Yes | Current spot exchange rate. |
| `domestic_rate` | `number` | Yes | Domestic (quote currency) annualized interest rate as a decimal. |
| `foreign_rate` | `number` | Yes | Foreign (base currency) annualized interest rate as a decimal. |
| `days` | `integer` | No | Swap period in days. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "swap_points_calculator",
  "arguments": {
    "spot_rate": 0,
    "domestic_rate": 0,
    "foreign_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "swap_points_calculator"`.
