---
skill: installment_loan_calculator
category: credit
description: Calculate monthly payment, total interest, and amortization summary for a fixed-rate installment loan.
tier: free
inputs: principal, apr, term_months
---

# Installment Loan Calculator

## Description
Calculate monthly payment, total interest, and amortization summary for a fixed-rate installment loan.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `principal` | `number` | Yes | Loan principal. |
| `apr` | `number` | Yes | Annual rate as decimal. |
| `term_months` | `integer` | Yes | Loan term in months. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "installment_loan_calculator",
  "arguments": {
    "principal": 0,
    "apr": 0,
    "term_months": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "installment_loan_calculator"`.
