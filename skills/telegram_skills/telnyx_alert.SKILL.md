---
skill: telnyx_alert
category: telegram_skills
description: Drafts Telnyx SMS payloads to notify Thunder of high-priority events.
tier: free
inputs: message, priority
---

# Telnyx Alert

## Description
Drafts Telnyx SMS payloads to notify Thunder of high-priority events.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `message` | `string` | Yes |  |
| `priority` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "telnyx_alert",
  "arguments": {
    "message": "<message>",
    "priority": "<priority>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "telnyx_alert"`.
