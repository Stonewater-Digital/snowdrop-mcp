---
skill: dual_class_collapse_timer
category: event_driven_trades
description: Estimates when dual-class sunsets or pressure points could unlock governance catalysts.
tier: free
inputs: none
---

# Dual Class Collapse Timer

## Description
Estimates when dual-class sunsets or pressure points could unlock governance catalysts.

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
  "tool": "dual_class_collapse_timer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dual_class_collapse_timer"`.
