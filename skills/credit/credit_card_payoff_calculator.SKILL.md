---
skill: credit_card_payoff_calculator
category: credit
description: Calculate how many months to pay off a credit card balance with a fixed monthly payment, and total interest paid.
tier: free
inputs: balance, apr, monthly_payment
---

# Credit Card Payoff Calculator

## Description
Calculate how many months to pay off a credit card balance with a fixed monthly payment, and total interest paid.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `balance` | `number` | Yes | Current card balance. |
| `apr` | `number` | Yes | Annual Percentage Rate as decimal. |
| `monthly_payment` | `number` | Yes | Fixed monthly payment amount. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_card_payoff_calculator",
  "arguments": {
    "balance": 0,
    "apr": 0,
    "monthly_payment": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_card_payoff_calculator"`.
