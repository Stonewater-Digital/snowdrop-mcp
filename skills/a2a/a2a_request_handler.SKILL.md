---
skill: a2a_request_handler
category: a2a
description: Performs JSON-RPC compliance checks and bearer-token auth for A2A requests.
tier: free
inputs: payload, authorization
---

# A2a Request Handler

## Description
Performs JSON-RPC compliance checks and bearer-token auth for A2A requests.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `object` | Yes | Raw JSON-RPC 2.0 request object from the counterparty. |
| `authorization` | `string` | Yes | HTTP Authorization header value (Bearer token). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "a2a_request_handler",
  "arguments": {
    "payload": {},
    "authorization": "<authorization>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "a2a_request_handler"`.
