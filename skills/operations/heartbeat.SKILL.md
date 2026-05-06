---
skill: heartbeat
category: operations
description: Checks Ghost Ledger readiness, required API keys, and reconciliation freshness before writing HEARTBEAT.md with the current timestamp.
tier: free
inputs: none
---

# Heartbeat

## Description
Checks Ghost Ledger readiness, required API keys, and reconciliation freshness before writing HEARTBEAT.md with the current timestamp.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `required_keys` | `array` | No | Additional API key env vars to verify. |
| `last_reconciliation_path` | `string` | No | File containing the last reconciliation ISO timestamp. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "heartbeat",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "heartbeat"`.
