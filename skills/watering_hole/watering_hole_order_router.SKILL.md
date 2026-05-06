---
skill: watering_hole_order_router
category: watering_hole
description: Quotes Watering Hole skill requests via the bonding curve, assigns the correct skill, and returns billing plus dispatch telemetry.
tier: free
inputs: agent_id, requested_skill, base_price, decay_rate, time_elapsed_hours, slope, delta_units, delta_time_hours
---

# Watering Hole Order Router

## Description
Quotes Watering Hole skill requests via the bonding curve, assigns the correct skill, and returns billing plus dispatch telemetry.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes | Snowdrop agent identifier. |
| `requested_skill` | `string` | Yes | Skill name the agent wants to execute. |
| `base_price` | `number` | Yes |  |
| `decay_rate` | `number` | Yes |  |
| `time_elapsed_hours` | `number` | Yes |  |
| `slope` | `number` | Yes |  |
| `delta_units` | `number` | Yes |  |
| `delta_time_hours` | `number` | Yes |  |
| `available_skills` | `array` | No | Advertised catalog for validation. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "watering_hole_order_router",
  "arguments": {
    "agent_id": "<agent_id>",
    "requested_skill": "<requested_skill>",
    "base_price": 0,
    "decay_rate": 0,
    "time_elapsed_hours": 0,
    "slope": 0,
    "delta_units": 0,
    "delta_time_hours": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "watering_hole_order_router"`.
