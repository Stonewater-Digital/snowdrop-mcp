---
skill: paycheck_withholding_estimator
category: personal_finance
description: Estimates paycheck taxes for federal, state, Social Security, and Medicare with net pay and annualized projections based on pay frequency.
tier: free
inputs: gross_pay, pay_frequency, filing_status, allowances, pre_tax_deductions, state
---

# Paycheck Withholding Estimator

## Description
Estimates paycheck taxes for federal, state, Social Security, and Medicare with net pay and annualized projections based on pay frequency.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gross_pay` | `number` | Yes | Gross wages per pay period before deductions. |
| `pay_frequency` | `string` | Yes | weekly, biweekly, semimonthly, monthly, or annual. |
| `filing_status` | `string` | Yes | single or mfj for withholding assumptions. |
| `allowances` | `number` | Yes | Number of withholding allowances, reduce taxable wages. |
| `pre_tax_deductions` | `object` | Yes | Dictionary of pre-tax deductions such as 401k, HSA. |
| `state` | `string` | Yes | Two-letter state code for state income tax estimate. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "paycheck_withholding_estimator",
  "arguments": {
    "gross_pay": 0,
    "pay_frequency": "<pay_frequency>",
    "filing_status": "<filing_status>",
    "allowances": 0,
    "pre_tax_deductions": {},
    "state": "<state>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "paycheck_withholding_estimator"`.
