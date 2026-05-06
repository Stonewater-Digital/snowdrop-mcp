---
skill: achievement_tracker
category: achievements
description: Evaluates activity events for new badges and upcoming milestones.
tier: free
inputs: agent_id, event
---

# Achievement Tracker

## Description
Evaluates activity events for new badges and upcoming milestones.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes |  |
| `event` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "achievement_tracker",
  "arguments": {
    "agent_id": "<agent_id>",
    "event": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "achievement_tracker"`.
