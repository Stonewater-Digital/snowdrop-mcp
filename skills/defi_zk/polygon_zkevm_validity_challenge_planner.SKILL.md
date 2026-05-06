---
skill: polygon_zkevm_validity_challenge_planner
category: defi_zk
description: Plans Polygon zkEVM validity challenge playbooks if proofs degrade.
tier: free
inputs: pending_transactions, proof_interval_minutes, l1_gas_price_gwei
---

# Polygon Zkevm Validity Challenge Planner

## Description
Plans Polygon zkEVM validity challenge playbooks if proofs degrade.

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
  "tool": "polygon_zkevm_validity_challenge_planner",
  "arguments": {
    "pending_transactions": 0,
    "proof_interval_minutes": 0,
    "l1_gas_price_gwei": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "polygon_zkevm_validity_challenge_planner"`.
