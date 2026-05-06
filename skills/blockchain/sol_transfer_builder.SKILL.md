---
skill: sol_transfer_builder
category: blockchain
description: Constructs Solana transfer payloads and fee estimates pending approval.
tier: free
inputs: from_pubkey, to_pubkey, amount_sol
---

# Sol Transfer Builder

## Description
Constructs Solana transfer payloads and fee estimates pending approval.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `from_pubkey` | `string` | Yes |  |
| `to_pubkey` | `string` | Yes |  |
| `amount_sol` | `number` | Yes |  |
| `memo` | `['string', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sol_transfer_builder",
  "arguments": {
    "from_pubkey": "<from_pubkey>",
    "to_pubkey": "<to_pubkey>",
    "amount_sol": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sol_transfer_builder"`.
