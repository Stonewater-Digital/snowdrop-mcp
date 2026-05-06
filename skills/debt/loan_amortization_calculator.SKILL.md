---
skill: loan_amortization_calculator
category: debt
description: Computes monthly payment, amortization schedule, and payoff projections.
tier: free
inputs: principal, annual_rate, term_months
---

# Loan Amortization Calculator

## Description
Computes monthly payment, amortization schedule, and payoff projections.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `principal` | `number` | Yes |  |
| `annual_rate` | `number` | Yes |  |
| `term_months` | `integer` | Yes |  |
| `extra_monthly_payment` | `number` | No |  |
| `start_date` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "loan_amortization_calculator",
  "arguments": {
    "principal": 0,
    "annual_rate": 0,
    "term_months": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "loan_amortization_calculator"`.
