---
skill: backdoor_roth_calc
category: personal_finance
description: Applies the IRS pro-rata rule to a backdoor Roth IRA conversion and reports the taxable portion, estimated tax bill, and feasibility guidance.
tier: free
inputs: traditional_ira_balance, contribution_amount, tax_bracket, pro_rata_basis
---

# Backdoor Roth Calc

## Description
Applies the IRS pro-rata rule to a backdoor Roth IRA conversion and reports the taxable portion, estimated tax bill, and feasibility guidance.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `traditional_ira_balance` | `number` | Yes | Aggregate value of traditional IRAs on December 31. |
| `contribution_amount` | `number` | Yes | Nondeductible contribution slated for conversion. |
| `tax_bracket` | `number` | Yes | Marginal federal tax rate as decimal. |
| `pro_rata_basis` | `number` | Yes | After-tax basis already tracked on Form 8606. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "backdoor_roth_calc",
  "arguments": {
    "traditional_ira_balance": 0,
    "contribution_amount": 0,
    "tax_bracket": 0,
    "pro_rata_basis": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "backdoor_roth_calc"`.
