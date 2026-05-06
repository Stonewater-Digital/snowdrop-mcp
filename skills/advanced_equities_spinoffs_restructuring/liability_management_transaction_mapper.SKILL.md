---
skill: liability_management_transaction_mapper
category: advanced_equities_spinoffs_restructuring
description: Maps tender/exchange sequences to assess residual capital structure risk.
tier: free
inputs: none
---

# Liability Management Transaction Mapper

## Description
Maps tender/exchange sequences to assess residual capital structure risk.

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
  "tool": "liability_management_transaction_mapper",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "liability_management_transaction_mapper"`.
