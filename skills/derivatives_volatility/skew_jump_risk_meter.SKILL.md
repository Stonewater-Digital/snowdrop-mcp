---
skill: skew_jump_risk_meter
category: derivatives_volatility
description: Quantifies skew jump risk around catalysts using historical skew shocks.
tier: free
inputs: none
---

# Skew Jump Risk Meter

## Description
Quantifies skew jump risk around catalysts using historical skew shocks.

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
  "tool": "skew_jump_risk_meter",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "skew_jump_risk_meter"`.
