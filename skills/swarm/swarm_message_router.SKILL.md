---
skill: swarm_message_router
category: swarm
description: Validates sender/recipient roles and produces routing envelopes.
tier: free
inputs: sender, recipient, message_type, payload
---

# Swarm Message Router

## Description
Validates sender/recipient roles and produces routing envelopes.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sender` | `string` | Yes |  |
| `recipient` | `string` | Yes |  |
| `message_type` | `string` | Yes |  |
| `payload` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "swarm_message_router",
  "arguments": {
    "sender": "<sender>",
    "recipient": "<recipient>",
    "message_type": "<message_type>",
    "payload": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "swarm_message_router"`.
