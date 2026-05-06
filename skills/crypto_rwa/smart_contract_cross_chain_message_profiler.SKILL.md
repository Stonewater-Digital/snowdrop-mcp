---
skill: smart_contract_cross_chain_message_profiler
category: crypto_rwa
description: Profiles bridge message flow for ack failures or stalled packets.
tier: free
inputs: payload
---

# Smart Contract Cross Chain Message Profiler

## Description
Profiles bridge message flow for ack failures or stalled packets.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "smart_contract_cross_chain_message_profiler",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_cross_chain_message_profiler"`.
