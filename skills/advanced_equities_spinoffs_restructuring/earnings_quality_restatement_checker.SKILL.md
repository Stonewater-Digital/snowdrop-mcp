---
skill: earnings_quality_restatement_checker
category: advanced_equities_spinoffs_restructuring
description: Flags restatement risk from irregular accruals and audit comments.
tier: free
inputs: none
---

# Earnings Quality Restatement Checker

## Description
Flags restatement risk from irregular accruals and audit comments.

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
  "tool": "earnings_quality_restatement_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "earnings_quality_restatement_checker"`.
