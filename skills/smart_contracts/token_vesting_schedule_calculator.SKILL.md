---
skill: token_vesting_schedule_calculator
category: smart_contracts
description: Converts vesting plans with cliffs into cumulative unlock curves and outstanding balances.
tier: free
inputs: total_tokens, cliff_months, vesting_months, months_elapsed
---

# Token Vesting Schedule Calculator

## Description
Converts vesting plans with cliffs into cumulative unlock curves and outstanding balances.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_tokens` | `number` | Yes | Total grant size |
| `cliff_months` | `integer` | Yes | Months before first unlock |
| `vesting_months` | `integer` | Yes | Total vesting duration after cliff |
| `months_elapsed` | `number` | Yes | Months passed since start |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_vesting_schedule_calculator",
  "arguments": {
    "total_tokens": 0,
    "cliff_months": 0,
    "vesting_months": 0,
    "months_elapsed": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_vesting_schedule_calculator"`.
