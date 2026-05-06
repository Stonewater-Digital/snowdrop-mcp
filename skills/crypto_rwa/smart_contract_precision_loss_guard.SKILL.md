---
skill: smart_contract_precision_loss_guard
category: crypto_rwa
description: Checks decimal math routines to prevent precision loss on rebasing assets.
tier: free
inputs: payload
---

# Smart Contract Precision Loss Guard

## Description
Checks decimal math routines to prevent precision loss on rebasing assets.

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
  "tool": "smart_contract_precision_loss_guard",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_precision_loss_guard"`.
