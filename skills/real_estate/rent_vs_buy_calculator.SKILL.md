---
skill: rent_vs_buy_calculator
category: real_estate
description: Compare 5-year total cost of renting vs buying. Accounts for mortgage payments, property tax, insurance, maintenance, appreciation, equity buildup, and rent increases.
tier: free
inputs: monthly_rent, home_price
---

# Rent Vs Buy Calculator

## Description
Compare 5-year total cost of renting vs buying. Accounts for mortgage payments, property tax, insurance, maintenance, appreciation, equity buildup, and rent increases.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `monthly_rent` | `number` | Yes | Current monthly rent in USD. |
| `home_price` | `number` | Yes | Home purchase price in USD. |
| `down_payment_pct` | `number` | No | Down payment as a decimal (e.g. 0.20 for 20%). |
| `mortgage_rate` | `number` | No | Annual mortgage interest rate as a decimal. |
| `term_years` | `integer` | No | Mortgage term in years. |
| `annual_appreciation` | `number` | No | Expected annual home appreciation rate as a decimal. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rent_vs_buy_calculator",
  "arguments": {
    "monthly_rent": 0,
    "home_price": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rent_vs_buy_calculator"`.
