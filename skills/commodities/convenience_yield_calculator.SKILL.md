---
skill: convenience_yield_calculator
category: commodities
description: Solves for implied convenience yield using the continuous cost-of-carry relation: F = S * exp((r + u - y) * T), rearranged as y = r + u - ln(F/S) / T.
tier: free
inputs: spot_price, futures_price, risk_free_rate_pct, time_to_maturity_years
---

# Convenience Yield Calculator

## Description
Solves for implied convenience yield using the continuous cost-of-carry relation: F = S * exp((r + u - y) * T), rearranged as y = r + u - ln(F/S) / T.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spot_price` | `number` | Yes | Current spot price of the commodity (must be > 0). |
| `futures_price` | `number` | Yes | Futures price for the given maturity (must be > 0). |
| `risk_free_rate_pct` | `number` | Yes | Annual continuous risk-free rate as % (e.g. 5.0 = 5%). |
| `storage_cost_pct` | `number` | No | Annual storage cost as % of spot (e.g. 2.0 = 2%). Defaults to 0. |
| `time_to_maturity_years` | `number` | Yes | Time to futures maturity in years (must be > 0). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "convenience_yield_calculator",
  "arguments": {
    "spot_price": 0,
    "futures_price": 0,
    "risk_free_rate_pct": 0,
    "time_to_maturity_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "convenience_yield_calculator"`.
