---
skill: exotic_barrier_option_pricer
category: derivatives
description: Provides approximate closed-form barrier option prices for single-barrier European options. Uses the Reiner-Rubinstein analytic formulas for standard barrier types.
tier: free
inputs: spot, strike, barrier, risk_free_rate_pct, volatility_pct, time_to_expiry_years, option_type, barrier_type
---

# Exotic Barrier Option Pricer

## Description
Provides approximate closed-form barrier option prices for single-barrier European options. Uses the Reiner-Rubinstein analytic formulas for standard barrier types.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spot` | `number` | Yes | Spot price. Must be > 0. |
| `strike` | `number` | Yes | Strike price. Must be > 0. |
| `barrier` | `number` | Yes | Barrier level. Must be > 0. |
| `risk_free_rate_pct` | `number` | Yes | Risk-free rate as a percentage. |
| `volatility_pct` | `number` | Yes | Volatility as a percentage. Must be > 0. |
| `time_to_expiry_years` | `number` | Yes | Time to expiry in years. Must be > 0. |
| `option_type` | `string` | Yes |  |
| `barrier_type` | `string` | Yes | Barrier type. In = knock-in; Out = knock-out. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "exotic_barrier_option_pricer",
  "arguments": {
    "spot": 0,
    "strike": 0,
    "barrier": 0,
    "risk_free_rate_pct": 0,
    "volatility_pct": 0,
    "time_to_expiry_years": 0,
    "option_type": "<option_type>",
    "barrier_type": "<barrier_type>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "exotic_barrier_option_pricer"`.
