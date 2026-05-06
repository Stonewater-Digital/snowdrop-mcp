---
skill: google_chat_reply
category: google_chat
description: Send a message or threaded reply to a Google Chat space via OAuth API.
tier: free
inputs: space_id, message_text
---

# Google Chat Reply

## Description
Send a message or threaded reply to a Google Chat space via OAuth API.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `space_id` | `string` | Yes | The space ID (e.g. 'AAQAbeAdvMk'). Will be prefixed with 'spaces/' if needed. |
| `message_text` | `string` | Yes | The message text to send. |
| `thread_name` | `string` | No | Optional thread resource name for threaded replies (e.g. 'spaces/AAQAbeAdvMk/threads/abc123'). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "google_chat_reply",
  "arguments": {
    "space_id": "<space_id>",
    "message_text": "<message_text>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "google_chat_reply"`.
