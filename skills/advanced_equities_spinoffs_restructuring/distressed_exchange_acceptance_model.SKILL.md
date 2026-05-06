---
skill: distressed_exchange_acceptance_model
category: advanced_equities_spinoffs_restructuring
description: Estimates acceptance probability for distressed exchanges across tranche holders.
tier: free
inputs: none
---

# Distressed Exchange Acceptance Model

## Description
Estimates acceptance probability for distressed exchanges across tranche holders.

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
  "tool": "distressed_exchange_acceptance_model",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "distressed_exchange_acceptance_model"`.
