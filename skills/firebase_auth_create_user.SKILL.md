---
skill: firebase_auth_create_user
category: root
description: Create a new Firebase Auth user account. Returns the user's UID, email, and creation time.
tier: free
inputs: email, password
---

# Firebase Auth Create User

## Description
Create a new Firebase Auth user account. Returns the user's UID, email, and creation time.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `email` | `string` | Yes |  |
| `password` | `string` | Yes |  |
| `display_name` | `string` | No |  |
| `phone_number` | `string` | No |  |
| `disabled` | `boolean` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_auth_create_user",
  "arguments": {
    "email": "<email>",
    "password": "<password>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_auth_create_user"`.
