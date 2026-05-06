---
skill: starknet_data_availability_cost_forecaster
category: defi_zk
description: Forecasts Starknet data availability costs when proofs spike.
tier: free
inputs: pending_transactions, proof_interval_minutes, l1_gas_price_gwei
---

# Starknet Data Availability Cost Forecaster

## Description
Forecasts Starknet data availability costs when proofs spike.

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
  "tool": "starknet_data_availability_cost_forecaster",
  "arguments": {
    "pending_transactions": 0,
    "proof_interval_minutes": 0,
    "l1_gas_price_gwei": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "starknet_data_availability_cost_forecaster"`.
