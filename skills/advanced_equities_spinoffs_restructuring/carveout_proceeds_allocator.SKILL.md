---
skill: carveout_proceeds_allocator
category: advanced_equities_spinoffs_restructuring
description: Simulates cash deployment from equity carveouts vs. balance-sheet needs.
tier: free
inputs: none
---

# Carveout Proceeds Allocator

## Description
Simulates cash deployment from equity carveouts vs. balance-sheet needs.

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
  "tool": "carveout_proceeds_allocator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "carveout_proceeds_allocator"`.
