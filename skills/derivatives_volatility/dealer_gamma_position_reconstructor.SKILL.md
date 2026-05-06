---
skill: dealer_gamma_position_reconstructor
category: derivatives_volatility
description: Infers dealer gamma balance using OI ladder and price levels.
tier: free
inputs: none
---

# Dealer Gamma Position Reconstructor

## Description
Infers dealer gamma balance using OI ladder and price levels.

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
  "tool": "dealer_gamma_position_reconstructor",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dealer_gamma_position_reconstructor"`.
