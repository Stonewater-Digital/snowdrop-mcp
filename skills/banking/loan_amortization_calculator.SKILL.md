---
skill: loan_amortization_calculator
category: banking
description: Generate a full amortization schedule for a fixed-rate loan showing month, payment, principal, interest, and remaining balance for each period.
tier: free
inputs: principal, annual_rate, term_months
---

# Loan Amortization Calculator

## Description
Generate a full amortization schedule for a fixed-rate loan showing month, payment, principal, interest, and remaining balance for each period.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `principal` | `number` | Yes | Loan principal amount. |
| `annual_rate` | `number` | Yes | Annual interest rate as decimal. |
| `term_months` | `integer` | Yes | Loan term in months. |

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
