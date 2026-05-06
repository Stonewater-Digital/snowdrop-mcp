---
skill: capital_gains_tax_calculator
category: tax
description: Calculate capital gains tax with short-term vs long-term classification, 0/15/20% rates based on income bracket, and 3.8% NIIT when applicable.
tier: free
inputs: purchase_price, sale_price, holding_period_months
---

# Capital Gains Tax Calculator

## Description
Calculate capital gains tax with short-term vs long-term classification, 0/15/20% rates based on income bracket, and 3.8% NIIT when applicable.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `purchase_price` | `number` | Yes | Original purchase price (cost basis) in USD. |
| `sale_price` | `number` | Yes | Sale price in USD. |
| `holding_period_months` | `number` | Yes | Number of months the asset was held. |
| `income_bracket` | `string` | No | Income bracket: low, middle, or high. Determines long-term CG rate (0%, 15%, 20%) and NIIT applicability. |

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
    "purchase_price": 0,
    "sale_price": 0,
    "holding_period_months": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "capital_gains_tax_calculator"`.
