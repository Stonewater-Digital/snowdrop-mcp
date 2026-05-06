---
skill: bankruptcy_exit_watchlist
category: event_driven_trades
description: Tracks Chapter 11 emergence timelines, valuation metrics, and tradeable post-reorg equities.
tier: free
inputs: none
---

# Bankruptcy Exit Watchlist

## Description
Tracks Chapter 11 emergence timelines, valuation metrics, and tradeable post-reorg equities.

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
  "tool": "bankruptcy_exit_watchlist",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bankruptcy_exit_watchlist"`.
