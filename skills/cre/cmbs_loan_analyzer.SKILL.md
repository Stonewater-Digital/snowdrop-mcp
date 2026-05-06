---
skill: cmbs_loan_analyzer
category: cre
description: Computes LTV, DSCR, debt yield, and balloon risk for CMBS loans.
tier: free
inputs: loan_amount, property_value, noi, interest_rate, amortization_years, term_years, io_period_years
---

# Cmbs Loan Analyzer

## Description
Computes LTV, DSCR, debt yield, and balloon risk for CMBS loans.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `loan_amount` | `number` | Yes |  |
| `property_value` | `number` | Yes |  |
| `noi` | `number` | Yes |  |
| `interest_rate` | `number` | Yes |  |
| `amortization_years` | `integer` | Yes |  |
| `term_years` | `integer` | Yes |  |
| `io_period_years` | `integer` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cmbs_loan_analyzer",
  "arguments": {
    "loan_amount": 0,
    "property_value": 0,
    "noi": 0,
    "interest_rate": 0,
    "amortization_years": 0,
    "term_years": 0,
    "io_period_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cmbs_loan_analyzer"`.
