---
skill: section382_cap_table_guard
category: advanced_equities_spinoffs_restructuring
description: Simulates ownership shifts to protect Section 382 limits.
tier: free
inputs: none
---

# Section382 Cap Table Guard

## Description
Simulates ownership shifts to protect Section 382 limits.

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
  "tool": "section382_cap_table_guard",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "section382_cap_table_guard"`.
