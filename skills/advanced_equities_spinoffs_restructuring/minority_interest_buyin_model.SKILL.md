---
skill: minority_interest_buyin_model
category: advanced_equities_spinoffs_restructuring
description: Values buy-in economics vs. minority protections and cash flow splits.
tier: free
inputs: none
---

# Minority Interest Buyin Model

## Description
Values buy-in economics vs. minority protections and cash flow splits.

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
  "tool": "minority_interest_buyin_model",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "minority_interest_buyin_model"`.
