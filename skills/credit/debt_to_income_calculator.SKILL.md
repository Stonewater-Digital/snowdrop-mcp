---
skill: debt_to_income_calculator
category: credit
description: Calculate debt-to-income ratio. Classifies front-end and back-end DTI and provides lender risk assessment.
tier: free
inputs: monthly_debt_payments, gross_monthly_income
---

# Debt To Income Calculator

## Description
Calculate debt-to-income ratio. Classifies front-end and back-end DTI and provides lender risk assessment.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `monthly_debt_payments` | `number` | Yes | Total monthly debt payments (all obligations). |
| `gross_monthly_income` | `number` | Yes | Gross (pre-tax) monthly income. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "debt_to_income_calculator",
  "arguments": {
    "monthly_debt_payments": 0,
    "gross_monthly_income": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "debt_to_income_calculator"`.
