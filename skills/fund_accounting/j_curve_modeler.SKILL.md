---
skill: j_curve_modeler
category: fund_accounting
description: Simulates fund cash flows, NAV, and J-curve inflection metrics. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: fund_size, investment_period_years, fund_life_years, management_fee_pct, deployment_pace, exit_multiples, loss_rate_pct
---

# J Curve Modeler

## Description
Simulates fund cash flows, NAV, and J-curve inflection metrics. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fund_size` | `number` | Yes | Total fund size (LP commitments) in dollars. |
| `investment_period_years` | `number` | Yes | Number of years in the investment period (capital deployment phase). |
| `fund_life_years` | `number` | Yes | Total fund life in years (investment period + harvesting period). |
| `management_fee_pct` | `number` | Yes | Annual management fee rate as a decimal (e.g. `0.02` for 2%). |
| `deployment_pace` | `array` | Yes | List of annual deployment percentages (as decimals) for each year of the investment period (must sum to ~1.0). |
| `exit_multiples` | `array` | Yes | List of exit scenario objects with `year` and `gross_moic` (gross money-on-invested-capital multiple). |
| `loss_rate_pct` | `number` | No | Expected portfolio loss rate as a percentage (e.g. `15.0` for 15% of invested capital written off). Defaults to `15.0`. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "j_curve_modeler",
  "arguments": {
    "fund_size": 100000000,
    "investment_period_years": 5,
    "fund_life_years": 10,
    "management_fee_pct": 0.02,
    "deployment_pace": [0.10, 0.25, 0.30, 0.25, 0.10],
    "exit_multiples": [
      {"year": 6, "gross_moic": 2.5},
      {"year": 7, "gross_moic": 3.1},
      {"year": 8, "gross_moic": 2.8},
      {"year": 9, "gross_moic": 3.5}
    ],
    "loss_rate_pct": 15.0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "j_curve_modeler"`.
