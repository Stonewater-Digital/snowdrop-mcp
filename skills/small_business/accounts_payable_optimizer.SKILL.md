---
skill: accounts_payable_optimizer
category: small_business
description: Evaluates supplier invoices for early payment discounts versus company cost of capital to recommend an optimal payment schedule.
tier: free
inputs: invoices, available_cash, cost_of_capital
---

# Accounts Payable Optimizer

## Description
Evaluates supplier invoices for early payment discounts versus company cost of capital to recommend an optimal payment schedule.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `invoices` | `array` | Yes | Invoices with id, amount, terms, early_pay_discount, early_pay_days. |
| `available_cash` | `number` | Yes | Cash available for accelerated payments. |
| `cost_of_capital` | `number` | Yes | Annual cost of capital as decimal. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "accounts_payable_optimizer",
  "arguments": {
    "invoices": [],
    "available_cash": 0,
    "cost_of_capital": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "accounts_payable_optimizer"`.
