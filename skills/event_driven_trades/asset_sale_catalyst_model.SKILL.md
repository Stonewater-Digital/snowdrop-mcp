---
skill: asset_sale_catalyst_model
category: event_driven_trades
description: Assesses probability-weighted asset sale proceeds versus enterprise value gap.
tier: free
inputs: none
---

# Asset Sale Catalyst Model

## Description
Assesses probability-weighted asset sale proceeds versus enterprise value gap.

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
  "tool": "asset_sale_catalyst_model",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "asset_sale_catalyst_model"`.
