---
skill: distribution_waterfall_calculator
category: fund_admin
description: Runs a full 4-tier distribution waterfall: (1) return of capital, (2) preferred return, (3) GP catch-up, (4) residual profit split. Supports both European (whole-fund) and American (deal-by-deal) modes.
tier: premium
inputs: gross_proceeds, capital_contributed, preferred_return_pct, carry_pct, catch_up_pct, years
---

# Distribution Waterfall Calculator

## Description
Runs a full 4-tier distribution waterfall: (1) return of capital, (2) preferred return, (3) GP catch-up, (4) residual profit split. Supports both European (whole-fund) and American (deal-by-deal) modes. Uses correct catch-up formula: GP gets 100% until carry% of total profits is met. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| gross_proceeds | number | Yes | Total gross exit proceeds available for distribution (USD) |
| capital_contributed | number | Yes | Aggregate LP capital contributed (cost basis used to calculate preferred return, USD) |
| preferred_return_pct | number | Yes | Annual preferred return (hurdle) rate that LPs receive before GP catch-up (e.g. 8.0 for 8%) |
| carry_pct | number | Yes | GP carry percentage of residual profits after catch-up (e.g. 20.0 for 20%) |
| catch_up_pct | number | No | Percentage of profits in the catch-up tranche allocated to the GP (default: 100.0) |
| years | number | No | Holding period in years, used to compound the preferred return (default: 1.0) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "distribution_waterfall_calculator",
  "arguments": {
    "gross_proceeds": 120000000,
    "capital_contributed": 60000000,
    "preferred_return_pct": 8.0,
    "carry_pct": 20.0,
    "catch_up_pct": 100.0,
    "years": 6.0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "distribution_waterfall_calculator"`.
