---
skill: gamma_squeeze_exposure_tracker
category: derivatives_volatility
description: Reconstructs dealer gamma exposure using OI, delta, and borrow metrics.
tier: free
inputs: none
---

# Gamma Squeeze Exposure Tracker

## Description
Reconstructs dealer gamma exposure using OI, delta, and borrow metrics.

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
  "tool": "gamma_squeeze_exposure_tracker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gamma_squeeze_exposure_tracker"`.
