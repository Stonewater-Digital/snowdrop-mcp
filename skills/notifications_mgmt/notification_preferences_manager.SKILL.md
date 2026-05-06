---
skill: notification_preferences_manager
category: notifications_mgmt
description: Gets, sets, or resets notification preferences per agent with persistence.
tier: free
inputs: operation, agent_id
---

# Notification Preferences Manager

## Description
Gets, sets, or resets notification preferences per agent with persistence.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes |  |
| `agent_id` | `string` | Yes |  |
| `preferences` | `object` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "notification_preferences_manager",
  "arguments": {
    "operation": "<operation>",
    "agent_id": "<agent_id>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "notification_preferences_manager"`.
