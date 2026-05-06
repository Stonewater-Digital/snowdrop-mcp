---
skill: spinoff_sum_of_the_parts_modeler
category: advanced_equities_spinoffs_restructuring
description: Aggregates segment data into SOP valuations to benchmark spin stub pricing.
tier: free
inputs: none
---

# Spinoff Sum Of The Parts Modeler

## Description
Aggregates segment data into SOP valuations to benchmark spin stub pricing.

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
  "tool": "spinoff_sum_of_the_parts_modeler",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "spinoff_sum_of_the_parts_modeler"`.
