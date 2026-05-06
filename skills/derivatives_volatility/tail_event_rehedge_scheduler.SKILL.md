---
skill: tail_event_rehedge_scheduler
category: derivatives_volatility
description: Automates re-hedge reminders when vol regime shifts breach thresholds.
tier: free
inputs: none
---

# Tail Event Rehedge Scheduler

## Description
Automates re-hedge reminders when vol regime shifts breach thresholds.

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
  "tool": "tail_event_rehedge_scheduler",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tail_event_rehedge_scheduler"`.
