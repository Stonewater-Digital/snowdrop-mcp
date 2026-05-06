---
skill: tax_bracket_calculator
category: personal_finance
description: Calculate federal income tax owed using 2024 tax brackets. Shows marginal rate, effective rate, and tax owed per bracket.
tier: free
inputs: taxable_income
---

# Tax Bracket Calculator

## Description
Calculate federal income tax owed using 2024 tax brackets. Shows marginal rate, effective rate, and tax owed per bracket.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `taxable_income` | `number` | Yes | Taxable income (after deductions). |
| `filing_status` | `string` | No | Filing status. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tax_bracket_calculator",
  "arguments": {
    "taxable_income": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tax_bracket_calculator"`.
