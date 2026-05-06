---
skill: drawdown_scheduler
category: fund_accounting
description: Schedules capital call drawdowns based on unfunded commitment and upcoming investment pipeline. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: total_commitment, called_to_date, upcoming_investments
---

# Drawdown Scheduler

## Description
Schedules capital call drawdowns based on unfunded commitment and upcoming investment pipeline. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_commitment` | `number` | Yes | Total LP commitment to the fund in dollars. |
| `called_to_date` | `number` | Yes | Capital already called from LPs to date in dollars. |
| `upcoming_investments` | `array` | Yes | List of planned investment objects, each with `deal_name`, `expected_close_date`, and `capital_required`. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "drawdown_scheduler",
  "arguments": {
    "total_commitment": 50000000,
    "called_to_date": 20000000,
    "upcoming_investments": [
      {"deal_name": "Portfolio Co Alpha", "expected_close_date": "2026-07-15", "capital_required": 8000000},
      {"deal_name": "Portfolio Co Beta", "expected_close_date": "2026-10-01", "capital_required": 12000000}
    ]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "drawdown_scheduler"`.
