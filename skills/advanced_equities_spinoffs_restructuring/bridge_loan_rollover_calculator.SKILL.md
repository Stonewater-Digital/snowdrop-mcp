---
skill: bridge_loan_rollover_calculator
category: advanced_equities_spinoffs_restructuring
description: Models bridge maturity walls and rollover probability.
tier: free
inputs: none
---

# Bridge Loan Rollover Calculator

## Description
Models bridge maturity walls and rollover probability.

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
  "tool": "bridge_loan_rollover_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bridge_loan_rollover_calculator"`.
