---
skill: fica_tax_calculator
category: payroll
description: Calculate FICA taxes: Social Security (6.2% up to $168,600), Medicare (1.45%), and Additional Medicare Tax (0.9% over $200k). Doubles rates for self-employed.
tier: free
inputs: gross_income
---

# Fica Tax Calculator

## Description
Calculate FICA taxes: Social Security (6.2% up to $168,600), Medicare (1.45%), and Additional Medicare Tax (0.9% over $200k). Doubles rates for self-employed.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gross_income` | `number` | Yes | Gross earned income in USD. |
| `self_employed` | `boolean` | No | Whether the taxpayer is self-employed (pays both employer and employee shares). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fica_tax_calculator",
  "arguments": {
    "gross_income": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fica_tax_calculator"`.
