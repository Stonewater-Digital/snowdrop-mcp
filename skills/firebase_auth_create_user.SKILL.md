---
skill: firebase_auth_create_user
category: root
description: Create a new Firebase Auth user account. Returns the user's UID, email, and creation time.
tier: free
inputs: none
---

# Firebase Auth Create User

## Description
Create a new Firebase Auth user account. Returns the user's UID, email, and creation time.

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_auth_create_user",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_auth_create_user"`.
