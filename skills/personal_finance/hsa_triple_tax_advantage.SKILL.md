---
skill: hsa_triple_tax_advantage
category: personal_finance
description: Projects HSA balances using constant contributions and growth to highlight tax savings from deductions, tax-free compounding, and qualified medical withdrawals.
tier: free
inputs: annual_contribution, years_to_retirement, investment_return, tax_bracket, medical_expenses_in_retirement
---

# Hsa Triple Tax Advantage

## Description
Projects HSA balances using constant contributions and growth to highlight tax savings from deductions, tax-free compounding, and qualified medical withdrawals.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_contribution` | `number` | Yes | Dollars contributed to HSA each year, typically IRS maximum. |
| `years_to_retirement` | `number` | Yes | Years remaining until retirement when HSA funds are tapped. |
| `investment_return` | `number` | Yes | Expected annual investment return on HSA assets as decimal. |
| `tax_bracket` | `number` | Yes | Marginal tax rate applicable today and in retirement. |
| `medical_expenses_in_retirement` | `number` | Yes | Estimated qualified medical spend that can be reimbursed tax-free. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "hsa_triple_tax_advantage",
  "arguments": {
    "annual_contribution": 0,
    "years_to_retirement": 0,
    "investment_return": 0,
    "tax_bracket": 0,
    "medical_expenses_in_retirement": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "hsa_triple_tax_advantage"`.
