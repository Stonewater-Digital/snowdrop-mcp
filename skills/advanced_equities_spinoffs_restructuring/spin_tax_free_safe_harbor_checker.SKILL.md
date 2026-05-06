---
skill: spin_tax_free_safe_harbor_checker
category: advanced_equities_spinoffs_restructuring
description: Tests transactions against IRS safe harbor requirements for tax-free status.
tier: free
inputs: none
---

# Spin Tax Free Safe Harbor Checker

## Description
Tests transactions against IRS safe harbor requirements for tax-free status.

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
  "tool": "spin_tax_free_safe_harbor_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "spin_tax_free_safe_harbor_checker"`.
