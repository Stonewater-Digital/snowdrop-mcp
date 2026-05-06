---
skill: futures_curve_analyzer
category: commodities
description: Classifies contango/backwardation, computes annualized roll yield per tenor, implied cost of carry, and carry trade signal from spot + futures curve.
tier: free
inputs: spot_price, futures
---

# Futures Curve Analyzer

## Description
Classifies contango/backwardation, computes annualized roll yield per tenor, implied cost of carry, and carry trade signal from spot + futures curve.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spot_price` | `number` | Yes | Current spot price of the commodity (must be > 0). |
| `futures` | `array` | Yes | List of futures contracts sorted or unsorted by expiry. |
| `storage_cost_pct_annual` | `['number', 'null']` | No | Annual storage cost as % of spot (optional, for cost-of-carry). |
| `convenience_yield_pct_annual` | `['number', 'null']` | No | Annual convenience yield as % (optional, for cost-of-carry). |
| `risk_free_rate_pct_annual` | `['number', 'null']` | No | Annual risk-free rate as % (optional, for theoretical forward). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "futures_curve_analyzer",
  "arguments": {
    "spot_price": 0,
    "futures": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "futures_curve_analyzer"`.
