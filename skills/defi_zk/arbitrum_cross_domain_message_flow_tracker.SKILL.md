---
skill: arbitrum_cross_domain_message_flow_tracker
category: defi_zk
description: Tracks Arbitrum cross-domain message queues to flag settlement delays.
tier: free
inputs: sequencer_backlog, avg_gas_price_gwei, l1_data_gas_price_gwei
---

# Arbitrum Cross Domain Message Flow Tracker

## Description
Tracks Arbitrum cross-domain message queues to flag settlement delays.

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
  "tool": "arbitrum_cross_domain_message_flow_tracker",
  "arguments": {
    "sequencer_backlog": 0,
    "avg_gas_price_gwei": 0,
    "l1_data_gas_price_gwei": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "arbitrum_cross_domain_message_flow_tracker"`.
