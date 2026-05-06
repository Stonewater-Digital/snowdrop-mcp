---
skill: firebase_auth_get_user
category: root
description: Look up a Firebase Auth user by UID or email address. Returns user profile data.
tier: free
inputs: none
---

# Firebase Auth Get User

## Description
Look up a Firebase Auth user by UID or email address. Returns user profile data.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `uid` | `string` | No |  |
| `email` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_auth_get_user",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_auth_get_user"`.
