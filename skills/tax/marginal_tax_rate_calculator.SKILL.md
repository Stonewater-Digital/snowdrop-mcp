---
skill: marginal_tax_rate_calculator
category: tax
description: Calculate marginal federal tax rate and bracket breakdown for 2024 US tax brackets given taxable income and filing status.
tier: free
inputs: taxable_income
---

# Marginal Tax Rate Calculator

## Description
Calculate marginal federal tax rate and bracket breakdown for 2024 US tax brackets given taxable income and filing status.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `taxable_income` | `number` | Yes | Total taxable income in USD. |
| `filing_status` | `string` | No | Filing status: single, married_filing_jointly, married_filing_separately, or head_of_household. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "marginal_tax_rate_calculator",
  "arguments": {
    "taxable_income": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "marginal_tax_rate_calculator"`.
