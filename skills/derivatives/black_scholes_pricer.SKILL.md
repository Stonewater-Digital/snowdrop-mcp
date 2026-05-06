---
skill: black_scholes_pricer
category: derivatives
description: Calculates Black-Scholes option prices with full Greek outputs.
tier: free
inputs: spot_price, strike_price, time_to_expiry_years, risk_free_rate, volatility, option_type
---

# Black Scholes Pricer

## Description
Calculates Black-Scholes option prices with full Greek outputs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spot_price` | `number` | Yes |  |
| `strike_price` | `number` | Yes |  |
| `time_to_expiry_years` | `number` | Yes |  |
| `risk_free_rate` | `number` | Yes |  |
| `volatility` | `number` | Yes |  |
| `option_type` | `string` | Yes | Option flavor for payoff selection. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "black_scholes_pricer",
  "arguments": {
    "spot_price": 0,
    "strike_price": 0,
    "time_to_expiry_years": 0,
    "risk_free_rate": 0,
    "volatility": 0,
    "option_type": "<option_type>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "black_scholes_pricer"`.
