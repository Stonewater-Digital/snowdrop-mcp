---
skill: token_standard_transfer_restriction_matrix
category: crypto_rwa
description: Generates restriction matrices mapping jurisdiction plus investor tier combinations.
tier: free
inputs: payload
---

# Token Standard Transfer Restriction Matrix

## Description
Generates restriction matrices mapping jurisdiction plus investor tier combinations.

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
  "tool": "token_standard_transfer_restriction_matrix",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_transfer_restriction_matrix"`.
