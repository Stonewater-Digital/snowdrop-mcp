---
skill: message_signer
category: crypto_auth
description: Signs messages with an env-provided key for agent authentication.
tier: free
inputs: message
---

# Message Signer

## Description
Signs messages with an env-provided key for agent authentication.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `message` | `string` | Yes |  |
| `signing_key_env` | `string` | No | Environment variable holding the signing key. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "message_signer",
  "arguments": {
    "message": "<message>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "message_signer"`.
