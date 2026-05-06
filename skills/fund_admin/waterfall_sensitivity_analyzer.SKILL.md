---
skill: waterfall_sensitivity_analyzer
category: fund_admin
description: Evaluates GP carry payouts across a grid of hurdle rates and carry percentages using a full 4-tier waterfall (ROC, pref, catch-up, split). Returns a sensitivity matrix and identifies optimal scenarios.
tier: premium
inputs: capital_contributed, gross_proceeds, hurdle_rates, carry_rates, years
---

# Waterfall Sensitivity Analyzer

## Description
Evaluates GP carry payouts across a grid of hurdle rates and carry percentages using a full 4-tier waterfall (ROC, pref, catch-up, split). Returns a sensitivity matrix and identifies optimal scenarios. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| capital_contributed | number | Yes | Total LP capital contributed to the fund (cost basis, USD) |
| gross_proceeds | number | Yes | Total gross exit proceeds available for distribution (USD) |
| hurdle_rates | array | Yes | List of hurdle rate percentages to test across the sensitivity grid (e.g. [6.0, 7.0, 8.0, 9.0]) |
| carry_rates | array | Yes | List of GP carry percentages to test across the sensitivity grid (e.g. [15.0, 17.5, 20.0, 25.0]) |
| years | number | No | Holding period in years used to compound the preferred return at each hurdle rate (default: 1.0) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "waterfall_sensitivity_analyzer",
  "arguments": {
    "capital_contributed": 50000000,
    "gross_proceeds": 110000000,
    "hurdle_rates": [6.0, 7.0, 8.0, 9.0, 10.0],
    "carry_rates": [15.0, 17.5, 20.0, 25.0],
    "years": 5.0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "waterfall_sensitivity_analyzer"`.
