---
skill: payment_terms_optimizer
category: supply_chain_finance
description: Evaluates early-pay discounts to maximize savings within cash constraints.
tier: free
inputs: invoices_payable, available_cash
---

# Payment Terms Optimizer

## Description
Evaluates early-pay discounts to maximize savings within cash constraints.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `invoices_payable` | `array` | Yes |  |
| `available_cash` | `number` | Yes |  |
| `opportunity_cost_annual_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "payment_terms_optimizer",
  "arguments": {
    "invoices_payable": [],
    "available_cash": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "payment_terms_optimizer"`.
