---
skill: sprint_planner
category: sprints
description: Selects backlog tasks for the sprint based on priority, capacity, and dependencies.
tier: free
inputs: backlog, team_capacity_points
---

# Sprint Planner

## Description
Selects backlog tasks for the sprint based on priority, capacity, and dependencies.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `backlog` | `array` | Yes |  |
| `team_capacity_points` | `integer` | Yes |  |
| `sprint_duration_days` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sprint_planner",
  "arguments": {
    "backlog": [],
    "team_capacity_points": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sprint_planner"`.
