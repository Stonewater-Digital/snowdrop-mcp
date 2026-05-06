---
skill: short_interest_crunch_indicator
category: event_driven_trades
description: Combines short interest days-to-cover with catalyst calendar to time squeezes.
tier: free
inputs: none
---

# Short Interest Crunch Indicator

## Description
Combines short interest days-to-cover with catalyst calendar to time squeezes.

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
  "tool": "short_interest_crunch_indicator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "short_interest_crunch_indicator"`.
