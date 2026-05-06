---
skill: student_loan_repayment_comparator
category: personal_finance
description: Models standard, graduated, IBR, PAYE, and REPAYE student loan plans to expose monthly payments, total paid, and potential forgiveness along with a recommendation.
tier: free
inputs: loan_balance, interest_rate, annual_income, income_growth_rate, filing_status, family_size
---

# Student Loan Repayment Comparator

## Description
Models standard, graduated, IBR, PAYE, and REPAYE student loan plans to expose monthly payments, total paid, and potential forgiveness along with a recommendation.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `loan_balance` | `number` | Yes | Total outstanding federal student loan balance. |
| `interest_rate` | `number` | Yes | Annual loan interest rate as decimal. |
| `annual_income` | `number` | Yes | Current adjusted gross income for payment calculations. |
| `income_growth_rate` | `number` | Yes | Expected annual income growth as decimal. |
| `filing_status` | `string` | Yes | single or mfj to estimate discretionary income. |
| `family_size` | `number` | Yes | Household size used for poverty guideline. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "student_loan_repayment_comparator",
  "arguments": {
    "loan_balance": 0,
    "interest_rate": 0,
    "annual_income": 0,
    "income_growth_rate": 0,
    "filing_status": "<filing_status>",
    "family_size": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "student_loan_repayment_comparator"`.
