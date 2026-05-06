---
skill: token_lockup_period_analyzer
category: rwa_tokenization
description: Summarizes lockup mechanics with current remaining term and unlock schedule.
tier: free
inputs: total_lockup_months, months_elapsed, penalty_schedule
---

# Token Lockup Period Analyzer

## Description
Summarizes lockup mechanics with current remaining term and unlock schedule.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_lockup_months` | `integer` | Yes | Total lockup duration |
| `months_elapsed` | `number` | Yes | Months passed since issuance |
| `penalty_schedule` | `array` | Yes | Penalty tiers for early exits |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_lockup_period_analyzer",
  "arguments": {
    "total_lockup_months": 0,
    "months_elapsed": 0,
    "penalty_schedule": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_lockup_period_analyzer"`.
