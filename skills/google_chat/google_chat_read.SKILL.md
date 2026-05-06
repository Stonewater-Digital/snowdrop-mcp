---
skill: google_chat_read
category: google_chat
description: Read messages from a Google Chat space via OAuth API.
tier: free
inputs: space_id
---

# Google Chat Read

## Description
Read messages from a Google Chat space via OAuth API.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `space_id` | `string` | Yes | The space ID (e.g. 'AAQAbeAdvMk'). Will be prefixed with 'spaces/' if needed. |
| `max_messages` | `integer` | No | Maximum number of messages to return (default 20). |
| `since_timestamp` | `string` | No | Optional ISO8601 timestamp — only return messages created after this time. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "google_chat_read",
  "arguments": {
    "space_id": "<space_id>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "google_chat_read"`.
