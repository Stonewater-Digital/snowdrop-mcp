---
skill: polygon_zkevm_prover_cluster_health_monitor
category: defi_zk
description: Monitors Polygon zkEVM prover clusters for saturation and fallback readiness.
tier: free
inputs: pending_transactions, proof_interval_minutes, l1_gas_price_gwei
---

# Polygon Zkevm Prover Cluster Health Monitor

## Description
Monitors Polygon zkEVM prover clusters for saturation and fallback readiness.

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
  "tool": "polygon_zkevm_prover_cluster_health_monitor",
  "arguments": {
    "pending_transactions": 0,
    "proof_interval_minutes": 0,
    "l1_gas_price_gwei": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "polygon_zkevm_prover_cluster_health_monitor"`.
