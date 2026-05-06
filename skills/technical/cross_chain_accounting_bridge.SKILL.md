---
skill: cross_chain_accounting_bridge
category: technical
description: Normalize TON, Solana, and Ethereum transactions into a unified single ledger with net positions per chain.
tier: free
inputs: transactions
---

# Cross Chain Accounting Bridge

## Description
Normalize TON, Solana, and Ethereum transactions into a unified single ledger with net positions per chain.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `transactions` | `array` | Yes | List of transaction dicts, each with: chain, tx_hash, amount, token, usd_value, timestamp, direction (in/out). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cross_chain_accounting_bridge",
  "arguments": {
    "transactions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cross_chain_accounting_bridge"`.
