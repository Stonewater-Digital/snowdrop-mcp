---
skill: options_volatility_smile_plotter
category: derivatives_volatility
description: Builds smile curves from free option chains and overlays realized anchors.
tier: free
inputs: none
---

# Options Volatility Smile Plotter

## Description
Builds smile curves from free option chains and overlays realized anchors.

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
  "tool": "options_volatility_smile_plotter",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "options_volatility_smile_plotter"`.
