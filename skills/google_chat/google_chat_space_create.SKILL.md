---
skill: google_chat_space_create
category: google_chat
description: Create a new Google Chat space.
tier: free
inputs: display_name
---

# Google Chat Space Create

## Description
Create a new Google Chat space.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `display_name` | `string` | Yes | Display name for the new space. |
| `space_type` | `string` | No | Type of space to create (default 'SPACE'). Options: SPACE, GROUP_CHAT. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "google_chat_space_create",
  "arguments": {
    "display_name": "<display_name>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "google_chat_space_create"`.
