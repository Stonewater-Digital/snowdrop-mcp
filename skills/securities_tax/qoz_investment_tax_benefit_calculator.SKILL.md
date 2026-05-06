---
skill: qoz_investment_tax_benefit_calculator
category: securities_tax
description: Quantifies tax deferral and exclusion benefits for QOZ capital gains.
tier: free
inputs: original_gain, investment_amount, holding_period_years
---

# Qoz Investment Tax Benefit Calculator

## Description
Quantifies tax deferral and exclusion benefits for QOZ capital gains.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `original_gain` | `number` | Yes |  |
| `investment_amount` | `number` | Yes |  |
| `holding_period_years` | `number` | Yes |  |
| `capital_gains_rate_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "qoz_investment_tax_benefit_calculator",
  "arguments": {
    "original_gain": 0,
    "investment_amount": 0,
    "holding_period_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "qoz_investment_tax_benefit_calculator"`.
