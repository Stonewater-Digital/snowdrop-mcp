---
skill: clinical_trial_binary_planner
category: event_driven_trades
description: Builds probability-weighted payoff trees for pivotal biotech readouts using open FDA calendars.
tier: free
inputs: none
---

# Clinical Trial Binary Planner

## Description
Builds probability-weighted payoff trees for pivotal biotech readouts using open FDA calendars.

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
  "tool": "clinical_trial_binary_planner",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "clinical_trial_binary_planner"`.
