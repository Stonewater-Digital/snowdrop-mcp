---
skill: volatility_risk_premium_surface_plotter
category: derivatives_volatility
description: Maps VRP across tenors and strikes for strategy selection.
tier: free
inputs: none
---

# Volatility Risk Premium Surface Plotter

## Description
Maps VRP across tenors and strikes for strategy selection.

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
  "tool": "volatility_risk_premium_surface_plotter",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "volatility_risk_premium_surface_plotter"`.
