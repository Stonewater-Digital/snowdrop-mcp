---
skill: cross_border_event_heat_gauge
category: event_driven_trades
description: Flags jurisdictions with rising policy risks affecting pending company-level events.
tier: free
inputs: none
---

# Cross Border Event Heat Gauge

## Description
Flags jurisdictions with rising policy risks affecting pending company-level events.

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
  "tool": "cross_border_event_heat_gauge",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cross_border_event_heat_gauge"`.
