---
skill: basis_risk_calculator
category: commodities
description: Quantifies commodity hedge basis risk. Computes hedged portfolio volatility, hedge effectiveness (R²), optimal hedge ratio (minimum-variance), and basis differential.
tier: free
inputs: spot_price, futures_price, asset_vol_pct
---

# Basis Risk Calculator

## Description
Quantifies commodity hedge basis risk. Computes hedged portfolio volatility, hedge effectiveness (R²), optimal hedge ratio (minimum-variance), and basis differential.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spot_price` | `number` | Yes | Current spot price of the asset being hedged (must be > 0). |
| `futures_price` | `number` | Yes | Current futures price used as the hedge instrument (must be > 0). |
| `asset_vol_pct` | `number` | Yes | Annualized volatility of the spot asset in % (must be > 0). |
| `futures_vol_pct` | `number` | No | Annualized volatility of the futures contract in % (must be > 0). If omitted, assumed equal to asset_vol_pct. |
| `hedge_ratio` | `number` | No | Hedge ratio h (futures position / spot position). Typically 0–1. |
| `correlation` | `number` | No | Correlation between spot and futures returns (−1 to 1). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "basis_risk_calculator",
  "arguments": {
    "spot_price": 0,
    "futures_price": 0,
    "asset_vol_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "basis_risk_calculator"`.
