---
skill: annuity_payment_calculator
category: personal_finance
description: Determines the periodic payment required to amortize a balance, including summary stats for total paid, interest, and early amortization snapshots.
tier: free
inputs: principal, annual_rate, years, payments_per_year, annuity_type
---

# Annuity Payment Calculator

## Description
Determines the periodic payment required to amortize a balance, including summary stats for total paid, interest, and early amortization snapshots.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `principal` | `number` | Yes | Amount financed or invested at present value. |
| `annual_rate` | `number` | Yes | Nominal annual interest rate as decimal. |
| `years` | `number` | Yes | Amortization term in years. |
| `payments_per_year` | `number` | Yes | Number of payments per year (12 for monthly). |
| `annuity_type` | `string` | Yes | ordinary for end-of-period, due for beginning-of-period payments. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "annuity_payment_calculator",
  "arguments": {
    "principal": 0,
    "annual_rate": 0,
    "years": 0,
    "payments_per_year": 0,
    "annuity_type": "<annuity_type>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "annuity_payment_calculator"`.
