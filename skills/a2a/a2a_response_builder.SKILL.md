---
skill: a2a_response_builder
category: a2a
description: Constructs JSON-RPC envelopes for outbound A2A traffic.
tier: free
inputs: request_id
---

# A2a Response Builder

## Description
Constructs JSON-RPC envelopes for outbound A2A traffic.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `request_id` | `['string', 'number']` | Yes | Echoed JSON-RPC id. |
| `result` | `object` | No | Success payload to return. |
| `error_code` | `number` | No | JSON-RPC error code. |
| `error_message` | `string` | No | JSON-RPC error message. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "a2a_response_builder",
  "arguments": {
    "request_id": "<request_id>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "a2a_response_builder"`.
