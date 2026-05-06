---
skill: nmtc_investor_return_calculator
category: nmtc
description: Calculates investor IRR over NMTC compliance period with tax credits and fees.
tier: free
inputs: investor_equity, tax_credits, leverage_loan_interest_received, cde_fees_received, put_price_at_year_7, investor_tax_rate
---

# Nmtc Investor Return Calculator

## Description
Calculates investor IRR over NMTC compliance period with tax credits and fees.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `investor_equity` | `number` | Yes |  |
| `tax_credits` | `array` | Yes |  |
| `leverage_loan_interest_received` | `number` | Yes |  |
| `cde_fees_received` | `number` | Yes |  |
| `put_price_at_year_7` | `number` | Yes |  |
| `investor_tax_rate` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "nmtc_investor_return_calculator",
  "arguments": {
    "investor_equity": 0,
    "tax_credits": [],
    "leverage_loan_interest_received": 0,
    "cde_fees_received": 0,
    "put_price_at_year_7": 0,
    "investor_tax_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "nmtc_investor_return_calculator"`.
