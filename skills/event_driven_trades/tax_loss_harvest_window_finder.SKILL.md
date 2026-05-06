---
skill: tax_loss_harvest_window_finder
category: event_driven_trades
description: Identifies crowded losers with elevated December bounce odds using seasonal factor models.
tier: free
inputs: none
---

# Tax Loss Harvest Window Finder

## Description
Identifies crowded losers with elevated December bounce odds using seasonal factor models.

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
  "tool": "tax_loss_harvest_window_finder",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tax_loss_harvest_window_finder"`.
