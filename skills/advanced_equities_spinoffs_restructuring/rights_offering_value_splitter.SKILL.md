---
skill: rights_offering_value_splitter
category: advanced_equities_spinoffs_restructuring
description: Values tradable rights vs. subscription commitments using historical take-up rates.
tier: free
inputs: none
---

# Rights Offering Value Splitter

## Description
Values tradable rights vs. subscription commitments using historical take-up rates.

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
  "tool": "rights_offering_value_splitter",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rights_offering_value_splitter"`.
