---
skill: bridge_loan_pricing
category: fund_accounting
description: Prices a fixed-rate amortizing bridge loan. Computes the monthly payment using the standard annuity formula, total interest cost, effective APR (nominal, monthly compounding), and a partial amortization schedule showing the first 3 months and final month.
tier: premium
inputs: principal, annual_rate, term_months
---

# Bridge Loan Pricing

## Description
Prices a fixed-rate amortizing bridge loan. Computes the monthly payment using the standard annuity formula, total interest cost, effective APR (nominal, monthly compounding), and a partial amortization schedule showing the first 3 months and final month. Rates are expressed as annual decimals (e.g. 0.05 = 5%). Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `principal` | `number` | Yes | Loan principal amount in dollars. |
| `annual_rate` | `number` | Yes | Annual interest rate as a decimal (e.g. `0.08` for 8%). |
| `term_months` | `number` | Yes | Loan term in months (e.g. `12` for a 1-year bridge). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "bridge_loan_pricing",
  "arguments": {
    "principal": 5000000,
    "annual_rate": 0.09,
    "term_months": 18
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bridge_loan_pricing"`.
