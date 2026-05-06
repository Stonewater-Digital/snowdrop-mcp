---
skill: bridge_loan_pricing
category: fund_accounting
description: Prices a fixed-rate amortizing bridge loan. Computes the monthly payment using the standard annuity formula, total interest cost, effective APR (nominal, monthly compounding), and a partial amortization schedule showing the first 3 months and final month.
tier: premium
inputs: none
---

# Bridge Loan Pricing

## Description
Prices a fixed-rate amortizing bridge loan. Computes the monthly payment using the standard annuity formula, total interest cost, effective APR (nominal, monthly compounding), and a partial amortization schedule showing the first 3 months and final month. Rates are expressed as annual decimals (e.g. 0.05 = 5%). (Premium — subscribe at https://snowdrop.ai)

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "bridge_loan_pricing",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bridge_loan_pricing"`.
