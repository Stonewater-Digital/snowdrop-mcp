---
skill: transaction_sim_pre_flight
category: technical
description: Simulates an on-chain transaction in isolation before submission. Checks for insufficient balances, high slippage, and other failure conditions.
tier: free
inputs: transaction, current_state
---

# Transaction Sim Pre Flight

## Description
Simulates an on-chain transaction in isolation before submission. Checks for insufficient balances, high slippage, and other failure conditions. Returns projected new balances, estimated gas cost in USD, and a success probability score derived from balance adequacy and warning count.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `transaction` | `object` | Yes |  |
| `current_state` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "transaction_sim_pre_flight",
  "arguments": {
    "transaction": {},
    "current_state": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "transaction_sim_pre_flight"`.
