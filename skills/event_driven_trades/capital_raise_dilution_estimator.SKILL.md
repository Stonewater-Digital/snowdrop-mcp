---
skill: capital_raise_dilution_estimator
category: event_driven_trades
description: Simulates rights, PIPE, and follow-on dilution paths to measure near-term overhangs.
tier: free
inputs: none
---

# Capital Raise Dilution Estimator

## Description
Simulates rights, PIPE, and follow-on dilution paths to measure near-term overhangs.

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
  "tool": "capital_raise_dilution_estimator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "capital_raise_dilution_estimator"`.
