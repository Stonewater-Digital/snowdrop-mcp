---
skill: pension_vs_lump_sum
category: personal_finance
description: Values lifetime pension payments versus a lump sum using discounting and inflation adjustments, providing breakeven timing and sensitivity scenarios.
tier: free
inputs: monthly_pension, lump_sum_offer, life_expectancy_years, discount_rate, inflation_rate, tax_bracket
---

# Pension Vs Lump Sum

## Description
Values lifetime pension payments versus a lump sum using discounting and inflation adjustments, providing breakeven timing and sensitivity scenarios.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `monthly_pension` | `number` | Yes | Guaranteed monthly pension payment before taxes. |
| `lump_sum_offer` | `number` | Yes | One-time buyout offer for the pension. |
| `life_expectancy_years` | `number` | Yes | Expected years of benefit payments. |
| `discount_rate` | `number` | Yes | Annual discount rate to present value the annuity. |
| `inflation_rate` | `number` | Yes | Expected inflation to adjust the real discount rate. |
| `tax_bracket` | `number` | Yes | Marginal tax rate applied to lump sum and pension. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "pension_vs_lump_sum",
  "arguments": {
    "monthly_pension": 0,
    "lump_sum_offer": 0,
    "life_expectancy_years": 0,
    "discount_rate": 0,
    "inflation_rate": 0,
    "tax_bracket": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pension_vs_lump_sum"`.
