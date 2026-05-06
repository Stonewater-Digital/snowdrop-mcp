---
skill: estimated_quarterly_tax
category: personal_finance
description: Combines income tax and self-employment tax to suggest quarterly estimated payments and safe harbor amounts to minimize penalties.
tier: free
inputs: annual_income, expected_withholding, filing_status, self_employment_income, deductions
---

# Estimated Quarterly Tax

## Description
Combines income tax and self-employment tax to suggest quarterly estimated payments and safe harbor amounts to minimize penalties.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_income` | `number` | Yes | Projected total income subject to federal tax. |
| `expected_withholding` | `number` | Yes | Taxes expected to be withheld from paychecks. |
| `filing_status` | `string` | Yes | single or mfj. |
| `self_employment_income` | `number` | Yes | Portion of income subject to self-employment tax. |
| `deductions` | `number` | Yes | Estimated deductions (standard + itemized) reducing taxable income. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "estimated_quarterly_tax",
  "arguments": {
    "annual_income": 0,
    "expected_withholding": 0,
    "filing_status": "<filing_status>",
    "self_employment_income": 0,
    "deductions": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "estimated_quarterly_tax"`.
