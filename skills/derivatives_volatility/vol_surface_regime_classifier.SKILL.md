---
skill: vol_surface_regime_classifier
category: derivatives_volatility
description: Labels vol regimes (contango/backwardation) and ties them to macro states.
tier: free
inputs: none
---

# Vol Surface Regime Classifier

## Description
Labels vol regimes (contango/backwardation) and ties them to macro states.

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
  "tool": "vol_surface_regime_classifier",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vol_surface_regime_classifier"`.
