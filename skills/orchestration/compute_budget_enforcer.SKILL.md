---
skill: compute_budget_enforcer
category: orchestration
description: Makes sure Snowdrop does not exceed the $50/day compute budget.
tier: free
inputs: daily_spend_usd, pending_call_cost
---

# Compute Budget Enforcer

## Description
Makes sure Snowdrop does not exceed the $50/day compute budget.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `daily_spend_usd` | `number` | Yes |  |
| `pending_call_cost` | `number` | Yes |  |
| `daily_cap_usd` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "compute_budget_enforcer",
  "arguments": {
    "daily_spend_usd": 0,
    "pending_call_cost": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "compute_budget_enforcer"`.
