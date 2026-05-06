---
skill: carried_interest_calculator
category: fund_admin
description: Computes GP carried interest after returning LP capital and preferred return. Supports optional full GP catch-up tranche before profit split.
tier: premium
inputs: total_distributions, capital_contributed, hurdle_rate_pct, carry_pct, catch_up, years
---

# Carried Interest Calculator

## Description
Computes GP carried interest after returning LP capital and preferred return. Supports optional full GP catch-up tranche before profit split. Uses European-style (whole-fund) waterfall logic. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| total_distributions | number | Yes | Total gross proceeds available for distribution to all partners (USD) |
| capital_contributed | number | Yes | Aggregate LP capital contributed to the fund (cost basis, USD) |
| hurdle_rate_pct | number | Yes | Preferred return rate (hurdle) that LPs receive before GP carry applies (e.g. 8.0 for 8%) |
| carry_pct | number | Yes | GP carried interest percentage of profits above the hurdle (e.g. 20.0 for 20%) |
| catch_up | boolean | No | Whether a full GP catch-up tranche applies before the LP/GP profit split (default: true) |
| years | number | No | Investment period in years, used to compound the preferred return (default: 1.0) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "carried_interest_calculator",
  "arguments": {
    "total_distributions": 85000000,
    "capital_contributed": 50000000,
    "hurdle_rate_pct": 8.0,
    "carry_pct": 20.0,
    "catch_up": true,
    "years": 5.0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "carried_interest_calculator"`.
