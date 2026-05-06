---
skill: estimated_tax_calculator
category: tax
description: Applies 90%/100% safe harbor logic to estimate quarterly payments and due dates.
tier: free
inputs: ytd_income, ytd_withholding, prior_year_tax, filing_status
---

# Estimated Tax Calculator

## Description
Applies 90%/100% safe harbor logic to estimate quarterly payments and due dates.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ytd_income` | `number` | Yes |  |
| `ytd_withholding` | `number` | Yes |  |
| `prior_year_tax` | `number` | Yes |  |
| `filing_status` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "estimated_tax_calculator",
  "arguments": {
    "ytd_income": 0,
    "ytd_withholding": 0,
    "prior_year_tax": 0,
    "filing_status": "<filing_status>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "estimated_tax_calculator"`.
