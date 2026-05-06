---
skill: gp_clawback_calculator
category: fund_accounting
description: Evaluates carry distributions versus whole-fund entitlement and recommends clawback. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: fund_distributions, fund_total_contributions, preferred_return_pct, gp_carry_pct
---

# Gp Clawback Calculator

## Description
Evaluates carry distributions versus whole-fund entitlement and recommends clawback. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fund_distributions` | `array` | Yes | List of historical distribution objects, each with `date`, `amount`, and `gp_carry_paid`. |
| `fund_total_contributions` | `number` | Yes | Total LP capital contributions made to the fund over its life in dollars. |
| `preferred_return_pct` | `number` | No | LP preferred return (hurdle) rate in percent (e.g. `8.0` for 8%). Defaults to `8.0`. |
| `gp_carry_pct` | `number` | No | GP carried interest percentage (e.g. `20.0` for 20%). Defaults to `20.0`. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "gp_clawback_calculator",
  "arguments": {
    "fund_distributions": [
      {"date": "2022-06-30", "amount": 30000000, "gp_carry_paid": 4000000},
      {"date": "2023-12-31", "amount": 45000000, "gp_carry_paid": 6000000},
      {"date": "2024-09-30", "amount": 20000000, "gp_carry_paid": 1500000}
    ],
    "fund_total_contributions": 80000000,
    "preferred_return_pct": 8.0,
    "gp_carry_pct": 20.0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gp_clawback_calculator"`.
