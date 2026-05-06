---
skill: velocity_tracker
category: sprints
description: Summarizes velocity averages, trend, and predictability over past sprints.
tier: free
inputs: sprint_history
---

# Velocity Tracker

## Description
Summarizes velocity averages, trend, and predictability over past sprints.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sprint_history` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "velocity_tracker",
  "arguments": {
    "sprint_history": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "velocity_tracker"`.
