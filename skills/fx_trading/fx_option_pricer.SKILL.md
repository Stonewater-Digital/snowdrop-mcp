---
skill: fx_option_pricer
category: fx_trading
description: Calculates FX option premiums and Greeks via Garman-Kohlhagen model.
tier: free
inputs: spot_rate, strike, domestic_rate, foreign_rate, volatility, time_to_expiry_years, option_type, notional
---

# Fx Option Pricer

## Description
Calculates FX option premiums and Greeks via Garman-Kohlhagen model.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spot_rate` | `number` | Yes |  |
| `strike` | `number` | Yes |  |
| `domestic_rate` | `number` | Yes |  |
| `foreign_rate` | `number` | Yes |  |
| `volatility` | `number` | Yes |  |
| `time_to_expiry_years` | `number` | Yes |  |
| `option_type` | `string` | Yes |  |
| `notional` | `number` | Yes |  |

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
    "spot_rate": 0,
    "strike": 0,
    "domestic_rate": 0,
    "foreign_rate": 0,
    "volatility": 0,
    "time_to_expiry_years": 0,
    "option_type": "<option_type>",
    "notional": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fx_option_pricer"`.
