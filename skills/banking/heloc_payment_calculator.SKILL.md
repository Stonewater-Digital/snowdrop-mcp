---
skill: heloc_payment_calculator
category: banking
description: Calculate HELOC payments: interest-only during draw period, principal + interest during repayment period.
tier: free
inputs: balance, rate, draw_period_months, repay_period_months
---

# Heloc Payment Calculator

## Description
Calculate HELOC payments: interest-only during draw period, principal + interest during repayment period.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `balance` | `number` | Yes | HELOC balance (amount drawn). |
| `rate` | `number` | Yes | Annual interest rate as decimal. |
| `draw_period_months` | `integer` | Yes | Length of draw period in months. |
| `repay_period_months` | `integer` | Yes | Length of repayment period in months. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "heloc_payment_calculator",
  "arguments": {
    "balance": 0,
    "rate": 0,
    "draw_period_months": 0,
    "repay_period_months": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "heloc_payment_calculator"`.
