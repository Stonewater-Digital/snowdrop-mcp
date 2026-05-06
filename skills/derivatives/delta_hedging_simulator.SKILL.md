---
skill: delta_hedging_simulator
category: derivatives
description: Simulates discrete delta hedging P&L decomposition over a price path.
tier: free
inputs: spot_prices, strike, risk_free_rate_pct, volatility_pct, time_to_expiry_start_years, option_type
---

# Delta Hedging Simulator

## Description
Simulates discrete delta hedging P&L decomposition over a price path.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spot_prices` | `array` | Yes | Time-ordered underlying price path (at least 2 values). |
| `strike` | `number` | Yes | Option strike price. Must be > 0. |
| `risk_free_rate_pct` | `number` | Yes | Risk-free rate as a percentage. |
| `volatility_pct` | `number` | Yes | Option vol as a percentage (must be > 0). |
| `time_to_expiry_start_years` | `number` | Yes | Time to expiry at the start of the path (must be > 0). |
| `option_type` | `string` | Yes |  |
| `notional` | `number` | No | Option notional multiplier. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "delta_hedging_simulator",
  "arguments": {
    "spot_prices": [],
    "strike": 0,
    "risk_free_rate_pct": 0,
    "volatility_pct": 0,
    "time_to_expiry_start_years": 0,
    "option_type": "<option_type>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "delta_hedging_simulator"`.
