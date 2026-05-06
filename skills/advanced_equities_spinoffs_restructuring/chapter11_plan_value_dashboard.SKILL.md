---
skill: chapter11_plan_value_dashboard
category: advanced_equities_spinoffs_restructuring
description: Compares plan recovery waterfalls against market pricing for multiple classes.
tier: free
inputs: none
---

# Chapter11 Plan Value Dashboard

## Description
Compares plan recovery waterfalls against market pricing for multiple classes.

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
  "tool": "chapter11_plan_value_dashboard",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "chapter11_plan_value_dashboard"`.
