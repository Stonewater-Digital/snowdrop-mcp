---
skill: signature_verifier
category: crypto_auth
description: Verifies HMAC-SHA256 signatures for incoming agent messages.
tier: free
inputs: message, signature, agent_id, known_public_keys
---

# Signature Verifier

## Description
Verifies HMAC-SHA256 signatures for incoming agent messages.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `message` | `string` | Yes |  |
| `signature` | `string` | Yes |  |
| `agent_id` | `string` | Yes |  |
| `known_public_keys` | `object` | Yes | Mapping of agent_id to shared secret. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "signature_verifier",
  "arguments": {
    "message": "<message>",
    "signature": "<signature>",
    "agent_id": "<agent_id>",
    "known_public_keys": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "signature_verifier"`.
