---
skill: volatility_etf_decay_tracker
category: derivatives_volatility
description: Tracks decay and rebalance drag in vol-linked ETFs.
tier: free
inputs: none
---

# Volatility Etf Decay Tracker

## Description
Tracks decay and rebalance drag in vol-linked ETFs.

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
  "tool": "volatility_etf_decay_tracker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "volatility_etf_decay_tracker"`.
