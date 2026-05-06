---
skill: employee_option_overhang_quantifier
category: advanced_equities_spinoffs_restructuring
description: Measures equity overhang vs. expected dilution through restructuring.
tier: free
inputs: none
---

# Employee Option Overhang Quantifier

## Description
Measures equity overhang vs. expected dilution through restructuring.

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
  "tool": "employee_option_overhang_quantifier",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "employee_option_overhang_quantifier"`.
