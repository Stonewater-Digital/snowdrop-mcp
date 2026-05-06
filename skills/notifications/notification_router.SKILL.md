---
skill: notification_router
category: notifications
description: Maps alert priority to Telegram/SMS/freeze workflows.
tier: free
inputs: message, priority
---

# Notification Router

## Description
Maps alert priority to Telegram/SMS/freeze workflows.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `message` | `string` | Yes |  |
| `priority` | `string` | Yes |  |
| `context` | `object` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "notification_router",
  "arguments": {
    "message": "<message>",
    "priority": "<priority>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "notification_router"`.
