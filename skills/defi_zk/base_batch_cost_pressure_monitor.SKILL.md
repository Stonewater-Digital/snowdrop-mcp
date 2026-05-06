---
skill: base_batch_cost_pressure_monitor
category: defi_zk
description: Projects Base batch posting cost pressure based on calldata pricing and queue depth.
tier: free
inputs: sequencer_backlog, avg_gas_price_gwei, l1_data_gas_price_gwei
---

# Base Batch Cost Pressure Monitor

## Description
Projects Base batch posting cost pressure based on calldata pricing and queue depth.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sequencer_backlog` | `number` | Yes | Current number of pending transactions waiting on the sequencer. |
| `avg_gas_price_gwei` | `number` | Yes | Average L2 gas price in gwei over the last minute. |
| `l1_data_gas_price_gwei` | `number` | Yes | Current L1 calldata gas price in gwei for the submission chain. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "base_batch_cost_pressure_monitor",
  "arguments": {
    "sequencer_backlog": 0,
    "avg_gas_price_gwei": 0,
    "l1_data_gas_price_gwei": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "base_batch_cost_pressure_monitor"`.
