---
skill: share_lockup_expiry_pressure_meter
category: event_driven_trades
description: Quantifies lockup expirations' float impact and price response odds.
tier: free
inputs: none
---

# Share Lockup Expiry Pressure Meter

## Description
Quantifies lockup expirations' float impact and price response odds.

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
  "tool": "share_lockup_expiry_pressure_meter",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "share_lockup_expiry_pressure_meter"`.
