---
skill: index_rebalance_flow_simulator
category: event_driven_trades
description: Models passive fund buying/selling pressure ahead of major index review announcements.
tier: free
inputs: none
---

# Index Rebalance Flow Simulator

## Description
Models passive fund buying/selling pressure ahead of major index review announcements.

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
  "tool": "index_rebalance_flow_simulator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "index_rebalance_flow_simulator"`.
