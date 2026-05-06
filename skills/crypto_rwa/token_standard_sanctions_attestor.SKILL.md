---
skill: token_standard_sanctions_attestor
category: crypto_rwa
description: Confirms sanctions screening proofs are attached to each restricted transfer.
tier: free
inputs: payload
---

# Token Standard Sanctions Attestor

## Description
Confirms sanctions screening proofs are attached to each restricted transfer.

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
  "tool": "token_standard_sanctions_attestor",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_sanctions_attestor"`.
