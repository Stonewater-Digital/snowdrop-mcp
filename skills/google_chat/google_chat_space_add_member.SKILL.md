---
skill: google_chat_space_add_member
category: google_chat
description: Add a member to a Google Chat space by email address.
tier: free
inputs: space_id, member_email
---

# Google Chat Space Add Member

## Description
Add a member to a Google Chat space by email address.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `space_id` | `string` | Yes | The space ID (e.g. 'AAQAbeAdvMk'). Will be prefixed with 'spaces/' if needed. |
| `member_email` | `string` | Yes | Email address of the user to add. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "google_chat_space_add_member",
  "arguments": {
    "space_id": "<space_id>",
    "member_email": "<member_email>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "google_chat_space_add_member"`.
