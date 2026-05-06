---
skill: options_flow_clustering_model
category: derivatives_volatility
description: Clusters notable options prints to surface stealth positioning.
tier: free
inputs: none
---

# Options Flow Clustering Model

## Description
Clusters notable options prints to surface stealth positioning.

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
  "tool": "options_flow_clustering_model",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "options_flow_clustering_model"`.
