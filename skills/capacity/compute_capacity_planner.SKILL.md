---
skill: compute_capacity_planner
category: capacity
description: Projects when capacity will be breached and recommends actions.
tier: free
inputs: usage_history, capacity_limit
---

# Compute Capacity Planner

## Description
Projects when capacity will be breached and recommends actions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `usage_history` | `array` | Yes |  |
| `capacity_limit` | `number` | Yes |  |
| `growth_rate_pct` | `['number', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "compute_capacity_planner",
  "arguments": {
    "usage_history": [],
    "capacity_limit": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "compute_capacity_planner"`.
