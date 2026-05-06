---
skill: options_greeks_calculator
category: market_analytics
description: Computes Black-Scholes option price and Greeks for calls and puts.
tier: free
inputs: stock_price, strike, time_to_expiry_years, risk_free_rate, volatility, option_type
---

# Options Greeks Calculator

## Description
Computes Black-Scholes option price and Greeks for calls and puts.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `stock_price` | `number` | Yes | Underlying price. |
| `strike` | `number` | Yes | Option strike. |
| `time_to_expiry_years` | `number` | Yes | Time to expiration in years. |
| `risk_free_rate` | `number` | Yes | Risk-free rate (decimal). |
| `volatility` | `number` | Yes | Implied volatility (decimal). |
| `option_type` | `string` | Yes | call or put. |

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
    "stock_price": 0,
    "strike": 0,
    "time_to_expiry_years": 0,
    "risk_free_rate": 0,
    "volatility": 0,
    "option_type": "<option_type>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "options_greeks_calculator"`.
