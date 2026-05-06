---
skill: options_greeks_calculator
category: middle_office
description: Returns price and Greeks for European options via Black-Scholes.
tier: free
inputs: spot, strike, rate, volatility, time_to_expiry, option_type
---

# Options Greeks Calculator

## Description
Returns price and Greeks for European options via Black-Scholes.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spot` | `number` | Yes |  |
| `strike` | `number` | Yes |  |
| `rate` | `number` | Yes |  |
| `volatility` | `number` | Yes |  |
| `time_to_expiry` | `number` | Yes |  |
| `option_type` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "options_greeks_calculator",
  "arguments": {
    "spot": 0,
    "strike": 0,
    "rate": 0,
    "volatility": 0,
    "time_to_expiry": 0,
    "option_type": "<option_type>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "options_greeks_calculator"`.
