---
skill: equity_cure_need_forecaster
category: advanced_equities_spinoffs_restructuring
description: Projects covenant breaches and equity cure sizing windows.
tier: free
inputs: none
---

# Equity Cure Need Forecaster

## Description
Projects covenant breaches and equity cure sizing windows.

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
  "tool": "equity_cure_need_forecaster",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "equity_cure_need_forecaster"`.
