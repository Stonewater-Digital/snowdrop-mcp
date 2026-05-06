---
skill: multi_leg_strategy_pnl_simulator
category: derivatives_volatility
description: Simulates P&L paths for iron condors, butterflies, and ratio spreads.
tier: free
inputs: none
---

# Multi Leg Strategy Pnl Simulator

## Description
Simulates P&L paths for iron condors, butterflies, and ratio spreads.

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
  "tool": "multi_leg_strategy_pnl_simulator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "multi_leg_strategy_pnl_simulator"`.
