---
skill: mortgage_amortization
category: personal_finance
description: Generates a month-by-month mortgage payoff schedule with support for extra principal payments and reports payoff timing and interest savings.
tier: free
inputs: principal, annual_rate, term_years
---

# Mortgage Amortization

## Description
Generates a month-by-month mortgage payoff schedule with support for extra principal payments and reports payoff timing and interest savings.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `principal` | `number` | Yes | Loan amount financed in dollars. |
| `annual_rate` | `number` | Yes | Annual percentage rate as decimal. |
| `term_years` | `number` | Yes | Original loan term in years. |
| `extra_payment` | `number` | No | Optional extra monthly principal payment, defaults to 0. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mortgage_amortization",
  "arguments": {
    "principal": 0,
    "annual_rate": 0,
    "term_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mortgage_amortization"`.
