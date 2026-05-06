---
skill: buyback_window_optimizer
category: event_driven_trades
description: Aligns blackout schedules with liquidity patterns to anticipate supportive repurchase flows.
tier: free
inputs: none
---

# Buyback Window Optimizer

## Description
Aligns blackout schedules with liquidity patterns to anticipate supportive repurchase flows.

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
  "tool": "buyback_window_optimizer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "buyback_window_optimizer"`.
