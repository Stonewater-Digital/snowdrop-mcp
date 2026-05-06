---
skill: product_launch_trade_setup
category: event_driven_trades
description: Compares historical launch announcements to realized demand signals to gauge trade direction.
tier: free
inputs: none
---

# Product Launch Trade Setup

## Description
Compares historical launch announcements to realized demand signals to gauge trade direction.

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
  "tool": "product_launch_trade_setup",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "product_launch_trade_setup"`.
