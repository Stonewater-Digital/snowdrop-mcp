---
skill: variance_swap_mark_to_market_estimator
category: derivatives_volatility
description: Calculates MTM on listed variance swaps using free realized data.
tier: free
inputs: none
---

# Variance Swap Mark To Market Estimator

## Description
Calculates MTM on listed variance swaps using free realized data.

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
  "tool": "variance_swap_mark_to_market_estimator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "variance_swap_mark_to_market_estimator"`.
