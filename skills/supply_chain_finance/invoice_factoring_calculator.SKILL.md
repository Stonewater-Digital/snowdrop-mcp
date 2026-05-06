---
skill: invoice_factoring_calculator
category: supply_chain_finance
description: Computes advance, fees, and effective annual rate for factoring transactions.
tier: free
inputs: invoice_amount, payment_terms_days
---

# Invoice Factoring Calculator

## Description
Computes advance, fees, and effective annual rate for factoring transactions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `invoice_amount` | `number` | Yes |  |
| `payment_terms_days` | `integer` | Yes |  |
| `discount_rate_pct` | `number` | No |  |
| `advance_rate_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "invoice_factoring_calculator",
  "arguments": {
    "invoice_amount": 0,
    "payment_terms_days": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "invoice_factoring_calculator"`.
