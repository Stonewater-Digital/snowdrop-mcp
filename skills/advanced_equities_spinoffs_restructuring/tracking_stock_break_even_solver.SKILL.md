---
skill: tracking_stock_break_even_solver
category: advanced_equities_spinoffs_restructuring
description: Computes break-even for tracking stock conversions and rollups.
tier: free
inputs: none
---

# Tracking Stock Break Even Solver

## Description
Computes break-even for tracking stock conversions and rollups.

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
  "tool": "tracking_stock_break_even_solver",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tracking_stock_break_even_solver"`.
