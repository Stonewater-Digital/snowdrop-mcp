---
skill: options_liquidity_pullback_detector
category: derivatives_volatility
description: Detects widening bid-ask spreads and volume drops signaling liquidity stress.
tier: free
inputs: none
---

# Options Liquidity Pullback Detector

## Description
Detects widening bid-ask spreads and volume drops signaling liquidity stress.

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
  "tool": "options_liquidity_pullback_detector",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "options_liquidity_pullback_detector"`.
