---
skill: fx_option_pricer
category: derivatives
description: Prices European FX options under Garman-Kohlhagen and returns Greeks.
tier: free
inputs: spot, strike, domestic_rate_pct, foreign_rate_pct, volatility_pct, time_to_expiry_years, option_type
---

# Fx Option Pricer

## Description
Prices European FX options under Garman-Kohlhagen and returns Greeks.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spot` | `number` | Yes | Spot FX rate (domestic per foreign). Must be > 0. |
| `strike` | `number` | Yes | Option strike rate. Must be > 0. |
| `domestic_rate_pct` | `number` | Yes | Domestic risk-free rate as a percentage. |
| `foreign_rate_pct` | `number` | Yes | Foreign risk-free (dividend) rate as a percentage. |
| `volatility_pct` | `number` | Yes | Annualised implied vol as a percentage. Must be > 0. |
| `time_to_expiry_years` | `number` | Yes | Time to expiry in years. Must be > 0. |
| `option_type` | `string` | Yes |  |
| `notional` | `number` | No | Notional (default 1.0). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fx_option_pricer",
  "arguments": {
    "spot": 0,
    "strike": 0,
    "domestic_rate_pct": 0,
    "foreign_rate_pct": 0,
    "volatility_pct": 0,
    "time_to_expiry_years": 0,
    "option_type": "<option_type>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fx_option_pricer"`.
