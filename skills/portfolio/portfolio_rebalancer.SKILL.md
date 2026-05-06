---
skill: portfolio_rebalancer
category: portfolio
description: Compares target weights vs current positions and builds pending trade list.
tier: free
inputs: current_positions, target_weights, total_portfolio_value
---

# Portfolio Rebalancer

## Description
Compares target weights vs current positions and builds pending trade list.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_positions` | `array` | Yes |  |
| `target_weights` | `object` | Yes |  |
| `total_portfolio_value` | `number` | Yes |  |
| `min_trade_threshold` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "portfolio_rebalancer",
  "arguments": {
    "current_positions": [],
    "target_weights": {},
    "total_portfolio_value": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "portfolio_rebalancer"`.
