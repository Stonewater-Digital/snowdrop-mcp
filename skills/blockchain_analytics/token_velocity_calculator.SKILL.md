---
skill: token_velocity_calculator
category: blockchain_analytics
description: Computes MV=PQ velocity metrics and highlights value unlocked through slower token circulation.
tier: free
inputs: transaction_volume, circulating_supply, average_holding_period_days
---

# Token Velocity Calculator

## Description
Computes MV=PQ velocity metrics and highlights value unlocked through slower token circulation.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `transaction_volume` | `number` | Yes | Total economic throughput (P*Q) in USD over the measured period. |
| `circulating_supply` | `number` | Yes | Token supply actively circulating (in tokens). |
| `average_holding_period_days` | `number` | Yes | Average number of days tokens stay in wallets before moving again. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_velocity_calculator",
  "arguments": {
    "transaction_volume": 0,
    "circulating_supply": 0,
    "average_holding_period_days": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_velocity_calculator"`.
