---
skill: federal_income_tax_estimator
category: personal_finance
description: Applies 2024 U.S. federal tax brackets to compute AGI, taxable income, tax liability, marginal rate, and bracket-level breakdown.
tier: free
inputs: filing_status, gross_income, above_line_deductions
---

# Federal Income Tax Estimator

## Description
Applies 2024 U.S. federal tax brackets to compute AGI, taxable income, tax liability, marginal rate, and bracket-level breakdown.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `filing_status` | `string` | Yes | single, mfj, mfs, or hoh. |
| `gross_income` | `number` | Yes | Total income prior to adjustments. |
| `above_line_deductions` | `number` | Yes | Adjustments to income (401k, HSA, etc.). |
| `itemized_deductions` | `number` | No | Optional itemized deductions; if omitted, standard is used. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "federal_income_tax_estimator",
  "arguments": {
    "filing_status": "<filing_status>",
    "gross_income": 0,
    "above_line_deductions": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "federal_income_tax_estimator"`.
