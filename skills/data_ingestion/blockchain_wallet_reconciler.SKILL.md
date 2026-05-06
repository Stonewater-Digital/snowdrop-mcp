---
skill: blockchain_wallet_reconciler
category: data_ingestion
description: Reconciles Ghost Ledger wallet balances against on-chain snapshots and surfaces tolerance breaches.
tier: free
inputs: ledger_positions, chain_balances
---

# Blockchain Wallet Reconciler

## Description
Reconciles Ghost Ledger wallet balances against on-chain snapshots and surfaces tolerance breaches.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ledger_positions` | `array` | Yes | Ledger entries with wallet, asset, and balance fields. |
| `chain_balances` | `array` | Yes | On-chain balances containing wallet, asset, balance. |
| `tolerance_pct` | `number` | No | Allowed percentage variance before raising a break. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "blockchain_wallet_reconciler",
  "arguments": {
    "ledger_positions": [],
    "chain_balances": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "blockchain_wallet_reconciler"`.
