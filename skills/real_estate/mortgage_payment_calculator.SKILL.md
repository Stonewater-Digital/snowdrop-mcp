---
skill: mortgage_payment_calculator
category: real_estate
description: Calculate monthly mortgage payment using the standard amortization formula: M = P[r(1+r)^n] / [(1+r)^n - 1]. Returns monthly payment, total interest, and total paid.
tier: free
inputs: principal, annual_rate
---

# Mortgage Payment Calculator

## Description
Calculate monthly mortgage payment using the standard amortization formula: M = P[r(1+r)^n] / [(1+r)^n - 1]. Returns monthly payment, total interest, and total paid.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `principal` | `number` | Yes | Loan principal (amount borrowed) in USD. |
| `annual_rate` | `number` | Yes | Annual interest rate as a decimal (e.g. 0.07 for 7%). |
| `term_years` | `integer` | No | Loan term in years. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mortgage_payment_calculator",
  "arguments": {
    "principal": 0,
    "annual_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mortgage_payment_calculator"`.
