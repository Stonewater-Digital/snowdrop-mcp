---
skill: gmail_read_inbox
category: gmail
description: Read Gmail inbox messages. Returns metadata + snippet by default; set include_body=True for full decoded body.
tier: free
inputs: none
---

# Gmail Read Inbox

## Description
Read Gmail inbox messages.  Returns metadata + snippet by default; set include_body=True for full decoded body.  gmail.readonly scope.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `max_results` | `integer` | No | Maximum number of messages to return (default 10, max 100). |
| `query` | `string` | No | Gmail search query (e.g. 'is:unread', 'from:user@example.com').  Omit to list recent messages. |
| `include_body` | `boolean` | No | If true, decode and return the full message body. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "gmail_read_inbox",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gmail_read_inbox"`.
