---
skill: token_standard_routing_number_verifier
category: crypto_rwa
description: Validates routing and account numbers used for fiat bridges in compliance workflows.
tier: free
inputs: payload
---

# Token Standard Routing Number Verifier

## Description
Validates routing and account numbers used for fiat bridges in compliance workflows.

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
  "tool": "token_standard_routing_number_verifier",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_routing_number_verifier"`.
