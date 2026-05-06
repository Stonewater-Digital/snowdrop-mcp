---
skill: macro_data_surprise_linker
category: event_driven_trades
description: Connects company guidance sensitivity with upcoming macro releases to prime event trays.
tier: free
inputs: none
---

# Macro Data Surprise Linker

## Description
Connects company guidance sensitivity with upcoming macro releases to prime event trays.

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
  "tool": "macro_data_surprise_linker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "macro_data_surprise_linker"`.
