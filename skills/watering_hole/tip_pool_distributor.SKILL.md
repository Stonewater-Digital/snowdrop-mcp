---
skill: tip_pool_distributor
category: watering_hole
description: Splits gratuities by hours worked and role multipliers for Watering Hole staff.
tier: free
inputs: gratuity_pool, shifts
---

# Tip Pool Distributor

## Description
Splits gratuities by hours worked and role multipliers for Watering Hole staff.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gratuity_pool` | `number` | Yes | Total USD pool to distribute. |
| `shifts` | `array` | Yes | Hours logged for each team member. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tip_pool_distributor",
  "arguments": {
    "gratuity_pool": 0,
    "shifts": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tip_pool_distributor"`.
