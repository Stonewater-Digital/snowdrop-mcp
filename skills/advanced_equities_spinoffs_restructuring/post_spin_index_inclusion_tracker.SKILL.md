---
skill: post_spin_index_inclusion_tracker
category: advanced_equities_spinoffs_restructuring
description: Tracks index add/drop impacts following spin-effective dates.
tier: free
inputs: none
---

# Post Spin Index Inclusion Tracker

## Description
Tracks index add/drop impacts following spin-effective dates.

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
  "tool": "post_spin_index_inclusion_tracker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "post_spin_index_inclusion_tracker"`.
