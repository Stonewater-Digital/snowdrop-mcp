---
skill: liquidity_sweep_impact_estimator
category: derivatives_volatility
description: Estimates market impact from large option sweeps to manage slippage.
tier: free
inputs: none
---

# Liquidity Sweep Impact Estimator

## Description
Estimates market impact from large option sweeps to manage slippage.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tickers` | `array` | No | Tickers or identifiers relevant to the analysis focus. |
| `lookback_days` | `integer` | No | Historical window (days) for synthetic / free-data calculations. |
| `analysis_notes` | `string` | No | Optional qualitative context to embed in the response. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "liquidity_sweep_impact_estimator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "liquidity_sweep_impact_estimator"`.
