---
skill: linea_proof_latency_profiler
category: defi_zk
description: Profiles Linea proof latency and confidence based on queue depth and L1 gas noise.
tier: free
inputs: pending_transactions, proof_interval_minutes, l1_gas_price_gwei
---

# Linea Proof Latency Profiler

## Description
Profiles Linea proof latency and confidence based on queue depth and L1 gas noise.

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
  "tool": "linea_proof_latency_profiler",
  "arguments": {
    "pending_transactions": 0,
    "proof_interval_minutes": 0,
    "l1_gas_price_gwei": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "linea_proof_latency_profiler"`.
