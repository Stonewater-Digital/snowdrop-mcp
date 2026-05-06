---
skill: request_rate_limiter
category: gateway
description: Enforces per-agent token bucket rate limits and returns retry hints.
tier: free
inputs: agent_id, bucket_state, current_time
---

# Request Rate Limiter

## Description
Enforces per-agent token bucket rate limits and returns retry hints.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes |  |
| `bucket_state` | `object` | Yes |  |
| `current_time` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "request_rate_limiter",
  "arguments": {
    "agent_id": "<agent_id>",
    "bucket_state": {},
    "current_time": "<current_time>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "request_rate_limiter"`.
