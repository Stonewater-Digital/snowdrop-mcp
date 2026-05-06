---
skill: executive_transition_sentiment_monitor
category: event_driven_trades
description: Correlates C-suite turnover with subsequent stock performance and option flow clues.
tier: free
inputs: none
---

# Executive Transition Sentiment Monitor

## Description
Correlates C-suite turnover with subsequent stock performance and option flow clues.

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
  "tool": "executive_transition_sentiment_monitor",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "executive_transition_sentiment_monitor"`.
