---
skill: calendar_spread_decay_optimizer
category: derivatives_volatility
description: Optimizes calendar spreads by simulating theta bleed vs. vol drift.
tier: free
inputs: none
---

# Calendar Spread Decay Optimizer

## Description
Optimizes calendar spreads by simulating theta bleed vs. vol drift.

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
  "tool": "calendar_spread_decay_optimizer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "calendar_spread_decay_optimizer"`.
