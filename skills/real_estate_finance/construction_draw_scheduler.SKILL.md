---
skill: construction_draw_scheduler
category: real_estate_finance
description: Generates draw schedules, interest carry, and LTC compliance checks.
tier: free
inputs: total_budget, loan_amount, ltc_ratio, phases, interest_rate
---

# Construction Draw Scheduler

## Description
Generates draw schedules, interest carry, and LTC compliance checks.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_budget` | `number` | Yes |  |
| `loan_amount` | `number` | Yes |  |
| `ltc_ratio` | `number` | Yes |  |
| `phases` | `array` | Yes |  |
| `interest_rate` | `number` | Yes |  |
| `interest_reserve_months` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "construction_draw_scheduler",
  "arguments": {
    "total_budget": 0,
    "loan_amount": 0,
    "ltc_ratio": 0,
    "phases": [],
    "interest_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "construction_draw_scheduler"`.
