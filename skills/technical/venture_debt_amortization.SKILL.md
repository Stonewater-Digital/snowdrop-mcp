---
skill: venture_debt_amortization
category: technical
description: Generates a complete monthly payment schedule for a venture debt instrument with an interest-only (IO) period followed by a fully-amortizing repayment period. Optionally calculates the warrant coverage value granted to the lender as a percentage of principal.
tier: free
inputs: principal, annual_rate, term_months, io_period_months
---

# Venture Debt Amortization

## Description
Generates a complete monthly payment schedule for a venture debt instrument with an interest-only (IO) period followed by a fully-amortizing repayment period. Optionally calculates the warrant coverage value granted to the lender as a percentage of principal.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `principal` | `number` | Yes | Loan principal in USD. |
| `annual_rate` | `number` | Yes | Annual interest rate as a decimal (e.g. 0.12 for 12%). |
| `term_months` | `integer` | Yes | Total loan term in months. |
| `io_period_months` | `integer` | Yes | Number of months for interest-only period. |
| `warrant_coverage_pct` | `number` | No | Warrant coverage as a percentage of principal (e.g. 20 for 20%). Optional. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "venture_debt_amortization",
  "arguments": {
    "principal": 0,
    "annual_rate": 0,
    "term_months": 0,
    "io_period_months": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "venture_debt_amortization"`.
