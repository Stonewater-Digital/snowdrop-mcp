---
skill: token_standard_registrar_sync_agent
category: crypto_rwa
description: Synchronizes token transfer agents with smart-contract registrars in near-real time.
tier: free
inputs: payload
---

# Token Standard Registrar Sync Agent

## Description
Synchronizes token transfer agents with smart-contract registrars in near-real time.

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
  "tool": "token_standard_registrar_sync_agent",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_registrar_sync_agent"`.
