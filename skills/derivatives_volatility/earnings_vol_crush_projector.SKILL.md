---
skill: earnings_vol_crush_projector
category: derivatives_volatility
description: Projects vol crush magnitude after earnings using historical analogs.
tier: free
inputs: none
---

# Earnings Vol Crush Projector

## Description
Projects vol crush magnitude after earnings using historical analogs.

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
  "tool": "earnings_vol_crush_projector",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "earnings_vol_crush_projector"`.
