---
skill: cap_table_simulator
category: fund_accounting
description: Models equity dilution across funding rounds, tracking ownership percentages per stakeholder with option pool. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: rounds, option_pool_pct
---

# Cap Table Simulator

## Description
Models equity dilution across funding rounds, tracking ownership percentages per stakeholder with option pool. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `rounds` | `array` | Yes | List of funding round objects, each with `name`, `pre_money_valuation`, `investment`, and `investors` (list of investor share objects). |
| `option_pool_pct` | `number` | Yes | Employee option pool percentage to reserve as a decimal (e.g. `0.10` for 10%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cap_table_simulator",
  "arguments": {
    "rounds": [
      {
        "name": "Seed",
        "pre_money_valuation": 5000000,
        "investment": 1000000,
        "investors": [{"name": "Founder A", "shares": 4000000}, {"name": "Angel Fund I", "shares": 800000}]
      },
      {
        "name": "Series A",
        "pre_money_valuation": 20000000,
        "investment": 5000000,
        "investors": [{"name": "VC Fund II", "shares": 2500000}]
      }
    ],
    "option_pool_pct": 0.10
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cap_table_simulator"`.
