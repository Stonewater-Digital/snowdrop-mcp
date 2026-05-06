---
skill: optimism_to_base_govtoken_bridge_optimizer
category: defi_zk
description: Optimizes governance token bridge routing from Optimism to Base with fee and latency heuristics.
tier: free
inputs: amount_usd, urgency, volatility_index
---

# Optimism To Base Govtoken Bridge Optimizer

## Description
Optimizes governance token bridge routing from Optimism to Base with fee and latency heuristics.

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
  "tool": "optimism_to_base_govtoken_bridge_optimizer",
  "arguments": {
    "amount_usd": 0,
    "urgency": "<urgency>",
    "volatility_index": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "optimism_to_base_govtoken_bridge_optimizer"`.
