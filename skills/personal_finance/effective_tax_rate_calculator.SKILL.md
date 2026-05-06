---
skill: effective_tax_rate_calculator
category: personal_finance
description: Calculate effective tax rate from total tax paid and total income. Compares effective rate to marginal rate for context.
tier: free
inputs: total_tax_paid, total_income
---

# Effective Tax Rate Calculator

## Description
Calculate effective tax rate from total tax paid and total income. Compares effective rate to marginal rate for context.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_tax_paid` | `number` | Yes | Total tax paid (federal, or total including state/local). |
| `total_income` | `number` | Yes | Total income (gross or adjusted gross income). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "effective_tax_rate_calculator",
  "arguments": {
    "total_tax_paid": 0,
    "total_income": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "effective_tax_rate_calculator"`.
