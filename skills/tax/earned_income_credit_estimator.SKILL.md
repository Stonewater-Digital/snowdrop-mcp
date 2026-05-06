---
skill: earned_income_credit_estimator
category: tax
description: Estimate the Earned Income Tax Credit (EITC) based on earned income, number of qualifying children, and filing status. Uses 2024 EIC parameters.
tier: free
inputs: earned_income
---

# Earned Income Credit Estimator

## Description
Estimate the Earned Income Tax Credit (EITC) based on earned income, number of qualifying children, and filing status. Uses 2024 EIC parameters.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `earned_income` | `number` | Yes | Total earned income (wages, salaries, self-employment) in USD. |
| `num_qualifying_children` | `integer` | No | Number of qualifying children (0-3+). |
| `filing_status` | `string` | No | Filing status. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "earned_income_credit_estimator",
  "arguments": {
    "earned_income": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "earned_income_credit_estimator"`.
