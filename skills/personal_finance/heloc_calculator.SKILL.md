---
skill: heloc_calculator
category: personal_finance
description: Calculates HELOC borrowing power, interest-only draw payments, amortized repayment amounts, and total interest based on rate and term parameters.
tier: free
inputs: home_value, mortgage_balance, ltv_limit, draw_amount, rate, draw_period_years, repayment_period_years
---

# Heloc Calculator

## Description
Calculates HELOC borrowing power, interest-only draw payments, amortized repayment amounts, and total interest based on rate and term parameters.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `home_value` | `number` | Yes | Current market value of the property securing the HELOC. |
| `mortgage_balance` | `number` | Yes | Outstanding first mortgage principal. |
| `ltv_limit` | `number` | Yes | Maximum combined loan-to-value allowed (e.g., 0.85). |
| `draw_amount` | `number` | Yes | Amount planned to draw from the HELOC immediately. |
| `rate` | `number` | Yes | Annual interest rate as decimal, assume constant. |
| `draw_period_years` | `number` | Yes | Years of interest-only payments during the draw. |
| `repayment_period_years` | `number` | Yes | Years for amortized repayment after draw ends. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "heloc_calculator",
  "arguments": {
    "home_value": 0,
    "mortgage_balance": 0,
    "ltv_limit": 0,
    "draw_amount": 0,
    "rate": 0,
    "draw_period_years": 0,
    "repayment_period_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "heloc_calculator"`.
