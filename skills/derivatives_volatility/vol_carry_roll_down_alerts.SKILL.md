---
skill: vol_carry_roll_down_alerts
category: derivatives_volatility
description: Alerts when rolling long-vol positions offers attractive carry improvements.
tier: free
inputs: none
---

# Vol Carry Roll Down Alerts

## Description
Alerts when rolling long-vol positions offers attractive carry improvements.

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
  "tool": "vol_carry_roll_down_alerts",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vol_carry_roll_down_alerts"`.
