---
skill: student_loan_payoff_calculator
category: personal_finance
description: Calculate student loan payoff timeline, total interest paid, and show accelerated payment scenarios.
tier: free
inputs: balance, interest_rate, monthly_payment
---

# Student Loan Payoff Calculator

## Description
Calculate student loan payoff timeline, total interest paid, and show accelerated payment scenarios.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `balance` | `number` | Yes | Current loan balance. |
| `interest_rate` | `number` | Yes | Annual interest rate as percentage (e.g., 5.5 for 5.5%). |
| `monthly_payment` | `number` | Yes | Monthly payment amount. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "student_loan_payoff_calculator",
  "arguments": {
    "balance": 0,
    "interest_rate": 0,
    "monthly_payment": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "student_loan_payoff_calculator"`.
