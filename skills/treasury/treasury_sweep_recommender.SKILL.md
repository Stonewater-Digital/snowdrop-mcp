---
skill: treasury_sweep_recommender
category: treasury
description: Identifies idle cash available for sweeps and proposes destinations (pending Thunder).
tier: free
inputs: account_balances, monthly_burn
---

# Treasury Sweep Recommender

## Description
Identifies idle cash available for sweeps and proposes destinations (pending Thunder).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `account_balances` | `object` | Yes |  |
| `operating_buffer_months` | `integer` | No |  |
| `monthly_burn` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "treasury_sweep_recommender",
  "arguments": {
    "account_balances": {},
    "monthly_burn": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "treasury_sweep_recommender"`.
