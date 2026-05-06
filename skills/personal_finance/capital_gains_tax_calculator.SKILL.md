---
skill: capital_gains_tax_calculator
category: personal_finance
description: Splits gains into short- and long-term buckets, applies 2024 tax brackets, and checks 3.8% NIIT applicability based on filing status and income.
tier: free
inputs: gains, ordinary_income, filing_status
---

# Capital Gains Tax Calculator

## Description
Splits gains into short- and long-term buckets, applies 2024 tax brackets, and checks 3.8% NIIT applicability based on filing status and income.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gains` | `array` | Yes | List of realized transactions with amount, holding_period_months, cost_basis. |
| `ordinary_income` | `number` | Yes | Other taxable ordinary income in dollars. |
| `filing_status` | `string` | Yes | single or mfj for capital gains thresholds. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "capital_gains_tax_calculator",
  "arguments": {
    "gains": [],
    "ordinary_income": 0,
    "filing_status": "<filing_status>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "capital_gains_tax_calculator"`.
