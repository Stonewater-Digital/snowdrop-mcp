---
skill: forward_vol_calendar_curve_builder
category: derivatives_volatility
description: Builds forward vol curves from listed options to spot anomalies.
tier: free
inputs: none
---

# Forward Vol Calendar Curve Builder

## Description
Builds forward vol curves from listed options to spot anomalies.

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
  "tool": "forward_vol_calendar_curve_builder",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "forward_vol_calendar_curve_builder"`.
