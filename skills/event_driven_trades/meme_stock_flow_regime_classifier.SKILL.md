---
skill: meme_stock_flow_regime_classifier
category: event_driven_trades
description: Detects social-volume and borrow-cost trigger points that precede melt-up or crash phases.
tier: free
inputs: none
---

# Meme Stock Flow Regime Classifier

## Description
Detects social-volume and borrow-cost trigger points that precede melt-up or crash phases.

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
  "tool": "meme_stock_flow_regime_classifier",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "meme_stock_flow_regime_classifier"`.
