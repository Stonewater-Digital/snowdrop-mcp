---
skill: qualified_dividend_tax_calculator
category: tax
description: Calculate tax on qualified dividends at preferential 0%, 15%, or 20% rates based on taxable income and filing status (2024 thresholds).
tier: free
inputs: dividend_amount, taxable_income
---

# Qualified Dividend Tax Calculator

## Description
Calculate tax on qualified dividends at preferential 0%, 15%, or 20% rates based on taxable income and filing status (2024 thresholds).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `dividend_amount` | `number` | Yes | Total qualified dividend amount in USD. |
| `taxable_income` | `number` | Yes | Total taxable income including dividends in USD. |
| `filing_status` | `string` | No | Filing status. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "qualified_dividend_tax_calculator",
  "arguments": {
    "dividend_amount": 0,
    "taxable_income": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "qualified_dividend_tax_calculator"`.
