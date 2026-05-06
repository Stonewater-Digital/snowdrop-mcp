---
skill: asset_light_transition_scorecard
category: advanced_equities_spinoffs_restructuring
description: Scores restructurings shifting to asset-light models based on margin potential.
tier: free
inputs: none
---

# Asset Light Transition Scorecard

## Description
Scores restructurings shifting to asset-light models based on margin potential.

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
  "tool": "asset_light_transition_scorecard",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "asset_light_transition_scorecard"`.
