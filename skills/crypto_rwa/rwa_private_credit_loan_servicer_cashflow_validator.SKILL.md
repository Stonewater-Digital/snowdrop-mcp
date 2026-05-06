---
skill: rwa_private_credit_loan_servicer_cashflow_validator
category: crypto_rwa
description: Reconciles servicer remittance files against token payout streams for private credit pools.
tier: free
inputs: none
---

# Rwa Private Credit Loan Servicer Cashflow Validator

## Description
Reconciles servicer remittance files against token payout streams for private credit pools.

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
  "tool": "rwa_private_credit_loan_servicer_cashflow_validator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_private_credit_loan_servicer_cashflow_validator"`.
