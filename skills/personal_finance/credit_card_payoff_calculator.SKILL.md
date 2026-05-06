---
skill: credit_card_payoff_calculator
category: personal_finance
description: Simulates credit card amortization for a chosen payment or target timeline and compares it against paying issuer minimums.
tier: free
inputs: balance, apr
---

# Credit Card Payoff Calculator

## Description
Simulates credit card amortization for a chosen payment or target timeline and compares it against paying issuer minimums.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `balance` | `number` | Yes | Current outstanding credit card balance. |
| `apr` | `number` | Yes | Annual percentage rate expressed as decimal. |
| `monthly_payment` | `number` | No | Custom monthly payment; either this or target_months is required. |
| `target_months` | `number` | No | Desired months to payoff used to solve for payment if monthly_payment omitted. |

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
    "apr": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_card_payoff_calculator"`.
