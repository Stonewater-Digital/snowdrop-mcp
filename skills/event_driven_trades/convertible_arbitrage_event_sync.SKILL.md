---
skill: convertible_arbitrage_event_sync
category: event_driven_trades
description: Aligns convertible hedge unwinds with catalysts to trade equity lag/lead.
tier: free
inputs: none
---

# Convertible Arbitrage Event Sync

## Description
Aligns convertible hedge unwinds with catalysts to trade equity lag/lead.

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
  "tool": "convertible_arbitrage_event_sync",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "convertible_arbitrage_event_sync"`.
