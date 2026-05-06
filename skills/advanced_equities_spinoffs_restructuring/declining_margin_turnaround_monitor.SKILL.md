---
skill: declining_margin_turnaround_monitor
category: advanced_equities_spinoffs_restructuring
description: Scores restructurings on margin recovery speed relative to guidance.
tier: free
inputs: none
---

# Declining Margin Turnaround Monitor

## Description
Scores restructurings on margin recovery speed relative to guidance.

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
  "tool": "declining_margin_turnaround_monitor",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "declining_margin_turnaround_monitor"`.
