---
skill: litigation_docket_event_tracker
category: event_driven_trades
description: Monitors docket updates and court calendars to quantify lawsuit resolution catalysts.
tier: free
inputs: none
---

# Litigation Docket Event Tracker

## Description
Monitors docket updates and court calendars to quantify lawsuit resolution catalysts.

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
  "tool": "litigation_docket_event_tracker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "litigation_docket_event_tracker"`.
