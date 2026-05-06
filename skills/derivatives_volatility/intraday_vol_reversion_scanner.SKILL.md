---
skill: intraday_vol_reversion_scanner
category: derivatives_volatility
description: Detects intraday vol spikes likely to mean revert based on order book metrics.
tier: free
inputs: none
---

# Intraday Vol Reversion Scanner

## Description
Detects intraday vol spikes likely to mean revert based on order book metrics.

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
  "tool": "intraday_vol_reversion_scanner",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intraday_vol_reversion_scanner"`.
