---
skill: supply_chain_disruption_signal_board
category: event_driven_trades
description: Uses shipping-data and supplier earnings to anticipate company-specific supply hits.
tier: free
inputs: none
---

# Supply Chain Disruption Signal Board

## Description
Uses shipping-data and supplier earnings to anticipate company-specific supply hits.

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
  "tool": "supply_chain_disruption_signal_board",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "supply_chain_disruption_signal_board"`.
