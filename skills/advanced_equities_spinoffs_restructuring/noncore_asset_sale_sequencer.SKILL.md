---
skill: noncore_asset_sale_sequencer
category: advanced_equities_spinoffs_restructuring
description: Orders asset dispositions to maximize deleveraging and valuation uplift.
tier: free
inputs: none
---

# Noncore Asset Sale Sequencer

## Description
Orders asset dispositions to maximize deleveraging and valuation uplift.

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
  "tool": "noncore_asset_sale_sequencer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "noncore_asset_sale_sequencer"`.
