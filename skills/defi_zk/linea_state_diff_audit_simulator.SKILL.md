---
skill: linea_state_diff_audit_simulator
category: defi_zk
description: Simulates Linea state diff coverage to spot risky batches before posting.
tier: free
inputs: pending_transactions, proof_interval_minutes, l1_gas_price_gwei
---

# Linea State Diff Audit Simulator

## Description
Simulates Linea state diff coverage to spot risky batches before posting.

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
  "tool": "linea_state_diff_audit_simulator",
  "arguments": {
    "pending_transactions": 0,
    "proof_interval_minutes": 0,
    "l1_gas_price_gwei": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "linea_state_diff_audit_simulator"`.
