---
skill: wallets_check
category: crypto
description: Checks on-chain balances versus Ghost Ledger and enforces $0.00 tolerance.
tier: free
inputs: on_chain_balances, ghost_ledger_balances
---

# Wallets Check

## Description
Checks on-chain balances versus Ghost Ledger and enforces $0.00 tolerance.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `on_chain_balances` | `array` | Yes |  |
| `ghost_ledger_balances` | `array` | Yes |  |
| `tolerance_usd` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "wallets_check",
  "arguments": {
    "on_chain_balances": [],
    "ghost_ledger_balances": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "wallets_check"`.
