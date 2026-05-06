---
skill: deleveraging_path_visualizer
category: advanced_equities_spinoffs_restructuring
description: Charts leverage trajectories under various asset sale and EBITDA scenarios.
tier: free
inputs: none
---

# Deleveraging Path Visualizer

## Description
Charts leverage trajectories under various asset sale and EBITDA scenarios.

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
  "tool": "deleveraging_path_visualizer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "deleveraging_path_visualizer"`.
