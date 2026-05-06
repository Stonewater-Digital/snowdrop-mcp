---
skill: credit_vix_calculator
category: credit_derivatives
description: Uses the VIX variance replication formula on CDS option strips to infer an implied volatility index for credit spreads.
tier: free
inputs: strikes_bp, option_prices_bp, forward_spread_bp, maturity_years
---

# Credit Vix Calculator

## Description
Uses the VIX variance replication formula on CDS option strips to infer an implied volatility index for credit spreads.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `strikes_bp` | `array` | Yes | Ordered strike spreads in basis points. |
| `option_prices_bp` | `array` | Yes | Out-of-the-money option mid prices in basis points of spread PV. |
| `forward_spread_bp` | `number` | Yes | Forward CDS spread in basis points corresponding to the strip. |
| `maturity_years` | `number` | Yes | Time to option expiry in years. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_vix_calculator",
  "arguments": {
    "strikes_bp": [],
    "option_prices_bp": [],
    "forward_spread_bp": 0,
    "maturity_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_vix_calculator"`.
