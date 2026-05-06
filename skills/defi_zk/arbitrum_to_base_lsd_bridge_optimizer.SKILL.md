---
skill: arbitrum_to_base_lsd_bridge_optimizer
category: defi_zk
description: Optimizes liquid staking derivative bridge routing from Arbitrum to Base with fee and latency heuristics.
tier: free
inputs: amount_usd, urgency, volatility_index
---

# Arbitrum To Base Lsd Bridge Optimizer

## Description
Optimizes liquid staking derivative bridge routing from Arbitrum to Base with fee and latency heuristics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `amount_usd` | `number` | Yes | Notional Size in USD. |
| `urgency` | `string` | Yes | Speed requirement for the transfer. |
| `volatility_index` | `number` | Yes | Bridge volatility proxy between 0-2. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "arbitrum_to_base_lsd_bridge_optimizer",
  "arguments": {
    "amount_usd": 0,
    "urgency": "<urgency>",
    "volatility_index": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "arbitrum_to_base_lsd_bridge_optimizer"`.
