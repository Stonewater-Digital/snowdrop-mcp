---
skill: activity_based_costing
category: cost_allocation
description: Distributes cost pools based on activity driver consumption.
tier: free
inputs: cost_pools, activities
---

# Activity Based Costing

## Description
Distributes cost pools based on activity driver consumption.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cost_pools` | `array` | Yes |  |
| `activities` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "activity_based_costing",
  "arguments": {
    "cost_pools": [],
    "activities": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "activity_based_costing"`.
