---
skill: zksync_sequencer_privacy_leak_scanner
category: defi_zk
description: Detects privacy leak heuristics across zkSync sequencer mempools and hints.
tier: free
inputs: pending_transactions, proof_interval_minutes, l1_gas_price_gwei
---

# Zksync Sequencer Privacy Leak Scanner

## Description
Detects privacy leak heuristics across zkSync sequencer mempools and hints.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pending_transactions` | `number` | Yes | Current pending transactions queued for the rollup batch. |
| `proof_interval_minutes` | `number` | Yes | Observed interval between recent proof submissions. |
| `l1_gas_price_gwei` | `number` | Yes | Layer-1 gas price in gwei. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "zksync_sequencer_privacy_leak_scanner",
  "arguments": {
    "pending_transactions": 0,
    "proof_interval_minutes": 0,
    "l1_gas_price_gwei": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "zksync_sequencer_privacy_leak_scanner"`.
