---
skill: estimated_tax_payment_calculator
category: tax
description: Calculate quarterly estimated tax payments including safe harbor rules (100%/110% of prior year tax) to avoid underpayment penalties.
tier: free
inputs: expected_annual_income, expected_withholding, prior_year_tax
---

# Estimated Tax Payment Calculator

## Description
Calculate quarterly estimated tax payments including safe harbor rules (100%/110% of prior year tax) to avoid underpayment penalties.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `expected_annual_income` | `number` | Yes | Expected total annual income in USD. |
| `expected_withholding` | `number` | Yes | Total expected tax withholding for the year (from W-2 jobs, etc.) in USD. |
| `prior_year_tax` | `number` | Yes | Total tax liability from the prior year in USD. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "estimated_tax_payment_calculator",
  "arguments": {
    "expected_annual_income": 0,
    "expected_withholding": 0,
    "prior_year_tax": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "estimated_tax_payment_calculator"`.
