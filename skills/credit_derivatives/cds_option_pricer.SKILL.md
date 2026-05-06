---
skill: cds_option_pricer
category: credit_derivatives
description: Applies the Black (1976) model with risky DV01 scaling to CDS swaptions for payer/receiver structures.
tier: free
inputs: forward_spread_bp, strike_bp, volatility, maturity_years, risk_free_rate, hazard_rate, notional, option_type
---

# Cds Option Pricer

## Description
Applies the Black (1976) model with risky DV01 scaling to CDS swaptions for payer/receiver structures.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `forward_spread_bp` | `number` | Yes | Forward CDS spread in basis points over the option expiry. |
| `strike_bp` | `number` | Yes | Strike spread in basis points. |
| `volatility` | `number` | Yes | Black implied volatility (decimal). |
| `maturity_years` | `number` | Yes | Option expiry in years. |
| `risk_free_rate` | `number` | Yes | Continuously compounded risk-free rate. |
| `hazard_rate` | `number` | Yes | Flat hazard rate used for risky DV01. |
| `notional` | `number` | Yes | Reference notional in currency units. |
| `option_type` | `string` | Yes | 'payer' for payer swaption (call on spread) or 'receiver' (put). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_option_pricer",
  "arguments": {
    "forward_spread_bp": 0,
    "strike_bp": 0,
    "volatility": 0,
    "maturity_years": 0,
    "risk_free_rate": 0,
    "hazard_rate": 0,
    "notional": 0,
    "option_type": "<option_type>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_option_pricer"`.
