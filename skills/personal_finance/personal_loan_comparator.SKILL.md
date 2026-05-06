---
skill: personal_loan_comparator
category: personal_finance
description: Evaluates personal loan offers by accounting for origination fees, payments, total interest, and estimated effective APR to rank the cheapest option.
tier: free
inputs: offers
---

# Personal Loan Comparator

## Description
Evaluates personal loan offers by accounting for origination fees, payments, total interest, and estimated effective APR to rank the cheapest option.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `offers` | `array` | Yes | List of loan offers with lender, amount, rate, term_months, origination_fee. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "personal_loan_comparator",
  "arguments": {
    "offers": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "personal_loan_comparator"`.
