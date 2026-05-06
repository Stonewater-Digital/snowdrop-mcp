---
skill: earnings_whisper_spread_analyzer
category: event_driven_trades
description: Measures gap between whisper numbers and official consensus to weight surprise odds.
tier: free
inputs: none
---

# Earnings Whisper Spread Analyzer

## Description
Measures gap between whisper numbers and official consensus to weight surprise odds.

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
  "tool": "earnings_whisper_spread_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "earnings_whisper_spread_analyzer"`.
