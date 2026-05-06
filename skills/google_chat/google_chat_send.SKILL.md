---
skill: google_chat_send
category: google_chat
description: Send a message to a Google Chat space via Incoming Webhook.
tier: free
inputs: message_text
---

# Google Chat Send

## Description
Send a message to a Google Chat space via Incoming Webhook.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `message_text` | `string` | Yes | Message text |
| `thread_id` | `string` | No | Optional thread key for threading |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "google_chat_send",
  "arguments": {
    "message_text": "<message_text>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "google_chat_send"`.
