---
skill: activist_campaign_scorecard
category: event_driven_trades
description: Scores activist campaigns using filing cadence, proposal quality, and precedent outcomes to frame trade bias.
tier: free
inputs: none
---

# Activist Campaign Scorecard

## Description
Scores activist campaigns using filing cadence, proposal quality, and precedent outcomes to frame trade bias.

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
  "tool": "activist_campaign_scorecard",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "activist_campaign_scorecard"`.
