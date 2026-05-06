---
skill: firebase_auth_revoke_tokens
category: root
description: Revoke all refresh tokens for a Firebase Auth user, forcing them to re-authenticate. Returns the user UID and revocation timestamp.
tier: free
inputs: uid
---

# Firebase Auth Revoke Tokens

## Description
Revoke all refresh tokens for a Firebase Auth user, forcing them to re-authenticate. Returns the user UID and revocation timestamp.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `uid` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_auth_revoke_tokens",
  "arguments": {
    "uid": "<uid>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_auth_revoke_tokens"`.
