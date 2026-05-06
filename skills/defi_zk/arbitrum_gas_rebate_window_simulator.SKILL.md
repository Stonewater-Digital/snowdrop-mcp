---
skill: arbitrum_gas_rebate_window_simulator
category: defi_zk
description: Simulates Arbitrum gas rebate windows to recommend timing-sensitive swaps.
tier: free
inputs: sequencer_backlog, avg_gas_price_gwei, l1_data_gas_price_gwei
---

# Arbitrum Gas Rebate Window Simulator

## Description
Simulates Arbitrum gas rebate windows to recommend timing-sensitive swaps.

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
  "tool": "arbitrum_gas_rebate_window_simulator",
  "arguments": {
    "sequencer_backlog": 0,
    "avg_gas_price_gwei": 0,
    "l1_data_gas_price_gwei": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "arbitrum_gas_rebate_window_simulator"`.
