---
skill: ton_transfer_builder
category: blockchain
description: Constructs TON transfer payloads without broadcasting.
tier: free
inputs: from_address, to_address, amount_ton
---

# Ton Transfer Builder

## Description
Constructs TON transfer payloads without broadcasting.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `from_address` | `string` | Yes |  |
| `to_address` | `string` | Yes |  |
| `amount_ton` | `number` | Yes |  |
| `memo` | `['string', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ton_transfer_builder",
  "arguments": {
    "from_address": "<from_address>",
    "to_address": "<to_address>",
    "amount_ton": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ton_transfer_builder"`.
