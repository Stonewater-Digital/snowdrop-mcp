---
skill: management_fee_calculator
category: fund_admin
description: Computes management fees with investment period step-down: before step_down_year, fees are based on committed capital; after step_down_year, fees step down to invested/cost basis. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: commitment_base, invested_capital, fee_rate_pct, fund_age_years, step_down_year, post_step_down_rate_pct
---

# Management Fee Calculator

## Description
Computes management fees with investment period step-down: before step_down_year, fees are based on committed capital; after step_down_year, fees step down to invested/cost basis. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| commitment_base | number | Yes | Total LP committed capital used as the fee base during the investment period (USD) |
| invested_capital | number | Yes | Deployed/invested capital at cost used as the fee base after the step-down year (USD) |
| fee_rate_pct | number | Yes | Annual management fee rate applied during the investment period (e.g. 2.0 for 2%) |
| fund_age_years | number | Yes | Current age of the fund in years, used to determine which fee base applies |
| step_down_year | number | No | Year in which the fee base transitions from committed to invested capital (default: 5.0) |
| post_step_down_rate_pct | number | No | Annual fee rate applied after the step-down year; if omitted, the same fee_rate_pct is used |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "management_fee_calculator",
  "arguments": {
    "commitment_base": 100000000,
    "invested_capital": 72000000,
    "fee_rate_pct": 2.0,
    "fund_age_years": 6.5,
    "step_down_year": 5.0,
    "post_step_down_rate_pct": 1.5
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "management_fee_calculator"`.
