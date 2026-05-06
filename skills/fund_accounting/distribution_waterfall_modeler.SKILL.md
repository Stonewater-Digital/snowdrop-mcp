---
skill: distribution_waterfall_modeler
category: fund_accounting
description: Calculates LP/GP outcomes for American and European waterfalls with tier detail. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: style, total_commitments, contributions, distributions, preferred_return_pct, gp_carry_pct, catch_up_pct, gp_commitment_pct, tiers
---

# Distribution Waterfall Modeler

## Description
Calculates LP/GP outcomes for American and European waterfalls with tier detail. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `style` | `string` | Yes | Waterfall style: `"american"` (deal-by-deal) or `"european"` (whole-fund). |
| `total_commitments` | `number` | Yes | Total LP + GP commitments to the fund in dollars. |
| `contributions` | `array` | Yes | List of contribution events, each with `date` and `amount`. |
| `distributions` | `array` | Yes | List of distribution events, each with `date` and `amount`. |
| `preferred_return_pct` | `number` | No | LP preferred return (hurdle) rate in percent (e.g. `8.0` for 8%). Defaults to `8.0`. |
| `gp_carry_pct` | `number` | No | GP carried interest percentage (e.g. `20.0` for 20%). Defaults to `20.0`. |
| `catch_up_pct` | `number` | No | GP catch-up percentage (e.g. `100.0` for full catch-up). Defaults to `100.0`. |
| `gp_commitment_pct` | `number` | No | GP co-investment commitment as a percentage of total fund (e.g. `2.0` for 2%). Defaults to `2.0`. |
| `tiers` | `array` | No | Optional custom waterfall tier definitions for non-standard structures. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "distribution_waterfall_modeler",
  "arguments": {
    "style": "european",
    "total_commitments": 100000000,
    "contributions": [
      {"date": "2020-03-31", "amount": 30000000},
      {"date": "2021-06-30", "amount": 40000000},
      {"date": "2022-09-30", "amount": 30000000}
    ],
    "distributions": [
      {"date": "2024-12-31", "amount": 160000000}
    ],
    "preferred_return_pct": 8.0,
    "gp_carry_pct": 20.0,
    "catch_up_pct": 100.0,
    "gp_commitment_pct": 2.0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "distribution_waterfall_modeler"`.
