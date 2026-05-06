---
skill: auto_loan_calculator
category: personal_finance
description: Builds a car financing model covering tax, amount financed, monthly payment, and total interest across the loan term.
tier: free
inputs: vehicle_price, down_payment, trade_in_value, loan_rate, loan_term_months, sales_tax_rate
---

# Auto Loan Calculator

## Description
Builds a car financing model covering tax, amount financed, monthly payment, and total interest across the loan term.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `vehicle_price` | `number` | Yes | Agreed purchase price of the vehicle before incentives. |
| `down_payment` | `number` | Yes | Cash down payment applied at signing. |
| `trade_in_value` | `number` | Yes | Value of vehicle traded in, reduces taxable base. |
| `loan_rate` | `number` | Yes | APR for financing as decimal. |
| `loan_term_months` | `number` | Yes | Loan duration in months. |
| `sales_tax_rate` | `number` | Yes | Sales tax applied to purchase price net of trade-in. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "auto_loan_calculator",
  "arguments": {
    "vehicle_price": 0,
    "down_payment": 0,
    "trade_in_value": 0,
    "loan_rate": 0,
    "loan_term_months": 0,
    "sales_tax_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "auto_loan_calculator"`.
