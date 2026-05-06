---
skill: event_manager
category: events
description: Handles creation, updates, registrations, and cancellations for events.
tier: free
inputs: operation
---

# Event Manager

## Description
Handles creation, updates, registrations, and cancellations for events.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes |  |
| `event` | `['object', 'null']` | No |  |
| `agent_id` | `['string', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "event_manager",
  "arguments": {
    "operation": "<operation>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "event_manager"`.
