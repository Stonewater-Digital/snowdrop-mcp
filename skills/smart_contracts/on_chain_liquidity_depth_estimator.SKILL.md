---
skill: on_chain_liquidity_depth_estimator
category: smart_contracts
description: Aggregates order book levels until price impact exceeds a defined slippage limit.
tier: free
inputs: orderbook_levels, mid_price
---

# On Chain Liquidity Depth Estimator

## Description
Aggregates order book levels until price impact exceeds a defined slippage limit.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `orderbook_levels` | `array` | Yes | Price/size tuples sorted best to worst. |
| `mid_price` | `number` | Yes | Reference mid-market price |
| `max_slippage_pct` | `number` | No | Allowed slippage percent |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "on_chain_liquidity_depth_estimator",
  "arguments": {
    "orderbook_levels": [],
    "mid_price": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "on_chain_liquidity_depth_estimator"`.
