---
skill: crowd_value_velocity
category: crowd_economics
description: Calculates weekly value velocity, acceleration, and forward projections.
tier: free
inputs: weekly_snapshots
---

# Crowd Value Velocity

## Description
Calculates weekly value velocity, acceleration, and forward projections.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `weekly_snapshots` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "crowd_value_velocity",
  "arguments": {
    "weekly_snapshots": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "crowd_value_velocity"`.
