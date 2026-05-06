---
skill: carried_interest_tracker
category: fund_accounting
description: Tracks cumulative GP carried interest earned, distributed, and held in reserve based on fund cash flows. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: fund_id, vintage_year, distributions, contributions, preferred_return_rate, carry_rate
---

# Carried Interest Tracker

## Description
Tracks cumulative GP carried interest earned, distributed, and held in reserve based on fund cash flows. Computes running carry balance across the fund lifecycle, accounting for clawback exposure and escrow. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fund_id` | `string` | Yes | Unique fund identifier. |
| `vintage_year` | `integer` | Yes | Fund vintage year (e.g. 2019). |
| `distributions` | `array` | Yes | List of distribution events, each with `date` and `amount`. |
| `contributions` | `array` | Yes | List of capital contribution events, each with `date` and `amount`. |
| `preferred_return_rate` | `number` | No | Annual hurdle rate; defaults to 0.08 (8%). |
| `carry_rate` | `number` | No | GP carry percentage; defaults to 0.20 (20%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "carried_interest_tracker",
  "arguments": {
    "fund_id": "FUND-001",
    "vintage_year": 2019,
    "distributions": [{"date": "2024-06-30", "amount": 5000000}],
    "contributions": [{"date": "2019-01-15", "amount": 10000000}],
    "preferred_return_rate": 0.08,
    "carry_rate": 0.20
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "carried_interest_tracker"`.
