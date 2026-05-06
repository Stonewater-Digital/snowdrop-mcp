---
skill: verify_hurdle_rate
category: fund_accounting
description: Validates whether LP preferred return hurdle has been met and computes a simple IRR approximation. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: committed_capital, distributions_to_date, hurdle_rate, time_period
---

# Verify Hurdle Rate

## Description
Validates whether LP preferred return hurdle has been met and computes a simple IRR approximation. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `committed_capital` | `number` | Yes | Total LP capital contributed to the fund in dollars. |
| `distributions_to_date` | `number` | Yes | Total cash distributions returned to LPs to date in dollars. |
| `hurdle_rate` | `number` | Yes | LP preferred return rate as a decimal (e.g. `0.08` for 8% preferred return). |
| `time_period` | `number` | Yes | Holding period in years since first capital call (e.g. `4.5` for 4.5 years). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "verify_hurdle_rate",
  "arguments": {
    "committed_capital": 50000000,
    "distributions_to_date": 28000000,
    "hurdle_rate": 0.08,
    "time_period": 3.5
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "verify_hurdle_rate"`.
