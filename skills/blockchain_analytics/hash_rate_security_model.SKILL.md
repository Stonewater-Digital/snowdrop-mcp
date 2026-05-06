---
skill: hash_rate_security_model
category: blockchain_analytics
description: Calculates PoW security metrics and estimated 51% attack costs drawing from Nakamoto consensus economics.
tier: free
inputs: network_hash_rate, block_reward, token_price, electricity_cost_kwh, hardware_efficiency
---

# Hash Rate Security Model

## Description
Calculates PoW security metrics and estimated 51% attack costs drawing from Nakamoto consensus economics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `network_hash_rate` | `number` | Yes | Total network hash rate in hashes per second. |
| `block_reward` | `number` | Yes | Block reward including fees in native tokens. |
| `token_price` | `number` | Yes | Spot token price in USD. |
| `electricity_cost_kwh` | `number` | Yes | Electricity cost per kWh in USD for miners. |
| `hardware_efficiency` | `number` | Yes | Hardware efficiency expressed as joules per terahash. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "hash_rate_security_model",
  "arguments": {
    "network_hash_rate": 0,
    "block_reward": 0,
    "token_price": 0,
    "electricity_cost_kwh": 0,
    "hardware_efficiency": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "hash_rate_security_model"`.
