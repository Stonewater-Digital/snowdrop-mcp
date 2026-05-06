---
skill: theta_decay_heatmap_builder
category: derivatives_volatility
description: Visualizes theta decay pockets across expiries and strikes.
tier: free
inputs: none
---

# Theta Decay Heatmap Builder

## Description
Visualizes theta decay pockets across expiries and strikes.

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
  "tool": "theta_decay_heatmap_builder",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "theta_decay_heatmap_builder"`.
