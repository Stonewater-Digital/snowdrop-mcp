---
skill: smart_contract_cross_pool_drain_simulator
category: crypto_rwa
description: Runs stress flows across linked pools to detect capital draining routes.
tier: free
inputs: payload
---

# Smart Contract Cross Pool Drain Simulator

## Description
Runs stress flows across linked pools to detect capital draining routes.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "smart_contract_cross_pool_drain_simulator",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_cross_pool_drain_simulator"`.
