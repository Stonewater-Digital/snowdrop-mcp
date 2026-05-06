---
skill: vendor_channel_check_synthesizer
category: event_driven_trades
description: Aggregates public datapoints (earnings calls, supply chain indices) into actionable sales inflection alerts.
tier: free
inputs: none
---

# Vendor Channel Check Synthesizer

## Description
Aggregates public datapoints (earnings calls, supply chain indices) into actionable sales inflection alerts.

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
  "tool": "vendor_channel_check_synthesizer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vendor_channel_check_synthesizer"`.
