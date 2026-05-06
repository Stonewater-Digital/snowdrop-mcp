---
skill: auto_lease_vs_buy_calculator
category: banking
description: Compare total cost of leasing versus buying a vehicle. Accounts for loan payments, down payment, lease payments, and residual value.
tier: free
inputs: purchase_price, down_payment, loan_rate, loan_months, lease_monthly, lease_months, residual_value
---

# Auto Lease Vs Buy Calculator

## Description
Compare total cost of leasing versus buying a vehicle. Accounts for loan payments, down payment, lease payments, and residual value.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `purchase_price` | `number` | Yes | Vehicle purchase price. |
| `down_payment` | `number` | Yes | Down payment for purchase. |
| `loan_rate` | `number` | Yes | Annual loan rate as decimal. |
| `loan_months` | `integer` | Yes | Loan term in months. |
| `lease_monthly` | `number` | Yes | Monthly lease payment. |
| `lease_months` | `integer` | Yes | Lease term in months. |
| `residual_value` | `number` | Yes | Estimated vehicle value at end of lease/loan term. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "auto_lease_vs_buy_calculator",
  "arguments": {
    "purchase_price": 0,
    "down_payment": 0,
    "loan_rate": 0,
    "loan_months": 0,
    "lease_monthly": 0,
    "lease_months": 0,
    "residual_value": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "auto_lease_vs_buy_calculator"`.
