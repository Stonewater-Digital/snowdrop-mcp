---
skill: optimism_latency_breaker_detector
category: defi_zk
description: Detects Optimism latency breaker events before users feel sequencer stalls.
tier: free
inputs: sequencer_backlog, avg_gas_price_gwei, l1_data_gas_price_gwei
---

# Optimism Latency Breaker Detector

## Description
Detects Optimism latency breaker events before users feel sequencer stalls.

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
  "tool": "optimism_latency_breaker_detector",
  "arguments": {
    "sequencer_backlog": 0,
    "avg_gas_price_gwei": 0,
    "l1_data_gas_price_gwei": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "optimism_latency_breaker_detector"`.
