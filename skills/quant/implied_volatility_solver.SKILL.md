---
skill: implied_volatility_solver
category: quant
description: Computes implied volatility from an observed option price using bisection on the Black-Scholes model.
tier: free
inputs: option_price, spot, strike, time_to_expiry, risk_free_rate, option_type
---

# Implied Volatility Solver

## Description
Computes implied volatility from an observed option price using bisection on the Black-Scholes model.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `option_price` | `number` | Yes | Observed market option price. Must be > 0. |
| `spot` | `number` | Yes | Underlying spot price. Must be > 0. |
| `strike` | `number` | Yes | Option strike price. Must be > 0. |
| `time_to_expiry` | `number` | Yes | Time to expiry in years. Must be > 0. |
| `risk_free_rate` | `number` | Yes | Risk-free rate as a decimal (e.g. 0.05 for 5%). |
| `option_type` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "implied_volatility_solver",
  "arguments": {
    "option_price": 0,
    "spot": 0,
    "strike": 0,
    "time_to_expiry": 0,
    "risk_free_rate": 0,
    "option_type": "<option_type>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "implied_volatility_solver"`.
